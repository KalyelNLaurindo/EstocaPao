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

    def test_scenario_4_recovery_from_bak(self):
        """Scenario 4: Recovery from .bak when main json is corrupted."""
        valid_data = {
            "FL-001": {
                "id": "FL-001",
                "name": "Wheat Flour",
                "safety_threshold": 10.0,
                "batches": [
                    {
                        "batch_id": "LOT-1",
                        "quantity": 10.0,
                        "expiration_date": "2026-12-31",
                        "received_date": "2026-06-12"
                    }
                ],
                "quarantine_batches": []
            }
        }
        import json
        with open(self.bak_path, "w", encoding="utf-8") as f:
            json.dump(valid_data, f)
        
        # Corrupted data in main db file
        with open(self.db_path, "w", encoding="utf-8") as f:
            f.write("corrupted JSON data {")
            
        # Instantiate repo
        repo = LocalJsonRepositoryAdapter(self.db_path)
        
        # Assert database loaded from .bak
        flour = repo.find_by_id("FL-001")
        self.assertIsNotNone(flour)
        self.assertEqual(flour.name, "Wheat Flour") # type: ignore
        self.assertEqual(flour.get_total_quantity(), 10.0) # type: ignore
        
        # Main db file should be restored and valid now
        self.assertTrue(os.path.exists(self.db_path))
        with open(self.db_path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        self.assertIn("FL-001", loaded_data)
        
        # The bak file should have been moved/replaced
        self.assertFalse(os.path.exists(self.bak_path))

    def test_scenario_5_recovery_to_empty(self):
        """Scenario 5: Full recovery to empty database when both main and .bak are corrupted."""
        # Corrupted data in both files
        with open(self.db_path, "w", encoding="utf-8") as f:
            f.write("{corrupt main}")
        with open(self.bak_path, "w", encoding="utf-8") as f:
            f.write("{corrupt backup}")
            
        # Instantiate repo (should not raise exception)
        repo = LocalJsonRepositoryAdapter(self.db_path)
        
        # Should initialize empty cache
        self.assertEqual(len(repo.get_all()), 0)
        
        # Main file should be an empty dictionary
        self.assertTrue(os.path.exists(self.db_path))
        with open(self.db_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        self.assertEqual(content, "{}")

    def test_scenario_6_recovery_logs_auditing(self):
        """Scenario 6: Verify audit logs are appended to estocapao.log during recovery actions."""
        log_file = "estocapao.log"
        initial_lines = 0
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                initial_lines = len(f.readlines())
                
        # Trigger Scenario 4 Recovery
        import json
        with open(self.bak_path, "w", encoding="utf-8") as f:
            json.dump({}, f)
        with open(self.db_path, "w", encoding="utf-8") as f:
            f.write("corrupt db")
            
        _ = LocalJsonRepositoryAdapter(self.db_path)
        
        # Trigger Scenario 5 Recovery
        with open(self.bak_path, "w", encoding="utf-8") as f:
            f.write("corrupt bak")
        with open(self.db_path, "w", encoding="utf-8") as f:
            f.write("corrupt db")
            
        _ = LocalJsonRepositoryAdapter(self.db_path)
        
        self.assertTrue(os.path.exists(log_file))
        with open(log_file, "r", encoding="utf-8") as f:
            all_lines = f.readlines()
            
        new_lines = all_lines[initial_lines:]
        log_content = "".join(new_lines)
        
        self.assertIn("Banco de dados principal corrompido. Tentando restaurar a partir do backup.", log_content)
        self.assertIn("Banco de dados restaurado com sucesso a partir do backup.", log_content)
        self.assertIn("Banco de dados e backup corrompidos/ausentes. Inicializando banco de dados limpo.", log_content)

if __name__ == "__main__":
    unittest.main()
