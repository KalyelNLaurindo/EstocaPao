"""This file defines the rules/contracts for how the inventory data should be saved and loaded.
It does not specify *how* the data is saved (like in a file or database), only *what* methods must be available.
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional
from estocapao.modules.inventory.domain.entity import IngredientEntity

class IInventoryRepository(ABC):
    """Rules (interface) that any storage component must follow to save and load ingredients."""

    @abstractmethod
    def save(self, ingredient: IngredientEntity) -> None:
        """Saves an ingredient's information (like its name, limits, and batches)."""
        pass

    @abstractmethod
    def find_by_id(self, ingredient_id: str) -> Optional[IngredientEntity]:
        """Finds and returns an ingredient by its unique text ID, if it exists."""
        pass

    @abstractmethod
    def get_all(self) -> Dict[str, IngredientEntity]:
        """Retrieves a dictionary of all ingredients currently in stock."""
        pass
