# **📋 Software Design Document: EstocaPão — High-Performance In-Memory Local CLI Inventory Engine**

**Role:** Project Owner / System Architect

**Objective:** Detail the technical implementation, architectural patterns, frameworks, and deployment topologies required to execute the business vision.

**Context:** EstocaPão — A local-first, zero-configuration Python command-line interface (CLI) inventory management system designed to eliminate human error and stockouts through high-speed, memory-resident CRUD structures and robust validation pipelines.

## **🏛️ Project Metadata**

* **Client / Segment:** Artisanal Bakeries (Boulangeries, Pastry Shops, and Specialty Micro-Bakeries)  
* **Date of Creation:** June 12, 2026  
* **Lead Architect:** Kalyel Nunes Laurindo / Tech Lead  
* **Document Version:** v1.0

## **🛠️ 1. Technical Stack Overview**

The technology stack is strategically selected to achieve a sub-5ms interactive execution loop, absolute offline resilience in harsh kitchen environments, and zero external runtime dependencies.

### **1.1. Core Architectural Layers**

| Layer | Component / Tech | Technical Rationale |
| :---- | :---- | :---- |
| **Frontend / Client** | Native OS Terminal Shell (argparse Engine) | Keyboard-driven, high-contrast CLI optimized for rapid numeric keypad typing by staff during shifts. |
| **Backend Core** | Python 3.10+ Standard Library (Pure OOP) | Zero-dependency application architecture ensuring boot times under 200ms on legacy kitchen computers. |
| **Specialized Engine** | Regex & Datetime Validation Engine | Custom validation intercepts raw input streams, trims whitespace, and rejects historical expiration dates. |
| **Database Engine** | In-Memory Hash Maps (Python dict) | Implements ![][image1] operations, keeping transaction cycles in memory to bypass slow disk lookups. |
| **Object Storage** | Local Filesystem Metadata | Standard disk space read/writes utilized to store system parameters and alerts configuration (config.ini). |
| **Cache & Queue** | In-Memory Quarantine Lists | Isolates expired batches inside dedicated memory holding structures requiring physical user write-off. |
| **Message Broker** | N/A (Local Call Stack) | Monolithic single-process execution; data flows entirely in-process to avoid open networking footprints. |
| **Gateway / Edge Proxy** | Standard I/O Streams (sys.stdin / sys.stdout) | Direct operating system standard stream routing. Supports pipeline automation and log redirection. |
| **Orchestration** | PyPI Installer Packaging (setuptools) | Simple pip install estocapao distribution. Avoids Docker hypervisor overhead on legacy hardware. |
| **IaC & Provisioning** | Automated Self-Healing Setup Script | Internal script auto-generates missing configuration, backups, and log structures on initial boot. |
| **Observability** | Standard Error Stream (sys.stderr) \+ ANSI Codes | Real-time CLI warnings, badges, and state notices flashed via colored console text to minimize cognitive fatigue. |

### **1.2. Technical Traceability Matrix (Pain Point ➔ Technical Module)**

This matrix maps user pain points identified during Product Discovery to concrete architectural components.

| User Friction / Pain Point | System Requirement (FR) | Responsible Technical Module |
| :---- | :---- | :---- |
| **Manual Data Entry Errors** | RF02: CLI Parser Validation Engine | validation_engine.py (Regex checking, datetime coercion, numeric bounds). |
| **Sudden Early Morning Stockouts** | RF03: Real-Time Warning Alert Flags | stock_monitor.py (Checks inventory levels against threshold metadata on boot). |
| **Ingredient Spoilage Losses** | RF03: Expiration Quarantine Pipeline | quarantine_manager.py (Filters expired items into a holding list, blocking use). |
| **Accidental Crash Data Loss** | RF04: Automatic JSON Fallback Persistence | atomic_persistence_service.py (Temp swap files & automatic memory rebuilding). |

## **🏗️ 2. Architectural Design: Ports, Adapters & OOP**

