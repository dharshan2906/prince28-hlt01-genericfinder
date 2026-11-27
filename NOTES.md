# Engineering Notes: GenericFinder

# D03 · PostgreSQL

## 1. Migrations (Upgrade → Downgrade → Upgrade)

**Commands:**

```powershell
uv run alembic downgrade -1
uv run alembic current
uv run alembic upgrade head
uv run alembic history
```

**Output:**

```text
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running downgrade 33109253a8d5 -> e3a1a83170de, add gin index on metadata

INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
e3a1a83170de

INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade e3a1a83170de -> 33109253a8d5, add gin index on metadata

e3a1a83170de -> 33109253a8d5 (head), add gin index on metadata
33b6760a5d5b -> e3a1a83170de, create documents and pages
4e1f23d45be8 -> 33b6760a5d5b, add gin index on metadata
<base> -> 4e1f23d45be8, create documents and pages
```

## 2. Loader Idempotency

**Run 1:**

```text
records=20 inserted=17 updated=0 unchanged=3
```

**Run 2:**

```text
records=20 inserted=0 updated=0 unchanged=20
```

**Run 3 (after editing one record):**

```text
records=20 inserted=0 updated=1 unchanged=19
```

## 3. EXPLAIN Analysis – `?drug_code=VALUE`

**Command:**

```powershell
uv run python scripts/explain.py drug_code VALUE
```

### 3.1 Default planner decision

```text
Seq Scan on documents
(cost=0.00..11.00 rows=1 width=36)
(actual time=0.880..0.880 rows=0.00 loops=1)

Filter: (metadata @> '{"drug_code": "VALUE"}'::jsonb)
Rows Removed by Filter: 20
Buffers: shared read=2 dirtied=2

Planning:
Buffers: shared hit=141 read=7

Planning Time: 4.128 ms
Execution Time: 0.906 ms
```

### 3.2 With sequential scan disabled

```text
Bitmap Heap Scan on documents
(cost=12.81..16.82 rows=1 width=36)
(actual time=1.296..1.297 rows=0.00 loops=1)

Recheck Cond: (metadata @> '{"drug_code": "VALUE"}'::jsonb)
Buffers: shared hit=1 read=2

-> Bitmap Index Scan on ix_documents_metadata_gin
(cost=0.00..12.81 rows=1 width=0)
(actual time=1.257..1.257 rows=0.00 loops=1)

Index Cond: (metadata @> '{"drug_code": "VALUE"}'::jsonb)
Index Searches: 1
Buffers: shared hit=1 read=2

Planning:
Buffers: shared hit=1

Planning Time: 0.077 ms
Execution Time: 1.347 ms
```

### 3.3 Why did the planner choose a Seq Scan? (2 lines)

The PostgreSQL planner estimated that scanning the entire table would be cheaper than using the index. This may happen when the table is small or the query matches a large percentage of rows.

### 3.4 When would it switch to the GIN index? (1 line)

When the query uses an index-supported operator and the planner estimates that using the GIN index is cheaper than a sequential scan.

---

# D04 · Docker, Compose and Tests

## 1. Docker Image

### 1.1 Image information

**Command:**

```powershell
docker images genericfinder:dev
```

**Output:**

```text
IMAGE               ID             DISK USAGE   CONTENT SIZE
genericfinder:dev   61ad5d9de906    301MB        70MB
```

### 1.2 Verify container user

**Command:**

```powershell
docker run --rm genericfinder:dev id
```

**Output:**

```text
uid=999(app) gid=999(app) groups=999(app)
```

### 1.3 Build measurements

| Measurement | Result |
|---|---:|
| Image content size | 70 MB |
| Target | Under 400 MB |
| First build | 24.32 seconds |
| After one-line code change | 5 seconds |

**Which step said CACHED, and why?**

Docker cached the dependency installation step because the dependency files hadn't changed, so it reused the existing layer instead of reinstalling packages.

## 2. Docker Compose Stack

### 2.1 Container status

**Command:**

```powershell
docker compose ps -a
```

**Output:**

```text
NAME                      IMAGE                    SERVICE   STATUS
genericfinder-api-1       genericfinder-api        api       Up (healthy)
genericfinder-db-1        pgvector/pgvector:pg17   db        Up (healthy)
genericfinder-migrate-1   genericfinder-migrate    migrate   Exited (0)
genericfinder-redis-1     redis:7-alpine           redis     Up (healthy)
```

### 2.2 Migration logs

**Command:**

```powershell
docker compose logs migrate
```

**First startup – final line:**

```text
records=20 inserted=20 updated=0 unchanged=0
```

**After `docker compose down` and `docker compose up -d`:**

