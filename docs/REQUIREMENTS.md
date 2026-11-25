# GenericFinder – Software Requirements Specification

**Project:** GenericFinder
**Version:** 1.0
**Last Updated:** 26 November 2026
**Status:** Under Development

## 1. Project Overview

GenericFinder helps users identify affordable generic medicine alternatives by matching medicine compositions, checking government medicine databases, and comparing prices.

The system provides reliable, source-backed information so users can discuss cost-effective treatment options with qualified healthcare professionals.

**Target Users:** Patients and caregivers seeking information about affordable generic medicines, particularly for common conditions such as diabetes and hypertension.

## 2. Project Objectives

- Identify exact generic medicine matches using active ingredients, strength, dosage form, and release type.
- Retrieve information from trusted government sources.
- Provide source citations for generated answers.
- Compare branded and generic medicine prices where reliable data is available.
- Avoid unsupported recommendations and misleading medicine matches.

## 3. Functional Requirements

| ID | Requirement | Priority |
|---|---|---|
| FR-01 | Accept natural-language medicine-related questions from users. | High |
| FR-02 | Retrieve relevant information from the available document corpus. | High |
| FR-03 | Generate answers grounded in retrieved documents. | High |
| FR-04 | Provide document citations, including page numbers or sections wherever available. | High |
| FR-05 | Respond with "I don't know" when the available sources do not contain sufficient evidence. | High |
| FR-06 | Match medicines using active ingredients, strength, dosage form, and release type. | High |
| FR-07 | Reject near matches when strength, composition, or release type differs. | High |
| FR-08 | Compare generic and branded medicine prices when verified price data is available. | Medium |
| FR-09 | Calculate estimated monthly savings using dosage frequency and available prices. | Medium |
| FR-10 | Provide an appropriate warning to consult a doctor before changing medicines. | High |
| FR-11 | Allow users to browse and search document records through `GET /v1/documents`. | Medium |

## 4. Non-Functional Requirements

| ID | Category | Requirement | Target |
|---|---|---|---|
| NFR-01 | Performance | Document lookup response time (p95). | Under 300 ms |
| NFR-02 | Performance | Complete answer response time (p95). | Under 4 seconds |
| NFR-03 | Performance | First-token response time. | Under 1.5 seconds |
| NFR-04 | Accuracy | Precision on the medicine composition test set. | 100% |
| NFR-05 | Accuracy | Recall on the medicine composition test set. | At least 90% |
| NFR-06 | Cost | Estimated cost per answered question. | Under ₹1 |
| NFR-07 | Availability | Initial pilot monthly availability target. | 95% |
| NFR-08 | Maintainability | Application code must pass configured linting and automated tests. | No outstanding check failures |

*These are project targets, not claims of measured production performance. Actual results must be recorded separately.*

## 5. Medicine Matching and Safety Requirements

Medicine matching is a safety-critical feature.

The system must compare:

1. Active ingredient or combination of ingredients.
2. Strength of every ingredient.
3. Dosage form, such as tablet or capsule.
4. Release type, such as immediate-release or sustained-release.
5. Other relevant formulation details when available.

**Example:**

- Requested: Glimepiride 2 mg + Metformin 500 mg SR.
- Candidate: Glimepiride 2 mg + Metformin 500 mg immediate-release.
- Expected result: Reject as an exact match.

The system must:

- Never present an approximate match as an exact match.
- Never invent medicine prices or availability.
- Display the source and date of price information.
- Clearly distinguish information from medical advice.
- Advise users to consult a qualified doctor before switching medicines.
- Return no exact match when reliable matching evidence is unavailable.

## 6. Data Sources

The system may use the following sources:

| Source | Purpose |
|---|---|
| Pradhan Mantri Bhartiya Janaushadhi Pariyojana (PMBJP) / PMBI | Generic medicine products and prices |
| National List of Essential Medicines (NLEM 2022) | Essential medicine classification |
| National Pharmaceutical Pricing Authority (NPPA) | Drug price-control information |
| Jan Aushadhi official website | Scheme information and guidelines |

Official references:

- https://janaushadhi.gov.in/
- https://www.pmbi.co.in/
- https://qps.nhsrcindia.org/sites/default/files/2022-09/nlem2022.pdf
- https://www.nppaindia.nic.in/

Data must be checked for reliability, source date, and relevance before being used in an answer.

## 7. Evaluation Requirements

The system will be evaluated using a set of 10 representative user questions.

| ID | Test Scenario | Expected Behaviour |
|---|---|---|
| Q01 | Jan Aushadhi availability and MRP of Telmisartan 40 mg | Return verified information with citations. |
| Q02 | Whether Metformin is included in NLEM 2022 | Answer using the official NLEM source. |
| Q03 | Jan Aushadhi price of Atorvastatin 10 mg | Return a verified price or state insufficient evidence. |
| Q04 | Multi-medicine composition and monthly savings calculation | Match exact compositions and show calculation details. |
| Q05 | Compare NLEM 2015 and NLEM 2022 antidiabetic medicines | Explain differences using both source documents. |
| Q06 | Current opening hours and stock at a nearby Jan Aushadhi Kendra | Return exactly "I don't know" when real-time data is unavailable. |
| Q07 | Estimate monthly savings on generic diabetes medicines | Calculate only from verified prices and stated quantities. |
| Q08 | Generic alternative for Telmisartan | Provide evidence-backed alternatives without recommending a treatment change. |
| Q09 | Difference between Metformin 500 mg and Metformin 500 mg SR | Explain the release-type difference using reliable sources. |
| Q10 | Find multiple diabetes and blood-pressure medicines and calculate total cost | Return verified matches and a transparent cost calculation. |

Each evaluation result should record:

- Question ID
- Expected answer
- Ground-truth source
- Actual answer
- Citation correctness
- Retrieval correctness
- Pass or fail status

## 8. Acceptance Criteria

GenericFinder will meet its initial acceptance criteria when:

- All 10 evaluation scenarios have documented expected behaviour.
- Medicine matching achieves 100% precision on the 60-case composition test set.
- Medicine matching achieves at least 90% recall on the same test set.
- Unsupported answers are handled without fabricated information.
- Retrieved answers include appropriate source citations.
- The application passes automated tests and configured code-quality checks.
- Performance and cost targets are measured and documented.

## 9. Requirement Change Justification

| Requirement | Target | Reason |
|---|---|---|
| Answer cost | ₹0.50 → ₹1.00 | Allows for retrieval and language-model processing costs. |
| Availability | 99% → 95% | More realistic for a student-developed application and limited infrastructure. |
| Medicine matching precision | Retained at 100% | Incorrect medicine matches could create safety risks. |

## 10. Future Scope

- Real-time Jan Aushadhi Kendra location and availability integration.
- Improved multilingual question answering.
- Expanded government medicine dataset coverage.
- More comprehensive medicine composition evaluation.
- Performance monitoring and production deployment improvements.
