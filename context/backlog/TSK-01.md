# TSK-01: Build Pure Domain Model - BatchValueObject

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 1 Story Point / 4 Hours  
* **Story / Epic Reference:** FT-02 (Bounded Domain Objects)

## 📖 Description & Objectives

Construct the pure immutable value object BatchValueObject in `src/estocapao/modules/inventory/domain/value.py`. This class encapsulates a single received supplier lot, enforcing deep immutability, datetime validation under ISO standards, and strict numeric boundaries on ingredients quantities.

## ✅ Definition of Ready (DoR)

* [ ] Directory namespace `src/estocapao/modules/inventory/domain/` created and clean.  
* [ ] Date string guidelines confirmed as ISO standard format (YYYY-MM-DD).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Criterion 1 (Functional):** The BatchValueObject must be completely immutable (implemented via frozen dataclasses or properties). It must encapsulate `batch_id` (string), `quantity` (positive float), `expiration_date` (ISO standard string converted to `datetime.date`), and `received_date` (ISO standard string converted to `datetime.date`).  
* [ ] **Criterion 2 (Domain Invariant):** Enforce instantiation boundaries. Any attempts to build a batch with negative or zero quantities must immediately raise a custom domain error (`ValueError`). Invalid date formats must raise structured date exceptions.  
* [ ] **Criterion 3 (Quality/Test):** Unit tests located in `tests/unit/test_domain_value.py` run 100% green, asserting immutability blocks and exception handling for invalid limits.  
* [ ] **Criterion 4 (Review):** Decoupled imports strictly verified. This file must only import standard libraries (`dataclasses`, `datetime`) and must have no knowledge of databases, storage adapters, or CLI mechanisms.