Pending: Capture the final migration log line.

## 3. Breaking the Database on Purpose

### 3.1 Expected verification sequence

| Condition | Endpoint | Expected result |
|---|---|---|
| Database stopped | `/health` | 200 OK |
| Database stopped | `/ready` | 503 Service Unavailable |
| Database started | `/ready` | 200 OK |

**Commands:**

```powershell
docker compose stop db

curl.exe -i http://localhost:8000/health
curl.exe -i http://localhost:8000/ready

docker

## D05 · CI/CD and going live

- **Live URL:** https://prince28-hlt01-genericfinder.onrender.com
- **CI run for pull request 1:** https://github.com/dharshan2906/prince28-hlt01-genericfinder/actions
- **First deploy that ran by itself:** https://github.com/dharshan2906/prince28-hlt01-genericfinder/actions
- **Merge clicked at:** 10:15 AM → "Smoke test passed" at 10:19 AM → **Lead time: 4 min**

### Smoke test output from that CD run

```text
✓ Live URL responded successfully
✓ HTTP status: 200 OK
✓ Application health: ok
✓ Smoke test passed
```

### Rollback drill

- Rolled back to sha `92d8a64`: started 10:30 AM, smoke passed 10:34 AM (**4 min**).
- Rolled forward to sha `565cda0`: **5 min**.
- During the rollback, the database stayed on the newer schema. Why is that safe here?

The rollback changes only the application version; it does not reverse database migrations.
The newer schema remains compatible with the older application because the migrations are backward-compatible.

### Where my secrets live

- Neon string: GitHub Secret `DATABASE_URL` + Render environment. Not in Git, not in the image.
- Render deploy hook: GitHub Secret `RENDER_DEPLOY_HOOK` only.

### Monitoring

- UptimeRobot checks `/health` every 5 minutes; alerts go to my email.
- One thing that would make my live app faster on its first request: Keep the Render service always running to prevent cold starts.

# D06 · Collecting the Corpus

**Project:** GenericFinder · HLT-01
**Repository:** `prince28-hlt01-genericfinder`

## 1. Corpus Collection Summary

- **Start target:** Jan Aushadhi product list (2,000+ rows) and NLEM 2022.
- **Successfully downloaded:** 51 files through the FastAPI documentation sitemap, plus 2 Markdown files from the Git repository.
- **Total confirmed additions:** 53 files.
- **Pages and total MB:** Pending successful generation of `DATASET.md`. These measurements have not yet been verified.
- **Collection methods used:**
  - URL list – processed `data/sources.csv`.
  - Git repository – collected Markdown files from my GitHub repository.
  - Sitemap – collected matching documentation URLs from FastAPI.
  - By hand – not successfully used for a verified document.

## 2. Licence Check

| Source | Licence or terms, in my words | May I show full text in answers? |
|---|---|---|
| FastAPI documentation | MIT License was specified during collection; verify it against the source repository's licence. | Yes, if MIT coverage is confirmed and attribution is retained. |
| My GitHub repository | Licence or terms were entered as a placeholder and need verification. | Not confirmed. |
| NLEM 2022 (NHSRC) | Reuse permission has not been verified. | No full-text reuse until permission is confirmed. |
| PMBI / Jan Aushadhi / NPPA | Official government sources; individual document reuse terms still need verification. | Not confirmed. |

## 3. robots.txt Check

- **Site:** `https://fastapi.tiangolo.com/`
- **robots.txt:** Its contents have not yet been recorded in my terminal notes, so I cannot claim specific allow/disallow rules.
- **Blocked requests:** The sitemap download reported `blocked=0` and `failed=0`.
- **Action taken:** Used the sitemap to identify documentation URLs and downloaded the matching pages through the project downloader.

## 4. Kill and Resume Test

| Run | Result |
|---|---|
| Run 1 | Ctrl+C interruption count not recorded. |
| Run 2 | Sitemap URL download completed: `downloaded=51`, `skipped=10`. |
| Run 3 | A separate completed resume test with `downloaded=0` has not yet been recorded. |

**Status:** The successful download and skip behaviour are demonstrated, but the explicit Ctrl+C and resume test still needs to be performed and documented.

## 5. Capacity Planning

- **Tokens per page, measured:** Pending `DATASET.md` generation.
- **Full corpus:** Pending measured capacity report.
- **Full corpus target:** 3,000 pages.
- **Tokens, chunks, embedding cost and vector storage:** Not yet verified; these must come from `docs/CAPACITY.md`.

The capacity calculation will use measured document text, estimated tokens, chunk size, embedding dimensions and the configured embedding price rather than arbitrary assumptions.

## 6. One Thing That Went Wrong and How I Fixed It

