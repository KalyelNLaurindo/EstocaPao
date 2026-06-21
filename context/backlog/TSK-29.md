# TSK-29: Localization of CLI Presenter & Unicode Table Strings

* **Owner / Assignee:** Kalyel Nunes Laurindo / PO  
* **Estimated Effort:** 3 Hours  
* **Story / Epic Reference:** FT-06 (Internationalization)  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

Extract all user-facing terminal interface labels, stock warnings, headers, and report logs in EstocaPão and pipe them to the dynamic i18n Translation Service.

This task includes:
1. Moving all hardcoded text strings in `src/infra/cli.py` and output functions to locale resources under `locales/`.
2. Resolving presenter table column labels, alerts, and stock status texts using translation keys.

## ✅ Definition of Ready (DoR)

* [x] i18n File Registry and resources mapping are implemented (TSK-28).
* [x] CommandLineInterfaceParser is operational (TSK-09).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Unit tests verify that calling CLI output functions displays translated texts for at least 3 distinct active locales.
* [ ] **[Functional - Tables]:** All tabular print outputs (`list-ingredients`, `low-stock`) use translated headers and status badges.
* [ ] **[Functional - Alignment]:** Alignment is preserved across different languages without layout wrapping.
* [ ] **[Verification]:** pytest runs successfully with 100% pass rate.
