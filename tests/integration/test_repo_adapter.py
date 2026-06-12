import unittest
import os
import tempfile
from estocapao.modules.inventory.domain.entity import IngredientEntity
from estocapao.modules.inventory.domain.value import BatchValueObject
from estocapao.modules.inventory.infra.repo import LocalJsonRepositoryAdapter

class TestLocalJsonRepositoryAdapter(unittest.TestCase):
    """Integration tests for the LocalJsonRepositoryAdapter storage port implementation."""

    def setUp(self):
        # Create a temp directory for DB file isolation
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, "db_backup.json")
        self.bak_path = self.db_path + ".bak"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_load_success(self):
        """Should successfully serialize, save, and reload ingredient and batch states from disk."""
        repo = LocalJsonRepositoryAdapter(self.db_path)

        # 1. Create a dummy ingredient with batches
        flour = IngredientEntity("FL-001", "Wheat Flour", 10.0)
        batch_valid = BatchValueObject("LOT-V", 15.0, "2026-12-31", "2026-06-12")
        batch_quarantined = BatchValueObject("LOT-Q", 5.0, "2026-06-10", "2026-06-08")
        flour.add_batch(batch_valid)
        flour.add_quarantine_batch(batch_quarantined)

        # 2. Save using the repo
        repo.save(flour)

        # File should exist
        self.assertTrue(os.path.exists(self.db_path))

        # 3. Create a second repo instance to reload state from disk
        repo_reload = LocalJsonRepositoryAdapter(self.db_path)
        loaded_flour = repo_reload.find_by_id("FL-001")

        self.assertIsNotNone(loaded_flour)
        self.assertEqual(loaded_flour.id, "FL-001") # type: ignore
        self.assertEqual(loaded_flour.name, "Wheat Flour") # type: ignore
        self.assertEqual(loaded_flour.safety_threshold, 10.0) # type: ignore
        
        # Verify batches
        self.assertEqual(len(loaded_flour.batches), 1) # type: ignore
        self.assertEqual(loaded_flour.batches[0].batch_id, "LOT-V") # type: ignore
        self.assertEqual(loaded_flour.batches[0].quantity, 15.0) # type: ignore

        # Verify quarantined batches
        self.assertEqual(len(loaded_flour.quarantine_batches), 1) # type: ignore
        self.assertEqual(loaded_flour.quarantine_batches[0].batch_id, "LOT-Q") # type: ignore
        self.assertEqual(loaded_flour.quarantine_batches[0].quantity, 5.0) # type: ignore

    def test_atomic_write_creates_backup(self):
        """Should verify that the previous database state is preserved in a .bak file upon saving new changes."""
        repo = IngredientEntity("FL-001", "Wheat Flour", 10.0)
        repo.add_batch(BatchValueObject("LOT-1", 10.0, "2026-12-31", "2026-06-12"))

        # Save State A
        adapter = LocalJsonRepositoryAdapter(self.db_path)
        adapter.save(repo)

        # State A should exist in active JSON, no bak file yet since it's the first save
        self.assertTrue(os.path.exists(self.db_path))
        self.assertFalse(os.path.exists(self.bak_path))

        # Modify ingredient to State B
        repo.add_batch(BatchValueObject("LOT-2", 5.0, "2026-12-31", "2026-06-12"))

        # Save State B
        adapter.save(repo)

        # Active JSON should now reflect State B (total 15.0)
        self.assertTrue(os.path.exists(self.db_path))
        adapter_b = LocalJsonRepositoryAdapter(self.db_path)
        loaded_b = adapter_b.find_by_id("FL-001")
        self.assertEqual(loaded_b.get_total_quantity(), 15.0) # type: ignore

        # Backup file .bak should exist and reflect State A (total 10.0)
        self.assertTrue(os.path.exists(self.bak_path))
        adapter_bak = LocalJsonRepositoryAdapter(self.bak_path)
        loaded_bak = adapter_bak.find_by_id("FL-001")
        self.assertEqual(loaded_bak.get_total_quantity(), 10.0) # type: ignore

    def test_atomic_write_failure_resilience(self):
        """Should guarantee that a writing failure during serialization preserves the target active database intact."""
        flour = IngredientEntity("FL-001", "Wheat Flour", 10.0)
        flour.add_batch(BatchValueObject("LOT-1", 10.0, "2026-12-31", "2026-06-12"))

        adapter = LocalJsonRepositoryAdapter(self.db_path)
        adapter.save(flour)

        # Get initial file contents
        with open(self.db_path, "r", encoding="utf-8") as f:
            initial_content = f.read()

        # Try to save an invalid state or simulate failure by patching JSON serialization
        # e.g. an object that cannot be serialized (like a set or lambda)
        class UnserializableClass:
            pass
        
        # Add an unserializable object to force json.dump to raise a TypeError
        flour.id = UnserializableClass() # type: ignore

        # Attempt to save should raise TypeError
        with self.assertRaises(TypeError):
            adapter.save(flour)

        # Verify that the active db_backup.json remains uncorrupted and equal to initial content
        with open(self.db_path, "r", encoding="utf-8") as f:
            current_content = f.read()

        self.assertEqual(current_content, initial_content)

        # Verify no orphaned tmp file exists
        tmp_path = self.db_path + ".tmp"
        self.assertFalse(os.path.exists(tmp_path))

if __name__ == "__main__":
    unittest.main()
