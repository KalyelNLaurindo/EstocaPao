# TSK-02: Build Pure Domain Model - IngredientEntity & Stock Invariants

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 2 Story Points / 8 Hours  
* **Story / Epic Reference:** FT-02 (Bounded Domain Objects)

## 📖 Description & Objectives

Develop the domain aggregate root IngredientEntity inside `src/estocapao/modules/inventory/domain/entity.py`. This component represents an individual baking ingredient (e.g., Yeast, Specialty Flour), manages its composite batches list, and protects business integrity boundaries (such as preventing total quantities from dropping below zero).

## ✅ Definition of Ready (DoR)

* [x] Immutable BatchValueObject from TSK-01 completed and functional.  
* [x] Core domain exception definitions mapped.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **Criterion 1 (Functional):** The entity manages a mutable collection of BatchValueObject elements in memory. It must expose calculations to calculate the combined stock volume (sum of all batches quantities) and compare total stock levels against its safety_threshold metric.  
* [x] **Criterion 2 (Domain Invariant):** Implement inventory boundaries: total ingredient quantities can never drop below a negative float. If a transaction attempts to draw down stock past zero, block the action and raise an invariant business error (`ValueError`).  
* [x] **Criterion 3 (Quality/Test):** Write extensive unit tests in `tests/unit/test_domain_entity.py` verifying quantity sums, threshold evaluations, and exception checks on boundary conditions (e.g. exactly at zero, null-batch lists).  
* [x] **Criterion 4 (Review):** Verify Clean Architecture standards. Ensure the core entity contains zero framework or database references.
