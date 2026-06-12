"""This module contains the core features and actions a user can take in the application,
such as adding new stock or checking current stock levels.
"""
from datetime import date
from typing import Union
from estocapao.modules.inventory.domain.ports import IInventoryRepository
from estocapao.modules.inventory.domain.value import BatchValueObject

class UpdateStockUseCase:
    """Action that adds new batches or updates existing stock counts of an ingredient in the repository."""

    def __init__(self, repository: IInventoryRepository):
        self.repository = repository

    def execute(
        self,
        ingredient_id: str,
        quantity: float,
        batch_id: str = None,
        expiration_date: Union[str, date] = None,
        received_date: Union[str, date] = None
    ) -> None:
        """Runs the stock update operation using the provided ingredient details."""
        if not isinstance(quantity, (int, float)):
            raise TypeError("Quantity adjustment must be a numeric value.")
        if quantity == 0.0:
            raise ValueError("Quantity adjustment must be non-zero.")

        ingredient = self.repository.find_by_id(ingredient_id)
        if not ingredient:
            raise ValueError(f"Ingredient with ID '{ingredient_id}' not found.")

        if quantity < 0.0:
            # Consume stock (quantity is negative, so consume the positive amount)
            ingredient.consume_quantity(abs(quantity))
        else:
            # Add new batch (quantity is positive)
            if not batch_id:
                raise ValueError("Batch ID is required when adding stock.")
            if not expiration_date:
                raise ValueError("Expiration date is required when adding stock.")
            
            # Default received date to today if not provided
            if not received_date:
                received_date = date.today()

            batch = BatchValueObject(
                batch_id=batch_id,
                quantity=quantity,
                expiration_date=expiration_date,
                received_date=received_date
            )
            ingredient.add_batch(batch)

        self.repository.save(ingredient)


class GetInventoryStatusUseCase:
    """Action that checks current stock amounts and warns about low items or items near expiration."""

    def __init__(self, repository: IInventoryRepository):
        self.repository = repository

    def execute(self) -> dict:
        """Checks the stock and returns a report list of ingredients and warning messages."""
        ingredients = self.repository.get_all()
        report = {}
        for ing_id, ing in ingredients.items():
            status = "LOW_STOCK" if ing.is_below_safety_threshold() else "OK"
            report[ing_id] = {
                "id": ing.id,
                "name": ing.name,
                "total_quantity": ing.get_total_quantity(),
                "safety_threshold": ing.safety_threshold,
                "status": status
            }
        return report
