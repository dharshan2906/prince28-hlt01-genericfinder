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
