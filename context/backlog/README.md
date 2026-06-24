# **📋 Backlog: EstocaPão**

**Role:** Agile Coach / Tech Lead / Project Manager

**Objective:** Maintain a prioritizable backlog of atomic, SMART tasks, tracking their progress across a basic Markdown Kanban board from planning to verification.

**Context:** EstocaPão — A performance-oriented, local-first Command Line Interface (CLI) inventory management application designed to eliminate human error and stockouts in artisanal bakeries through high-speed, memory-resident CRUD operations and rigorous input-validation pipelines.

## **🏛️ Backlog Metadata**

* **Project Owner:** Kalyel Nunes Laurindo / PO  
* **Lead Tech Lead:** Kalyel Nunes Laurindo / Tech Lead  
* **Current Sprint / Iteration:** Sprint 1 (Infrastructure & Domain Foundations)  
* **Target Delivery Date:** July 15, 2026  
* **Document Version:** v1.3

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
  * Status: Done

### **🔮 Phase 7: Sprint 2 - Recursos Avançados e Internacionalização (Backlog Futuro)**

* **[TSK-12](TSK-12.md): Basic Language Menu Support (Menu de Idiomas Básico)**  
  * Epic Link: FT-06 (Internationalization)  
  * RICE Score: 80.0 (High Priority / Should Have) | Value: 4 / Effort: 1 / Reach: 100 / Impact: 2 / Confidence: 1.0  
  * Status: To Do  
* **[TSK-13](TSK-13.md): Baking Recipes Engine (Dedução Automática por Receita)**  
  * Epic Link: FT-07 (Recipes & Auto-deductions)  
  * RICE Score: 70.0 (High Priority / Should Have) | Value: 5 / Effort: 3 / Reach: 70 / Impact: 3 / Confidence: 0.9  
  * Status: To Do  
* **[TSK-14](TSK-14.md): Batch Financial Controls (Custo de Aquisição e Perdas de Inventário)**  
  * Epic Link: FT-08 (Financial Monitoring)  
  * RICE Score: 64.0 (Medium Priority / Should Have) | Value: 4 / Effort: 2 / Reach: 80 / Impact: 2 / Confidence: 1.0  
  * Status: To Do  
* **[TSK-15](TSK-15.md): Report Exporting Engine (Exportação PDF/CSV)**  
  * Epic Link: FT-09 (Reporting & Exports)  
  * RICE Score: 48.0 (Medium Priority / Could Have) | Value: 3 / Effort: 2 / Reach: 80 / Impact: 2 / Confidence: 0.8  
  * Status: To Do  
* **[TSK-16](TSK-16.md): Cloud Syncing Adapter (Sincronização Remota Backup Offline-First)**  
  * Epic Link: FT-10 (Remote Synchronization)  
  * RICE Score: 36.0 (Low Priority / Could Have) | Value: 3 / Effort: 3 / Reach: 60 / Impact: 2 / Confidence: 0.9  
  * Status: To Do  

### **✨ Phase 8: Sprint 2 - UX Terminal & Hardening de Segurança (Backlog Futuro)**

* **[TSK-17](TSK-17.md): Welcome Screen & Interactive Command Prompt (Tela de Apresentação e Prompt Interativo)**  
  * Epic Link: FT-11 (UX Terminal & Onboarding)  
  * RICE Score: 150.0 (High Priority / Must Have) | Value: 5 / Effort: 2 / Reach: 100 / Impact: 3 / Confidence: 1.0  
  * Status: To Do  
* **[TSK-18](TSK-18.md): Semi-Visual Terminal Table Renderer (Renderizador de Tabelas Semi-Visuais)**  
  * Epic Link: FT-11 (UX Terminal & Onboarding)  
  * RICE Score: 150.0 (High Priority / Must Have) | Value: 5 / Effort: 2 / Reach: 100 / Impact: 3 / Confidence: 1.0  
  * Status: To Do  
* **[TSK-19](TSK-19.md): Built-in Help System (Sistema de Ajuda Embutido)**  
  * Epic Link: FT-11 (UX Terminal & Onboarding)  
  * RICE Score: 100.0 (High Priority / Must Have) | Value: 5 / Effort: 1 / Reach: 100 / Impact: 2 / Confidence: 1.0  
  * Status: To Do  
