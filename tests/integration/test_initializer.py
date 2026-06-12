import unittest
import os
import tempfile
from estocapao.bootstrap.initializer import (
    load_config,
    SystemConfig,
    DEFAULT_CONFIG_CONTENT,
    secure_file_permissions,
    validate_database_schema,
    InvalidSchemaError,
    initialize_dependencies
)

class TestInitializerIntegration(unittest.TestCase):
    """Integration tests for the system initializer configuration parser and auto-healing."""

    def setUp(self):
        # Create a temporary directory for config.ini isolation
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_path = os.path.join(self.temp_dir.name, "config.ini")

    def tearDown(self):
        # Clean up temporary directory
        self.temp_dir.cleanup()

    def test_load_config_file_exists_success(self):
        """Should read configuration correctly when a valid config.ini file is present."""
        custom_content = """[system_defaults]
alert_color_enabled = false
automatic_backup_generations = 3
passcode_sha256_hash = dummy_hash

[alerts_threshold]
expiration_alert_days_window = 5
low_stock_default_kg_limit = 10.0
"""
        with open(self.config_path, "w", encoding="utf-8") as f:
            f.write(custom_content)

        config = load_config(self.config_path)

        self.assertFalse(config.alert_color_enabled)
        self.assertEqual(config.automatic_backup_generations, 3)
        self.assertEqual(config.passcode_sha256_hash, "dummy_hash")
        self.assertEqual(config.expiration_alert_days_window, 5)
        self.assertEqual(config.low_stock_default_kg_limit, 10.0)

    def test_load_config_auto_heals_missing_file(self):
        """Should auto-heal by generating a default config.ini if the file is missing."""
        # Ensure file does not exist
        self.assertFalse(os.path.exists(self.config_path))

        config = load_config(self.config_path)

        # File should now exist
        self.assertTrue(os.path.exists(self.config_path))

        # File contents should match the default template
        with open(self.config_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, DEFAULT_CONFIG_CONTENT)

        # Loaded values should be the default values
        self.assertTrue(config.alert_color_enabled)
        self.assertEqual(config.automatic_backup_generations, 5)
        self.assertEqual(config.passcode_sha256_hash, "e99a18c428cb38d5f260853678922e03f88ef685652e00845a72233f520b2241")
        self.assertEqual(config.expiration_alert_days_window, 3)
        self.assertEqual(config.low_stock_default_kg_limit, 5.0)

    def test_load_config_malformed_file_fallback(self):
        """Should fallback to safe default configuration values if the file contains garbage/malformed data."""
        with open(self.config_path, "w", encoding="utf-8") as f:
            f.write("this is garbage config data [not ini format}\n")

        # Loading should not raise exceptions
        config = load_config(self.config_path)

        # Should fall back to standard defaults
        self.assertTrue(config.alert_color_enabled)
        self.assertEqual(config.automatic_backup_generations, 5)
        self.assertEqual(config.passcode_sha256_hash, "e99a18c428cb38d5f260853678922e03f88ef685652e00845a72233f520b2241")
        self.assertEqual(config.expiration_alert_days_window, 3)
        self.assertEqual(config.low_stock_default_kg_limit, 5.0)

    def test_load_config_missing_keys_fallback(self):
        """Should successfully parse declared keys and fallback to safe defaults for missing sections/keys."""
        partial_content = """[system_defaults]
alert_color_enabled = false
# missing automatic_backup_generations and passcode_sha256_hash

[alerts_threshold]
# missing expiration_alert_days_window
low_stock_default_kg_limit = 2.5
"""
        with open(self.config_path, "w", encoding="utf-8") as f:
            f.write(partial_content)

        config = load_config(self.config_path)

        # Parsed successfully
        self.assertFalse(config.alert_color_enabled)
        self.assertEqual(config.low_stock_default_kg_limit, 2.5)

        # Default fallbacks applied
        self.assertEqual(config.automatic_backup_generations, 5)
        self.assertEqual(config.passcode_sha256_hash, "e99a18c428cb38d5f260853678922e03f88ef685652e00845a72233f520b2241")
        self.assertEqual(config.expiration_alert_days_window, 3)

    def test_secure_file_permissions_posix(self):
        """Should restrict file permissions to 600 in POSIX environments."""
        # Create a dummy file
        dummy_file = os.path.join(self.temp_dir.name, "dummy.txt")
        with open(dummy_file, "w") as f:
            f.write("test")

        # Call permission securing
        secure_file_permissions(dummy_file)

        # On POSIX, check permissions.
        # On Windows, this is a clean fallback/noop.
        if os.name == "posix":
            import stat
            permissions = os.stat(dummy_file).st_mode
            self.assertEqual(permissions & 0o777, 0o600)

    def test_validate_database_schema_missing_file_success(self):
        """Should pass schema validation without error if the database file is missing."""
        missing_db_path = os.path.join(self.temp_dir.name, "missing_db.json")
        try:
            validate_database_schema(missing_db_path)
        except InvalidSchemaError:
            self.fail("validate_database_schema raised InvalidSchemaError for missing file.")

    def test_validate_database_schema_empty_file_raises_error(self):
        """Should raise InvalidSchemaError if the database file exists but is empty."""
        empty_db_path = os.path.join(self.temp_dir.name, "empty_db.json")
        with open(empty_db_path, "w", encoding="utf-8") as f:
            f.write("")

        with self.assertRaises(InvalidSchemaError):
            validate_database_schema(empty_db_path)

    def test_validate_database_schema_corrupted_json_raises_error(self):
        """Should raise InvalidSchemaError if the database file contains malformed JSON."""
        corrupt_db_path = os.path.join(self.temp_dir.name, "corrupt_db.json")
        with open(corrupt_db_path, "w", encoding="utf-8") as f:
            f.write("invalid json data here {")

        with self.assertRaises(InvalidSchemaError):
            validate_database_schema(corrupt_db_path)

    def test_validate_database_schema_missing_keys_raises_error(self):
        """Should raise InvalidSchemaError if mandatory ingredient keys are missing."""
        bad_db_path = os.path.join(self.temp_dir.name, "bad_db.json")
        # Missing 'batches' key
        bad_content = """{
            "FL-001": {
                "id": "FL-001",
                "name": "Flour",
                "safety_threshold": 10.0
            }
        }"""
        with open(bad_db_path, "w", encoding="utf-8") as f:
            f.write(bad_content)

        with self.assertRaises(InvalidSchemaError):
            validate_database_schema(bad_db_path)

    def test_validate_database_schema_valid_content_success(self):
        """Should pass schema validation without raising exceptions for valid structures."""
        valid_db_path = os.path.join(self.temp_dir.name, "valid_db.json")
        valid_content = """{
            "FL-001": {
                "id": "FL-001",
                "name": "Flour",
                "safety_threshold": 10.0,
                "batches": [
                    {
                        "batch_id": "LOT-1",
                        "quantity": 5.0,
                        "expiration_date": "2026-12-31",
                        "received_date": "2026-06-12"
                    }
                ],
                "quarantine_batches": []
            }
        }"""
        with open(valid_db_path, "w", encoding="utf-8") as f:
            f.write(valid_content)

        try:
            validate_database_schema(valid_db_path)
        except InvalidSchemaError:
            self.fail("validate_database_schema raised InvalidSchemaError for valid database contents.")

    def test_initialize_dependencies_recovers_from_bak(self):
        """Should restore database from backup during initializer bootstrapping if main db is corrupted."""
        db_path = os.path.join(self.temp_dir.name, "db_backup.json")
        bak_path = db_path + ".bak"
        
        valid_data = {
            "FL-001": {
                "id": "FL-001",
                "name": "Flour",
                "safety_threshold": 10.0,
                "batches": [],
                "quarantine_batches": []
            }
        }
        import json
        with open(bak_path, "w", encoding="utf-8") as f:
            json.dump(valid_data, f)
            
        with open(db_path, "w", encoding="utf-8") as f:
            f.write("{corrupt_json}")
            
        # Should initialize dependencies without raising exceptions and heal the main DB file
        initialize_dependencies(config_path=self.config_path, db_path=db_path)
        
        # Verify db_path is valid now and holds the restored data
        self.assertTrue(os.path.exists(db_path))
        try:
            validate_database_schema(db_path)
        except InvalidSchemaError:
            self.fail("initialize_dependencies did not successfully restore a valid schema to the main database file.")

    def test_initialize_dependencies_recovers_to_empty(self):
        """Should fall back to empty database during initializer bootstrapping if both main and backup are corrupted."""
        db_path = os.path.join(self.temp_dir.name, "db_backup.json")
        bak_path = db_path + ".bak"
        
        with open(db_path, "w", encoding="utf-8") as f:
            f.write("{corrupt_json_db}")
        with open(bak_path, "w", encoding="utf-8") as f:
            f.write("{corrupt_json_bak}")
            
        # Should initialize dependencies without raising exceptions and create an empty dict
        initialize_dependencies(config_path=self.config_path, db_path=db_path)
        
        # Verify db_path is now an empty valid json
        self.assertTrue(os.path.exists(db_path))
        with open(db_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        self.assertEqual(content, "{}")

if __name__ == "__main__":
    unittest.main()
