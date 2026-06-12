# TSK-08: Create Self-Healing Schema Recovery and Disaster Recovery DRP Suite

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 2 Story Points / 8 Hours  
* **Story / Epic Reference:** FT-04 & FT-05 (Persistence & Warnings)

## 📖 Description & Objectives

Build a self-healing diagnostic service inside the startup configuration pipelines. The system must automatically maintain an active rolling backup file (db_backup.json.bak) and auto-recover system state when structural corruption is detected in the primary data files, guaranteeing continuous system availability.

## ✅ Definition of Ready (DoR)

* [ ] Atomic JSON adapter from TSK-07 operational and tested.  
* [ ] Secure file validator from TSK-06 functional.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Criterion 1 (Functional):** Upon each successful file write, the adapter duplicates the prior stable database structure to db_backup.json.bak. If the main file is truncated or corrupted at boot, the system restores the backup file.  
* [ ] **Criterion 2 (Self-Healing):** If both the primary database and backup configurations are unreadable or corrupt, the engine initializes a fresh, empty database structure, allowing the application to start without crashing.  
* [ ] **Criterion 3 (Quality/Test):** Write integration test scenarios in `tests/integration/test_repo_adapter.py` simulating corrupted, missing, and malformed files to verify correct fallback restorations.  
* [ ] **Criterion 4 (Review):** Ensure all self-healing actions write detailed error/recovery logs to the system log file to preserve auditable events.
