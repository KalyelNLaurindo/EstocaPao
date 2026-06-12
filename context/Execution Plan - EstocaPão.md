# **📋 Execution Plan: EstocaPão — High-Performance In-Memory Local CLI Inventory Engine**

**Role:** Project Owner / Tech Lead / AI Prompt Engineer

**Objective:** Map out the phased execution roadmap for the EstocaPão local CLI tool, prioritizing a Test-First (TDD) cycle and optimizing the workspace environment for AI-assisted code generation via structured specifications (.cursorrules / claude.md).

**Context:** EstocaPão — A local-first, zero-configuration Python CLI inventory management system designed to eliminate human error and stockouts in artisanal bakeries through high-speed, memory-resident CRUD operations and robust data validation pipelines.

## **🏛️ Project Metadata**

* **Target Stack:** Pure Python 3.10+ (Standard Library only: argparse, json, re, datetime, os, configparser, unittest)  
* **Date of Creation:** June 12, 2026  
* **Lead Architect:** Kalyel Nunes Laurindo / Tech Lead  
* **Execution Version:** v1.0  
* **Licensing:** MIT License (FOSS)

## **🚀 1. Phased Production Roadmap (The Order of Execution)**

To prevent architectural regression, production follows a strict bottom-up approach. Core domain layers and atomic file system utilities must be locked and verified before terminal router behaviors are assigned to the development team or AI agents.

### **Phase 1: Backing Infrastructure & Configuration Setup**

* **Core Focus:** Local filesystem initialization, configuration file handling, and fallback definitions.  
* **Key Tasks:**  
  * Initialize the configuration parser for [config.ini](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/config.ini) with default alert thresholds.  
  * Establish file-permission lock mechanisms via `os.chmod` (restricting access to owner: `chmod 600`).  
  * Define schema validation routines for incoming JSON files to prevent bootstrap corruptions.  
* **Output Deliverable:** Functional bootstrapping layer capable of reading config setups and enforcing secure local file creation.

### **Phase 2: Bounded Domain Context & Core Models**

* **Core Focus:** Pure OOP entities and immutable Value Objects with absolute framework isolation.  
* **Key Tasks:**  
  * Define `BatchValueObject` to represent incoming supplier lots (with immutable variables: quantity, expiration date, received date).  
  * Build the `IngredientEntity` containing domain invariants (e.g., stock levels can never fall below zero, batch calculations, low-stock threshold comparison).  
  * Design the abstract persistence interface (`IInventoryRepository` Outbound Port).  
* **Output Deliverable:** Fully isolated domain models and storage boundary interfaces with zero external file system or parser imports.

### **Phase 3: Test-Driven Use Case Logic**

* **Core Focus:** Application services coordinating business rules in-memory.  
* **Key Tasks:**  
  * Develop `UpdateStockUseCase` executing CRUD steps inside the memory-resident dynamic dictionary.  
  * Program the logical quarantine redirection engine (`QuarantineManager`) to isolate expired batches automatically without deleting them.  
  * Build the `GetInventoryStatusUseCase` to scan thresholds and generate alert indicators on boot.  
* **Output Deliverable:** Robust use-case engine covered by comprehensive, failing unit-test specifications before code execution starts.

### **Phase 4: CLI Interfaces & Local Atomic Persistence Adapters**

* **Core Focus:** Concrete adapters connecting the core application to the command line and physical disk.  
* **Key Tasks:**  
  * Construct `LocalJsonRepositoryAdapter` implementing the `IInventoryRepository` port.  
  * Write the atomic replacement routine: write state changes to [db_backup.tmp](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/db_backup.tmp) first, then perform an instant operating system-level rename to [db_backup.json](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/db_backup.json) to prevent partial write corruptions.  
  * Implement the `CommandLineInterfaceParser` (built on `argparse`) translating user commands into application use-case calls.  
* **Output Deliverable:** Fully functional terminal-interactive system storing encrypted configurations and serializing state reliably under O(1) in-memory performance.

### **Phase 5: Diagnostics, Log Writing & Redundancy Systems**

* **Core Focus:** Local diagnostics, log output formatting, and self-healing.  
* **Key Tasks:**  
  * Implement local log append tools writing actions to [estocapao.log](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/estocapao.log) with standardized timestamp strings.  
  * Integrate ANSI color formatting outputs into terminal displays to indicate status ranges (Critical Red, Warning Yellow, OK Cyan).  
  * Create automated recovery tests simulating corrupted JSON reads and verifying auto-restores from [db_backup.json.bak](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/db_backup.json.bak).  
* **Output Deliverable:** Ready-to-ship, robust CLI package prepared for local distribution and pipeline execution.

## **🧪 2. The Test-First (TDD) Lifecycle Gate**

Every code routine produced for EstocaPão must comply with the strict Red-Green-Refactor sequence. The development loop forces test suite specifications to precede functional implementation.

### **2.1. The AI Prompt-to-Code Loop**

1. **The Specification Input:** Provide the AI agent with exact domain rules, boundary constraints, and functional requirements.  
2. **Step 1 (RED Phase):** The AI writes the automated test classes (e.g., subclassing `unittest.TestCase`) targeting the required module. Run the test suite; it must fail because the production classes do not exist.  
3. **Step 2 (GREEN Phase):** The AI writes the absolute minimum production code required to make the failing test cases pass successfully.  
4. **Step 3 (REFACTOR Phase):** Clean up the code. Ensure compliance with Clean Architecture rules (e.g., no infra imports inside domain modules) while keeping all tests in a green state.

### **⚠️ Strict AI Implementation Constraint**

