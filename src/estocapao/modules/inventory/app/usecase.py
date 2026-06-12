"""This module contains the core features and actions a user can take in the application,
such as adding new stock or checking current stock levels.
"""
from estocapao.modules.inventory.domain.ports import IInventoryRepository

class UpdateStockUseCase:
    """Action that adds new batches or updates existing stock counts of an ingredient in the repository."""

    def __init__(self, repository: IInventoryRepository):
        self.repository = repository

    def execute(self, ingredient_id: str, quantity: float, batch_id: str = None) -> None:
        """Runs the stock update operation using the provided ingredient details."""
        pass

class GetInventoryStatusUseCase:
    """Action that checks current stock amounts and warns about low items or items near expiration."""

    def __init__(self, repository: IInventoryRepository):
        self.repository = repository

    def execute(self) -> dict:
        """Checks the stock and returns a report list of ingredients and warning messages."""
        return {}
