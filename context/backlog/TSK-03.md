# TSK-03: Create Core Use Cases: UpdateStock & GetInventoryStatus

* **Owner / Assignee:** Tech Lead / AI Agent  
* **Estimated Effort:** 3 Story Points / 12 Hours  
* **Story / Epic Reference:** FT-03 (Use Case Interactors)

## 📖 Description & Objectives

Program the application use cases UpdateStockUseCase and GetInventoryStatusUseCase within `src/estocapao/modules/inventory/app/usecase.py`. These orchestrators implement the application ports, driving the domain models' state transition and querying database operations via abstract outbound port interfaces.

## ✅ Definition of Ready (DoR)

* [x] Core domain models (IngredientEntity, BatchValueObject) completed and validated.  
* [x] Outbound port interface IInventoryRepository defined in `src/estocapao/modules/inventory/domain/ports.py`.

## 🏁 Definition of Done (DoD) & Acceptance Criteria

* [x] **Criterion 1 (Functional):** UpdateStockUseCase manages in-memory dictionary transitions, searching ingredient registries, adding/removing batches, and committing saved changes via the repository port. GetInventoryStatusUseCase returns a complete system status report mapping all products and alert flags (OK/Low Stock).  
* [x] **Criterion 2 (Performance):** All dynamic map-based retrieval, search, and storage mutations within use-cases must maintain ![][image1] complexity, achieving an execution timeframe of under 5 milliseconds.  
* [x] **Criterion 3 (Quality/Test):** Implement a comprehensive test set in `tests/unit/test_usecases.py` utilizing standard double mocks for storage, ensuring 100% decoupling from disk access.  
* [x] **Criterion 4 (Review):** Dependency Inversion Principle (DIP) validated: application code relies only on abstract repository interfaces, not concrete implementations.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACsAAAAaCAYAAAAue6XIAAAC7klEQVR4Xu2WP2gUQRjF70gEBUWjRvH+7d6dEIIWhlOxUAsRSQoVJGAgjZ3WahStYpHCRiQIQprTSsG0GrAxEBHRTggKUUQ5FBW1sRMTf+9u9xi+ZC97mAsI9+Bjdr/3Zr43uzOzm0i08Z+gu7t7ve/7a20+CqVSaU2hUNho800jnU5vyWazx3K53KDneb2kOqzGBSb3oC03U1xm6XOT8U9ZLg6S+Xz+MIVfMMAUMazg/jHtHOb32Q4CE8vAP6HwLssJmUxmHWOcITZZTg+Fvo+ou99ykdAsGew6Hd9bU+LITxA/iT6XA0k9HfqOukkMbiZ3Gu5O0O8DscPVhEDXrweiZWS5RQhex20G+xE1Qy0F4jtxi9tkmGdiu8m9UevIQ7Mnye9l7PuNzGrpwD1DP2S5RUB0DvG8WsuFoGAXmpfEbCqV2urkL5N76DfYWHB3G5kV4MaISS47LVcHT2Anok/Ea57qdsuHcMzWi8qgjBJXrd5FTLMD0mj9W64OBhpFtKCZWc4FZgtoPrtF1eoe7rjVu4hjljFK8BW7X+rQgkYwTcwjPmp5F+KlI2Z6eno2BDkV+EJ70OpdxDG77MRDgVfbODpLIwE/TizoTYQ5mSU+qnWki9CMWWLYclU4goYDsaGy8HPEt5xzlrbI7HnLVaFdDTm7zEBJil3xauv6gku0wmzkMgCdCO4Rv6PWnc5dr3aoT+g8drlcbdPpJBlw8xZxzMYaC7JPZhCXrRnyR4ivxA19Ml1OCN8MZs5azkVgttLoWNIpgOadt8zeCYVv/do/QfV/gJji/pUMJ5wvloE+tWU045YoFovbyM8Qv7zaElL8ISr+Eh+foOZ0rE8u6EDcS/FBrRsmkEpEm6yDwkOaJH26LNcEqsvRN/8XK47gr+kphfotFxfBV/S5WsutOHgLJyj2YKl1HQM6ba7xZi7p2pKtQBKzIwpdW7IRmOgh+k0289P+zwj+eS/ylA5YLgq8iTR9xlbVaBttrBL+AqG828/L5VzTAAAAAElFTkSuQmCC>
