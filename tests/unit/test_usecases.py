import unittest
from datetime import date
from typing import Dict, Optional

from estocapao.modules.inventory.domain.ports import IInventoryRepository
from estocapao.modules.inventory.domain.entity import IngredientEntity
from estocapao.modules.inventory.domain.value import BatchValueObject
from estocapao.modules.inventory.app.usecase import (
    UpdateStockUseCase,
    GetInventoryStatusUseCase
)

class InMemoryInventoryRepository(IInventoryRepository):
    """An in-memory fake repository implementation of IInventoryRepository for unit testing."""

    def __init__(self):
        self._ingredients: Dict[str, IngredientEntity] = {}

    def save(self, ingredient: IngredientEntity) -> None:
        # In a real repository we might deep copy, but for simple mocks storing the reference is fine
        self._ingredients[ingredient.id] = ingredient

    def find_by_id(self, ingredient_id: str) -> Optional[IngredientEntity]:
        return self._ingredients.get(ingredient_id)

    def get_all(self) -> Dict[str, IngredientEntity]:
        return self._ingredients.copy()


class TestInventoryUseCases(unittest.TestCase):
    """Unit tests for the inventory application use cases using an in-memory test double."""

    def setUp(self):
        self.repository = InMemoryInventoryRepository()
        
        # Seed repo with standard ingredient
        self.flour = IngredientEntity(
            ingredient_id="FL-001",
            name="Wheat Flour",
            safety_threshold=10.0
        )
        self.repository.save(self.flour)

    def test_update_stock_add_batch_success(self):
        """Should add a new batch to an existing ingredient and save changes to repository."""
        use_case = UpdateStockUseCase(self.repository)
        
        use_case.execute(
            ingredient_id="FL-001",
            quantity=15.0,
            batch_id="BATCH-001",
            expiration_date="2026-12-31"
        )
        
        # Check ingredient status in repo
        updated_flour = self.repository.find_by_id("FL-001")
        self.assertIsNotNone(updated_flour)
        self.assertEqual(updated_flour.get_total_quantity(), 15.0) # type: ignore
        self.assertEqual(len(updated_flour.batches), 1) # type: ignore
        
        batch = updated_flour.batches[0] # type: ignore
        self.assertEqual(batch.batch_id, "BATCH-001")
        self.assertEqual(batch.quantity, 15.0)
        self.assertEqual(batch.expiration_date, date(2026, 12, 31))
        # Default received_date should be today
        self.assertEqual(batch.received_date, date.today())

    def test_update_stock_consume_success(self):
        """Should consume inventory quantity from active batches and save changes to repository."""
        # Setup starting batch
        starting_batch = BatchValueObject("LOT-A", 10.0, "2026-12-31", "2026-06-12")
        self.flour.add_batch(starting_batch)
        self.repository.save(self.flour)
        
        use_case = UpdateStockUseCase(self.repository)
        
        # Consume 4.0 units (indicated as negative quantity)
        use_case.execute(
            ingredient_id="FL-001",
            quantity=-4.0
        )
        
        updated_flour = self.repository.find_by_id("FL-001")
        self.assertIsNotNone(updated_flour)
        self.assertEqual(updated_flour.get_total_quantity(), 6.0) # type: ignore
        self.assertEqual(len(updated_flour.batches), 1) # type: ignore
        self.assertEqual(updated_flour.batches[0].quantity, 6.0) # type: ignore

    def test_update_stock_ingredient_not_found(self):
        """Should raise ValueError if attempting to update stock of a non-existent ingredient."""
        use_case = UpdateStockUseCase(self.repository)
        
        with self.assertRaises(ValueError):
            use_case.execute(
                ingredient_id="UNKNOWN-ID",
                quantity=5.0,
                batch_id="BATCH-001",
                expiration_date="2026-12-31"
            )

    def test_update_stock_missing_arguments_on_add(self):
        """Should raise ValueError if positive quantity is provided but batch_id or expiration_date is missing."""
        use_case = UpdateStockUseCase(self.repository)
        
        # Missing batch_id
        with self.assertRaises(ValueError):
            use_case.execute(
                ingredient_id="FL-001",
                quantity=10.0,
                expiration_date="2026-12-31"
            )
            
        # Missing expiration_date
        with self.assertRaises(ValueError):
            use_case.execute(
                ingredient_id="FL-001",
                quantity=10.0,
                batch_id="LOT-123"
            )

    def test_update_stock_zero_quantity_raises_error(self):
        """Should raise ValueError if updating stock with a zero quantity adjustment."""
        use_case = UpdateStockUseCase(self.repository)
        with self.assertRaises(ValueError):
            use_case.execute(ingredient_id="FL-001", quantity=0.0)

    def test_get_inventory_status_report(self):
        """Should generate a complete report mapping ingredients and their safety alert states."""
        # 1. Flour: stock is 5.0, threshold is 10.0 -> status should be LOW_STOCK
        batch_flour = BatchValueObject("LOT-F", 5.0, "2026-12-31", "2026-06-12")
        self.flour.add_batch(batch_flour)
        self.repository.save(self.flour)
        
        # 2. Sugar: stock is 12.0, threshold is 10.0 -> status should be OK
        sugar = IngredientEntity("SG-002", "Granulated Sugar", 10.0)
        batch_sugar = BatchValueObject("LOT-S", 12.0, "2026-12-31", "2026-06-12")
        sugar.add_batch(batch_sugar)
        self.repository.save(sugar)
        
        use_case = GetInventoryStatusUseCase(self.repository)
        report = use_case.execute()
        
        self.assertEqual(len(report), 2)
        
        # Assert Flour status details
        self.assertIn("FL-001", report)
        self.assertEqual(report["FL-001"]["name"], "Wheat Flour")
        self.assertEqual(report["FL-001"]["total_quantity"], 5.0)
        self.assertEqual(report["FL-001"]["safety_threshold"], 10.0)
        self.assertEqual(report["FL-001"]["status"], "LOW_STOCK")
        
        # Assert Sugar status details
        self.assertIn("SG-002", report)
        self.assertEqual(report["SG-002"]["name"], "Granulated Sugar")
        self.assertEqual(report["SG-002"]["total_quantity"], 12.0)
        self.assertEqual(report["SG-002"]["safety_threshold"], 10.0)
        self.assertEqual(report["SG-002"]["status"], "OK")

if __name__ == "__main__":
    unittest.main()
