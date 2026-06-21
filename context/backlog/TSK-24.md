# TSK-24: Supplier Batch Traceability Logger (Rastreabilidade de Lotes por Fornecedor)

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 2 Story Points / 8 Hours  
* **Story / Epic Reference:** FT-15 (Traceability & Compliance)

## 📖 Description & Objectives

Implementar um sistema de rastreabilidade de lotes que associa cada entrada de ingrediente no inventário ao seu fornecedor de origem, número de lote e data de entrega. Atualmente, o `EstocaPão` registra apenas quantidade e data de validade — sem nenhuma referência ao fornecedor. Essa ausência impede reembolso de lotes defeituosos, inviabiliza inspeções da ANVISA e elimina a possibilidade de análise de qualidade por fornecedor. O `BatchValueObject` existente deve ser estendido para incluir os campos de rastreabilidade, e um novo comando `estocapao batch-info` deve exibir o histórico de lotes de qualquer ingrediente.

## ✅ Definition of Ready (DoR)

* [ ] TSK-01 (BatchValueObject) está completa — a estrutura base do lote está definida e pode ser estendida.
* [ ] TSK-07 (LocalJsonRepositoryAdapter) está completa — o formato de persistência JSON suporta campos adicionais.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Critério 1 (Domínio):** `BatchValueObject` é estendido com os campos `supplier_name: str`, `batch_code: str`, e `delivery_date: date`. Todos os campos são obrigatórios na criação do lote.
* [ ] **Critério 2 (Validação de Entrada):** O comando `estocapao add` ou `estocapao update --add-batch` solicita interativamente `supplier_name`, `batch_code` e `delivery_date`, com validação: `batch_code` não pode ser vazio, `delivery_date` não pode ser no futuro.
* [ ] **Critério 3 (Persistência):** Os campos de rastreabilidade são serializados e desserializados corretamente no `LocalJsonRepositoryAdapter` sem quebrar compatibilidade com registros legados (campos ausentes são preenchidos como `"unknown"` durante a migração de leitura).
* [ ] **Critério 4 (Comando batch-info):** `estocapao batch-info --ingredient <id>` exibe uma tabela Rich com o histórico completo de lotes do ingrediente — fornecedor, código, data de entrega, data de validade e status (ativo/descartado).
* [ ] **Critério 5 (Qualidade/Testes):** Testes unitários em `tests/unit/test_domain.py` cobrem: criação válida de lote com rastreabilidade, rejeição de `delivery_date` no futuro, e leitura de lotes legados sem os campos de rastreabilidade (retrocompatibilidade).
