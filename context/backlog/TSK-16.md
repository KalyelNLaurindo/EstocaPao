# TSK-16: Cloud Syncing Adapter (Sincronização Remota Backup Offline-First)

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 3 Story Points / 12 Hours  
* **Story / Epic Reference:** FT-10 (Remote Synchronization)

## 📖 Description & Objectives

Add a background cloud synchronization adapter. When the system detects an active internet connection, it must securely upload the encrypted database state (`db_backup.json`) to remote storage (e.g., AWS S3 or a secure Webhook endpoint) to guarantee off-site backup durability.

## ✅ Definition of Ready (DoR)

* [ ] Local database adapter and encryption/security rules defined.
* [ ] Network connectivity verification engine designed.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Criterion 1 (Functional):** Implement a non-blocking network check. If connection is active, upload database copy without adding latency to CLI commands.
* [ ] **Criterion 2 (DRP):** Allow restoring state from the cloud bucket during system boots when the local JSON is completely corrupted or missing.
* [ ] **Criterion 3 (Quality/Test):** Mock the network requests to write integration tests validating retry configurations, upload states, and timeouts.
* [ ] **Criterion 4 (Review):** Synchronization must never leak credentials or credentials files; store them securely in local configurations.
