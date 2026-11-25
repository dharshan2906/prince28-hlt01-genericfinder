"""Evaluation of GenericFinder document retrieval results."""

from collections.abc import Iterable, Mapping
from typing import Any

from .metrics import retrieval_metrics


def evaluate_retrieval(
    examples: Iterable[Mapping[str, Any]],
    k: int = 5,
) -> dict[str, int | float | list[dict[str, int | float]]]:
    """Evaluate query examples with ``relevant_ids`` and ``retrieved_ids``.

    Returns per-query metrics and macro averages across all queries.
    """
    rows = list(examples)
    if not rows:
        raise ValueError("At least one retrieval example is required")

    per_query = []
    for index, row in enumerate(rows, start=1):
        if "relevant_ids" not in row or "retrieved_ids" not in row:
            raise ValueError(f"Retrieval example {index} needs relevant_ids and retrieved_ids")
        per_query.append(retrieval_metrics(row["relevant_ids"], row["retrieved_ids"], k=k))

    count = len(per_query)
    return {
        "k": k,
        "queries_evaluated": count,
        "mean_precision_at_k": round(sum(row["precision_at_k"] for row in per_query) / count, 4),
        "mean_recall_at_k": round(sum(row["recall_at_k"] for row in per_query) / count, 4),
        "mean_f1_at_k": round(sum(row["f1_at_k"] for row in per_query) / count, 4),
        "per_query": per_query,
    }
