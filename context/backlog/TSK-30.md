# TSK-30: Layperson Interactive Prompts & Validation Badges

* **Owner / Assignee:** Kalyel Nunes Laurindo / PO  
* **Estimated Effort:** 2 Hours  
* **Story / Epic Reference:** FT-11 / UX Terminal  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Improve terminal usability for non-technical bakery workers by establishing dynamic shortcut helpers, simple interactive loops, and unified validation warnings.

Tasks:
1. Provide a language selection prompt menu (`[L] Idioma / Language`) within the interactive shell using single-character shortcuts.
2. Render clear color-coded Unicode alert boxes and validation brackets for warning of expired or low stock batches.
3. Establish ASCII fallbacks for environments with restricted unicode support.

## ✅ Definition of Ready (DoR)

* [x] Presenter localization adapter is fully functional (TSK-29).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Functional - Prompt]:** Interactive CLI shell supports dynamically switching the language on key input.
* [ ] **[Functional - Visuals]:** Validation errors show warning symbols `[⚠]` or `[✗]` in the selected language.
* [ ] **[Functional - Help]:** Detailed CLI usage reference is rendered in the active language.
* [ ] **[Verification]:** pytest runs successfully with 100% pass rate.
