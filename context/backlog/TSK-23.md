# TSK-23: Low-Stock Threshold Alert Engine (Motor de Alertas de Estoque Mínimo)

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 1 Story Point / 4 Hours  
* **Story / Epic Reference:** FT-14 (Alerts & Inventory Intelligence)

## 📖 Description & Objectives

Implementar um motor de alertas de estoque mínimo que monitora automaticamente os níveis de cada ingrediente cadastrado no inventário e dispara avisos coloridos na CLI sempre que um item cair abaixo do limite configurado (threshold). Atualmente, o operador descobre a falta de estoque apenas ao tentar registrar uma produção — um ponto de falha tardio. O sistema deve avaliar todos os ingredientes durante o comando `status` e destacar visualmente qualquer item abaixo do seu `min_stock` configurado, classificando-os por criticidade (CRÍTICO < 20%, BAIXO < 50% do mínimo).

## ✅ Definition of Ready (DoR)

* [ ] TSK-02 (IngredientEntity & Stock Invariants) está completa — o campo `min_stock` está definido e estável no domínio.
* [ ] TSK-09 (CommandLineInterfaceParser) está completa — o comando `status` existe e renderiza o inventário.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Critério 1 (Domínio):** `IngredientEntity.stock_alert_level()` retorna `AlertLevel.CRITICAL` quando `current_qty < min_stock * 0.2`, `AlertLevel.LOW` quando `current_qty < min_stock`, e `AlertLevel.OK` caso contrário.
* [ ] **Critério 2 (Integração CLI):** O comando `estocapao status` exibe um painel Rich destacando todos os ingredientes com `AlertLevel != OK`, ordenados por criticidade (CRITICAL primeiro), com nome, quantidade atual, e limiar mínimo.
* [ ] **Critério 3 (Log de Auditoria):** Cada ingrediente com alerta ativo gera uma entrada `[WARNING]` no log de auditoria via `log_action`, com o identificador do ingrediente e o nível de alerta.
* [ ] **Critério 4 (Configurabilidade):** O `min_stock` de cada ingrediente é editável via `estocapao update --ingredient <id> --min-stock <valor>` sem exigir reinicialização da aplicação.
* [ ] **Critério 5 (Qualidade/Testes):** Testes unitários em `tests/unit/test_domain.py` cobrem: item abaixo de 20% (CRITICAL), item entre 20%-100% do mínimo (LOW), item acima do mínimo (OK), e item com `min_stock=0` (deve sempre retornar OK para evitar falsos positivos).
