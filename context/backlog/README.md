# **📋 Backlog: EstocaPão**

**Role:** Agile Coach / Tech Lead / Project Manager

**Objective:** Maintain a prioritizable backlog of atomic, SMART tasks, tracking their progress across a basic Markdown Kanban board from planning to verification.

**Context:** EstocaPão — A performance-oriented, local-first Command Line Interface (CLI) inventory management application designed to eliminate human error and stockouts in artisanal bakeries through high-speed, memory-resident CRUD operations and rigorous input-validation pipelines.

## **🏛️ Backlog Metadata**

* **Project Owner:** Kalyel Nunes Laurindo / PO  
* **Lead Tech Lead:** Kalyel Nunes Laurindo / Tech Lead  
* **Current Sprint / Iteration:** Sprint 1 (Infrastructure & Domain Foundations)  
* **Target Delivery Date:** July 15, 2026  
* **Document Version:** v1.1

## **1\. 📊 Prioritization & Task Sizing Framework**

To keep development cycles efficient, tasks are estimated and prioritized before execution using the RICE framework.

### **1.1. RICE Score Calculation Formula**

RICE = (Reach * Impact * Confidence) / Effort

* **Reach:** Scaled from 1 to 100 based on the proportion of system layers or user touchpoints affected.  
* **Impact:** Qualitative contribution to the product vision (3 = Massive, 2 = High, 1 = Medium, 0.5 = Low).  
* **Confidence:** Certainty of estimates (1 = High/100%, 0.8 = Medium/80%, 0.5 = Low/50%).  
* **Effort:** Total developer-weeks or story points required (1 = Low, 5 = High).

## **2\. 🗂️ Prioritized Product Backlog Ledger**

The backlog has been structured in a strict TDD (Domain-Driven Bottom-Up) order, starting with pure domain logic and working outwards to infrastructure, CLI routing, and deployment.

### **📦 Phase 1: Pure Domain Layer (TDD Innermost Core)**

* **[TSK-01](TSK-01.md): Build Pure Domain Model - BatchValueObject**  
  * Epic Link: FT-02 (Bounded Domain Objects)  
  * RICE Score: 270.0 (High Priority / Must Have) | Value: 5 / Effort: 1 / Reach: 90 / Impact: 3 / Confidence: 1.0  
  * Status: Done  
* **[TSK-02](TSK-02.md): Build Pure Domain Model - IngredientEntity & Stock Invariants**  
  * Epic Link: FT-02 (Bounded Domain Objects)  
  * RICE Score: 150.0 (High Priority / Must Have) | Value: 5 / Effort: 2 / Reach: 100 / Impact: 3 / Confidence: 1.0  
  * Status: Done

### **⚙️ Phase 2: Application Use Cases (In-Memory Orchestration)**

* **[TSK-03](TSK-03.md): Create Core Use Cases: UpdateStock & GetInventoryStatus**  
  * Epic Link: FT-03 (Use Case Interactors)  
  * RICE Score: 100.0 (High Priority / Must Have) | Value: 5 / Effort: 3 / Reach: 100 / Impact: 3 / Confidence: 1.0  
  * Status: Done  
* **[TSK-04](TSK-04.md): Program Logical Quarantine Redirection and Expiration Gatekeeper**  
  * Epic Link: FT-03 (Use Case Interactors)  
  * RICE Score: 56.0 (Medium Priority / Must Have) | Value: 4 / Effort: 2 / Reach: 70 / Impact: 2 / Confidence: 0.8  
  * Status: Done

### **📂 Phase 3: Infrastructure - Configurations & Verification Setup**

* **[TSK-05](TSK-05.md): Implement Core Configuration Parser and Secure File Bootstrapping**  
  * Epic Link: FT-01 (Bootstrap & Config Setup)  
  * RICE Score: 150.0 (High Priority / Must Have) | Value: 5 / Effort: 2 / Reach: 100 / Impact: 3 / Confidence: 1.0  
  * Status: Done  
