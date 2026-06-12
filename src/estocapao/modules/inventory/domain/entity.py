"""This module represents a baking ingredient in the bakery's inventory, like flour or yeast."""
from typing import List
from estocapao.modules.inventory.domain.value import BatchValueObject, DomainValidationError

class InsufficientStockError(DomainValidationError):
    """Exception raised when an operation attempts to consume more stock than is available."""
    pass

class IngredientEntity:
    """An ingredient that is tracked in the inventory, keeping track of its name, minimum safety amount, and current batches."""

    def __init__(self, ingredient_id: str, name: str, safety_threshold: float):
        if not isinstance(safety_threshold, (int, float)):
            raise TypeError("Safety threshold must be a numeric value.")
        if safety_threshold < 0:
            raise ValueError("Safety threshold cannot be negative.")

        self.id = ingredient_id
        self.name = name
        self.safety_threshold = float(safety_threshold)  # The minimum amount we should keep in stock before warning the user
        self.batches: List[BatchValueObject] = []  # List of different batches/lots of this ingredient

    def add_batch(self, batch: BatchValueObject) -> None:
        """Adds an incoming batch (lot) to the ingredient's stock."""
        if not isinstance(batch, BatchValueObject):
            raise TypeError("Only BatchValueObject instances can be added to batches.")
        self.batches.append(batch)

    def get_total_quantity(self) -> float:
        """Sum up the total quantity across all active batches of this ingredient."""
        return sum(batch.quantity for batch in self.batches)

    def is_below_safety_threshold(self) -> bool:
        """Returns True if the total stock level is strictly below the safety threshold limit."""
        return self.get_total_quantity() < self.safety_threshold

    def consume_quantity(self, amount: float) -> None:
        """Consumes a specific amount of the ingredient's stock across batches following FEFO order.
        
        FEFO order: First-Expired, First-Out. Lotes are consumed first based on proximity of
        their expiration date, then their received date, and finally by their batch ID as a tiebreaker.
        
        If the amount requested exceeds available stock, InsufficientStockError is raised.
        """
        if not isinstance(amount, (int, float)):
            raise TypeError("Consumption amount must be a numeric value.")
        if amount <= 0:
            raise ValueError("Consumption amount must be a positive float greater than zero.")

        total_qty = self.get_total_quantity()
        if amount > total_qty:
            raise InsufficientStockError(
                f"Insufficient stock for ingredient '{self.name}'. "
                f"Requested: {amount}, Available: {total_qty}."
            )

        # Sort batches by expiration_date, received_date, and batch_id (FEFO strategy)
        sorted_batches = sorted(
            self.batches,
            key=lambda b: (b.expiration_date, b.received_date, b.batch_id)
        )

        remaining_to_consume = float(amount)
        new_batches: List[BatchValueObject] = []

        for batch in sorted_batches:
            if remaining_to_consume <= 0.0:
                new_batches.append(batch)
                continue

            if batch.quantity <= remaining_to_consume:
                # Fully consume this batch and subtract quantity from remaining target
                remaining_to_consume -= batch.quantity
            else:
                # Partially consume: create a new immutable BatchValueObject with the remaining balance
                reduced_qty = batch.quantity - remaining_to_consume
                new_batch = BatchValueObject(
                    batch_id=batch.batch_id,
                    quantity=reduced_qty,
                    expiration_date=batch.expiration_date,
                    received_date=batch.received_date
                )
                new_batches.append(new_batch)
                remaining_to_consume = 0.0

        self.batches = new_batches
