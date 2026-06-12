# TSK-09: Build CommandLineInterfaceParser and Command Arguments Router

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 3 Story Points / 12 Hours  
* **Story / Epic Reference:** FT-05 (CLI & Alerts Router)

## 📖 Description & Objectives

Build the core CLI parsing and navigation gateway CommandLineInterfaceParser in `src/estocapao/modules/inventory/infra/cli.py`. Built on Python's native argparse standard library, it handles routing terminal requests, validating raw console arguments, and calling the corresponding application use-cases.

## ✅ Definition of Ready (DoR)

* [x] Use cases and persistence adapters complete and fully tested.  
* [x] Target CLI commands defined and standardized.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **Criterion 1 (Functional):** Build parsing layouts for terminal executions:  
  * `estocapao add <name> <qty> --exp <date> --limit <threshold>`  
  * `estocapao update <id> <qty>`  
  * `estocapao status`  
  * `estocapao discard <batch_id>`  
* [x] **Criterion 2 (Validation):** The console parser performs initial whitespace cleaning, validates quantity inputs (preventing string values or invalid negatives), and structures dates into operational formats, generating helpful user-facing errors instead of system trace crashes.  
* [x] **Criterion 3 (Quality/Test):** E2E shell execution tests located in `tests/e2e/test_cli_commands.py` simulate standard CLI inputs and assert correct operational outputs.  
* [x] **Criterion 4 (Review):** Verify structural boundaries; CLI router files should act only as adapters and must not run business rules directly.
