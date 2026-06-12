# TSK-06: Secure File Permission Locks & Structural Scheme Validator

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 2 Story Points / 8 Hours  
* **Story / Epic Reference:** FT-01 & FT-04 (File Setup & Safe Persistence)

## 📖 Description & Objectives

Incorporate local file-protection configurations into the system initializers using standard OS calls (`os.chmod`) to prevent unauthorized process access. In addition, create a fast, pre-load structural checker that inspects the integrity of the backup file before parsing data into runtime memory.

## ✅ Definition of Ready (DoR)

* [x] Core bootstrap initializers from TSK-05 written and tested.  
* [x] Explicit schema layouts mapped out in system SDDs.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **Criterion 1 (Functional):** File initializers must invoke `os.chmod` to enforce highly restrictive access structures on config.ini and db_backup.json (`chmod 600` on POSIX environments). Non-Unix platforms must implement a clean fallback execution.  
* [x] **Criterion 2 (Security):** If the JSON file contains malformed structures, empty arrays, or lacks mandatory keys (id, name, safety_threshold, batches), the validator halts initialization, protecting memory state from corrupt external modifications.  
* [x] **Criterion 3 (Quality/Test):** Write integration tests in `tests/integration/test_initializer.py` asserting correct permission settings and schema rejection under corrupted mock JSON data.  
* [x] **Criterion 4 (Review):** Verify OS module interactions do not cause platform-specific failures, ensuring flawless executions on Windows-based terminal structures.