* **[TSK-20](TSK-20.md): Malicious Input & Edge Case Hardening (Proteção contra Entradas Maliciosas)**  
  * Epic Link: FT-12 (Security & Input Hardening)  
  * RICE Score: 90.0 (High Priority / Must Have) | Value: 5 / Effort: 2 / Reach: 90 / Impact: 2 / Confidence: 1.0  
  * Status: To Do  
* **[TSK-21](TSK-21.md): Elegant Field Control & Auto-formatting (Controle de Campos Elegante e Auto-formatação)**  
  * Epic Link: FT-12 (Security & Input Hardening)  
  * RICE Score: 100.0 (High Priority / Must Have) | Value: 5 / Effort: 1 / Reach: 100 / Impact: 2 / Confidence: 1.0  
  * Status: To Do  
* **[TSK-22](TSK-22.md): Structured Audit Logging Coverage (Cobertura Completa de Logs de Auditoria)**  
  * Epic Link: FT-13 (Audit Trail)  
  * RICE Score: 90.0 (High Priority / Must Have) | Value: 5 / Effort: 1 / Reach: 90 / Impact: 2 / Confidence: 1.0  
  * Status: To Do  

### **🔗 Phase 9: Integração de Dados, Telemetria & Automação de Compras (Backlog Futuro)**

* **[TSK-23](TSK-23.md): Low-Stock Threshold Alert Engine (Motor de Alertas de Estoque Mínimo)**  
  * Epic Link: FT-14 (Alerts & Inventory Intelligence)  
  * RICE Score: 90.0 (High Priority / Must Have) | Value: 5 / Effort: 1 / Reach: 90 / Impact: 2 / Confidence: 1.0  
  * Status: To Do  
* **[TSK-24](TSK-24.md): Supplier Batch Traceability Logger (Rastreabilidade de Lotes por Fornecedor)**  
  * Epic Link: FT-15 (Traceability & Compliance)  
  * RICE Score: 72.0 (High Priority / Should Have) | Value: 4 / Effort: 2 / Reach: 90 / Impact: 2 / Confidence: 0.8  
  * Status: To Do  
* **[TSK-25](TSK-25.md): Ingredient Expiration Purge Scheduler (Quarentena Automática de Ingredientes Vencidos)**  
  * Epic Link: FT-16 (Lifecycle Management)  
  * RICE Score: 64.0 (Medium Priority / Should Have) | Value: 4 / Effort: 2 / Reach: 80 / Impact: 2 / Confidence: 1.0  
  * Status: To Do  
* **[TSK-26](TSK-26.md): Production Yield Calculator (Calculadora de Rendimento de Produção)**  
  * Epic Link: FT-17 (Analytics & Pricing Intelligence)  
  * RICE Score: 56.0 (Medium Priority / Could Have) | Value: 3 / Effort: 2 / Reach: 70 / Impact: 2 / Confidence: 0.8  
  * Status: To Do  

* **[TSK-27](TSK-27.md): Isolate Domain Exceptions in Dedicated Module**  
  * Epic Link: FT-02 (Bounded Domain Objects / Refactor)  
  * RICE Score: 180.0 (High Priority / Should Have) | Value: 4 / Effort: 1 / Reach: 90 / Impact: 2 / Confidence: 1.0  
  * Status: To Do  

### **🌐 Phase 9.1: Internacionalização (i18n) & Localização**

* **[TSK-28](TSK-28.md): i18n File Registry & Config Parser**  
  * Epic Link: FT-06 (Internationalization)  
  * RICE Score: 72.0 (High Priority / Should Have) | Value: 4 / Effort: 2 / Reach: 90 / Impact: 2 / Confidence: 0.8  
  * Status: To Do  

* **[TSK-29](TSK-29.md): Localization of CLI Presenter & Unicode Table Strings**  
  * Epic Link: FT-06 (Internationalization)  
  * RICE Score: 72.0 (High Priority / Should Have) | Value: 4 / Effort: 2 / Reach: 90 / Impact: 2 / Confidence: 0.8  
  * Status: To Do  

### **🎨 Phase 9.2: Acessibilidade CLI & Prompt Interativo**

