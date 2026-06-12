import unittest
from datetime import date
from estocapao.modules.inventory.domain.value import BatchValueObject
from estocapao.modules.inventory.domain.entity import IngredientEntity, InsufficientStockError

class TestIngredientEntity(unittest.TestCase):
    """Unit tests for the IngredientEntity domain aggregate root."""

    def test_initialization(self):
        """Should initialize IngredientEntity with ID, name, safety threshold, and empty batches."""
        ingredient = IngredientEntity(
            ingredient_id="ING-001",
            name="Specialty Flour",
            safety_threshold=10.0
        )
        self.assertEqual(ingredient.id, "ING-001")
        self.assertEqual(ingredient.name, "Specialty Flour")
        self.assertEqual(ingredient.safety_threshold, 10.0)
        self.assertEqual(ingredient.batches, [])

    def test_add_batch(self):
        """Should successfully append a BatchValueObject to the batches collection."""
        ingredient = IngredientEntity("ING-001", "Specialty Flour", 10.0)
        batch = BatchValueObject("LOT-001", 5.0, "2026-12-31", "2026-06-12")
        ingredient.add_batch(batch)
        self.assertEqual(len(ingredient.batches), 1)
        self.assertEqual(ingredient.batches[0], batch)

    def test_get_total_quantity(self):
        """Should calculate the sum of quantities across all active batches."""
        ingredient = IngredientEntity("ING-001", "Specialty Flour", 10.0)
        self.assertEqual(ingredient.get_total_quantity(), 0.0)

        batch_1 = BatchValueObject("LOT-001", 5.5, "2026-12-31", "2026-06-12")
        batch_2 = BatchValueObject("LOT-002", 3.0, "2026-11-30", "2026-06-12")
        ingredient.add_batch(batch_1)
        ingredient.add_batch(batch_2)
        
        self.assertEqual(ingredient.get_total_quantity(), 8.5)

    def test_is_below_safety_threshold(self):
        """Should return True if total stock is strictly below the safety threshold, False otherwise."""
        ingredient = IngredientEntity("ING-001", "Specialty Flour", 10.0)
        
        # Empty stock (0.0 < 10.0) -> True
        self.assertTrue(ingredient.is_below_safety_threshold())

        # Low stock (9.5 < 10.0) -> True
        batch_low = BatchValueObject("LOT-001", 9.5, "2026-12-31", "2026-06-12")
        ingredient.add_batch(batch_low)
        self.assertTrue(ingredient.is_below_safety_threshold())

        # Exact stock (10.0 is not strictly below 10.0) -> False
        ingredient.batches = []
        batch_exact = BatchValueObject("LOT-002", 10.0, "2026-12-31", "2026-06-12")
        ingredient.add_batch(batch_exact)
        self.assertFalse(ingredient.is_below_safety_threshold())

        # High stock (15.0 < 10.0) -> False
        batch_high = BatchValueObject("LOT-003", 5.0, "2026-12-31", "2026-06-12")
        ingredient.add_batch(batch_high)
        self.assertFalse(ingredient.is_below_safety_threshold())

    def test_consume_quantity_fefo_strategy(self):
        """Should consume stock from batches using the FEFO (First-Expired, First-Out) priority order."""
        ingredient = IngredientEntity("ING-001", "Yeast", 5.0)

        # Batch A: Expires later (2026-06-30), received earlier (2026-06-08)
        batch_a = BatchValueObject("LOT-A", 5.0, "2026-06-30", "2026-06-08")
        # Batch B: Expires first (2026-06-20), received later (2026-06-10)
        batch_b = BatchValueObject("LOT-B", 3.0, "2026-06-20", "2026-06-10")
        # Batch C: Expires last (2026-07-05), received last (2026-06-12)
        batch_c = BatchValueObject("LOT-C", 4.0, "2026-07-05", "2026-06-12")

        ingredient.add_batch(batch_a)
        ingredient.add_batch(batch_b)
        ingredient.add_batch(batch_c)

        # Total starting quantity: 12.0
        # Expiration order: LOT-B (expires 06-20) -> LOT-A (expires 06-30) -> LOT-C (expires 07-05)

        # Consume 4.0
        # This should fully consume LOT-B (3.0) and partially consume 1.0 from LOT-A.
        ingredient.consume_quantity(4.0)

        self.assertEqual(ingredient.get_total_quantity(), 8.0)
        self.assertEqual(len(ingredient.batches), 2)
        
        # LOT-B should be completely gone.
        # LOT-A should have 4.0 remaining (5.0 - 1.0).
        # LOT-C should remain untouched at 4.0.
        remaining_ids = [b.batch_id for b in ingredient.batches]
        self.assertNotIn("LOT-B", remaining_ids)
        self.assertIn("LOT-A", remaining_ids)
        self.assertIn("LOT-C", remaining_ids)

        lot_a_remaining = next(b for b in ingredient.batches if b.batch_id == "LOT-A")
        self.assertEqual(lot_a_remaining.quantity, 4.0)

    def test_consume_exact_quantity(self):
        """Should successfully clear all batches when exactly the total stock quantity is consumed."""
        ingredient = IngredientEntity("ING-001", "Sugar", 5.0)
        batch_1 = BatchValueObject("LOT-1", 5.0, "2026-12-31", "2026-06-12")
        batch_2 = BatchValueObject("LOT-2", 2.5, "2026-12-31", "2026-06-12")
        ingredient.add_batch(batch_1)
        ingredient.add_batch(batch_2)

        ingredient.consume_quantity(7.5)
        self.assertEqual(ingredient.get_total_quantity(), 0.0)
        self.assertEqual(ingredient.batches, [])

    def test_consume_insufficient_stock_raises_error(self):
        """Should raise InsufficientStockError and leave batches unchanged if request exceeds total stock."""
        ingredient = IngredientEntity("ING-001", "Sugar", 5.0)
        batch = BatchValueObject("LOT-1", 5.0, "2026-12-31", "2026-06-12")
        ingredient.add_batch(batch)

        with self.assertRaises(InsufficientStockError):
            ingredient.consume_quantity(5.1)
        
        # Stock levels must remain unchanged
        self.assertEqual(ingredient.get_total_quantity(), 5.0)
        self.assertEqual(len(ingredient.batches), 1)

        # Assert custom error is subclass of ValueError
        try:
            ingredient.consume_quantity(6.0)
        except InsufficientStockError as e:
            self.assertTrue(isinstance(e, ValueError))

    def test_consume_invalid_quantity_raises_error(self):
        """Should raise ValueError for non-positive or non-numeric consumption values."""
        ingredient = IngredientEntity("ING-001", "Sugar", 5.0)
        batch = BatchValueObject("LOT-1", 5.0, "2026-12-31", "2026-06-12")
        ingredient.add_batch(batch)

        with self.assertRaises(ValueError):
            ingredient.consume_quantity(0.0)

        with self.assertRaises(ValueError):
            ingredient.consume_quantity(-1.5)

        with self.assertRaises(TypeError):
            ingredient.consume_quantity("not-a-number")  # type: ignore

if __name__ == "__main__":
    unittest.main()
