# TSK-10: Build Logging Engine & Colored CLI Warn/Info Outputs

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 1 Story Point / 4 Hours  
* **Story / Epic Reference:** FT-05 (CLI & Alerts Router)

## 📖 Description & Objectives

Develop a local event logger (Logger) and terminal output formatting tool (TerminalAnsiFormatter) inside `src/estocapao/shared/`. The component records system actions to a local file and formats warnings using bright, high-contrast ANSI colors for easy readability.

## ✅ Definition of Ready (DoR)

* [x] Operational CommandLineInterfaceParser functional and tested.  
* [x] Color parameters and warning formatting specifications defined.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **Criterion 1 (Functional):** Business mutations (additions, updates, deletions, and quarantine warnings) must append automatically to `estocapao.log` with standardized timestamp layouts (YYYY-MM-DD HH:MM:SS).  
* [x] **Criterion 2 (Visual Style):** Critical conditions (Low Stock, Expiration) must render using bold Red (`\033[91m`) and Yellow (`\033[93m`) ANSI codes. Non-interactive terminals (non-TTY) must strip ANSI codes automatically to prevent display garbage.  
* [x] **Criterion 3 (Quality/Test):** Write unit tests in `tests/unit/test_usecases.py` verifying correct log formatting and standard stdout color code stripping.  
* [x] **Criterion 4 (Review):** Logging and terminal ANSI generation operations must execute without introducing system latency.
