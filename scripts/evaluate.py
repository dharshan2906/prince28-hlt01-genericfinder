"""Run live GenericFinder scope-adherence evaluation."""

import argparse
import asyncio
import json
from pathlib import Path

from genericfinder.api.routes.chat import PROMPT_VERSION, load_prompt
from genericfinder.config import get_settings
from genericfinder.evaluation import evaluate_scope_guard
from genericfinder.llm.gateway import LLMUnavailable, build_gateway

ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "evals" / "datasets" / "scope_guard.jsonl"
OUT_OF_SCOPE_PREFIX = "Outside GenericFinder's scope:"


def load_dataset() -> list[dict]:
    """Load labelled Scope Guard questions."""
    with DATASET_PATH.open(encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def classify_response(answer: str) -> str:
    """Classify an answer using the required out-of-scope prefix."""
    if answer.strip().startswith(OUT_OF_SCOPE_PREFIX):
        return "out_of_scope"
    return "in_scope"


async def evaluate_live(examples: list[dict]) -> dict:
    """Run questions through the configured LLM gateway."""
    settings = get_settings()
    prompt = load_prompt(settings.prompts_dir, PROMPT_VERSION)
    gateway = build_gateway(settings)

    predictions = []
    failures = []

    for example in examples:
        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": example["question"]},
        ]

        try:
            result = await gateway.generate(
                messages,
                purpose="scope_evaluation",
                prompt_version=PROMPT_VERSION,
            )
        except LLMUnavailable as exc:
            failures.append({"id": example["id"], "error": str(exc)})
            continue

        predicted = classify_response(result.text)

        predictions.append(
            {
                "id": example["id"],
                "question": example["question"],
                "expected": example["expected"],
                "predicted": predicted,
                "correct": example["expected"] == predicted,
                "answer": result.text,
                "provider": result.provider,
                "model": result.model,
            }
        )

        print(f"\n[{example['id']}] {example['question']}")
        print(f"Expected:  {example['expected']}")
        print(f"Predicted: {predicted}")
        print(f"Answer:    {result.text}")

    metrics = evaluate_scope_guard(predictions) if predictions else {}

    return {
        "evaluated": len(predictions),
        "failures": failures,
        "metrics": metrics,
        "predictions": predictions,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate GenericFinder scope adherence")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "evals" / "scope_results.json",
        help="Path for evaluation results",
    )
    args = parser.parse_args()

    examples = load_dataset()
    results = asyncio.run(evaluate_live(examples))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(results, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print("\n=== Scope Evaluation Results ===")
    print(f"Questions: {len(examples)}")
    print(f"Evaluated: {results['evaluated']}")
    print(f"Failed calls: {len(results['failures'])}")

    if results["metrics"]:
        for metric in ("precision", "recall", "f1_score", "accuracy"):
            print(f"{metric}: {results['metrics'][metric]}")

    print(f"Results saved to: {args.output}")


if __name__ == "__main__":
    main()
