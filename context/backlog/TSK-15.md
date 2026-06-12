# TSK-15: Report Exporting Engine (Exportação PDF/CSV)

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 2 Story Points / 8 Hours  
* **Story / Epic Reference:** FT-09 (Reporting & Exports)

## 📖 Description & Objectives

Build a reporting engine that writes standard inventory audit reports to disk. The application will allow exporting active pantry lists, expiration warning sheets, and waste discard history into cleanly formatted CSV files and structured printable PDF sheets.

## ✅ Definition of Ready (DoR)

* [ ] Use cases for stock state and log query adapters are functional.
* [ ] Target formatting rules and directory write permissions checked.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Criterion 1 (Functional):** Implement subcommand `estocapao export --format [csv|pdf] --output <path>` generating the files.
* [ ] **Criterion 2 (Validation):** Exported reports must include headers, timestamps, stock levels, safety thresholds, and active warnings.
* [ ] **Criterion 3 (Quality/Test):** Write integration tests verifying file creation, permission handling, and raw file structure.
* [ ] **Criterion 4 (Review):** Implement PDF export using pure Python libraries or simple structured generation to avoid external bloat.
