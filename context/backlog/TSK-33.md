# TSK-33: Terminal UI/UX Overhaul — Interactive Shell Visual Redesign

* **Owner / Assignee:** Kalyel Nunes Laurindo / PO  
* **Estimated Effort:** 3 Hours  
* **Story / Epic Reference:** FT-11 / UX Terminal  
* **Development Methodology:** TDD (Red-Green-Refactor)

## 📖 Description & Objectives

The current interactive CLI loop (`estocapao>` prompt) is functional but visually raw. It lacks a proper welcome banner, clear visual hierarchy in outputs, consistent color usage, and formatted feedback messages. This task performs a full visual redesign of the interactive shell experience without breaking any existing functionality.

### Pain Points Identified (User Reported)

1. **No welcome screen / banner** — The user lands directly in the raw prompt with no context.
2. **Unformatted output tables** — Stock listing, low-stock alerts, and status outputs are plain text without visual structure.
3. **Inconsistent feedback** — Success, warning, and error messages use no consistent color/icon convention.
4. **No visual separation between commands** — Each command output blends visually into the next.
5. **Missing prompt polish** — The `estocapao>` prompt has no color or visual affordance.

### Deliverables

1. **Branded ASCII banner** displayed once on shell startup (app name, version, short tagline).
2. **Color-coded prompt** — `estocapao ❯` in a distinct color (e.g., cyan/green), with the input kept white.
3. **Consistent message icons** — `✅` success, `⚠️` warning, `❌` error, `ℹ️` info — prepended to all feedback lines.
4. **Boxed/bordered output sections** — Command output wrapped in light ASCII box borders for visual clarity (`─`, `│`, `╭`, `╰`).
5. **Separator lines** — Thin `─` dividers between consecutive command outputs in the REPL loop.
6. **Graceful degradation** — All visual enhancements behind a `supports_unicode()` check; plain ASCII fallback for restricted terminals.

## ✅ Definition of Ready (DoR)

* [x] Interactive CLI loop is implemented and functional (shipped in the interactive shell fix).
* [x] Basic color output via `colorama` or `rich` is available in the dependency stack.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **[Functional - Banner]:** Running `estocapao.exe` (or `python -m estocapao`) displays a branded ASCII art banner with version and tagline before entering the prompt.
* [ ] **[Functional - Prompt]:** The interactive prompt renders as a colored `estocapao ❯` with user input in default terminal color.
* [ ] **[Functional - Feedback Icons]:** All success/error/warning/info outputs include the appropriate icon prefix consistently across all commands.
* [ ] **[Functional - Tables]:** `status` and `list` command outputs render inside light ASCII box borders with aligned columns.
* [ ] **[Functional - Separators]:** A thin `─` divider line is printed between each command output cycle in the REPL.
* [ ] **[Functional - Fallback]:** Setting `NO_COLOR=1` or `--no-color` strips all ANSI codes and unicode box chars, replacing with plain ASCII equivalents.
* [ ] **[Testing/Quality - TDD]:** New visual rendering functions are unit-tested via stdout capture (`capsys`) verifying presence of expected strings/icons.
* [ ] **[Verification]:** `python -m pytest` runs successfully with 100% pass rate (no regressions).
