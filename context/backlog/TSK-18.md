# TSK-18: Semi-Visual Terminal Table Renderer (Renderizador de Tabelas Semi-Visuais)

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 2 Story Points / 8 Hours  
* **Story / Epic Reference:** FT-11 (UX Terminal & Onboarding)

## 📖 Description & Objectives

Upgrade the `status` command output from raw pipe-separated plain text to a rich, box-drawing character table with colored headers, aligned columns, and status-aware row highlight. The goal is a semi-visual interface that leigo (non-technical) users can read at a glance — similar to the experience of a spreadsheet in the terminal. No external dependencies (e.g., `rich`, `tabulate`) should be introduced; the renderer must be implemented using only Python standard library constructs and ANSI escape sequences already present in `shared/ansi.py`.

## ✅ Definition of Ready (DoR)

* [ ] `TerminalAnsiFormatter` and ANSI color constants confirmed available in `estocapao/shared/ansi.py`.
* [ ] `status` use case data contract (report dictionary keys) stable and documented.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Criterion 1 (Functional — Box Table):** `estocapao status` renders a Unicode box-drawing table (`╔═╦═╗ / ║ / ╠═╬═╣ / ╚═╩═╝`) with properly aligned columns: ID, Nome, Quantidade, Lote Mais Próximo do Vencimento, Limite Mín., Status.
* [ ] **Criterion 2 (Color Coding):** Rows with `LOW_STOCK` status are highlighted in amber/yellow; rows with quarantined batches display a red badge. `OK` rows are rendered in default or green text.
* [ ] **Criterion 3 (Quarantine Sub-section):** Expired/quarantined batches appear in a clearly separated sub-table below the main table, formatted with box-drawing characters and a distinct header.
* [ ] **Criterion 4 (Responsive Width):** Table column widths adapt dynamically to the longest value in each column, preventing content truncation on any realistic ingredient name.
* [ ] **Criterion 5 (Quality/Test):** Unit tests strip ANSI codes from rendered output and assert that column headers and at least one data row are present with correct pipe/box character structure.
* [ ] **Criterion 6 (Review):** Table rendering must be encapsulated in `src/estocapao/shared/table_renderer.py`. The `cli.py` file calls this renderer; it does not perform column formatting directly.
