"""Evaluation of GenericFinder Scope Guard predictions."""

from collections.abc import Iterable, Mapping
from typing import Any

from .metrics import binary_classification_metrics


def evaluate_scope_guard(
    examples: Iterable[Mapping[str, Any]],
    positive_label: str = "in_scope",
) -> dict[str, int | float]:
    """Evaluate labelled examples containing ``expected`` and ``predicted``.

    Each label should be ``in_scope`` or ``out_of_scope``. The positive class
    defaults to ``in_scope``; pass ``out_of_scope`` to measure that class instead.
    """
    rows = list(examples)
    if not rows:
        raise ValueError("At least one Scope Guard example is required")

    try:
        expected = [row["expected"] for row in rows]
        predicted = [row["predicted"] for row in rows]
    except KeyError as exc:
        raise ValueError(f"Missing required Scope Guard field: {exc.args[0]}") from exc

    allowed = {"in_scope", "out_of_scope"}
    if any(label not in allowed for label in expected + predicted):
        raise ValueError(f"Labels must be one of: {sorted(allowed)}")
    if positive_label not in allowed:
        raise ValueError(f"positive_label must be one of: {sorted(allowed)}")

    return binary_classification_metrics(expected, predicted, positive_label)