Initially, I used the placeholder sitemap URL `https://SITE/sitemap.xml`, which caused a DNS resolution error (`getaddrinfo failed`). I replaced it with the actual FastAPI sitemap URL:

`https://fastapi.tiangolo.com/sitemap.xml`

I then applied the `/tutorial/` filter and a 300-URL limit. The sitemap returned 154 URLs, of which 51 matched. All 51 matching pages were downloaded successfully, with zero blocked and zero failed downloads.

**Learning:** Placeholder URLs must be replaced with real endpoints before running collection commands. Successful downloads must also be checked for source relevance and licence compliance before being included in the final medicine corpus.

## D07 · Parser comparison

<!-- parsers:start -->
| File | Parsers (A / B) | Pages | A found | B found | Time (A / B) | Better, why |
|---|---|---|---|---|---|---|
| pmbi-medicines-brochure-18102024-aeb9ec25.pdf | PyMuPDF / pypdf | - | FAILED: no_text_layer | FAILED: no_text_layer | 5.83 s / 8.37 s | Neither; both fail because the PDF has no text layer |
| nlem2022-457ffe96.pdf | PyMuPDF / pypdf | 135 | 266,280 chars, 53 headings, 101 tables | 109,147 chars, 0 headings, 0 tables | 17.47 s / 13.89 s | PyMuPDF; extracts more text, headings and tables |
| sql-databases-5b402114.html | trafilatura / strip tags | 47 | 96,339 chars, 47 headings, 0 tables | 117,570 chars, 35 headings, 0 tables | 3.55 s / 0.07 s | Trafilatura; better heading structure, strip tags is faster |
| view-more-f304ce98.html | trafilatura / strip tags | 1 | 23,090 chars, 0 headings, 0 tables | 25,181 chars, 0 headings, 0 tables | 0.71 s / 0.03 s | Needs manual inspection; strip tags is faster |
| oauth2-jwt-657ba832.html | trafilatura / strip tags | 19 | 40,295 chars, 19 headings, 0 tables | 50,527 chars, 16 headings, 0 tables | 1.09 s / 0.02 s | Trafilatura; better heading structure, strip tags is faster |
| simple-oauth2-1593ce4a.html | trafilatura / strip tags | 13 | 30,758 chars, 23 headings, 0 tables | 41,152 chars, 20 headings, 0 tables | 0.77 s / 0.03 s | Trafilatura; identifies more headings |
| query-params-str-validations-22be137a.html | trafilatura / strip tags | 10 | 27,024 chars, 22 headings, 0 tables | 36,479 chars, 3 headings, 0 tables | 1.05 s / 0.02 s | Trafilatura; much better heading extraction |
| bigger-applications-18edb09b.html | trafilatura / strip tags | 9 | 24,470 chars, 23 headings, 0 tables | 32,391 chars, 0 headings, 0 tables | 0.52 s / 0.02 s | Trafilatura; extracts meaningful heading structure |
| response-model-188ea97b.html | trafilatura / strip tags | 8 | 20,396 chars, 11 headings, 0 tables | 27,788 chars, 2 headings, 0 tables | 0.51 s / 0.01 s | Trafilatura; better heading extraction |
| classes-as-dependencies-e5b92d20.html | trafilatura / strip tags | 6 | 13,465 chars, 10 headings, 0 tables | 20,549 chars, 0 headings, 0 tables | 0.48 s / 0.02 s | Trafilatura; identifies headings that strip tags misses |
<!-- parsers:end -->

### D07 · Parsing my corpus

- **Files in the manifest:** 63
- **Successfully parsed:** 62
- **Failed:** 1
- **Pages stored in PostgreSQL:** 218
- **Parsing coverage:** 98.41% of files

The parser successfully processed 62 out of 63 files. One PDF could not be parsed because it did not contain an extractable text layer.

### Failures by reason

| Reason | Files | What I did |
|---|---:|---|
| `no_text_layer` | 1 | Retried parsing using `--retry-failed` and confirmed that the PDF still had no extractable text. Recorded it as a known parsing limitation. |

- **The one I investigated:** `pmbi-medicines-brochure-18102024-aeb9ec25.pdf`
- **Reason:** `no_text_layer`
- **Fix:** Retried the parser and verified the failure. The file requires OCR or an alternative text-based copy; it has not yet been successfully parsed.

### What I saw when I read my parsed pages

- **A page where the heading path is right:** To be filled after checking an actual parsed page in Neon SQL Editor.
- **Something that came out wrong:** To be filled after inspecting an extracted page for missing headings, repeated headers, footers or unwanted content.
- **A table:** To be filled after checking whether an extracted table appears as a Markdown grid or loose text.

### My parser choice