* **[TSK-30](TSK-30.md): Layperson Interactive Prompts & Validation Badges**  
  * Epic Link: FT-11 (UX Terminal & Onboarding)  
  * RICE Score: 213.75 (High Priority / Should Have) | Value: 5 / Effort: 1 / Reach: 95 / Impact: 2.5 / Confidence: 0.9  
  * Status: To Do  

* **[TSK-31](TSK-31.md): CLI Accessibility and Daltonism Protection Mode**  
  * Epic Link: FT-11 (UX Terminal & Onboarding)  
  * RICE Score: 285.0 (High Priority / Should Have) | Value: 5 / Effort: 1 / Reach: 95 / Impact: 3.0 / Confidence: 1.0  
  * Status: To Do  



## **3\. 📋 Basic Markdown Kanban Board**

### **🔴 To Do (Ready for Development)**

**Phase 7 — Sprint 2: Recursos Avançados & Internacionalização**
* [ ] **[TSK-12](TSK-12.md):** Basic Language Menu Support (Menu de Idiomas Básico)  
* [ ] **[TSK-13](TSK-13.md):** Baking Recipes Engine (Dedução Automática por Receita)  
* [ ] **[TSK-14](TSK-14.md):** Batch Financial Controls (Custo de Aquisição e Perdas de Inventário)  
* [ ] **[TSK-15](TSK-15.md):** Report Exporting Engine (Exportação PDF/CSV)  
* [ ] **[TSK-16](TSK-16.md):** Cloud Syncing Adapter (Sincronização Remota Backup Offline-First)  

**Phase 8 — Sprint 2: UX Terminal & Hardening de Segurança**
* [ ] **[TSK-17](TSK-17.md):** Welcome Screen & Interactive Command Prompt (Tela de Apresentação e Prompt Interativo)  
* [ ] **[TSK-18](TSK-18.md):** Semi-Visual Terminal Table Renderer (Renderizador de Tabelas Semi-Visuais)  
* [ ] **[TSK-19](TSK-19.md):** Built-in Help System (Sistema de Ajuda Embutido)  
* [ ] **[TSK-20](TSK-20.md):** Malicious Input & Edge Case Hardening (Proteção contra Entradas Maliciosas)  
* [ ] **[TSK-21](TSK-21.md):** Elegant Field Control & Auto-formatting (Controle de Campos Elegante e Auto-formatação)  
* [ ] **[TSK-22](TSK-22.md):** Structured Audit Logging Coverage (Cobertura Completa de Logs de Auditoria)  

**Phase 9 — Integração de Dados, Telemetria & Automação de Compras**
* [ ] **[TSK-23](TSK-23.md):** Low-Stock Threshold Alert Engine (Motor de Alertas de Estoque Mínimo)  
* [ ] **[TSK-24](TSK-24.md):** Supplier Batch Traceability Logger (Rastreabilidade de Lotes por Fornecedor)  
* [ ] **[TSK-25](TSK-25.md):** Ingredient Expiration Purge Scheduler (Quarentena Automática de Ingredientes Vencidos)  
* [ ] **[TSK-26](TSK-26.md):** Production Yield Calculator (Calculadora de Rendimento de Produção)  
* [ ] **[TSK-27](TSK-27.md):** Isolate Domain Exceptions in Dedicated Module
* [ ] **[TSK-28](TSK-28.md):** i18n File Registry & Config Parser (2 SP)
* [ ] **[TSK-29](TSK-29.md):** Localization of CLI Presenter & Unicode Table Strings (2 SP)
* [ ] **[TSK-30](TSK-30.md):** Layperson Interactive Prompts & Validation Badges (1 SP)
* [ ] **[TSK-31](TSK-31.md):** CLI Accessibility and Daltonism Protection Mode (1 SP)
* [ ] **[TSK-32](TSK-32.md):** HTTP REST API Backend Server Integration (3 SP)




### **🟡 In Progress (Actively Being Built)**

* None

### **🔵 In Review (QA & Test Verification)**

* None

### **🟢 Done (Merged & Verified in Main Trunk)**

* [x] **[TSK-11](TSK-11.md):** Establish Package Setup (pyproject.toml) and Entry Point Execution Engine  
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
