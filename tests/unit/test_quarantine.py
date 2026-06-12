import unittest
from datetime import date
from typing import Dict, Optional

from estocapao.modules.inventory.domain.ports import IInventoryRepository
from estocapao.modules.inventory.domain.entity import IngredientEntity
from estocapao.modules.inventory.domain.value import BatchValueObject
from estocapao.modules.inventory.app.quarantine import QuarantineManager
from estocapao.modules.inventory.app.usecase import GetInventoryStatusUseCase

class InMemoryInventoryRepository(IInventoryRepository):
    """An in-memory fake repository implementation of IInventoryRepository for testing."""

    def __init__(self):
        self._ingredients: Dict[str, IngredientEntity] = {}

    def save(self, ingredient: IngredientEntity) -> None:
        self._ingredients[ingredient.id] = ingredient

    def find_by_id(self, ingredient_id: str) -> Optional[IngredientEntity]:
        return self._ingredients.get(ingredient_id)

    def get_all(self) -> Dict[str, IngredientEntity]:
        return self._ingredients.copy()

class TestQuarantineManager(unittest.TestCase):
    """Unit tests for the QuarantineManager use-case layer."""

    def setUp(self):
        self.repository = InMemoryInventoryRepository()
        self.manager = QuarantineManager(self.repository)

        # Seed repository with some ingredients
        self.flour = IngredientEntity("FL-001", "Wheat Flour", safety_threshold=10.0)
        self.yeast = IngredientEntity("YS-001", "Dry Yeast", safety_threshold=2.0)
        self.repository.save(self.flour)
        self.repository.save(self.yeast)

    def test_quarantine_expired_batches_isolation(self):
        """Should dynamically isolate expired batches and remove their weight from active stock."""
        # Active batch (not expired)
        batch_valid = BatchValueObject("LOT-V", 15.0, "2026-06-15", "2026-06-12")
        # Expired batch
        batch_expired = BatchValueObject("LOT-E", 5.0, "2026-06-10", "2026-06-08")

        self.flour.add_batch(batch_valid)
        self.flour.add_batch(batch_expired)
        self.repository.save(self.flour)

        # System operational date: 2026-06-12
        system_date = date(2026, 6, 12)
        quarantined = self.manager.quarantine_expired_batches(system_date)

        # Verify return structure: mapping of ingredient ID to list of quarantined batches
        self.assertIn("FL-001", quarantined)
        self.assertEqual(len(quarantined["FL-001"]), 1)
        self.assertEqual(quarantined["FL-001"][0].batch_id, "LOT-E")

        # Verify active batches on entity
        updated_flour = self.repository.find_by_id("FL-001")
        self.assertIsNotNone(updated_flour)
        self.assertEqual(len(updated_flour.batches), 1) # type: ignore
        self.assertEqual(updated_flour.batches[0].batch_id, "LOT-V") # type: ignore

        # Verify quarantined batches on entity
        self.assertEqual(len(updated_flour.quarantine_batches), 1) # type: ignore
        self.assertEqual(updated_flour.quarantine_batches[0].batch_id, "LOT-E") # type: ignore

        # Verify total active quantity excludes expired batch (15.0 instead of 20.0)
        self.assertEqual(updated_flour.get_total_quantity(), 15.0) # type: ignore

    def test_quarantine_exact_expiration_date(self):
        """Should quarantine batch whose expiration date matches the system date exactly."""
        batch_expires_today = BatchValueObject("LOT-T", 10.0, "2026-06-12", "2026-06-12")
        self.flour.add_batch(batch_expires_today)
        self.repository.save(self.flour)

        system_date = date(2026, 6, 12)
        quarantined = self.manager.quarantine_expired_batches(system_date)

        self.assertIn("FL-001", quarantined)
        self.assertEqual(quarantined["FL-001"][0].batch_id, "LOT-T")
        
        updated_flour = self.repository.find_by_id("FL-001")
        self.assertEqual(len(updated_flour.batches), 0) # type: ignore
        self.assertEqual(len(updated_flour.quarantine_batches), 1) # type: ignore

    def test_quarantine_no_expired_batches(self):
        """Should not quarantine anything if all batches expire in the future."""
        batch_future = BatchValueObject("LOT-F", 10.0, "2026-06-13", "2026-06-12")
        self.flour.add_batch(batch_future)
        self.repository.save(self.flour)

        system_date = date(2026, 6, 12)
        quarantined = self.manager.quarantine_expired_batches(system_date)

        self.assertEqual(len(quarantined), 0)
        
        updated_flour = self.repository.find_by_id("FL-001")
        self.assertEqual(len(updated_flour.batches), 1) # type: ignore
        self.assertEqual(len(updated_flour.quarantine_batches), 0) # type: ignore

    def test_automatic_quarantine_during_inventory_status_query(self):
        """Should automatically quarantine expired batches when checking inventory status."""
        batch_valid = BatchValueObject("LOT-V", 12.0, "2026-06-20", "2026-06-12")
        batch_expired = BatchValueObject("LOT-E", 8.0, "2026-06-11", "2026-06-08")
        
        self.flour.add_batch(batch_valid)
        self.flour.add_batch(batch_expired)
        self.repository.save(self.flour)

        use_case = GetInventoryStatusUseCase(self.repository)
        # Call execute with system date
        system_date = date(2026, 6, 12)
        report = use_case.execute(system_date=system_date)

        # Active stock total should only reflect valid batch weight
        self.assertIn("FL-001", report)
        self.assertEqual(report["FL-001"]["total_quantity"], 12.0)
        self.assertEqual(report["FL-001"]["status"], "OK") # 12.0 >= 10.0 safety threshold

        # Expiry batch is quarantined in DB/repo
        updated_flour = self.repository.find_by_id("FL-001")
        self.assertEqual(len(updated_flour.batches), 1) # type: ignore
        self.assertEqual(len(updated_flour.quarantine_batches), 1) # type: ignore

    def test_discard_quarantined_batch_success(self):
        """Should remove the batch from quarantine list permanently and save entity."""
        batch_expired = BatchValueObject("LOT-E", 5.0, "2026-06-10", "2026-06-08")
        self.flour.add_quarantine_batch(batch_expired)
        self.repository.save(self.flour)

        self.manager.discard_quarantined_batch("LOT-E")

        updated_flour = self.repository.find_by_id("FL-001")
        self.assertIsNotNone(updated_flour)
        self.assertEqual(len(updated_flour.quarantine_batches), 0) # type: ignore

    def test_discard_quarantined_batch_not_found(self):
        """Should raise ValueError if attempting to discard a batch ID not present in quarantine."""
        with self.assertRaises(ValueError):
            self.manager.discard_quarantined_batch("NON-EXISTENT-ID")

    def test_serialization_compatibility(self):
        """Should verify ingredient entity can be serialized and deserialized with quarantine state."""
        batch_valid = BatchValueObject("LOT-V", 10.0, "2026-06-20", "2026-06-12")
        batch_expired = BatchValueObject("LOT-E", 5.0, "2026-06-10", "2026-06-08")

        self.flour.add_batch(batch_valid)
        self.flour.add_quarantine_batch(batch_expired)

        # Simulate conversion to dict for serialization
        state = {
            "id": self.flour.id,
            "name": self.flour.name,
            "safety_threshold": self.flour.safety_threshold,
            "batches": [
                {
                    "batch_id": b.batch_id,
                    "quantity": b.quantity,
                    "expiration_date": b.expiration_date.isoformat(),
                    "received_date": b.received_date.isoformat()
                } for b in self.flour.batches
            ],
            "quarantine_batches": [
                {
                    "batch_id": b.batch_id,
                    "quantity": b.quantity,
                    "expiration_date": b.expiration_date.isoformat(),
                    "received_date": b.received_date.isoformat()
                } for b in self.flour.quarantine_batches
            ]
        }

        # Simulate loading from dict for deserialization
        loaded_ingredient = IngredientEntity(
            ingredient_id=state["id"],
            name=state["name"],
            safety_threshold=state["safety_threshold"]
        )
        for b_dict in state["batches"]:
            loaded_ingredient.add_batch(BatchValueObject(
                batch_id=b_dict["batch_id"],
                quantity=b_dict["quantity"],
                expiration_date=b_dict["expiration_date"],
                received_date=b_dict["received_date"]
            ))
        for b_dict in state["quarantine_batches"]:
            loaded_ingredient.add_quarantine_batch(BatchValueObject(
                batch_id=b_dict["batch_id"],
                quantity=b_dict["quantity"],
                expiration_date=b_dict["expiration_date"],
                received_date=b_dict["received_date"]
            ))

        self.assertEqual(loaded_ingredient.id, self.flour.id)
        self.assertEqual(loaded_ingredient.name, self.flour.name)
        self.assertEqual(loaded_ingredient.safety_threshold, self.flour.safety_threshold)
        self.assertEqual(len(loaded_ingredient.batches), 1)
        self.assertEqual(loaded_ingredient.batches[0].batch_id, "LOT-V")
        self.assertEqual(len(loaded_ingredient.quarantine_batches), 1)
        self.assertEqual(loaded_ingredient.quarantine_batches[0].batch_id, "LOT-E")

if __name__ == "__main__":
    unittest.main()
