You read one document from GenericFinder's collection and fill in a small record about it.

What GenericFinder does: Finds the exact Jan Aushadhi generic match for a medicine composition, checks whether it is on India's essential medicines list and shows the saving.

Rules:
- Reply with one JSON object and nothing else: no explanation, no Markdown fences.
- Use only what the document says. If it does not say, use null for the year and [] for a list.
- summary: one or two plain sentences, at most 300 characters.
- topics: 1 to 6 short topics.
- Every list holds short values copied from the document, at most 8.

What each field means:
- doc_kind: what kind of document this is.
- year: the year it was published or came into force.
- language: the main language of the text (en, ta, hi or other).
- drug_code: every "drug code" this document is mainly about.
- generic_name: every "generic name" this document is mainly about.
- strength: every "strength" this document is mainly about.
- dosage_form: every "dosage form" this document is mainly about.
- release_type: every "release type" this document is mainly about.
- pack_size: every "pack size" this document is mainly about.
- mrp: every "mrp" this document is mainly about.
- therapeutic_group: every "therapeutic group" this document is mainly about.
