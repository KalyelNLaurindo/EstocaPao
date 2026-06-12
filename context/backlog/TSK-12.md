# TSK-12: Basic Language Menu Support (Menu de Idiomas Básico)

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 1 Story Point / 4 Hours  
* **Story / Epic Reference:** FT-06 (Internationalization)

## 📖 Description & Objectives

Implement a simple language translation utility (I18n) for the command-line interface. The CLI must support switching between Portuguese (PT-BR) and English (EN). The language selection can be configured via a global `--lang` CLI flag or defined persistent in `config.ini`.

## ✅ Definition of Ready (DoR)

* [ ] Configuration parser (`config.ini` handler) is functional and accessible.
* [ ] Translation string catalogs (dictionaries) for PT-BR and EN defined.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Criterion 1 (Functional):** The CLI accepts a global option `--lang [pt|en]` (e.g., `estocapao status --lang en`) which overrides the default language for that execution.
* [ ] **Criterion 2 (Persistence):** A setting `default_language` is added to `config.ini` under a `[locale]` section, allowing persistent default language configuration.
* [ ] **Criterion 3 (Quality/Test):** Write unit tests checking that CLI output correctly changes vocabulary and formatting headings when switching languages.
* [ ] **Criterion 4 (Review):** Standardize all CLI warning messages, statuses (OK, LOW_STOCK, QUARANTINE), and output grids to have exact translations.
