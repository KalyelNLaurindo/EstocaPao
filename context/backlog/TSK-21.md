# TSK-21: Elegant Field Control & Auto-formatting (Controle de Campos Elegante e Auto-formatação)

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 1 Story Point / 4 Hours  
* **Story / Epic Reference:** FT-12 (Security & Input Hardening)

## 📖 Description & Objectives

Improve the user experience and data consistency of all string inputs by implementing automatic field normalization rules at the CLI adapter layer. Currently, ingredient names are stored as-typed, leading to inconsistencies (e.g., "farinha", "Farinha", "FARINHA" coexisting as separate IDs). This task standardizes how names, IDs, and other text fields are persisted: first-letter capitalization, whitespace collapsing, and ID derivation rules. These transformations must be transparent to the user (no manual formatting required) and must be visible in the confirmation message printed after each operation.

## ✅ Definition of Ready (DoR)

* [ ] TSK-20 (Input Hardening) DoD is met or actively in progress, so that sanitizer functions are available for reuse.
* [ ] Existing `add` and `update` command flows are stable.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Criterion 1 (Title Case Capitalization):** Ingredient names entered in any case variation (e.g., `"FARINHA DE TRIGO"`, `"farinha de trigo"`) are stored with title-case formatting (`"Farinha De Trigo"`). The transformation is applied before persistence and reflected in all outputs.
* [ ] **Criterion 2 (Whitespace Collapsing):** Multiple consecutive spaces within a name are collapsed into a single space (e.g., `"Farinha  De  Trigo"` → `"Farinha De Trigo"`). Leading and trailing spaces are always stripped.
* [ ] **Criterion 3 (Deterministic ID Derivation):** The ingredient ID (used as the lookup key in the repository) is derived by: (a) lower-casing the normalized name, (b) replacing spaces with underscores, and (c) stripping any remaining non-alphanumeric characters except underscore. Example: `"Farinha De Trigo"` → ID `"farinha_de_trigo"`. This prevents duplicate records for the same ingredient.
* [ ] **Criterion 4 (Quantity Display Precision):** Quantities are always displayed with exactly 3 decimal places in confirmation messages and status tables (e.g., `"12.500 kg"` instead of `"12.5"`). The unit label (if provided) is appended to the display string.
* [ ] **Criterion 5 (Confirmation Echo):** After each successful `add` or `update`, the confirmation message echoes the normalized (post-transformation) name and derived ID so the user can verify the stored key: *`Ingrediente 'Farinha De Trigo' (ID: farinha_de_trigo) adicionado com sucesso no lote LOT-xxxxx.`*
* [ ] **Criterion 6 (Quality/Test):** Unit tests in `tests/unit/test_field_normalization.py` assert correct output for: all-uppercase input, all-lowercase input, mixed-case input, multi-space input, and special character stripping. At least one integration test verifies that adding `"FARINHA"` and then attempting to add `"farinha"` results in an update to the same record, not a duplicate.
* [ ] **Criterion 7 (Review):** Normalization functions (`normalize_name`, `derive_id`) are added to `src/estocapao/shared/sanitizer.py` (or its own `src/estocapao/shared/normalizer.py` if sanitizer scope is too broad). `cli.py` calls these functions; domain entities receive already-normalized data.
