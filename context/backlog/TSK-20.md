# TSK-20: Malicious Input & Edge Case Hardening (Proteção contra Entradas Maliciosas e Edge Cases)

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 2 Story Points / 8 Hours  
* **Story / Epic Reference:** FT-12 (Security & Input Hardening)

## 📖 Description & Objectives

Perform a comprehensive audit of all CLI entry points and domain validation logic to identify and close security and data-integrity gaps introduced by malformed, oversized, or intentionally malicious inputs. This task targets injection-style attacks (shell metacharacters, path traversal sequences), buffer-overflow-like payloads (extremely long strings), Unicode normalization attacks (homoglyphs, RTL overrides), and numeric boundary violations. All mitigations must be enforced at the CLI adapter layer — before data ever reaches domain objects — and must produce clear, user-friendly Portuguese error messages rather than stack traces.

## ✅ Definition of Ready (DoR)

* [ ] All CLI commands (`add`, `update`, `status`, `discard`) are implemented and covered by E2E tests.
* [ ] Domain validation layer (`DomainValidationError`) is functional.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Criterion 1 (String Sanitization):** Ingredient names are stripped of leading/trailing whitespace and control characters (`\x00`–`\x1f`, `\x7f`). Shell metacharacters (`; & | > < $ \` ( )`) are rejected with a clear error: *"Nome do ingrediente contém caracteres não permitidos."*
* [ ] **Criterion 2 (Length Limits):** Ingredient names are capped at 64 characters. Batch IDs and date strings are capped at 32 characters. Any input exceeding these limits is rejected with an informative error before processing.
* [ ] **Criterion 3 (Numeric Boundaries):** Quantities are validated to be within `(0, 999_999.999]` for additions and `(-999_999.999, 0)` for consumptions. Safety limits are validated within `[0, 999_999.999]`. Inputs outside these ranges are rejected as invalid domain data.
* [ ] **Criterion 4 (Date Integrity):** Expiration dates must not be in the past at time of insertion. Received dates must not be in the future. Both constraints raise descriptive `ValueError` messages at the CLI layer.
* [ ] **Criterion 5 (Unicode Hardening):** Names are normalized to NFC Unicode form. Inputs containing bidirectional override characters (U+202A–U+202E, U+2066–U+2069) or zero-width characters (U+200B, U+FEFF) are rejected.
* [ ] **Criterion 6 (Path Traversal):** The `discard` command's `batch_id` argument must not contain path separators (`/`, `\`, `..`) or null bytes. Violations are rejected before reaching the repository layer.
* [ ] **Criterion 7 (Quality/Test):** A dedicated test module `tests/unit/test_input_hardening.py` covers each criterion above with at least two boundary inputs each — one that should pass and one that should fail with the correct error type and message substring.
* [ ] **Criterion 8 (Review):** All sanitization logic lives in a new `src/estocapao/shared/sanitizer.py` module, exposed as pure functions called by `cli.py`. Domain entities must not be responsible for this level of surface-area protection.
