# TSK-25: Ingredient Expiration Purge Scheduler (Quarentena Automática de Ingredientes Vencidos)

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 2 Story Points / 8 Hours  
* **Story / Epic Reference:** FT-16 (Lifecycle Management)

## 📖 Description & Objectives

Implementar uma rotina de quarentena automática que identifica e isola ingredientes vencidos durante a inicialização da aplicação ou na execução do comando `status`. Atualmente, ingredientes expirados permanecem no inventário ativo sem nenhuma sinalização automática — o operador só descobre o vencimento ao verificar manualmente cada item. Esta task introduz a transição de estado `ACTIVE → QUARANTINED` para ingredientes cuja `expiry_date < today`, com exibição destacada na CLI e opção de confirmação de descarte via `estocapao discard --expired`.

## ✅ Definition of Ready (DoR)

* [ ] TSK-04 (Quarantine Gatekeeper) está completa — a lógica base de quarentena existe e pode ser estendida.
* [ ] TSK-05 (Core Configuration Parser) está completa — o `config.ini` pode ser consultado para configurar o comportamento (ex.: dias de grace period antes da quarentena).

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [ ] **Critério 1 (Verificação Automática):** Ao executar `estocapao status` ou inicializar a aplicação, todos os ingredientes com `expiry_date < today` são automaticamente marcados como `QUARANTINED` no repositório em memória.
* [ ] **Critério 2 (Grace Period Configurável):** O `config.ini` suporta o campo `[inventory] expiry_grace_days = N`. Ingredientes com `expiry_date + N days >= today` ficam em estado `EXPIRING_SOON` (aviso) em vez de `QUARANTINED` (bloqueio).
* [ ] **Critério 3 (Bloqueio de Uso):** Qualquer tentativa de `update` ou dedução de estoque em um ingrediente `QUARANTINED` é rejeitada com `QuarantinedIngredientError` — impedindo uso acidental em produção.
* [ ] **Critério 4 (Comando de Descarte):** `estocapao discard --expired` lista todos os itens em quarentena, solicita confirmação interativa, e remove-os permanentemente do repositório com registro de auditoria.
* [ ] **Critério 5 (Qualidade/Testes):** Testes unitários cobrem: ingrediente com `expiry_date = yesterday` → QUARANTINED, ingrediente com `expiry_date = today + grace_days` → EXPIRING_SOON, tentativa de update em QUARANTINED → levanta `QuarantinedIngredientError`, e grace_days=0 (configuração padrão) funciona corretamente.
