# TSK-04: Program Logical Quarantine Redirection and Expiration Gatekeeper

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 2 Story Points / 8 Hours  
* **Story / Epic Reference:** FT-03 (Use Case Interactors)

## 📖 Description & Objectives

Implement a dedicated QuarantineManager use-case layer inside `src/estocapao/modules/inventory/app/quarantine.py`. This module acts as an internal gatekeeper, parsing active lots, checking batch expiration dates against the system's runtime date, and isolating expired materials to preserve food safety.

## ✅ Definition of Ready (DoR)

* [x] Bounded use cases from TSK-03 fully operational.  
* [x] Config parser modules mapped to support safe expiration window parameters.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **Criterion 1 (Functional):** During inventory queries, the quarantine controller automatically scans lot dates. Any lot whose expiration date matches or precedes the current operational date is dynamically isolated to a quarantine list, removing its weight from active kitchen ingredient availability.  
* [x] **Criterion 2 (Human-in-the-Loop):** Quarantined expired stock is physically blocked from standard use but is retained in-memory and in file storage until a specific manual CLI discard action is triggered, keeping waste statistics auditable.  
* [x] **Criterion 3 (Quality/Test):** Execute tests in `tests/unit/test_quarantine.py` simulating standard, warning-state, and post-expired batch timelines (relative to system date) to confirm correct quarantine isolation.  
* [x] **Criterion 4 (Review):** Verify quarantined states persist correctly to the serialization engine without state degradation upon restart.
