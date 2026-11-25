"""Tests for document retrieval evaluation."""

import pytest

from genericfinder.evaluation.retrieval import evaluate_retrieval


def test_retrieval_evaluation():
    examples = [
        {
            "relevant_ids": ["doc-1", "doc-3"],
            "retrieved_ids": ["doc-1", "doc-2", "doc-3"],
        },
        {
            "relevant_ids": ["doc-4"],
            "retrieved_ids": ["doc-4", "doc-5", "doc-6"],
        },
    ]

    result = evaluate_retrieval(examples, k=3)

    assert result["queries_evaluated"] == 2
    assert result["mean_precision_at_k"] == 0.5
    assert result["mean_recall_at_k"] == 1.0
    assert result["mean_f1_at_k"] == 0.65


def test_retrieval_empty_dataset():
    with pytest.raises(ValueError):
        evaluate_retrieval([])


def test_retrieval_invalid_example():
    examples = [{"question": "Find a medicine"}]

    with pytest.raises(ValueError):
        evaluate_retrieval(examples)


def test_retrieval_invalid_k():
    examples = [
        {
            "relevant_ids": ["doc-1"],
            "retrieved_ids": ["doc-1"],
        }
    ]

    with pytest.raises(ValueError):
        evaluate_retrieval(examples, k=0)
