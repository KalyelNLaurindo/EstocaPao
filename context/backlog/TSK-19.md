# TSK-19: Built-in Help System (Sistema de Ajuda Embutido)

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 1 Story Point / 4 Hours  
* **Story / Epic Reference:** FT-11 (UX Terminal & Onboarding)

## 📖 Description & Objectives

Add a dedicated `help` command and a `--help` / `-h` flag that renders a structured, human-friendly help guide directly in the terminal. Unlike argparse's default auto-generated help (which caused the error `invalid choice: 'help'`), this built-in system presents contextual help per command (e.g., `help add` shows only the `add` command guide), uses color and box-drawing characters for clarity, and is readable by frontline staff who have never used a CLI before. Replace or override argparse's default help mechanism to ensure `estocapao help` and `estocapao help <command>` work natively.

## ✅ Definition of Ready (DoR)

* [ ] All current CLI commands (`add`, `update`, `status`, `discard`) have stable argument signatures.
* [ ] TSK-17 (Welcome Screen) is delivered or in progress so that help styling is visually consistent.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Criterion 1 (Functional — Global Help):** `estocapao help` renders a full command reference: name, syntax, description, and one example per command, displayed in a styled box-drawing card layout.
* [ ] **Criterion 2 (Functional — Contextual Help):** `estocapao help add` (and equivalently for `update`, `status`, `discard`) renders a dedicated help card for that single command, including all flags, their types, constraints, and a concrete usage example.
* [ ] **Criterion 3 (Native Integration):** `estocapao help` does NOT produce the argparse error `invalid choice: 'help'`. The `help` subcommand is registered as a first-class subparser that captures optional positional `[command]` argument.
* [ ] **Criterion 4 (Interactive Prompt Integration):** When the user is inside the interactive REPL prompt (TSK-17), typing `help` or `help add` dispatches the same help rendering without exiting the prompt loop.
* [ ] **Criterion 5 (Quality/Test):** Tests assert that `estocapao help` exits with code 0 and that stdout contains the syntax string for all four commands. Tests also assert `estocapao help add` does NOT contain the syntax for `update` or `status`.
* [ ] **Criterion 6 (Review):** Help content must be maintained as a data structure (e.g., a dict of command descriptors) in `src/estocapao/shared/help_content.py`. Rendering logic is separate in `shared/welcome.py` or a new `shared/help_renderer.py`. No help strings should be hardcoded inside `cli.py`.
