# TSK-13: Baking Recipes Engine (Dedução Automática por Receita)

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 3 Story Points / 12 Hours  
* **Story / Epic Reference:** FT-07 (Recipes & Auto-deductions)

## 📖 Description & Objectives

Develop a recipe book context allowing bakers to register ingredient formulations (e.g., "Sourdough Bread" requires 500g Flour, 10g Yeast, 350g Water). When triggering a baking event (e.g., producing 10 loaves), the application must automatically deduct the correct aggregated amounts from active pantry batches following FEFO order.

## ✅ Definition of Ready (DoR)

* [ ] Pure domain entities and repository adapter from Sprint 1 are locked and tested.
* [ ] Schema layout definitions for storing recipes inside local disk files structured.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Criterion 1 (Domain/Functional):** Create `RecipeEntity` storing ingredient associations and quantities. Add `estocapao bake <recipe_name> <quantity>` CLI subcommand.
* [ ] **Criterion 2 (FEFO Deduction):** The use case must identify available batches, deduct quantities starting from the first expiring batch (FEFO), and automatically quarantine expired lots before deduction.
* [ ] **Criterion 3 (Quality/Test):** Write unit tests for recipe deduction logic, ensuring stock invariants are checked (e.g., abort transaction if any ingredient has insufficient stock).
* [ ] **Criterion 4 (Logs):** Log all baked events and detailed batch deductions in `estocapao.log`.
