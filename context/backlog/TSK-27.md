# TSK-27: Isolate Domain Exceptions in Dedicated Module

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 2 Hours  
* **Story / Epic Reference:** FT-02 / REFACTOR  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

To improve cohesion and adhere to the Single Responsibility Principle, extract domain exception classes (`DomainValidationError`, `InvalidQuantityError`, and `InvalidDateError`) from `estocapao/modules/inventory/domain/value.py` (which houses Value Objects) and isolate them in a new dedicated module `estocapao/modules/inventory/domain/exceptions.py`. Update all entity, cli, use-case, and test imports to pull exceptions from this new module.

## ✅ Definition of Ready (DoR)

* [x] Basic domain structure and models implemented (TSK-01, TSK-02).
* [x] All unit tests pass before commencing refactor.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Testing/Quality - TDD]:** Adapt the test suite `tests/unit/test_domain_value.py` to import exception classes from the new module and run them to ensure no regressions occur.
* [ ] **[Refactor - Domain]:** Create the `estocapao/modules/inventory/domain/exceptions.py` module and move exception definitions there.
* [ ] **[Refactor - Imports]:** Update imports in `entity.py`, `value.py`, `cli.py`, and any other module that catches or raises these exceptions.
* [ ] **[Verification]:** Run the `pytest` test suite and ensure all tests remain green.