- **For PDFs I use PyMuPDF** because the NLEM 2022 comparison produced **266,280 characters, 53 headings and 101 tables**, compared with pypdf's **109,147 characters, 0 headings and 0 tables**. Although PyMuPDF took 17.47 seconds compared with pypdf's 13.89 seconds, it provided substantially richer structured output.
- **A kind of document neither parser handles well:** Scanned or image-only PDFs without an extractable text layer, such as the PMBI medicines brochure.

### One thing that went wrong today, and how I fixed it

The PMBI medicines brochure failed during parsing with the `no_text_layer` error. Initially, I retried the failed file using `--retry-failed`, but the same issue remained. I checked the failure summary in PostgreSQL and confirmed that the problem was limited to one file. This helped distinguish a document-level extraction issue from a problem with the overall parsing pipeline. The remaining 62 files were successfully processed, giving the corpus a parsing coverage of 98.41%.

# D08 · LLM Gateway Evaluation

## 1. Gateway configuration

| Component | Configuration |
|---|---|
| Primary provider | Google Gemini |
| Primary model declared in the D08 plan | `gemini-3.8-flash` |
| Fallback provider | Groq |
| Fallback model | `openai/gpt-oss-20b` |

> **Configuration verification:** The terminal output captured during testing identifies the actual model as `gemini-3.5-flash-lite`, not `gemini-3.8-flash`. Confirm the configured model and update either the application configuration or this report. The measurements below are attributed to the model name printed by the terminal.

## 2. First-question performance

The first captured laptop test was the Jan Aushadhi assistant greeting / scope test. The detailed timing record available in the terminal was:

| Metric | Measured result |
|---|---:|
| Provider / model shown in log | Gemini / `gemini-3.5-flash-lite` |
| Time to first words | 8.25 s |
| Total response time | 13.21 s |
| Input tokens | 185 |
| Output tokens | 24 |
| Estimated request cost | Rs 0.010972 |
| Attempts | 1 |
| Fallback used | No |

**Live deployment measurement:** Not present in the supplied terminal evidence. The second, awake request on the live URL still needs to be timed; do not substitute the laptop result for the live result.

**Day 1 latency target:** First words in under **1.5 seconds**.

**Evaluation:** The measured laptop time to first words (8.25 s) is 6.75 seconds above the target, or about 5.5 times the target. This is a performance gap to investigate. The total response time was 13.21 seconds.

## 3. Token comparison: English against Tamil

The three captured requests produced the following input-token counts:

| Message | Input tokens |
|---|---:|
| `Hi` (baseline; mostly system prompt) | 168 |
| `Explain in one sentence what a refund is.` | 176 |
| `பணத்தைத் திரும்பப் பெறுதல் என்றால் என்ன என்பதை ஒரே வாக்கியத்தில் விளக்கவும்.` | 184 |

Tamil-to-English token ratio:

`184 / 176 = 1.045`

The Tamil message used approximately **1.05 times** as many input tokens as the English message, or about **4.5% more**.

**Interpretation:** In this specific pair of prompts, the Tamil text used slightly more tokens. This is a single-example comparison, not a general rule for all English and Tamil inputs. Token counts can vary with wording, script, tokeniser and sentence length.

## 4. Behaviour when the answer is not in the documents

### Question 6: live Kendra hours and stock

**Prompt:**

> Is the Jan Aushadhi Kendra on my street open now and does it have stock?

**Exact captured response:**

> That question is outside this product's subject. For any dose or treatment decision, please ask a doctor or pharmacist.

**Evaluation:**

- The assistant did not claim that the Kendra was open.
- It did not invent stock availability or opening hours.
- It did not explicitly explain that it cannot access live store hours or inventory.
- The response therefore avoided fabricating facts, but its limitation message could be more precise.

**Recommended behaviour:** The assistant should say that it cannot verify a specific Kendra's current opening status or medicine stock unless a live store-hours or inventory source is connected. It should not guess.

### Off-topic question

**Prompt:**

> Who won the 2011 cricket world cup?

**Exact captured response:**

> That question is outside this product's subject.

**Evaluation:** The assistant declined the unrelated question in one sentence. This is consistent with the product's narrow scope.

### Incorrect or invented detail

No incorrect opening-hour or stock detail was observed in the supplied output. The assistant did not provide a factual answer to the live-availability question, so there is no demonstrated hallucinated detail to report.

## 5. Fallback and circuit breaker

The configured fallback is `openai/gpt-oss-20b` through Groq. However, the supplied test output shows `attempts=1` and `fallback=no` for the captured Gemini requests.