* **[TSK-06](TSK-06.md): Secure File Permission Locks & Structural Scheme Validator**  
  * Epic Link: FT-01 & FT-04 (File Setup & Safe Persistence)  
  * RICE Score: 80.0 (High Priority / Must Have) | Value: 4 / Effort: 2 / Reach: 80 / Impact: 2 / Confidence: 1.0  
  * Status: Done

### **💾 Phase 4: Infrastructure - Persistence & Data Safety**

* **[TSK-07](TSK-07.md): Develop LocalJsonRepositoryAdapter & Atomic Write Protocol**  
  * Epic Link: FT-04 (Repository Ports & Safe Adapter)  
  * RICE Score: 100.0 (High Priority / Must Have) | Value: 5 / Effort: 3 / Reach: 100 / Impact: 3 / Confidence: 1.0  
  * Status: Done  
* **[TSK-08](TSK-08.md): Create Self-Healing Schema Recovery and Disaster Recovery DRP Suite**  
  * Epic Link: FT-04 & FT-05 (Persistence & Warnings)  
  * RICE Score: 90.0 (High Priority / Should Have) | Value: 4 / Effort: 2 / Reach: 90 / Impact: 2 / Confidence: 1.0  
  * Status: Done

### **💻 Phase 5: Client Interface (CLI Router & Logs)**

* **[TSK-09](TSK-09.md): Build CommandLineInterfaceParser and Command Arguments Router**  
  * Epic Link: FT-05 (CLI & Alerts Router)  
  * RICE Score: 100.0 (High Priority / Must Have) | Value: 5 / Effort: 3 / Reach: 100 / Impact: 3 / Confidence: 1.0  
  * Status: Done  
* **[TSK-10](TSK-10.md): Build Logging Engine & Colored CLI Warn/Info Outputs**  
  * Epic Link: FT-05 (CLI & Alerts Router)  
  * RICE Score: 64.0 (Medium Priority / Should Have) | Value: 3 / Effort: 1 / Reach: 80 / Impact: 1 / Confidence: 0.8  
  * Status: Done

### **🚀 Phase 6: Packaging & Master Entry Point (Deployable Deliverable)**

* **[TSK-11](TSK-11.md): Establish Package Setup (pyproject.toml) and Entry Point Execution Engine**  
  * Epic Link: FT-01 & FT-05 (Packaging / Execution)  
  * RICE Score: 150.0 (High Priority / Must Have) | Value: 5 / Effort: 2 / Reach: 100 / Impact: 3 / Confidence: 1.0  
  * Status: To Do

## **3\. 📋 Basic Markdown Kanban Board**

### **🔴 To Do (Ready for Development)**

* [ ] **[TSK-11](TSK-11.md):** Establish Package Setup (pyproject.toml) and Entry Point Execution Engine

### **🟡 In Progress (Actively Being Built)**

* None

### **🔵 In Review (QA & Test Verification)**

* None

### **🟢 Done (Merged & Verified in Main Trunk)**

* [x] **[TSK-10](TSK-10.md):** Build Logging Engine & Colored CLI Warn/Info Outputs  
* [x] **[TSK-09](TSK-09.md):** Build CommandLineInterfaceParser and Command Arguments Router  
* [x] **[TSK-08](TSK-08.md):** Create Self-Healing Schema Recovery and Disaster Recovery DRP Suite  
* [x] **[TSK-07](TSK-07.md):** Develop LocalJsonRepositoryAdapter & Atomic Write Protocol  
* [x] **[TSK-06](TSK-06.md):** Secure File Permission Locks & Structural Scheme Validator  
* [x] **[TSK-05](TSK-05.md):** Implement Core Configuration Parser and Secure File Bootstrapping  
* [x] **[TSK-04](TSK-04.md):** Program Logical Quarantine Redirection and Expiration Gatekeeper  
* [x] **[TSK-03](TSK-03.md):** Create Core Use Cases: UpdateStock & GetInventoryStatus
* [x] **[TSK-02](TSK-02.md):** Build Pure Domain Model - IngredientEntity & Stock Invariants
* [x] **[TSK-01](TSK-01.md):** Build Pure Domain Model - BatchValueObject
* [x] **TSK-00:** Bootstrap project workspace directory layout and initial PEP8 configs
