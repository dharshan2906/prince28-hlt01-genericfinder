# GenericFinder — Dataset Documentation

## 1. Project Overview

**GenericFinder** is a medicine information and comparison system designed to identify exact generic medicine matches based on their composition, verify their inclusion in India's National List of Essential Medicines (NLEM), and present potential cost savings.

## 2. Dataset Scope

The dataset is planned in two phases.

### Initial Dataset

- Jan Aushadhi product and pricing list (target: 2,000+ product records).
- National List of Essential Medicines (NLEM 2022).

### Extended Dataset

The full corpus will include:

- Five historical Jan Aushadhi price lists.
- National List of Essential Medicines (NLEM 2015).
- Government scheme guidelines.
- NPPA ceiling-price notifications and orders.
- Additional supporting documents, targeting 3,000+ pages.

## 3. Data Sources

The following official sources have been identified for collection:

| Source | Information |
|---|---|
| [Jan Aushadhi](https://janaushadhi.gov.in/) | Generic medicine information and product listings |
| [PMBI](https://www.pmbi.co.in/) | Product and Maximum Retail Price (MRP) lists |
| [NHSRC — NLEM 2022](https://qps.nhsrc.org/sites/default/files/2022-09/nlem2022.pdf) | Essential medicines reference |
| [NPPA](https://www.nppaindia.nic.in/) | Drug price control notifications and ceiling-price orders |

## 4. Data Collection Methodology

Data collection is managed through the project's `scripts/fetch.py` utility.

**Repository:** [GenericFinder — GitHub](https://github.com/dharshan2906/prince28-hlt01-genericfinder)

The downloader is designed with the following safeguards:

- Respects website `robots.txt` restrictions.
- Limits concurrent requests to a maximum of four.
- Maintains a minimum delay of 0.5 seconds between requests to the same website.
- Supports manual document registration when automated retrieval is unavailable.
- Tracks source information and licensing terms for collected documents.

## 5. Data Usage and Attribution

GenericFinder follows these data-handling principles:

- Preserve the original source and publication date of every document.
- Link answers to their original source documents wherever possible.
- Display the applicable list or notification date because medicine prices and policies may change.
- Avoid collecting or storing personal information.
- Verify applicable copyright, licensing, and reuse conditions before storing or redistributing documents.

**Important:** Public availability does not automatically mean unrestricted reuse. Each source's applicable terms must be checked independently.

## 6. Known Gaps and Limitations

The initial dataset is not yet complete.

- The Jan Aushadhi product and pricing list still needs to be downloaded, validated, and registered.
- The NLEM 2022 document still needs to be collected and processed.
- Historical price lists, NLEM 2015, scheme guidelines, and NPPA ceiling-price orders remain part of the extended dataset.
- Source-specific reuse permissions and licensing conditions require verification.
- Product prices must be associated with their publication or effective dates to avoid presenting outdated information as current.

These gaps will be addressed progressively as the data collection pipeline is completed and validated.

## 7. Dataset Maintenance

The dataset will be periodically reviewed to identify updated price lists, revised essential medicines references, and new NPPA notifications.

Each collected document should retain its source, title, publication date, and applicable licence or terms to support traceability and reliable retrieval.

<!-- generated:start -->
## Sources (generated 2026-11-24 09:32 UTC by scripts/dataset_report.py)

| Source | Licence / terms | Files | MB | Pages* | How | Fetched | Example URL |
|---|---|---|---|---|---|---|---|
| NAME | LICENCE OR TERMS | 2 | 0.0 | 1 | git @ c32d55c179 | 2026-11-24 | https://github.com/dharshan2906/prince28-hlt01-genericfinder/blob/HEAD/docs/QUESTIONS.md |
| fastapi-docs | MIT License | 51 | 8.0 | 252 | http | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/ |
| janaushadhi | Reuse permission unverified | 1 | 0.0 | 0 | http | 2026-11-24 | https://janaushadhi.gov.in/product-portfolio/product-view-list |
| nhsrc | Reuse permission unverified | 1 | 4.7 | 135 | http | 2026-11-24 | https://qps.nhsrcindia.org/sites/default/files/2022-09/nlem2022.pdf |
| nppa | Reuse permission unverified | 6 | 1.1 | 13 | http | 2026-11-24 | https://nppa.gov.in/en/nlem2015 |
| pmbi | Reuse permission unverified | 2 | 5.1 | 8 | http | 2026-11-24 | https://www.pmbi.co.in/ProductList.aspx |

**Total:** 63 files, 18.9 MB, 410 pages. Not downloaded: 0 blocked by robots.txt, 0 failed.

*Pages = PDF pages, plus one page per 3,000 characters of text or HTML.

## Files (first 63 of 63)

The complete list, with a sha256 fingerprint of every file, is `data/manifest.jsonl`.

| # | Title / file | Source | Pages | Fetched | URL |
|---|---|---|---|---|---|
| 1 | docs/QUESTIONS.md | NAME | 1 | 2026-11-24 | https://github.com/dharshan2906/prince28-hlt01-genericfinder/blob/HEAD/docs/QUESTIONS.md |
| 2 | docs/REQUIREMENTS.md | NAME | 1 | 2026-11-24 | https://github.com/dharshan2906/prince28-hlt01-genericfinder/blob/HEAD/docs/REQUIREMENTS.md |
| 3 | background-tasks-3e17b7a1.html | fastapi-docs | 4 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/background-tasks/ |
| 4 | bigger-applications-18edb09b.html | fastapi-docs | 9 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/bigger-applications/ |
| 5 | body-db923f63.html | fastapi-docs | 4 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/body/ |
| 6 | body-fields-f7417381.html | fastapi-docs | 3 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/body-fields/ |
| 7 | body-multiple-params-79340250.html | fastapi-docs | 4 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/body-multiple-params/ |
| 8 | body-nested-models-99d5900d.html | fastapi-docs | 4 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/body-nested-models/ |
| 9 | body-updates-2d06f4f5.html | fastapi-docs | 4 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/body-updates/ |
| 10 | classes-as-dependencies-e5b92d20.html | fastapi-docs | 6 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/dependencies/classes-as-dependencies/ |
| 11 | cookie-param-models-b8bfc7ce.html | fastapi-docs | 3 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/cookie-param-models/ |
| 12 | cookie-params-6018d1dd.html | fastapi-docs | 2 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/cookie-params/ |
| 13 | cors-4f1cea92.html | fastapi-docs | 3 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/cors/ |
| 14 | debugging-222721d9.html | fastapi-docs | 2 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/debugging/ |
| 15 | dependencies-5ffb54cb.html | fastapi-docs | 5 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/dependencies/ |
| 16 | dependencies-in-path-operation-decorators-9cbf10cd.html | fastapi-docs | 4 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-in-path-operation-decorators/ |
| 17 | dependencies-with-yield-5c0232ed.html | fastapi-docs | 7 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/ |
| 18 | encoder-474e9700.html | fastapi-docs | 2 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/encoder/ |
| 19 | extra-data-types-5c77cdd1.html | fastapi-docs | 3 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/extra-data-types/ |
| 20 | extra-models-bcff185a.html | fastapi-docs | 4 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/extra-models/ |
| 21 | first-steps-1d1f5505.html | fastapi-docs | 6 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/first-steps/ |
| 22 | first-steps-3368d50f.html | fastapi-docs | 4 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/security/first-steps/ |
| 23 | frontend-3854a0fd.html | fastapi-docs | 3 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/frontend/ |
| 24 | get-current-user-6666a3a6.html | fastapi-docs | 5 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/security/get-current-user/ |
| 25 | global-dependencies-eafe5a52.html | fastapi-docs | 2 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/dependencies/global-dependencies/ |
| 26 | handling-errors-9e3b6bbf.html | fastapi-docs | 5 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/handling-errors/ |
| 27 | header-param-models-22664928.html | fastapi-docs | 3 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/header-param-models/ |
| 28 | header-params-4033bc35.html | fastapi-docs | 3 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/header-params/ |
| 29 | metadata-afa173ff.html | fastapi-docs | 4 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/metadata/ |
| 30 | middleware-6bcf3c71.html | fastapi-docs | 3 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/middleware/ |
| 31 | oauth2-jwt-657ba832.html | fastapi-docs | 14 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/ |
| 32 | path-operation-configuration-c7921cf3.html | fastapi-docs | 3 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/path-operation-configuration/ |
| 33 | path-params-ec79efde.html | fastapi-docs | 5 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/path-params/ |
| 34 | path-params-numeric-validations-0c9737f6.html | fastapi-docs | 5 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/ |
| 35 | query-param-models-a2cdd64f.html | fastapi-docs | 4 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/query-param-models/ |
| 36 | query-params-07af7caf.html | fastapi-docs | 3 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/query-params/ |
| 37 | query-params-str-validations-22be137a.html | fastapi-docs | 10 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/query-params-str-validations/ |
| 38 | request-files-07a3c0ee.html | fastapi-docs | 5 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/request-files/ |
| 39 | request-form-models-934cf05f.html | fastapi-docs | 4 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/request-form-models/ |
| 40 | request-forms-16928256.html | fastapi-docs | 3 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/request-forms/ |
| 41 | request-forms-and-files-44778666.html | fastapi-docs | 2 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/request-forms-and-files/ |
| 42 | response-model-188ea97b.html | fastapi-docs | 8 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/response-model/ |
| 43 | response-status-code-0daf007f.html | fastapi-docs | 3 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/response-status-code/ |
| 44 | schema-extra-example-65a090b7.html | fastapi-docs | 5 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/schema-extra-example/ |
| 45 | security-c2d779e5.html | fastapi-docs | 3 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/security/ |
| 46 | server-sent-events-fa46f3b7.html | fastapi-docs | 5 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/server-sent-events/ |
| 47 | simple-oauth2-1593ce4a.html | fastapi-docs | 11 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/security/simple-oauth2/ |
| 48 | sql-databases-5b402114.html | fastapi-docs | 31 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/sql-databases/ |
| 49 | static-files-08b76fb1.html | fastapi-docs | 2 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/static-files/ |
| 50 | stream-json-lines-591a9b1b.html | fastapi-docs | 4 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/stream-json-lines/ |
| 51 | sub-dependencies-7c664f58.html | fastapi-docs | 3 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/ |
| 52 | testing-459f3498.html | fastapi-docs | 5 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/testing/ |
| 53 | tutorial-d77ca978.html | fastapi-docs | 4 | 2026-11-24 | https://fastapi.tiangolo.com/tutorial/ |
| 54 | Jan Aushadhi Product List | janaushadhi |  | 2026-11-24 | https://janaushadhi.gov.in/product-portfolio/product-view-list |
| 55 | National List of Essential Medicines 2022 | nhsrc | 135 | 2026-11-24 | https://qps.nhsrcindia.org/sites/default/files/2022-09/nlem2022.pdf |
| 56 | CAPPMS Guidelines | nppa | 1 | 2026-11-24 | https://nppa.gov.in/en/cappmsguidelines |
| 57 | Compendium of Medicine Prices | nppa | 1 | 2026-11-24 | https://nppa.gov.in/en/compendiumofprice |
| 58 | Drugs Prices Control Order 2013 | nppa | 1 | 2026-11-24 | https://nppa.gov.in/en/dpco2013 |
| 59 | National List of Essential Medicines 2015 | nppa | 1 | 2026-11-24 | https://nppa.gov.in/en/nlem2015 |
| 60 | Therapeutic Category Wise Ceiling Price List | nppa | 1 | 2026-11-24 | https://nppa.gov.in/en/therapeuticcategorywiseceilingpricelist |
| 61 | NPPA Circulars and Orders | nppa | 8 | 2026-11-24 | https://nppa.gov.in/en/view_more?id=4 |
| 62 | PMBI Medicines Price List Brochure 2024 | pmbi | 8 | 2026-11-24 | https://www.pmbi.co.in/Data/eBrochure/PMBI%20MEDICINES%20BROCHURE_18102024.pdf |
| 63 | PMBI Product and MRP List | pmbi |  | 2026-11-24 | https://www.pmbi.co.in/ProductList.aspx |
<!-- generated:end -->
