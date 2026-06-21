# TSK-26: Production Yield Calculator (Calculadora de Rendimento de Produção)

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 2 Story Points / 8 Hours  
* **Story / Epic Reference:** FT-17 (Analytics & Pricing Intelligence)

## 📖 Description & Objectives

Implementar um módulo de cálculo de rendimento de produção que compara o estoque de ingredientes consumido por receita (`BatchValueObject` deduzido) com as unidades produzidas registradas pelo operador. O `EstocaPão` atualmente gerencia apenas entrada e saída de estoque em termos de peso/volume — sem nenhuma visibilidade sobre quantas unidades de produto final foram produzidas por lote de ingredientes. Esta feature introduz o conceito de `ProductionRun` (uma execução de produção) e o cálculo de `yield_rate = units_produced / ingredients_consumed_kg`, que é o dado estratégico fundamental para precificação, análise de desperdício e planejamento de compras.

## ✅ Definition of Ready (DoR)

* [ ] TSK-13 (Baking Recipes Engine) está completa ou em andamento — a associação receita → ingredientes está mapeada.
* [ ] TSK-14 (Batch Financial Controls) está completa ou em andamento — os custos de aquisição por lote estão disponíveis para o cálculo de custo por unidade produzida.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Critério 1 (Domínio):** `ProductionRun` implementado em `src/domain/production.py` como dataclass com campos: `recipe_name: str`, `ingredients_consumed: dict[str, float]`, `units_produced: int`, `production_date: date`, e `yield_rate: float` (calculado automaticamente).
* [ ] **Critério 2 (Registro de Produção):** Comando `estocapao produce --recipe <nome> --units <n>` deduz automaticamente os ingredientes da receita do estoque ativo, registra o `ProductionRun`, e calcula o `yield_rate`.
* [ ] **Critério 3 (Relatório de Rendimento):** Comando `estocapao yield-report` exibe uma tabela Rich com histórico de `ProductionRun`, ordenada por data, mostrando: receita, unidades produzidas, total de ingredientes consumidos (kg), yield rate, e custo por unidade (se TSK-14 estiver disponível).
* [ ] **Critério 4 (Análise de Tendência):** O relatório inclui uma linha de sumário com o yield médio dos últimos 30 dias por receita — permitindo ao padeiro identificar deterioração no rendimento ao longo do tempo.
* [ ] **Critério 5 (Qualidade/Testes):** Testes unitários cobrem: criação de `ProductionRun` com `yield_rate` calculado corretamente, produção com estoque insuficiente levanta `InsufficientStockError`, e `units_produced <= 0` levanta `InvalidProductionRunError`.
