"""This module represents a baking ingredient in the bakery's inventory, like flour or yeast."""

class IngredientEntity:
    """An ingredient that is tracked in the inventory, keeping track of its name, minimum safety amount, and current batches."""

    def __init__(self, ingredient_id: str, name: str, safety_threshold: float):
        self.id = ingredient_id
        self.name = name
        self.safety_threshold = safety_threshold  # The minimum amount we should keep in stock before warning the user
        self.batches = []  # List of different batches/lots of this ingredient

    def get_total_quantity(self) -> float:
        """Sum up the total quantity across all active batches of this ingredient."""
        return sum(batch.quantity for batch in self.batches)
