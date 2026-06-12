import unittest
import os
import tempfile
from estocapao.bootstrap.initializer import load_config, SystemConfig, DEFAULT_CONFIG_CONTENT

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

if __name__ == "__main__":
    unittest.main()