The system enforces strict **Hexagonal Architecture (Ports and Adapters)** integrated with Domain-Driven Design (DDD) principles. This ensures absolute decoupling of domain-level baking validation policies from file handling, configuration, and command-line parsing modules.

```text
                  +-------------------------------------------------+  
                  |             EstocaPão CLI Core App              |  
                  |                                                 |  
[ CLI Commands ] ===> [ CLI Input Parser ]                          |  
                  |         (Inbound Adapter)                       |  
                  |                 ||                              |  
                  |                 \/                              |  
                  |       [ IInventoryUseCase ]                     |  
                  |          (Inbound Port)                         |  
                  |                 ||                              |  
                  |                 \/                              |  
                  |    +--------------------------+                 |  
                  |    |      Domain Model        |                 |  
                  |    |  - IngredientEntity      |                 |  
                  |    |  - BatchValueObject      |                 |  
                  |    +--------------------------+                 |  
                  |                 ||                              |  
                  |                 \/                              |  
                  |      [ IInventoryRepository ]                   |  
                  |         (Outbound Port)                         |  
                  |                 ||                              |  
                  +-----------------||------------------------------+  
                                    ||  
                                    \/  
                         [ LocalJsonRepository ] ===> [ db_backup.json ]  
                           (Outbound Adapter)
```

### **2.1. System Module Layering (Clean Architecture Structure)**

Every domain module maintains a strict internal layer separation:

1. **Domain Layer (Core):** Contains pure, framework-free entities (IngredientEntity) and value objects (BatchValueObject). Responsible for calculating batch lifespan, evaluating stock status (OK/Low/Expired), and protecting business invariants (e.g., quantities can never be negative).  
2. **Application Layer (Use Cases):** Contains services that coordinate operations (AddStockUseCase, GetInventoryStatusUseCase). Interacts with outer infrastructure layers strictly through abstract boundary interfaces (**Ports**).  
3. **Infrastructure Layer (Adapters):** Concrete implementations of ports. Includes CommandLineInterfaceParser (converts sys arguments into application commands) and LocalJsonRepositoryAdapter (handles file I/O, writing data to disk).

### **2.2. Dependency Injection & SOLID Principles**

* **Dependency Inversion Principle (DIP):** Core domain use cases depend strictly on interfaces (IInventoryRepository). During system bootstrap, the LocalJsonRepositoryAdapter class is instantiated and injected into the appropriate use-case handlers.  
* **Liskov Substitution Principle (LSP):** The persistence layer is designed so that any alternative storage adapter (e.g., a mock database repository used during test runs) can replace the actual production JSON repository without altering application behavior.

### **2.3. Communication Taxonomy**

| Mechanism | Purpose | Technical Characteristics |
| :---- | :---- | :---- |
| **In-Memory Service Calls** | Internal component orchestration during processing. | Synchronous, in-process, zero performance overhead. |
| **Atomic File Flush** | Serializing the updated memory map safely to disk. | Writes to db_backup.tmp before performing a native OS rename. |
| **Quarantine Redirect** | Isolating bad/expired stock safely from normal operations. | Direct logical redirection in-memory; persists state flags to disk. |

## **🔐 3. Security Architecture & Data Protection**

Because EstocaPão runs entirely as an offline, local-first utility, security focus shifts from defending against network breaches to ensuring local data integrity, preventing access tampering, and protecting local configuration settings.

### **3.1. File Permissions & Administrative Control**

* **OS-Level Access Lock (Unix/Linux/macOS):** When initializing db_backup.json and config.ini, the application dynamically invokes os.chmod to restrict read/write access strictly to the operating system user running the terminal (chmod 600).  
* **Configuration Protection:** To adjust safety alert thresholds or override quarantined expiration batches, users must pass an administrator passcode. This passcode is verified locally using a salt and a high-performance hash algorithm:  
  ![][image2]

### **3.2. Data Verification Routine**

Every time the program boots, a data integrity validator scans db_backup.json to verify that external edits haven't introduced corrupt values:

