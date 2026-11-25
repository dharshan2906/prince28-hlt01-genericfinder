"""Reusable evaluation metrics for classification and document retrieval."""

from collections.abc import Sequence
from typing import Any


def binary_classification_metrics(
    y_true: Sequence[Any],
    y_pred: Sequence[Any],
    positive_label: Any = True,
) -> dict[str, int | float]:
    """Calculate binary precision, recall, F1-score, and accuracy.

    Zero-division is handled safely: a metric is 0.0 when its denominator is 0.
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same length")
    if not y_true:
        raise ValueError("At least one labelled example is required")

    tp = fp = fn = tn = 0
    for expected, predicted in zip(y_true, y_pred, strict=True):
        expected_positive = expected == positive_label
        predicted_positive = predicted == positive_label
        if expected_positive and predicted_positive:
            tp += 1
        elif not expected_positive and predicted_positive:
            fp += 1
        elif expected_positive and not predicted_positive:
            fn += 1
        else:
            tn += 1

    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if precision + recall else 0.0
    accuracy = (tp + tn) / len(y_true)

    return {
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "accuracy": round(accuracy, 4),
        "total_examples": len(y_true),
    }


def retrieval_metrics(
    relevant_ids: Sequence[str],
    retrieved_ids: Sequence[str],
    k: int = 5,
) -> dict[str, int | float]:
    """Calculate Precision@K, Recall@K, and F1@K for one query."""
    if k < 1:
        raise ValueError("k must be at least 1")

    relevant = set(relevant_ids)
    top_k = list(retrieved_ids[:k])
    relevant_retrieved = len(set(top_k) & relevant)

    precision = relevant_retrieved / k
    recall = relevant_retrieved / len(relevant) if relevant else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if precision + recall else 0.0

    return {
        "k": k,
        "relevant_documents": len(relevant),
        "retrieved_documents_at_k": len(top_k),
        "relevant_retrieved_at_k": relevant_retrieved,
        "precision_at_k": round(precision, 4),
        "recall_at_k": round(recall, 4),
        "f1_at_k": round(f1, 4),
    }
