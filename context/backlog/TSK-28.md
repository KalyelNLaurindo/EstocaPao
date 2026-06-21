# TSK-28: i18n File Registry & Config Parser

* **Owner / Assignee:** Kalyel Nunes Laurindo / PO  
* **Estimated Effort:** 3 Hours  
* **Story / Epic Reference:** FT-06 (Internationalization)  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Implement a localized string resource manager for EstocaPão supporting Portuguese, English, French, Spanish, and German to aid bakery workers of different nationalities.

The engine will:
1. Load locale resource files (JSON format) from the `locales/` directory.
2. Read system language settings from `config.json`.
3. Provide a localized translation resolver that accepts variables for dynamic message outputs (e.g. `translate("batch_added", ingredient="Farinha")`).

## ✅ Definition of Ready (DoR)

* [x] Configuration parsing and bootstrapping configuration file are implemented (TSK-05).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Test suite asserts that localized maps load without error and return expected translation strings in all 5 target languages.
* [ ] **[Functional - Selection]:** System selects active language with preference: 1. argparse `--lang` flag, 2. `config.json` entry, 3. system locale settings, 4. fallback `pt`.
* [ ] **[Functional - Files]:** Directory `locales/` contains valid resource schemas: `pt.json`, `en.json`, `fr.json`, `es.json`, `de.json`.
* [ ] **[Verification]:** pytest runs successfully with 100% pass rate.
