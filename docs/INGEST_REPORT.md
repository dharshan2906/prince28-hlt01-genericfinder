# Ingestion report

<!-- generated:start -->
_Generated 27 Nov 2026 20:40 from the database._

| What | Count |
|---|---|
| Documents in the database | 16 |
| Pages | 165 |
| Tokens of text (characters ÷ 4) | 86,976 |
| Files the parser gave up on | 1 |
| Documents with an extracted record | 16 |
| Documents whose extraction failed | 0 |

| Queue | Count |
|---|---|
| Ingest jobs started | 11 |
| Items finished (done or skipped) | 136 |
| Items that needed more than one try | 2 |
| Items in the dead-letter list | 0 |

Model calls for extraction: 198 · tokens in 500,638 · tokens out 32,162 · cost at list price Rs 21.72

Last job `7b4f4bf36b7149fbbb435a344700cc0b`: 46 requested, 0 ok, 0 failed, 0.0 minutes.
<!-- generated:end -->

## What I learnt

Learned how to implement asynchronous document ingestion using FastAPI, Redis, and ARQ workers.
Understood job tracking, retries, failure handling, and queue monitoring through database-backed statistics.
Identified PDF parsing limitations and learned why OCR is necessary for scanned documents without a text layer.
