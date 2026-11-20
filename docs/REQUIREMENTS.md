# Requirements: GenericFinder

## Functional (what it does)

1. A user can ask a question in plain English and get an answer drawn from my sources.
2. Every answer cites the document and page (or section) it came from.
3. If the documents do not contain the answer, the product says "I don't know" instead of guessing.
4. Signature feature: Strip checker: type the composition from the strip and see exact matches, monthly saving and an 'ask your doctor before switching' banner.
5. A user can browse and search the underlying records through GET /v1/documents.

## Non-functional (how well, with numbers)

| # | Quality | Target | How I will measure it |
|---|---|---|---|
| 1 | Speed: record lookups | p95 under 300 ms for GET /v1/documents | Load test (Week 6) |
| 2 | Speed: answers | p95 under 4 s for a full answer; first token under 1.5 s | Traces (Week 5) |
| 3 | Accuracy | 100% precision on 60 composition tests (never a wrong strength or release type); 90%+ recall. | Golden question set (Weeks 4 and 5) |
| 4 | Cost | Under Rs 1.00 per answered question | llm_calls table (Week 2) |
| 5 | Availability | 95% monthly uptime during the initial pilot | Uptime monitor from Day 5 |

## Target change explanations

- **Cost:** Increased the target from Rs 0.50 to Rs 1.00 because document retrieval and LLM processing may increase the cost per answered question.
- **Availability:** Changed the target from 99% to 95% because this is an initial student-project deployment with limited infrastructure and maintenance resources.
- **Accuracy:** Kept 100% precision for composition matching because incorrect medicine strength or release-type matches could be dangerous. The 90% recall target is retained.