| Check | Evidence / result |
|---|---|
| Primary provider | Gemini |
| Configured fallback provider | Groq |
| Configured fallback model | `openai/gpt-oss-20b` |
| Fallback used in the supplied normal-request logs | No |
| Provider used when the primary was deliberately broken | Not supplied |
| Fallback first-word latency | Not supplied |
| Question number when Gemini error messages stopped appearing | Not supplied |

**Evaluation:** The configuration identifies a fallback, but the supplied normal-request logs do not prove that fallback execution or circuit-breaker recovery succeeded. A deliberate primary-provider failure test and its logs are required before marking this section as passed.

## 6. Usage and cost

The four captured request costs were:

| Request | Cost |
|---|---:|
| Greeting (`Hi`) | Rs 0.022601 |
| English refund question | Rs 0.007391 |
| Tamil refund question | Rs 0.008806 |
| Kendra open / stock question | Rs 0.010972 |
| **Total for these four captured requests** | **Rs 0.049770** |

The cricket question was also tested, but no separate cost or token line for it was included in the supplied output.

### Daily usage summary

| Metric | Value |
|---|---:|
| `/v1/usage` calls today | Not supplied |
| Errors | Not supplied |
| Fallbacks | Not supplied |
| `/v1/usage` total cost | Not supplied |
| Total cost of the four requests listed above | Rs 0.049770 |
| Average cost across those four requests | Rs 0.0124425 |
| Day 1 average-cost target | Under Rs 0.50 |

The average above is calculated only from the four requests with recorded costs:

`Rs 0.049770 / 4 = Rs 0.0124425`

This is approximately **Rs 0.0124 per request**, comfortably below the Rs 0.50 target. It is not a substitute for the complete `/v1/usage` daily average, because the full day's call and answer counts have not been provided.

## 7. What went wrong today and how it was addressed

During the live Kendra availability test, the assistant returned a generic out-of-scope message. Although it correctly avoided inventing opening hours or stock information, it did not explain the actual limitation: the application has no confirmed real-time connection to Kendra operating hours or inventory.

**Finding:** The current scope response is safe from an unsupported availability claim, but it is not sufficiently informative for this user question.

**Required improvement:**
1. Distinguish unsupported general-knowledge questions from questions that are relevant to Jan Aushadhi but require live data.
2. For live store status and stock questions, clearly state that the information cannot currently be verified.
3. Do not generate estimated opening hours, stock quantities or availability claims.
4. If a verified store-hours or inventory integration is added later, answer only from that source and identify when the information was checked.

**Status:** Issue identified; the improved response and any live-data integration still need to be implemented and tested. Do not describe this as fixed until a new test confirms the behaviour.

## 8. Overall D08 assessment

| Area | Current assessment |
|---|---|
| English and Tamil scope rejection | Passed in the captured examples |
| Greeting behaviour | Passed in the captured example |
| Off-topic rejection | Passed |
| Avoiding invented live stock / hours | No fabrication observed |
| Explaining live-data limitations | Needs improvement |
| Laptop first-word latency | Above target |
| Cost of four measured requests | Below target |
| Live URL latency | Measurement pending |
| Groq fallback | Not verified by supplied logs |
| Circuit breaker | Not verified by supplied logs |
| Daily `/v1/usage` totals | Pending |

### Evidence still required to close D08

- [ ] Record first-word latency for the second, awake request on the live URL.
- [ ] Verify whether the deployed primary model is `gemini-3.8-flash` or `gemini-3.5-flash-lite`.
- [ ] Run a controlled primary-provider failure test and capture proof that Groq handled the request.
- [ ] Record fallback first-word latency.
- [ ] Identify the question number after which Gemini error messages stopped appearing.
- [ ] Capture `/v1/usage` totals for calls, errors, fallbacks and cost.
- [ ] Retest the Kendra availability question after improving the limitation response.

---

**Reporting note:** Values marked as measured come directly from the terminal output supplied for this report. Values marked as pending or not supplied have deliberately not been estimated.

## D09 · Prompt versions compared

<!-- prompts:start -->

| Prompt version | Correct | Accuracy | Invalid replies | Avg tokens in |
|---|---|---|---|---|
| classify_v1 | 18/21 | 86% | 0 | 53 |
| classify_v2 | 20/21 | 95% | 0 | 237 |
| classify_v3 | 21/21 | 100% | 0 | 465 |
| classify_v4 | 20/21 | 95% | 0 | 237 |

<!-- prompts:end -->

### Resumability

Metadata extraction is resumable. Each document's validated metadata
or failure reason is committed independently to PostgreSQL.

The extraction query skips documents already processed with the
current prompt version. If execution is interrupted, rerunning the
same command processes only pending documents.

Failed documents can be retried explicitly using:

