# TSK-31: CLI Accessibility and Daltonism Protection Mode

* **Owner / Assignee:** Kalyel Nunes Laurindo / PO  
* **Estimated Effort:** 2 Hours  
* **Story / Epic Reference:** FT-11 / UX Terminal  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Ensure the EstocaPão inventory CLI interface operates correctly in accessibility mode, supporting blind/visually impaired operators using screen readers and those with color blindness.

Tasks:
1. Detect standard `NO_COLOR` env variable and `--no-color` option to disable all terminal escape color sequences.
2. Structure printed tables (`list-ingredients`, `low-stock`) to render linearly without complex Unicode borders when `--linear` is requested.
3. Validate error messages output so they use explicit textual annotations instead of only green/red text flags.

## ✅ Definition of Ready (DoR)

* [x] i18n Presenter Localization and table printing is implemented (TSK-29).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Test cases verify that setting `NO_COLOR=1` env or `--no-color` param strips stdout of all escape code sequences.
* [ ] **[Functional - Accessibility]:** CLI implements parameter `--linear` which strips tables of double-lines and wraps properties vertically for linear reading.
* [ ] **[Functional - Visuals]:** Validation errors render prefix text blocks (e.g. `[WARNING]`) instead of relying solely on colors to indicate alerts.
* [ ] **[Verification]:** pytest runs successfully with 100% pass rate.