* Confirms that structural properties exist (ID, Name, Thresholds, Batches).  
* Validates that date values correspond to standard ISO formats (YYYY-MM-DD).  
* Runs a structural regex check over the entire file before populating the local dictionary memory space.

## **🧩 4. Evolutionary Blueprint (Scaling Path)**

The codebase is organized modularly to enable a frictionless migration to a client-server or cloud architecture when business scale warrants:

```text
[Local CLI App]   
     │  
     ├── 1. Move Storage Interface ──► Swap "LocalJsonRepositoryAdapter" for "PostgresRepositoryAdapter"  
     │  
     └── 2. Decouple User Interface ──► Wrap Use Cases inside a "FastAPI Controller Router"  
                                                     │  
                                                     ▼  
                                            [Enterprise Web REST API]
```

* **Database Migration:** The existing repository interface (IInventoryRepository) abstracts storage details. Moving to a relational database (e.g., PostgreSQL via SQLAlchemy) simply requires creating a new adapter class that implements the port interface—zero modifications to domain entities are needed.  
* **REST API Extraction:** The application use cases can be wrapped inside web routers (such as FastAPI) in under a day, exposing JSON endpoints to support multi-terminal web and mobile applications on kitchen tablets.

### **Sprint 2 Incremental Evolution (Planned Future Features)**

The following Sprint 2 tasks extend existing boundaries without breaking the Hexagonal Architecture isolation:

| Feature | Target Module | Architectural Impact |
| :--- | :--- | :--- |
| **TSK-12 — Language Menu (I18n)** | `estocapao/shared/i18n.py` (new) | New shared utility translating CLI strings based on `config.ini` locale config. Zero domain impact. |
| **TSK-13 — Baking Recipes Engine** | `estocapao/modules/inventory/domain/recipe.py` (new) | New `RecipeEntity` and `BakeUseCase`. Calls existing `UpdateStockUseCase` in FEFO batch order. |
| **TSK-14 — Batch Financial Controls** | `estocapao/modules/inventory/domain/value.py` | Add optional `unit_cost` field to `BatchValueObject`. Cost aggregation computed in `GetInventoryStatusUseCase`. |
| **TSK-15 — Report Exporting Engine** | `estocapao/modules/inventory/infra/exporter.py` (new) | New outbound adapter `ReportExporterAdapter` implementing a new `IReportExporter` port. No domain changes. |
| **TSK-16 — Cloud Syncing Backup** | `estocapao/modules/inventory/infra/cloud.py` (new) | New outbound adapter `CloudSyncAdapter` calling external HTTP APIs behind the existing `IInventoryRepository` boundary. |

## **📐 5. System Component Diagram (C4 Model — Level 3: Inside Core Backend App)**

This diagram details the internal structural components of the core EstocaPão command-line process.

```mermaid
graph TD  
    subgraph Client_and_External [Client Input Layer]  
        CLI_Input["Terminal Commands<br>(e.g., estocapao add flour 10)"]  
    end

    subgraph Core_Backend_Component [EstocaPão Core Process (C4 Level 3)]  
        subgraph Adapters_Inbound [Inbound Adapters]  
            ArgparseController["CLI Input Controller<br>(argparse Wrapper Adapter)"]  
        end

        subgraph Ports_Inbound [Inbound Ports / Use Case Interfaces]  
            UCInterface["Use Case Boundary Ports<br>(e.g., IInventoryUseCase)"]  
        end

        subgraph Application_Layer [Application Services / Use Cases]  
            UseCase["Core Use Case Handlers<br>(e.g., UpdateStockUseCase)"]  
        end

        subgraph Domain_Layer [Domain Core - Bounded Context]  
            Entities["IngredientEntity<br>(Encapsulates rules, statuses)"]  
            VOs["BatchValueObject<br>(Immutable properties: qty, exp)"]  
        end

        subgraph Ports_Outbound [Outbound Ports / Infrastructure Interfaces]  
            RepoInterface["IInventoryRepository Port<br>(Abstract Contract)"]  
        end

        subgraph Adapters_Outbound [Outbound Adapters / Infrastructure Implementations]  
            JsonAdapter["Local JSON Storage Adapter<br>(Concrete Repo Implementation)"]  
            AtomicService["Atomic File Service<br>(Protects file integrity)"]  
        end  
    end

    subgraph External_Infrastructure [Local Filesystem Layer]  
        BackupFile["db_backup.json<br>(Local Disk Storage)"]  
    end

    %% Flow connections  
    CLI_Input -->|Calls| ArgparseController  
    ArgparseController -->|Invokes| UCInterface  
    UCInterface -.->|Implemented by| UseCase  
    UseCase -->|Mutates| Entities  
    Entities -->|Composes| VOs  
    UseCase -->|Queries/Persists| RepoInterface  
      
    RepoInterface -.->|Implemented by| JsonAdapter  
    JsonAdapter -->|Delegates safe write| AtomicService  
    AtomicService -->|Atomic overwrite| BackupFile
```

