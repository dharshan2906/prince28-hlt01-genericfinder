# Capacity Planning & Cost Analysis — GenericFinder

## Corpus Growth Target

The planned full corpus includes five historical medicine price lists, NLEM 2015, government scheme guidelines, and NPPA ceiling-price orders, targeting **3,000+ document pages**.

This assessment estimates the storage and embedding requirements for the planned corpus and identifies the measurements required before production deployment.

## 1. Embedding Cost Assessment

**Conclusion:** Embedding cost is expected to be manageable for an initial corpus of 3,000 pages, provided documents are cleaned, deduplicated, and divided into appropriately sized chunks before embedding.

For an initial planning estimate, assume:

| Parameter | Planning assumption |
|---|---:|
| Total document pages | 3,000 |
| Average extracted text per page | 500 tokens |
| Estimated input tokens | 1,500,000 |
| Embedding operations | One initial batch, plus future updates |

Estimated embedding cost:

\[
\text{Cost} =
\frac{1,500,000}{1,000,000}
\times \text{model price per million tokens}
\]

The final cost depends on the embedding provider, model, chunking strategy, and whether documents need to be re-embedded after updates.

**Assessment:** Initial embedding is a one-time ingestion expense for unchanged documents. Incremental embedding can reduce repeated processing costs.

## 2. PostgreSQL Storage Assessment

**Conclusion:** The planned corpus is expected to be manageable for a small PostgreSQL deployment, but actual compatibility with the free-tier storage quota must be confirmed using the database dashboard.

Storage consists of three major components:

- **Document text:** Extracted content and metadata stored for retrieval and source attribution.
- **Embeddings:** Numerical vectors stored using the PostgreSQL vector extension.
- **Indexes and overhead:** Vector indexes, relational indexes, metadata, and database storage overhead.

For illustration, assuming 6,000 chunks and 1,536-dimensional single-precision vectors:

\[
6,000 \times (1,536 \times 4 + 8)
= 36,912,000 \text{ bytes}
\]

This is approximately **35.2 MiB of raw vector data**, excluding text, indexes, metadata, and database overhead.

Actual storage must be measured after ingestion.

**Free PostgreSQL storage limit:** [Enter dashboard quota]

**Measured database usage:** [Enter current usage]

**Storage headroom:** [Quota minus current usage]

## 3. Least Certain Estimate and Measurement Plan

**Conclusion:** The least certain estimate is the actual number of chunks generated from the source documents, because PDF extraction quality, page density, tables, repeated content, and chunk size can significantly affect the final count.

To improve accuracy:

1. Collect a representative sample of documents from each source.
2. Extract and clean their text.
3. Record the total extracted tokens and generated chunk count.
4. Generate embeddings and measure their actual storage usage.
5. Extrapolate the measured averages to the complete corpus.

This approach replaces theoretical estimates with measurements from the actual ingestion pipeline.

## 4. Impact of 10× Corpus Growth

A tenfold increase would raise the corpus target from 3,000 to approximately **30,000 pages**, increasing the number of text chunks, embedding operations, and database storage requirements.

Embedding expenses and raw vector storage would grow approximately in proportion to the number of chunks, while indexing, query performance, and maintenance requirements would need additional evaluation. Potential improvements include batch processing, incremental embedding, efficient indexing, and archival of outdated price lists.

## 5. Final Assessment

GenericFinder's initial corpus is suitable for a controlled prototype, subject to successful document ingestion and storage verification. The primary capacity risks are inaccurate PDF extraction, unexpected chunk growth, and database index overhead rather than the raw embedding vectors alone.

The estimates in this document are planning assumptions, not measured production results. They should be updated after the first complete ingestion and database storage measurement.

<!-- generated:start -->
## Measured on my start corpus (2026-11-24 09:32 UTC)

| What | Value |
|---|---|
| Files | 63 |
| Size on disk | 18.9 MB |
| Pages (PDF pages + 1 per 3,000 characters of text/HTML) | 410 |
| Characters of text | 885,907 |
| Estimated tokens (characters / 4) | 221,477 |
| Tokens per page | 541 |
| PDFs with almost no text (scanned? OCR is Day 7) | 1 |
| Files not measured (zip, xlsx, unreadable) | 0 |

## Estimate for the full corpus (target: 3,000 pages)

| What | How | Value |
|---|---|---|
| Scale factor | target / measured | x 7.3 |
| Tokens | measured tokens x scale | 1.62 M |
| Raw files | measured MB x scale | 139 MB |
| Chunks | tokens / 400 x 1.15 overlap | 4,662 |
| Embedding cost, one time | tokens x 1.15 x $0.15 per 1M | $0.28 = Rs 27 |
| Vector storage | chunks x 768 numbers x 4 bytes | 14 MB |
| Text in Postgres | characters x scale x 1.2 | 8 MB |

Assumptions: 4 characters per token, 400-token chunks, 768-dimension embeddings at $0.15 per 1M tokens, Rs 95 per US dollar.
<!-- generated:end -->
