# GenericFinder

Finds the exact Jan Aushadhi generic match for a medicine composition, checks whether it is on India's essential medicines list and shows the saving.

**Status:** Day 1 foundation (FastAPI skeleton, quality gates). Live URL from Day 5.

## Who it's for

Son of a retired mill worker in Madurai who buys diabetes and BP medicines worth about Rs 3,000 a month and wants cheaper options to discuss with the doctor.

## The problem

Many patients spend significant amounts on branded medicines for common health conditions. They often lack reliable information about affordable generic alternatives with the same active ingredients. Comparing medicine prices across different sources is also difficult. GenericFinder aims to simplify generic medicine identification and price comparison using Indian government datasets, helping users discuss cost-effective options with their doctors.

## Data sources

PMBI Jan Aushadhi product and MRP list, NLEM 2022, Jan Aushadhi FAQs and scheme guidelines, NPPA ceiling price notices.

- https://janaushadhi.gov.in/
- https://www.pmbi.co.in/ (Product & MRP List)
- https://qps.nhsrcindia.org/sites/default/files/2022-09/nlem2022.pdf
- https://www.nppaindia.nic.in/
- Terms: Public government lists. Always show the list date because prices change.

## Hardest problem (my interview story)

Composition matching: 'Glimepiride 2 mg + Metformin 500 mg SR' must match the exact combination, strength and release type. A near match (500 mg immediate-release) is dangerous, so matching uses parsed fields and exact rules, and the app must say 'no exact match' instead of guessing.

## Signature feature

Strip checker: type the composition from the strip and see exact matches, monthly saving and an 'ask your doctor before switching' banner.

## Target metric

100% precision on 60 composition tests (never a wrong strength or release type); 90%+ recall.

## Limitations

- Medicine information depends on the availability and freshness of source datasets.
- Real-time Jan Aushadhi Kendra stock and opening hours are not currently supported.
- GenericFinder does not provide medical diagnosis or prescribe medicine.
- Users should consult a qualified healthcare professional before changing medication.

## Project Highlights

- Retrieval-augmented question answering.
- Source-grounded responses with document citations.
- Exact medicine composition matching.
- Scope guard for unsupported questions.
- Automated evaluation and testing.
- PostgreSQL-backed document storage.

## Run it locally

```bash
uv sync
cp .env.example .env   # Windows: copy .env.example .env
uv run uvicorn genericfinder.api.main:create_app --factory --reload
```

Then open http://localhost:8000/docs

## Checks

```bash
uv run pytest
uv run ruff check .
```
## Documentation

- [Requirements](requirements.md)
- [Changelog](CHANGELOG.md)

## Project Status

GenericFinder is under active development. Features and evaluation results are updated as development progresses.

## Run locally in one command

You need Docker Desktop running. From a fresh clone:

```bash
docker compose up --build
```

This starts Postgres (with pgvector), Redis, runs the migrations and loads the sample data once, then starts the API.

- API docs: http://localhost:8000/docs
- Liveness: http://localhost:8000/health
- Readiness (checks the database): http://localhost:8000/ready

Stop with `Ctrl+C`, then `docker compose down`. Add `-v` to also delete the database volume.

## Develop and test

| Task | Mac / Linux | Windows |
|---|---|---|
| Run the API with reload | `make dev` | `uv run poe dev` |
| Unit tests (no network) | `make test` | `uv run poe test` |
| Integration tests (needs `docker compose up`) | `make test-integration` | `uv run poe test-integration` |
| Coverage report | `make cov` | `uv run poe cov` |
| Lint and format check | `make lint` | `uv run poe lint` |

[![CI](https://github.com/dharshan2906/prince28-hlt01-genericfinder/actions/workflows/ci.yml/badge.svg)](https://github.com/dharshan2906/prince28-hlt01-genericfinder/actions/workflows/ci.yml)
[![Live](https://img.shields.io/website?url=https%3A%2F%2Fprince28-hlt01-genericfinder.onrender.com%2Fhealth&label=live)](https://prince28-hlt01-genericfinder.onrender.com/docs)
[![Uptime (30 days)](https://img.shields.io/uptimerobot/ratio/m804787866-a994cf42c71d0ff3ae5fa765)](https://prince28-hlt01-genericfinder.onrender.com/health)

**Live:** https://prince28-hlt01-genericfinder.onrender.com · [API docs](https://prince28-hlt01-genericfinder.onrender.com/docs) · [health](https://prince28-hlt01-genericfinder.onrender.com/health)


##  Day 07: Corpus Parsing

Run all commands from the project root:

```powershell
cd C:\class\GENAI\prince28-hlt01-genericfinder
```

### 1. Source Collection

```powershell
# Fetch Markdown files from a GitHub repository
uv run python scripts/fetch.py repo fastapi/fastapi --path docs --ext .md --source fastapi-docs --licence "MIT License"

# Process URLs listed in the sources manifest
uv run python scripts/fetch.py urls

# View the source manifest
Get-Content data/sources.csv
```

### 2. Dataset Report

```powershell
# Generate a full dataset and capacity report
uv run python scripts/dataset_report.py --full-pages 3000
```

### 3. Database Migrations

```powershell
# Generate a migration automatically from model changes
uv run alembic revision --autogenerate -m "add page headings and parse failures"

# Apply migrations to the database
uv run alembic upgrade head
```

### 4. Corpus Parsing

```powershell
# Parse all files in the corpus
uv run python scripts/parse_corpus.py

# Retry previously failed files
uv run python scripts/parse_corpus.py --retry-failed

# Parse a limited number of files
uv run python scripts/parse_corpus.py --limit 20
```

### 5. Check Parsing Failures in PostgreSQL

Run in the Neon SQL Editor:

```sql
SELECT
    reason,
    COUNT(*) AS files,
    MIN(path) AS example
FROM parse_failures
GROUP BY reason
ORDER BY files DESC;
```

### 6. Compare Parsers

```powershell
# Compare the two available parsers on selected difficult files
uv run python scripts/compare_parsers.py
```

### 7. Code Quality and Testing

```powershell
# Run linting and formatting checks
uv run poe lint

# Run tests with coverage report
uv run poe cov
```

### 8. Git Status

```powershell
# Check current branch and working-tree changes
git status

# Review staged and unstaged changes
git diff

# Review staged changes
git diff --cached
```

**Key Result:** The corpus contained 63 files. Parsing successfully processed 62 files and stored 218 pages in PostgreSQL, achieving 98.41% file parsing coverage. One scanned/image-based PDF remained unsuccessful because of `no_text_layer`.
