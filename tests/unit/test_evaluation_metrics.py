"""Tests for evaluation metric calculations."""

import pytest

from genericfinder.evaluation.metrics import (
    binary_classification_metrics,
    retrieval_metrics,
)


def test_binary_classification_metrics():
    result = binary_classification_metrics(
        [True, True, False, False],
        [True, False, True, False],
    )

    assert result["true_positives"] == 1
    assert result["false_positives"] == 1
    assert result["false_negatives"] == 1
    assert result["true_negatives"] == 1
    assert result["precision"] == 0.5
    assert result["recall"] == 0.5
    assert result["f1_score"] == 0.5
    assert result["accuracy"] == 0.5


def test_perfect_classification():
    result = binary_classification_metrics(
        [True, False],
        [True, False],
    )

    assert result["precision"] == 1.0
    assert result["recall"] == 1.0
    assert result["f1_score"] == 1.0
    assert result["accuracy"] == 1.0


def test_zero_division():
    result = binary_classification_metrics(
        [False, False],
        [False, False],
    )

    assert result["precision"] == 0.0
    assert result["recall"] == 0.0
    assert result["f1_score"] == 0.0


def test_mismatched_classification_lengths():
    with pytest.raises(ValueError):
        binary_classification_metrics([True], [True, False])


def test_empty_classification_data():
    with pytest.raises(ValueError):
        binary_classification_metrics([], [])


def test_retrieval_metrics():
    result = retrieval_metrics(
        relevant_ids=["doc-1", "doc-3"],
        retrieved_ids=["doc-1", "doc-2", "doc-3"],
        k=3,
    )

    assert result["precision_at_k"] == 0.6667
    assert result["recall_at_k"] == 1.0
    assert result["f1_at_k"] == 0.8


def test_invalid_k():
    with pytest.raises(ValueError):
        retrieval_metrics(["doc-1"], ["doc-1"], k=0)
