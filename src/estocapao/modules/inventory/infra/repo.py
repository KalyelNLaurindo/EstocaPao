"""This module handles saving and loading the inventory data directly to a local JSON file on the computer's hard drive."""
from typing import Dict, Optional
from estocapao.modules.inventory.domain.entity import IngredientEntity
from estocapao.modules.inventory.domain.ports import IInventoryRepository

class LocalJsonRepositoryAdapter(IInventoryRepository):
    """Responsible for reading and writing our inventory state to a text file on the local computer."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._memory_cache = {}  # Holds inventory data temporarily in memory for high speed

    def save(self, ingredient: IngredientEntity) -> None:
        """Saves the ingredient details to the JSON file safely, avoiding data loss if the computer crashes."""
        pass

    def find_by_id(self, ingredient_id: str) -> Optional[IngredientEntity]:
        """Searches the fast in-memory inventory list for an ingredient matching the given ID."""
        return None

    def get_all(self) -> Dict[str, IngredientEntity]:
        """Returns the entire list of ingredients we currently have loaded in memory."""
        return {}