`uv run python scripts/extract_metadata.py --retry-failed`

The full available corpus of 57 documents was processed to validate
metadata extraction across the complete collected dataset rather
than relying on a smaller sample of 50 documents.


### Resumability Test

| Test | Result |
|---|---|
| Initial extraction | 57/57 successful |
| Second execution | pending=0 |
| Duplicate extraction | 0 documents |
| Additional token usage | 0 |
| Additional cost | Rs 0.0000 |

**Result:** Passed. Each document is committed independently.
Rerunning the extraction script skips documents already processed
with the current prompt version.

Command: `uv run python scripts/extract_metadata.py`

### Provider-Enforced JSON Schema

Command:
`uv run python scripts/extract_metadata.py --limit 20 --schema`

Prompt version: `extract_v2`

| Metric | Result |
|---|---:|
| Documents processed | 20 |
| Successful | 20 |
| Repaired | 0 |
| Failed | 0 |
| Input tokens | 47,501 |
| Output tokens | 3,418 |
| Cost | Rs 2.1656 |
| Duration | 211 seconds |

**Observation:** The provider accepted the JSON schema through
`response_format`. All 20 documents were extracted successfully
without validation retries or failures. No HTTP 400 error occurred.

# D10 · Queue and worker

## First run

-   Documents queued: **10**
-   Finished in: **52.6 seconds**
-   Done: **10**
-   Skipped: **0**
-   Failed: **0**
-   Pages processed: **33**
-   Pace: **5.26 seconds per document** (52.6 ÷ 10)
-   `INGEST_RPM`: **Not recorded**
-   `INGEST_CONCURRENCY`: **Not recorded**

## Kill test

-   Queued: **20**

-   At the kill:

    -   Queued: **13**
    -   Running: **2**
    -   Done: **5**
    -   Failed: **0**

-   After the new worker: final done + skipped + failed = **Not
    recorded** (must equal 20).

-   Documents in the database: **Not recorded**

-   Different document IDs: **Not recorded** (must equal the document
    count).

-   ARQ logged the interrupted jobs with a delay of approximately
    **471.67 seconds** (`try=2`). The exact elapsed time from worker
    termination to retry has not been independently measured.

-   Why that long: the jobs were scheduled for a delayed retry by the
    queue's retry/backoff mechanism. The exact configuration has not
    been checked.

-   Why nothing was doubled (in my own words):

    > The pipeline is idempotent, so retrying a document does not create
    > a duplicate document record.

## Dead-letter list

The endpoint returned:

``` json
{
  "count": 0,
  "items": []
}
```

  Stage (parse / extract / download / gave up)     Items What I did
  ---------------------------------------------- ------- -----------------
  parse                                                0 No retry needed
  extract                                              0 No retry needed
  download                                             0 No retry needed
  gave up                                              0 No retry needed

Running `uv run python scripts/ingest.py --retry-failed` returned
`Nothing to do: all of it is ingested.` because there were no
dead-letter items to retry.

## Live ingestion

-   GenericFinder on Render: **Not recorded** of 5 documents done.
-   Failed: **Not recorded**.
-   Failure reasons: **Not recorded**.
-   Status for a request without the token: **Not recorded**.

## Week 2 against Monday's estimate

-   `docs/CAPACITY.md`: **Not recorded** pages and **Not recorded**
    tokens.
-   `docs/INGEST_REPORT.md`: **Not recorded** pages and **Not recorded**
    tokens.
-   Difference and explanation: **Cannot calculate until both reports
    are checked.**

## One thing that went wrong today, and how I fixed it

The worker was forcefully terminated while two documents were running. I
restarted it with `uv run poe worker`. ARQ then picked up delayed jobs
again; the logs showed item 52 being skipped and items 53 onward
completing. The dead-letter endpoint remained empty.

## Remaining checks

1.  Retrieve the final status of job `995c368da04e4cf1a0fd5e66614d29ec`
    and confirm the final counts total 20.
2.  Query the database for the total document count and distinct
    document IDs.
3.  Record the Render ingestion result for all 5 documents.
4.  Send a request without the required token and record its HTTP
    status.
5.  Read `docs/CAPACITY.md` and `docs/INGEST_REPORT.md`, then compare
    their page and token estimates.


## 4. Additional Tests
- Test cases: 136 unit tests
- Passed: 136
- Failed: 0
- Execution time: 148.87 seconds
- Warning: Optional PySocks dependency missing (urllib3 SOCKS support)


### Two Workers, One Queue

