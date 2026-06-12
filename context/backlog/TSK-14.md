# TSK-14: Batch Financial Controls (Custo de Aquisição e Perdas de Inventário)

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 2 Story Points / 8 Hours  
* **Story / Epic Reference:** FT-08 (Financial Monitoring)

## 📖 Description & Objectives

Add financial cost tracking to ingredient lots. Each batch can be registered with an acquisition cost per unit (e.g., unit cost of flour). Update the system reporting and discard commands to calculate and present the total financial value of stored inventory and loss metrics from discarded/quarantined batches.

## ✅ Definition of Ready (DoR)

* [ ] `BatchValueObject` and persistence schemas are editable.
* [ ] Domain parameters for unit formatting locked.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Criterion 1 (Domain):** Add an optional `unit_cost` property to `BatchValueObject` validation schemas.
* [ ] **Criterion 2 (Reporting):** Update `estocapao status` to show total stock value, and highlight the financial value of currently quarantined batches.
* [ ] **Criterion 3 (Discard Losses):** Log and print the exact monetary loss whenever a batch is discarded via `estocapao discard <batch_id>`.
* [ ] **Criterion 4 (Quality/Test):** Write unit tests checking negative cost boundaries and math operations validation.
