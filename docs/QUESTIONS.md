# GenericFinder – Real User Evaluation Questions

**Evaluation Set:** Week 3 – Initial Evaluation
**Version:** 1.0
**Last Updated:** 26 November 2026
**Total Questions:** 10
**Status:** Ground-truth mapping in progress

## 1. User Persona

**Target User:**

A son of a retired mill worker in Madurai whose father spends approximately ₹3,000 per month on diabetes and blood-pressure medicines.

He wants to identify affordable generic medicine alternatives, compare prices, and discuss potential savings with a doctor before making any changes.

**User's primary needs:**
- Find exact Jan Aushadhi medicine matches.
- Understand medicine prices and availability from official sources.
- Compare generic and branded medicine costs.
- Identify potential monthly savings.
- Receive reliable answers supported by government documents.

## 2. Real User Questions

These questions are intentionally written in natural language, reflecting how the target user would actually ask them.

| # | User Question | Query Type | Expected Source | Multi-page? |
|---|---|---|---|---|
| 1 | Is Telmisartan 40 mg available under Jan Aushadhi, and what is its MRP? | Factual retrieval | PMBI Product & MRP List – Page TBD | No |
| 2 | Is Metformin on the NLEM 2022, and at which level of care? | Factual retrieval | NLEM 2022 – Page TBD | No |
| 3 | What is the Jan Aushadhi price of Atorvastatin 10 mg tablets? | Price retrieval | PMBI Product & MRP List – Page TBD | No |
| 4 | My father takes Glimepiride 2 mg + Metformin 500 mg SR twice a day and Telmisartan 40 mg once a day. What are the exact Jan Aushadhi matches and the monthly saving against ₹3,000? | Multi-step reasoning | PMBI Product & MRP List – Pages TBD | Yes |
| 5 | Compare NLEM 2015 and NLEM 2022 for antidiabetic medicines: what was added or removed? | Document comparison | NLEM 2015 and NLEM 2022 – Pages TBD | Yes |
| 6 | Is the Jan Aushadhi Kendra on my street open now and does it have stock? | Unanswerable / Scope guard | No supporting document | N/A |
| 7 | How much can I save monthly if I buy generic diabetes medicines instead of branded ones? | Cost calculation | PMBI Product & MRP List and verified branded price sources – Pages TBD | Yes |
| 8 | Is there a generic alternative for my father's BP medicine, Telmisartan? | Medicine identification | PMBI Product & MRP List – Page TBD | No |
| 9 | What is the difference between Metformin 500 mg normal tablets and SR tablets? | Formulation comparison | Reliable medicine reference documents – Pages TBD | Yes |
| 10 | Can I find all these diabetes and BP medicines at Jan Aushadhi, and what will be the total monthly cost? | Multi-step retrieval and calculation | PMBI Product & MRP List – Pages TBD | Yes |

*Page numbers must be filled after checking the actual source documents. Do not assume or fabricate page references.*

## 3. Expected Behaviour

| Question | Expected System Behaviour |
|---|---|
| Q01 | Find the exact Telmisartan 40 mg entry and return its verified MRP. |
| Q02 | Confirm Metformin's NLEM 2022 listing and healthcare level with a citation. |
| Q03 | Retrieve the exact Atorvastatin 10 mg tablet price or report insufficient evidence. |
| Q04 | Match both prescriptions exactly, verify release type, calculate 30-day quantities and compare costs. |
| Q05 | Compare both NLEM versions and identify supported additions and removals. |
| Q06 | Return exactly `I don't know`. |
| Q07 | Calculate savings only when equivalent medicine prices and quantities are available. |
| Q08 | Identify the generic ingredient and matching products without recommending a treatment change. |
| Q09 | Explain immediate-release versus sustained-release formulations using reliable evidence. |
| Q10 | Identify exact matches, calculate individual and total monthly costs, and identify unavailable matches. |

## 4. Ground-Truth Source Mapping

Before evaluating answers, complete this table using the original source documents.

| Question | Source Document | Page / Section | Verified? |
|---|---|---|---|
| Q01 | PMBI Product & MRP List | TBD | Pending |
| Q02 | NLEM 2022 | TBD | Pending |
| Q03 | PMBI Product & MRP List | TBD | Pending |
| Q04 | PMBI Product & MRP List | TBD | Pending |
| Q05 | NLEM 2015 and NLEM 2022 | TBD | Pending |
| Q06 | None | Not available | Confirmed |
| Q07 | PMBI list and branded price source | TBD | Pending |
| Q08 | PMBI Product & MRP List | TBD | Pending |
| Q09 | Reliable formulation reference | TBD | Pending |
| Q10 | PMBI Product & MRP List | TBD | Pending |

## 5. Evaluation Rules

### Answer correctness
- Answers must be supported by retrieved documents.
- Important factual claims must include source citations.
- Missing evidence must never be replaced with invented information.

### Medicine matching
- Match active ingredients and combinations exactly.
- Verify the strength of every ingredient.
- Verify dosage form and release type.
- Reject approximate matches as exact matches.

### Cost calculation
- Use verified prices for both branded and generic products.
- Calculate quantities using the stated dosage frequency and a 30-day month.
- Show the calculation and assumptions.
- Do not claim savings when comparable prices are unavailable.

### Scope guard
- Q06 must return exactly `I don't know`.
- The system must not invent Kendra opening hours, location-specific stock, or real-time availability.

## 6. Evaluation Metrics

| Metric | Target |
|---|---:|
| Exact medicine matching precision | 100% |
| Exact medicine matching recall | ≥ 90% |
| Q06 scope-guard correctness | 100% |
| Citation correctness | To be measured |
| Retrieval correctness | To be measured |
| Answer latency (p95) | Under 4 seconds |

## 7. Evaluation Results

Record actual results after running each question through GenericFinder.

| Question | Retrieval | Citation | Answer | Result |
|---|---|---|---|---|
| Q01 | Pending | Pending | Pending
