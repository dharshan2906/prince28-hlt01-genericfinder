"""Tests for Scope Guard evaluation."""

import pytest

from genericfinder.evaluation.scope_guard import evaluate_scope_guard


def test_scope_guard_metrics():
    examples = [
        {"expected": "in_scope", "predicted": "in_scope"},
        {"expected": "in_scope", "predicted": "out_of_scope"},
        {"expected": "out_of_scope", "predicted": "in_scope"},
        {"expected": "out_of_scope", "predicted": "out_of_scope"},
    ]

    result = evaluate_scope_guard(examples)

    assert result["true_positives"] == 1
    assert result["false_positives"] == 1
    assert result["false_negatives"] == 1
    assert result["true_negatives"] == 1
    assert result["precision"] == 0.5
    assert result["recall"] == 0.5
    assert result["f1_score"] == 0.5
    assert result["accuracy"] == 0.5


def test_scope_guard_perfect_predictions():
    examples = [
        {"expected": "in_scope", "predicted": "in_scope"},
        {"expected": "out_of_scope", "predicted": "out_of_scope"},
    ]

    result = evaluate_scope_guard(examples)

    assert result["f1_score"] == 1.0
    assert result["accuracy"] == 1.0


def test_scope_guard_rejects_invalid_labels():
    examples = [
        {"expected": "unknown", "predicted": "in_scope"},
    ]

    with pytest.raises(ValueError):
        evaluate_scope_guard(examples)


def test_scope_guard_empty_dataset():
    with pytest.raises(ValueError):
        evaluate_scope_guard([])
