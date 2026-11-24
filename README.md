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
