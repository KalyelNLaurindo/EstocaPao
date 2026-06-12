# TSK-22: Structured Audit Logging Coverage (Cobertura Completa de Logs de Auditoria)

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 1 Story Point / 4 Hours  
* **Story / Epic Reference:** FT-05 (CLI & Alerts Router) / FT-13 (Audit Trail)

## 📖 Description & Objectives

Extend the existing `log_action` logging mechanism to ensure every significant system event — successful operations, validation failures, schema recovery decisions, startup initialization, and discard actions — is captured with a consistent, machine-readable log entry. Currently, many code paths silently swallow exceptions (`except Exception: pass`) without emitting any log record, creating invisible failure modes. This task also introduces structured log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) and standardizes the timestamp format across the entire codebase (fixing the inconsistency between ISO-8601 UTC and local `%Y-%m-%d %H:%M:%S` formats observed in `estocapao.log`).

## ✅ Definition of Ready (DoR)

* [ ] TSK-20 (Input Hardening / `sanitizer.py`) delivered or in progress — its exception types must be loggable.
* [ ] The double-validation bug in `initialize_dependencies()` / `_load_from_disk()` is resolved (see bug fix commit preceding this task) so that log entries reflect single, authoritative recovery decisions.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Criterion 1 (Timestamp Standardization):** `log_action` in `shared/logger.py` emits timestamps in UTC ISO-8601 format consistently: `[2026-06-12T15:25:08.097267+00:00]`. All existing callers continue to work without modification.
* [ ] **Criterion 2 (Silent Exception Coverage):** Every `except Exception: pass` block across `repo.py`, `initializer.py`, and `cli.py` is replaced with `except Exception as e: log_action("ERROR", f"<context>: {e}")`. No exception may be silently swallowed without a log entry.
* [ ] **Criterion 3 (Operation Lifecycle Events):** The following events must generate log entries:
  * `[INFO]` — Application startup (`estocapao` invoked), including the subcommand dispatched.
  * `[INFO]` — Successful `add`, `update`, `discard` operations (already partially present — verify completeness).
  * `[INFO]` — Database schema validation passed.
  * `[WARNING]` — Low-stock threshold crossed during `status` evaluation.
  * `[WARNING]` — Expiration date within the alert window during `status` evaluation.
  * `[ERROR]` — Any `DomainValidationError` or `InsufficientStockError` raised and caught at the CLI layer.
  * `[CRITICAL]` — Database AND backup both unreadable, initiating clean DB.
* [ ] **Criterion 4 (TEST_ANSI_LOG Removal):** Remove the `TEST_ANSI_LOG` log entries being emitted during normal invocations (observed in `estocapao.log`). These appear to originate from a debug/development test call left in `ansi.py` or `logger.py`; it must be removed from production code paths.
* [ ] **Criterion 5 (Log Rotation):** Implement basic log rotation in `log_action`: when `estocapao.log` exceeds 500 KB, it is renamed to `estocapao.log.1` and a new `estocapao.log` is started. At most 3 rotated files are kept; older ones are deleted. No external library (`logging.handlers` is acceptable as it is stdlib).
* [ ] **Criterion 6 (Quality/Test):** Unit tests in `tests/unit/test_logger.py` assert: (a) log file is created and contains correctly formatted entries, (b) timestamp is valid ISO-8601 UTC, (c) rotation triggers correctly at the 500 KB threshold, and (d) silent exception paths in `repo.py` now emit `ERROR` entries.
* [ ] **Criterion 7 (Review):** No `print()` statements in non-CLI layers (`repo.py`, `initializer.py`, domain modules). All diagnostic output in those layers must go through `log_action`. `cli.py` retains `print()` for user-facing output only.