> [!WARNING]
> Under no circumstances shall the AI output production business logic before delivering its corresponding Python `unittest` suite. Any class generated without preceding automated unit or integration tests will be rejected.

## **🤖 3. AI Context Engineering (claude.md / .cursorrules)**

Save this context blueprint in the root workspace directory as `.cursorrules` or `claude.md` to ensure the AI operates with maximum architectural alignment.

```markdown
# EstocaPão — AI Engineering Context Rules

## 1. Role and Persona
You are a Staff Software Engineer and Principal Architect for local-first Python software. You write clean, production-ready, highly performant code adhering to SOLID principles, Hexagonal Architecture, and Domain-Driven Design (DDD).

## 2. Technical Stack & Environment Constraints
- Runtime: Pure Python 3.10+ Standard Library only.
- Dependencies: ZERO external third-party dependencies. No pip-installable packages in production (e.g., no SQLAlchemy, no Typer, no Pydantic).
- Persistence: In-Memory dynamic dictionaries serialized atomically to a local JSON file (`db_backup.json`).
- Performance Target: All memory-resident searches, lookups, and state mutations must maintain O(1) complexity and run in under 5 milliseconds.

## 3. Architecture Rules
- Domain Isolation: Code inside `estocapao/modules/inventory/domain/` must remain completely pure. It cannot import from `infra`, `cli`, or application use cases.
- Ports & Adapters: Interactivity with filesystem and terminal shell must happen strictly through adapters. Use cases depend only on abstract interface declarations (e.g., `IInventoryRepository`).
- Data Durability: All database mutator actions must run through the atomic write service: serialize to `.tmp`, then execute `os.replace()` to replace the target `.json`.
- Logical Quarantine: Never delete expired lots automatically. Isolate expired batches in a separated list, triggering manual prompt decisions.

## 4. Testing Paradigm (TDD Mandatory)
- Always deliver the corresponding `unittest` test file (e.g., under `tests/unit/` or `tests/integration/`) BEFORE providing production classes.
- Write explicit test boundary checks (e.g., rejecting historical dates, checking float bounds, ensuring empty values trigger structured exceptions).
```

## **📋 4. Specification-to-Execution Matrix**

This execution control checklist maps the technical implementation steps to their validation tests and corresponding instruction modules.

### **FT-01: Bootstrap, Config Parsing & Alert Setup**

* **Target Boundary:** [estocapao/bootstrap/](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/estocapao/bootstrap/) and [config.ini](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/config.ini)  
* **Pre-Condition Test File:** [tests/integration/test_initializer.py](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/tests/integration/test_initializer.py)  
* **Associated Prompt Spec File:** [docs/prompts/ft01_config_bootstrap.md](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/docs/prompts/ft01_config_bootstrap.md)  
* **Status:** Completed

### **FT-02: Bounded Domain Objects (Ingredients & Batches)**

* **Target Boundary:** [estocapao/modules/inventory/domain/](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/estocapao/modules/inventory/domain/) (Entities, VOs)  
* **Pre-Condition Test File:** [tests/unit/test_domain_entity.py](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/tests/unit/test_domain_entity.py)  
* **Associated Prompt Spec File:** [docs/prompts/ft02_domain_logic.md](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/docs/prompts/ft02_domain_logic.md)  
* **Status:** Completed

### **FT-03: Use Case Interactors & Quarantine Gatekeeper**

* **Target Boundary:** [estocapao/modules/inventory/app/](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/estocapao/modules/inventory/app/) (Use Cases)  
* **Pre-Condition Test File:** [tests/unit/test_usecases.py](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/tests/unit/test_usecases.py)  
* **Associated Prompt Spec File:** [docs/prompts/ft03_usecases_quarantine.md](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/docs/prompts/ft03_usecases_quarantine.md)  
* **Status:** Completed

### **FT-04: Repository Ports & Safe Atomic Replacement Adapter**

* **Target Boundary:** [estocapao/modules/inventory/infra/](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/estocapao/modules/inventory/infra/) (JSON Persistence)  
* **Pre-Condition Test File:** [tests/integration/test_repo_adapter.py](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/tests/integration/test_repo_adapter.py)  
* **Associated Prompt Spec File:** [docs/prompts/ft04_atomic_persistence.md](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/docs/prompts/ft04_atomic_persistence.md)  
* **Status:** Completed

### **FT-05: Argparse Router & Color Alert CLI UI**

* **Target Boundary:** [estocapao/modules/inventory/infra/cli.py](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/estocapao/modules/inventory/infra/cli.py)  
* **Pre-Condition Test File:** [tests/e2e/test_cli_commands.py](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/tests/e2e/test_cli_commands.py)  
* **Associated Prompt Spec File:** [docs/prompts/ft05_cli_router.md](file:///e:/Desenvolvimento%20de%20Software/Software%20Engineering%20Portfolio/01-programacao/EstocaP%C3%A3o/docs/prompts/ft05_cli_router.md)  
* **Status:** Completed

## **🛡️ 5. Definition of Done (DoD) for AI Iterations**

An execution task is considered complete and ready to merge into main trunks only when it satisfies all constraints under this automated quality check:

* [ ] **Structural Validation:** The code complies with linter configurations and package boundary parameters without leakages.  
* [ ] **Test Execution:** Pre-written unit and integration components execute with green logs.  
* [ ] **Coverage Benchmark:** The newly introduced code preserves or raises global coverage metrics (Target: 85% Core Coverage).  
* [ ] **Safety Assurance:** Confirmed that write operations implement the atomic `.tmp` rename pattern and lock directories with strict file system permissions (`chmod 600`).  
* [ ] **Context Sync:** Any structural pivots or interface modifications are updated in the master `claude.md` tracking layout.