## **📂 6. Data Architecture (In-Memory Design & Schemas)**

EstocaPão structures its storage model to ensure fast search, clean update steps, and reliable offline data serialization.

### **6.1. In-Memory Hash Map Architecture**

The dynamic application state is held entirely within a nested hash map structure, enabling instant dictionary access:

```json
{  
    "ingredients": {  
        "specialty_flour": {  
            "id": "specialty_flour",  
            "name": "Specialty Flour",  
            "safety_threshold": 15.0,  
            "batches": [  
                {  
                    "batch_id": "FL-001",  
                    "quantity": 25.5,  
                    "expiration_date": "2026-07-20",  
                    "received_date": "2026-06-12"  
                }  
            ]  
        },  
        "fresh_yeast": {  
            "id": "fresh_yeast",  
            "name": "Fresh Yeast",  
            "safety_threshold": 5.0,  
            "batches": [  
                {  
                    "batch_id": "YS-002",  
                    "quantity": 2.1,  
                    "expiration_date": "2026-06-14",  
                    "received_date": "2026-06-10"  
                }  
            ]  
        }  
    }  
}
```

### **6.2. Local Storage Schema Definitions**

#### **A. db_backup.json (Structured Representation Schema)**

```json
{  
  "$schema": "http://json-schema.org/draft-07/schema#",  
  "title": "EstocapaoBackupSchema",  
  "type": "OBJECT",  
  "properties": {  
    "ingredients": {  
      "type": "OBJECT",  
      "additionalProperties": {  
        "type": "OBJECT",  
        "required": ["id", "name", "safety_threshold", "batches"],  
        "properties": {  
          "id": { "type": "STRING" },  
          "name": { "type": "STRING" },  
          "safety_threshold": { "type": "NUMBER", "minimum": 0 },  
          "batches": {  
            "type": "ARRAY",  
            "items": {  
              "type": "OBJECT",  
              "required": ["batch_id", "quantity", "expiration_date", "received_date"],  
              "properties": {  
                "batch_id": { "type": "STRING" },  
                "quantity": { "type": "NUMBER", "minimum": 0 },  
                "expiration_date": { "type": "STRING", "format": "date" },  
                "received_date": { "type": "STRING", "format": "date" }  
              }  
            }  
          }  
        }  
      }  
    }  
  },  
  "required": ["ingredients"]  
}
```

#### **B. config.ini (System Alert Parameters Metadata)**

```ini
[system_defaults]  
alert_color_enabled = true  
automatic_backup_generations = 5  
passcode_sha256_hash = e99a18c428cb38d5f260853678922e03f88ef685652e00845a72233f520b2241 

[alerts_threshold]  
expiration_alert_days_window = 3  
low_stock_default_kg_limit = 5.0
```

## **🚀 7. Continuous Integration, Deployment & QA**

Since the system runs entirely offline, reliability testing is automated and executed via local pipelines prior to PyPI package publishing.

### **7.1. Quality Control Flow**

```text
 [ Local TDD Cycle ] ────► [ AST Code Linter ] ────► [ Architectural Check ] ────► [ Local Executable Build ]  
   (unittest execution)        (PEP8 Compliance)        (Import Dependency Gate)       (Tested local artifact)
```

