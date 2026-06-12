# EstocaPão — Claude Code Reference Guide

This file provides system context, build/test commands, architecture guidelines, and coding standards for **EstocaPão** (an offline, local-first Python CLI inventory management system).

---

## 🛠️ Common Commands

### Running the CLI
Run the main entry point via:
```bash
python src/main.py [command] [args]
```

### Running Tests
EstocaPão uses the pure Python `unittest` standard library.
* **Run all tests:**
  ```bash
  python -m unittest discover -s tests
  ```
* **Run unit tests only:**
  ```bash
  python -m unittest discover -s tests/unit
  ```
* **Run integration tests only:**
  ```bash
  python -m unittest discover -s tests/integration
  ```
* **Run E2E tests only:**
  ```bash
  python -m unittest discover -s tests/e2e
  ```
* **Run a specific test file:**
  ```bash
  python -m unittest tests/unit/test_domain_entity.py
  ```

---

## 🏛️ Technology Stack & Constraints

- **Runtime Environment:** Pure Python 3.10+ (Standard Library only).
- **Dependencies:** **ZERO external third-party dependencies**. Do NOT import or install external packages (no SQLAlchemy, no Typer, no Pydantic, no Pytest).
- **Persistence:** In-Memory dynamic dictionaries serialized atomically to a local JSON file (`db_backup.json`), backed up as `db_backup.json.bak` on save.
- **Performance Target:** All memory-resident searches, lookups, and state mutations must maintain $O(1)$ complexity and run in under 5 milliseconds.

---

## 🏗️ Architectural Guardrails (Hexagonal & DDD)

Code must follow strict Hexagonal Architecture / Clean Architecture principles:

1. **Domain Isolation:** Code inside `src/estocapao/modules/inventory/domain/` must remain completely pure. It cannot import from `infra`, `cli`, `app`, or use-cases.
2. **Ports & Adapters (DIP):** Interactivity with filesystem, config, and terminal shell must happen strictly through adapters. Use cases must only depend on abstract interface declarations (Ports) e.g., `IInventoryRepository`.
3. **Data Durability:** All database mutator actions must run through the atomic write service: serialize to `.tmp` first, then execute `os.replace()` to replace the target `.json` file to avoid corruption.
4. **Logical Quarantine:** Expired lots must never be deleted automatically. Isolate them inside a separate quarantine list requiring manual administrative write-off.

---

## 🧪 Testing Paradigm (TDD Mandatory)

- **Strict Order:** Write and deliver the corresponding `unittest` file (e.g., under `tests/unit/` or `tests/integration/`) **BEFORE** implementing the production classes. Any production code without preceding tests will be rejected.
- **Boundary Conditions:** Implement explicit tests checking boundary conditions (e.g., negative stock, empty values, float bounds, historical/invalid expiration dates).

---

## 📂 Codebase Directory Structure

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
├── tests/                        # Validation suite directory  
│   ├── unit/                     # Validates domain rules and assertions  
│   ├── integration/              # Verifies atomic local disk operations  
│   └── e2e/                      # Runs real process shell loop tests  
├── pyproject.toml                # Standard setuptools configuration file  
├── config.ini                    # Core parameter configurations  
└── README.md                     # Initial setup instructions and documentation
```

---

## 🏷️ Code Governance & Naming Conventions

Maintain strict compliance with PEP 8 and the following conventions:

*   **Language & Style:** All inline code comments and code docstrings must be written in English. However, **all implementation plans (`implementation_plan.md`), walkthroughs (`walkthrough.md`), and user-facing design explanations must be written in Portuguese (PT-BR)**, using clear, simple, and highly explanatory language so that any developer or stakeholder can easily understand the proposed changes.
*   **Suffixes & Prefixes:**

| Role / Pattern | Suffix / Prefix | Example Name |
| :--- | :--- | :--- |
| **Domain Entity** | `Entity` suffix | `IngredientEntity` |
| **Value Object** | `ValueObject` suffix | `BatchValueObject` |
| **Application Action** | `UseCase` suffix | `UpdateStockUseCase` |
| **Storage Port Interface** | `I` prefix | `IInventoryRepository` |
| **Concrete Adapter** | `Adapter` suffix | `LocalJsonRepositoryAdapter` |
| **Console Command Router**| `Parser` suffix | `CommandLineInterfaceParser` |