- Workers: 2
- Queue size: 20
- Done: 10
- Skipped: 10
- Failed: 0
- Completion time: 58 seconds
- Duplicate item IDs in supplied logs: 0
- Worker 1 recovered 8 unfinished items at startup.
- Worker 2 started approximately 39 seconds after Worker 1.
- Both workers consumed the shared Redis queue.
- 2x speedup: Not established.
- Bottleneck: Shared model-provider quota and processing latency need further measurement.

### Redis Queue Inspection
- Redis queue type: Sorted Set (zset)
- Queue size observed: 26
- Queued jobs observed: ingest:137 through ingest:142
- Active in-progress locks: None in captured snapshot
- Job record TTL: 86,214 seconds (~23h 57m)
- Job serialization: Python pickle
- Queue inspection: Successful



138 tests passed
Full unit-test suite completed successfully:
- 138 passed
- 0 failed
- 1 non-blocking SOCKS dependency warning
- Runtime: 155.81 seconds
The D10 changes pass the complete unit-test suite.




### D10 · Queue and worker

- First run: 63 documents queued, finished in 311 s.
- Done: 62, skipped: 0, failed: 1.
- Pace: 4.94 s per document (INGEST_RPM = 20, INGEST_CONCURRENCY = 2).
- Final queue: 0 queued, 0 running.
- Pages processed: 400.
- Database verification: 62 done + 1 failed = 63.
- Failed file: pmbi-medicines-brochure-18102024-aeb9ec25.pdf
- Failure reason: parse: no_text_layer



### Database report

Documents in database: 16
Pages: 165
Tokens of text: 86,976
Files parser gave up on: 1
Documents with extracted record: 16
Documents whose extraction failed: 0

Ingest jobs started: 11
Items finished: 136
Items needing more than one try: 2
Dead-letter items: 0

Extraction model calls: 198
Tokens in: 500,638
Tokens out: 32,162
Cost: Rs 21.72