### **7.2. Automated Architecture Guardrails**

A custom build script leverages Python's abstract syntax trees (ast library) to scan module imports automatically, validating clean architecture rules:

* **Zero Leakage Rule:** Classes within the domain namespace cannot import from application or infrastructure.  
* **Interface Access Rule:** Use cases are strictly restricted to communicating with external systems via interface classes.

### **7.3. Test Isolation Pyramid**

```text
   /\  
  /  \    End-to-End Tests: Complete command simulation checks (using "subprocess")  
 /----\  
/      \  Integration Tests: Validates atomic disk persistence on real temporary directories  
/--------\  
/          \  Unit Tests: Runs logic checks on entities and value objects (using mock dependencies)  
/------------\
```

## **🎨 8. User Interface Design System (UI Architecture)**

EstocaPão uses a unified, keyboard-centric command structure. Standard ANSI escape codes apply high-contrast colors and formatting options to ensure optimal text legibility in environments with heavy flour dust.

### **8.1. UI Color Palettes**

* **Critical Alerts (Low Stock, Expired Batch):** Bright Red ANSI (\033[91m) bold text combined with high-contrast alert symbols.  
* **Success Notifications:** Vibrant Green ANSI (\033[92m) confirmation brackets surrounding updated numbers.  
* **Informational Messages:** Soft Cyan ANSI (\033[96m) borders around data columns for easy reading during fast inventory scans.

### **8.2. Screen Layout Constraints**

* **Column Sizing:** Fixed character limits prevent visual wrapping on older monitors.  
* **Interactive Lists:** Clean ASCII lines map current inventory levels, highlighting low-stock levels visually:

```text
========================================================================  
 ESTOCAPÃO — KITCHEN STOCK CHECK                         [SHIFT: CLOSING]  
========================================================================  
 [LOW]  Ingredient: Yeast  | ID: fresh_yeast | Level:  2.1kg (Limit:  5.0kg)  
 [OK]   Ingredient: Flour  | ID: spec_flour  | Level: 25.5kg (Limit: 15.0kg)  
========================================================================  
 [WARN] Batch YS-002 (Yeast) expires in 2 days! [Action Required]
```

## **📈 9. Observability & System Monitoring**

* **Local Activity Log (estocapao.log):** Updates, deletes, and safety alerts append automatically to a simple, local, time-stamped text file.  
* **Error Redirection:** Non-critical operational problems write to standard output. Severe errors (such as disk serialization failures or invalid file formatting) map to standard error streams, ensuring immediate tracking.

## **🚀 10. Deployment Topology (Transition Plan)**

| Component | Local / Development Environment | Production Cloud Environment (Future Option) |
| :---- | :---- | :---- |
| **Relational Database** | Python dynamic dictionary memory structures. | Managed SQL Database (e.g., AWS RDS / GCP Cloud SQL). |
| **Object Storage** | Local directory path on user storage disk. | Secure Cloud Storage (e.g., AWS S3 / Cloudflare R2). |
| **Message Queue / Cache** | In-process arrays & list pipelines. | Redis instance handling jobs and cached records. |
| **Compute / Runtime** | Terminal command line execution framework. | Container service (e.g., AWS ECS, Docker Container Engine). |
| **SSL / Routing Edge** | Direct OS terminal inputs. | CDN Routing gateway & SSL API termination layer. |

## **📂 11. Codebase Structure & Directory Standards**

```text
estocapao-root/  
├── src/                          # System codebase root directory  
│   ├── estocapao/                # Primary application context package  
│   │   ├── __init__.py           # Application entry definition  
│   │   ├── bootstrap/            # Application bootstrap controller  
│   │   │   └── initializer.py    # Configures dependency injection mappings  
│   │   │  
│   │   ├── modules/              # Subsystem domains & bounded contexts  
│   │   │   └── inventory/        # Primary inventory module  
│   │   │       ├── domain/       # Core business logic (entities, value objects, ports)  
│   │   │       │   ├── entity.py # IngredientEntity logic  
│   │   │       │   ├── value.py  # BatchValueObject logic  
│   │   │       │   └── ports.py  # Outbound interfaces (IInventoryRepository)  
│   │   │       │  
│   │   │       ├── app/          # Application layer (business use cases)  
│   │   │       │   └── usecase.py# UpdateStock, GetInventory use cases  
│   │   │       │  
│   │   │       └── infra/        # Adaption layer (file systems, terminal integrations)  
│   │   │           ├── cli.py    # CommandLineInterfaceParser logic  
│   │   │           └── repo.py   # LocalJsonRepositoryAdapter logic  
│   │   │  
│   │   └── shared/               # Globally accessible application resources  
│   │       ├── ansi.py           # ANSI color definitions for output layouts  
│   │       └── logger.py         # Appends actions to estocapao.log  
│   │  
│   └── main.py                   # Process starter executing CLI commands  
│  
├── tests/                        # Validation suite directory  
│   ├── unit/                     # Validates domain rules and assertions  
│   ├── integration/              # Verifies atomic local disk operations  
│   └── e2e/                      # Runs real process shell loop tests  
│  
├── pyproject.toml                # Standard setuptools configuration file  
├── config.ini                    # Core parameter configurations  
└── README.md                     # Initial setup instructions and documentation
```

## **🧪 12. Validation Strategy & Testing Matrix**

### **12.1. Test Execution Taxonomy**

| Scope | Execution Framework | Focus | Target Cadence |
| :---- | :---- | :---- | :---- |
| **Unit Testing** | unittest (std library) | Asserts boundary logic, expiration calculations, entity rules. | Runs on every file save. |
| **Integration** | unittest (std library) | Verifies atomic replacement loops and backup restores. | Runs prior to every commit. |
| **End-to-End** | subprocess & sys.argv | Simulates real console command inputs and ANSI outputs. | Pre-release check gate. |

## **📝 13. Architecture Decision Records (ADR)**

### **ADR-001 (Dynamic Dictionary Structure Selection)**

* **Context:** Choosing between a local SQLite database or an in-memory dictionary with JSON serialization.  
* **Decision:** Selected an in-memory dictionary with JSON serialization.  
* **Rationale:** A local dictionary guarantees ![][image1] performance, maintaining sub-millisecond execution times. Using a simple backup file avoids the installation and locking issues common to database engine configurations on legacy machines.

### **ADR-002 (Atomic File Replace Implementation)**

* **Context:** Eliminating file corruption risks caused by unexpected power loss during closing shifts.  
* **Decision:** Implement atomic file writes using secondary temporary files.  
* **Rationale:** The persistence layer writes changes to db\_backup.tmp first. Once the transfer completes successfully, it renames the file to db\_backup.json using os.replace. This keeps data intact even if the terminal process is abruptly terminated mid-write.

## **🏛️ 14. Code Governance & Naming Standards**

All classes, methods, and files must follow strict naming rules to maintain clear communication across development cycles.

| Domain Layer Role | Suffix / Style | Example Name |
| :---- | :---- | :---- |
| **Domain Entity** | Entity | IngredientEntity |
| **Value Object** | ValueObject | BatchValueObject |
| **Application Action** | UseCase | UpdateStockUseCase |
| **Storage Port Interface** | Port / Interface prefix I | IInventoryRepository |
| **Concrete Adapter** | Adapter / Suffix | LocalJsonRepositoryAdapter |
| **Console Command Router** | Parser | CommandLineInterfaceParser |

## **🛡️ 15. Resilience & Disaster Recovery Plan (DRP)**

To prevent loss of critical stock logs, EstocaPão utilizes three automated layers of redundancy:

1. **Rotational File Backups:** During save processes, the system preserves the previous database file as db\_backup.json.bak as a safe fallback.  
2. **Data Auto-Healing:** If structural corruption is detected on boot, the application repairs the schemas automatically using default structures or reverts cleanly to the backup file.  
3. **Write Protection:** The application locks save actions while writes are active to prevent concurrent processes from corrupting the local file.

## **🤝 16. System Service Integration Contracts**

When exporting daily shift performance reviews, the system formats events according to a standardized structure:

```json
{    
  "event_id": "8c5b1c90-28bf-4a92-9f37-14bf590d6e2e",    
  "timestamp": "2026-06-12T22:00:00Z",    
  "payload": {    
    "scope_code": "SP_BOULANGERIE_01",    
    "category": "INVENTORY_CLOSING",    
    "change_type": "UPDATE",    
    "raw_diff": {    
      "field": "fresh_yeast",    
      "old_value": "3.5",    
      "new_value": "2.1"    
    },    
    "summarized_explanation": "Shift closing update: 1.4kg of Fresh Yeast consumed during production."    
  }    
}
```

## **📖 17. Ubiquitous Domain Glossary**

* **In-Memory Tracking Engine:** The core system components that manage ingredient balances and batch records entirely within local RAM.  
* **Atomic Save Process:** File-writing pattern that protects data by validating updates in temporary files before overwriting the main database.  
* **Logical Expiration Quarantine:** Virtual isolation system that blocks expired items from active stock without permanently deleting them, ensuring accurate waste logs.  
* **Safe Alert Boundaries:** Customizable indicators within the configuration settings that flag low stock or close expiration dates during boot.

🏁 **End of Document:** This Software Design Document is a live engineering artifact. Architectural pivots, engine choices, or model changes must be documented via sequential updates here and registered via official ADR entries.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAaCAYAAAAue6XIAAAC7klEQVR4Xu2WP2gUQRjF70gEBUWjRvH+7d6dEIIWhlOxUAsRSQoVJGAgjZ3WahStYpHCRiQIQprTSsG0GrAxEBHRTggKUUQ5FBW1sRMTf+9u9xi+ZC97mAsI9+Bjdr/3Zr43uzOzm0i08Z+gu7t7ve/7a20+CqVSaU2hUNho800jnU5vyWazx3K53KDneb2kOqzGBSb3oC03U1xm6XOT8U9ZLg6S+Xz+MIVfMMAUMazg/jHtHOb32Q4CE8vAP6HwLssJmUxmHWOcITZZTg+Fvo+ou99ykdAsGew6Hd9bU+LITxA/iT6XA0k9HfqOukkMbiZ3Gu5O0O8DscPVhEDXrweiZWS5RQhex20G+xE1Qy0F4jtxi9tkmGdiu8m9UevIQ7Mnye9l7PuNzGrpwD1DP2S5RUB0DvG8WsuFoGAXmpfEbCqV2urkL5N76DfYWHB3G5kV4MaISS47LVcHT2Anok/Ea57qdsuHcMzWi8qgjBJXrd5FTLMD0mj9W64OBhpFtKCZWc4FZgtoPrtF1eoe7rjVu4hjljFK8BW7X+rQgkYwTcwjPmp5F+KlI2Z6eno2BDkV+EJ70OpdxDG77MRDgVfbODpLIwE/TizoTYQ5mSU+qnWki9CMWWLYclU4goYDsaGy8HPEt5xzlrbI7HnLVaFdDTm7zEBJil3xauv6gku0wmzkMgCdCO4Rv6PWnc5dr3aoT+g8drlcbdPpJBlw8xZxzMYaC7JPZhCXrRnyR4ivxA19Ml1OCN8MZs5azkVgttLoWNIpgOadt8zeCYVv/do/QfV/gJji/pUMJ5wvloE+tWU045YoFovbyM8Qv7zaElL8ISr+Eh+foOZ0rE8u6EDcS/FBrRsmkEpEm6yDwkOaJH26LNcEqsvRN/8XK47gr+kphfotFxfBV/S5WsutOHgLJyj2YKl1HQM6ba7xZi7p2pKtQBKzIwpdW7IRmOgh+k0289P+zwj+eS/ylA5YLgq8iTR9xlbVaBttrBL+AqG828/L5VzTAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,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>