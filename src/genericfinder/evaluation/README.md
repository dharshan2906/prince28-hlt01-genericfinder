# GenericFinder Evaluation Module

This folder contains standalone evaluation functions. It is intentionally separate
from production API request analytics.

## Scope Guard input

Pass an iterable of dictionaries with `expected` and `predicted` labels:

```python
from genericfinder.evaluation import evaluate_scope_guard

examples = [
    {"expected": "in_scope", "predicted": "in_scope"},
    {"expected": "out_of_scope", "predicted": "in_scope"},
]
print(evaluate_scope_guard(examples))
```

The default positive class is `in_scope`. The function returns precision, recall,
F1-score, accuracy, and confusion-matrix counts.

## Document retrieval input

Pass an iterable of dictionaries with `relevant_ids` (ground-truth document IDs)
and `retrieved_ids` (IDs returned by the retriever, in ranked order):

```python
from genericfinder.evaluation import evaluate_retrieval

examples = [
    {
        "relevant_ids": ["doc-1", "doc-3"],
        "retrieved_ids": ["doc-1", "doc-2", "doc-3"],
    },
]
print(evaluate_retrieval(examples, k=3))
```

The retrieval evaluator returns per-query Precision@K, Recall@K, F1@K and macro
averages. Precision@K uses K as its denominator, including when fewer than K
results are returned.

## Important

These functions evaluate predictions against labelled ground truth. They do not
infer relevance or correctness automatically. The dataset labels must be reviewed
and validated before treating the scores as meaningful. This module is not yet
wired into GenericFinder's live Scope Guard or document retriever; integration
should be done after confirming their actual interfaces.
