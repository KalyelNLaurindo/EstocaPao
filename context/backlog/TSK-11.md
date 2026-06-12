# TSK-11: Establish Package Setup (pyproject.toml) and Entry Point Execution Engine

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 2 Story Points / 8 Hours  
* **Story / Epic Reference:** FT-01 & FT-05 (Packaging / Execution)

## 📖 Description & Objectives

Write the global execution entrypoint `src/main.py` and build the packaging configuration `pyproject.toml` at the project's root directory. This configures the application for distribution, enabling immediate installation via standard Python tools and defining `estocapao` as a system-wide executable command.

## ✅ Definition of Ready (DoR)

* [ ] All core domain models, use cases, repository adapters, and CLI routing structures complete and tested.  
* [ ] Project metadata, execution dependencies, and license definitions locked.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Criterion 1 (Functional):** The master file `src/main.py` bootstraps the system initialization parser and passes terminal inputs to the CLI routing module. The `pyproject.toml` file declares the entry points section, mapping the global terminal command `estocapao` to target execution functions.  
* [ ] **Criterion 2 (Distribution):** Verify that executing `pip install -e .` on a local development terminal compiles the application cleanly, making the executable console command `estocapao` available globally.  
* [ ] **Criterion 3 (Quality/Test):** Create comprehensive end-to-end integration tests in `tests/e2e/test_cli_commands.py` validating command behavior using subprocess calls to the compiled executable.  
* [ ] **Criterion 4 (Review):** Validate PEP8 standards on the packaging configuration. The setup must specify zero external third-party execution dependencies, relying only on standard libraries.
