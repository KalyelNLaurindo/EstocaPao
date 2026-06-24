# TSK-32: HTTP REST API Backend Server Integration

* **Owner / Assignee:** Kalyel N. Laurindo / Project Owner  
* **Estimated Effort:** 5 Hours  
* **Story / Epic Reference:** RF10 / HTTP Backend Services  
* **Development Methodology:** TDD & Port-Adapter Pattern

## 📖 Description & Objectives

Expose the EstocaPão inventory engine as an HTTP REST API server. This allows external tools or dashboards to fetch real-time stock levels, record updates, and monitor quarantine items via HTTP.

The server will expose the following endpoints:
1. `GET /inventory` - Get current stock levels and alerts (triggers `GetInventoryStatusUseCase`).
2. `POST /inventory/lots` - Add a new ingredient lot (triggers `UpdateStockUseCase`).
3. `POST /inventory/updates` - Consume/add stock to an existing lot (triggers `UpdateStockUseCase`).
4. `DELETE /quarantine/lots/{batch_id}` - Discard a quarantined batch (triggers `QuarantineManager`).

## ✅ Definition of Ready (DoR)

* [ ] HTTP endpoint routing and request validation logic defined.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

### BDD Scenarios (Gherkin Format):

```gherkin
Scenario: Query inventory status via GET request
  Given the database has active stock
  When a GET request is sent to "/inventory"
  Then the response status code is 200
  And the JSON payload contains stock quantities and safety threshold status

Scenario: Record consumption via POST update
  Given ingredient "flour" has 20.0 units
  When a POST request is sent to "/inventory/updates" with payload:
    | id    | qty  |
    | flour | -5.0 |
  Then the response status code is 200
  And flour stock is reduced to 15.0 units
```

* [ ] **[Functional]:** HTTP server implemented in `infra/` folder.
* [ ] **[Functional]:** Inputs are validated and exceptions mapped to standard HTTP status codes.
* [ ] **[Verification]:** End-to-end HTTP integration tests pass successfully.