uv run python scripts/ingest.py --limit 63
HTTP 202: job d74cde8e0e9f40e9977c930a8d1d8268, 63 queued
working   queued=63 running=0 done=0 skipped=0 failed=0 pages=0 0s
working   queued=61 running=1 done=1 skipped=0 failed=0 pages=1 3s
working   queued=60 running=2 done=1 skipped=0 failed=0 pages=1 6s
working   queued=59 running=2 done=2 skipped=0 failed=0 pages=2 9s
working   queued=58 running=2 done=3 skipped=0 failed=0 pages=3 15s
working   queued=57 running=2 done=3 skipped=0 failed=1 pages=3 18s
working   queued=56 running=2 done=4 skipped=0 failed=1 pages=4 21s
working   queued=55 running=2 done=5 skipped=0 failed=1 pages=5 24s
working   queued=54 running=2 done=6 skipped=0 failed=1 pages=6 30s
working   queued=53 running=2 done=7 skipped=0 failed=1 pages=7 36s
working   queued=52 running=2 done=8 skipped=0 failed=1 pages=8 42s
working   queued=51 running=2 done=9 skipped=0 failed=1 pages=9 48s
working   queued=51 running=1 done=10 skipped=0 failed=1 pages=10 52s
working   queued=50 running=2 done=10 skipped=0 failed=1 pages=10 54s
working   queued=49 running=2 done=11 skipped=0 failed=1 pages=14 58s
working   queued=48 running=2 done=12 skipped=0 failed=1 pages=149 64s
working   queued=47 running=2 done=13 skipped=0 failed=1 pages=155 67s
working   queued=46 running=2 done=14 skipped=0 failed=1 pages=159 73s
working   queued=46 running=1 done=15 skipped=0 failed=1 pages=162 76s
working   queued=45 running=2 done=15 skipped=0 failed=1 pages=162 79s
working   queued=44 running=2 done=16 skipped=0 failed=1 pages=165 82s
working   queued=43 running=2 done=17 skipped=0 failed=1 pages=175 88s
working   queued=42 running=2 done=18 skipped=0 failed=1 pages=179 94s
working   queued=41 running=2 done=19 skipped=0 failed=1 pages=182 97s
working   queued=40 running=2 done=20 skipped=0 failed=1 pages=186 103s
working   queued=40 running=1 done=21 skipped=0 failed=1 pages=188 106s
working   queued=39 running=2 done=21 skipped=0 failed=1 pages=188 109s
working   queued=38 running=2 done=22 skipped=0 failed=1 pages=192 112s
working   queued=37 running=2 done=23 skipped=0 failed=1 pages=198 118s
working   queued=37 running=1 done=24 skipped=0 failed=1 pages=201 121s
working   queued=36 running=2 done=24 skipped=0 failed=1 pages=201 124s
working   queued=35 running=2 done=25 skipped=0 failed=1 pages=202 127s
working   queued=34 running=2 done=26 skipped=0 failed=1 pages=204 133s
working   queued=34 running=1 done=27 skipped=0 failed=1 pages=206 136s
working   queued=33 running=2 done=27 skipped=0 failed=1 pages=206 139s
working   queued=32 running=2 done=28 skipped=0 failed=1 pages=209 142s
working   queued=31 running=2 done=29 skipped=0 failed=1 pages=217 148s
working   queued=31 running=1 done=30 skipped=0 failed=1 pages=221 151s
working   queued=30 running=2 done=30 skipped=0 failed=1 pages=221 154s
working   queued=29 running=2 done=31 skipped=0 failed=1 pages=223 157s
working   queued=28 running=2 done=32 skipped=0 failed=1 pages=225 163s
working   queued=28 running=1 done=33 skipped=0 failed=1 pages=229 166s
working   queued=27 running=2 done=33 skipped=0 failed=1 pages=229 169s
working   queued=26 running=2 done=34 skipped=0 failed=1 pages=234 172s
working   queued=25 running=2 done=35 skipped=0 failed=1 pages=235 178s
working   queued=25 running=1 done=36 skipped=0 failed=1 pages=240 182s
working   queued=24 running=2 done=36 skipped=0 failed=1 pages=240 184s
working   queued=23 running=2 done=37 skipped=0 failed=1 pages=243 188s
working   queued=22 running=2 done=38 skipped=0 failed=1 pages=244 194s
working   queued=22 running=1 done=39 skipped=0 failed=1 pages=247 197s
working   queued=21 running=2 done=39 skipped=0 failed=1 pages=247 200s
working   queued=20 running=2 done=40 skipped=0 failed=1 pages=252 203s
working   queued=19 running=2 done=41 skipped=0 failed=1 pages=258 209s
working   queued=18 running=2 done=42 skipped=0 failed=1 pages=261 212s
working   queued=17 running=2 done=43 skipped=0 failed=1 pages=264 218s
working   queued=16 running=2 done=44 skipped=0 failed=1 pages=265 221s
working   queued=15 running=2 done=45 skipped=0 failed=1 pages=272 227s
working   queued=14 running=2 done=46 skipped=0 failed=1 pages=274 233s
working   queued=14 running=1 done=47 skipped=0 failed=1 pages=278 236s
working   queued=13 running=2 done=47 skipped=0 failed=1 pages=278 239s
working   queued=12 running=2 done=48 skipped=0 failed=1 pages=283 242s
working   queued=11 running=2 done=49 skipped=0 failed=1 pages=296 248s
working   queued=11 running=1 done=50 skipped=0 failed=1 pages=315 251s
working   queued=10 running=2 done=50 skipped=0 failed=1 pages=315 254s
working   queued=9 running=2 done=51 skipped=0 failed=1 pages=317 257s
working   queued=8 running=2 done=52 skipped=0 failed=1 pages=319 263s
working   queued=8 running=1 done=53 skipped=0 failed=1 pages=366 266s
working   queued=7 running=2 done=53 skipped=0 failed=1 pages=366 269s
working   queued=6 running=2 done=54 skipped=0 failed=1 pages=375 272s
working   queued=5 running=2 done=55 skipped=0 failed=1 pages=379 278s
working   queued=5 running=1 done=56 skipped=0 failed=1 pages=384 281s
working   queued=4 running=2 done=56 skipped=0 failed=1 pages=384 284s
working   queued=3 running=2 done=57 skipped=0 failed=1 pages=387 287s
working   queued=2 running=2 done=58 skipped=0 failed=1 pages=390 293s
working   queued=2 running=1 done=59 skipped=0 failed=1 pages=393 296s
working   queued=1 running=2 done=59 skipped=0 failed=1 pages=393 299s
working   queued=0 running=2 done=60 skipped=0 failed=1 pages=394 302s
working   queued=0 running=1 done=61 skipped=0 failed=1 pages=399 308s
finished  queued=0 running=0 done=62 skipped=0 failed=1 pages=400 311s
FAILED   data/raw/pmbi/pmbi-medicines-brochure-18102024-aeb9ec25.pdf  (1 try)  parse: no_text_layer

One failed document

data/raw/pmbi/pmbi-medicines-brochure-18102024-aeb9ec25.pdf

Reason: parse: no_text_layer

This indicates the PDF has no extractable text layer. It may require OCR. Do not count this as a worker or queue failure.



D10 · Queue and Worker in your report.
Live Queue Monitoring — API Stats Endpoint
Endpoint: GET http://localhost:8000/v1/ingest/stats


Queue status snapshot:

Queued: 24
Running: 2
Done: 36
Skipped: 0
Failed: 1

Total items: 63
Oldest queued item age: 183.8 seconds
