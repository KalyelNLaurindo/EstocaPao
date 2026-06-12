# TSK-17: Welcome Screen & Interactive Command Prompt (Tela de Apresentação e Prompt Interativo)

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 2 Story Points / 8 Hours  
* **Story / Epic Reference:** FT-11 (UX Terminal & Onboarding)

## 📖 Description & Objectives

Replace the blank startup experience with a branded welcome screen displayed on first invocation (or with no arguments). The screen must greet the user, display the EstocaPão ASCII-art logo, version information, and a concise cheat-sheet of available commands. After the welcome banner, an interactive REPL-like prompt must allow the user to type commands sequentially without re-invoking the binary — reducing friction for non-technical kitchen staff unfamiliar with CLI paradigms.

## ✅ Definition of Ready (DoR)

* [ ] Existing `CommandLineInterfaceParser` routing is stable and fully tested.
* [ ] Terminal color/ANSI formatter (`TerminalAnsiFormatter`) confirmed working across target OS environments.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Criterion 1 (Functional — Welcome Banner):** Running `estocapao` with no arguments displays a full-width branded banner containing: ASCII logo, product tagline, current version, and a compact command reference table (command syntax + one-line description per command).
* [ ] **Criterion 2 (Functional — Interactive Prompt):** After the banner, a `[EstocaPão] >` prompt is rendered and loops, accepting and dispatching the same commands as the regular CLI (`add`, `update`, `status`, `discard`, `help`, `sair/exit`). Users do not need to prefix commands with `estocapao`.
* [ ] **Criterion 3 (UX):** The prompt must handle empty input gracefully (re-render prompt without error) and accept `sair`, `exit`, or `Ctrl+C` / `Ctrl+D` to quit cleanly.
* [ ] **Criterion 4 (Quality/Test):** Unit tests assert that (a) banner output contains version string and command list, and (b) prompt loop correctly dispatches `status` and `add` commands and exits on `sair`.
* [ ] **Criterion 5 (Review):** Welcome screen and prompt code must live in a dedicated `src/estocapao/shared/welcome.py` module; `cli.py` must not contain banner rendering logic directly.
