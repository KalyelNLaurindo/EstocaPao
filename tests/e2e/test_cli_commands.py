import unittest
import os
import tempfile
import subprocess
import json
import sys

class TestCLIE2E(unittest.TestCase):
    """End-to-End integration tests for the EstocaPão CLI commands."""

    def setUp(self):
        # Create a temporary directory to isolate config.ini and database files
        self.temp_dir = tempfile.TemporaryDirectory()
        self.cwd = self.temp_dir.name

        # Locate root directory and setup PYTHONPATH
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
        self.src_dir = os.path.join(root_dir, "src")
        self.main_py = os.path.join(self.src_dir, "main.py")

        self.env = os.environ.copy()
        self.env["PYTHONPATH"] = self.src_dir
        if sys.platform == "win32":
            user_scripts = os.path.join(
                os.environ.get("APPDATA", ""),
                "Python",
                f"Python{sys.version_info.major}{sys.version_info.minor}",
                "Scripts"
            )
            if os.path.exists(user_scripts):
                self.env["PATH"] = user_scripts + os.pathsep + self.env.get("PATH", "")

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_cmd(self, args: list) -> subprocess.CompletedProcess:
        """Helper to run the CLI main script with arguments."""
        cmd = [sys.executable, self.main_py] + args
        return subprocess.run(
            cmd,
            cwd=self.cwd,
            env=self.env,
            capture_output=True,
            text=True
        )

    def test_scenario_1_init_command(self):
        """Scenario 1: Verify that the --init command bootstraps configurations and files successfully."""
        res = self.run_cmd(["--init"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("Inicializado", res.stdout)

        # Check that files were created
        self.assertTrue(os.path.exists(os.path.join(self.cwd, "config.ini")))
        self.assertTrue(os.path.exists(os.path.join(self.cwd, "db_backup.json")))

    def test_scenario_2_add_and_status(self):
        """Scenario 2: Verify adding a new ingredient lot and checking status."""
        # Initialize first
        self.run_cmd(["--init"])

        # Add flour
        res = self.run_cmd(["add", "flour", "25.5", "--exp", "2026-12-31", "--limit", "15.0"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("adicionado com sucesso", res.stdout.lower() or res.stderr.lower())

        # Check status
        res_status = self.run_cmd(["status"])
        self.assertEqual(res_status.returncode, 0)
        self.assertIn("flour", res_status.stdout.lower())
        self.assertIn("25.5", res_status.stdout)
        self.assertIn("15.0", res_status.stdout)
        self.assertIn("ok", res_status.stdout.lower())

    def test_scenario_3_update_stock_consume_and_add(self):
        """Scenario 3: Verify consuming stock (negative update) and adding stock (positive update)."""
        self.run_cmd(["--init"])
        self.run_cmd(["add", "flour", "25.5", "--exp", "2026-12-31", "--limit", "15.0"])

        # Consume 5.5 units
        res = self.run_cmd(["update", "flour", "-5.5"])
        self.assertEqual(res.returncode, 0)
        self.assertIn("atualizado com sucesso", res.stdout.lower() or res.stderr.lower())

        # Check status shows 20.0
        res_status = self.run_cmd(["status"])
        self.assertIn("20.0", res_status.stdout)

        # Add 10.0 units with exp date
        res = self.run_cmd(["update", "flour", "10.0", "--exp", "2026-08-15"])
        self.assertEqual(res.returncode, 0)

        # Check status shows 30.0
        res_status = self.run_cmd(["status"])
        self.assertIn("30.0", res_status.stdout)

    def test_scenario_4_discard_quarantined_batch(self):
        """Scenario 4: Verify placing a batch in quarantine and discarding it."""
        self.run_cmd(["--init"])
        # Add a batch with an expiration date in the past and received date earlier
        self.run_cmd(["add", "flour", "5.0", "--exp", "2026-02-01", "--received", "2026-01-01", "--limit", "15.0"])

        # Trigger status to run quarantine isolation logic
        self.run_cmd(["status"])

        # Find the batch ID in the db_backup.json file
        db_file = os.path.join(self.cwd, "db_backup.json")
        with open(db_file, "r", encoding="utf-8") as f:
            db_data = json.load(f)
        
        quarantine_batches = db_data["flour"]["quarantine_batches"]
        self.assertEqual(len(quarantine_batches), 1)
        batch_id = quarantine_batches[0]["batch_id"]

        # Run discard command on the batch ID
        res = self.run_cmd(["discard", batch_id])
        self.assertEqual(res.returncode, 0)
        self.assertIn("descartado com sucesso", res.stdout.lower() or res.stderr.lower())

        # Verify that it is removed from the database
        with open(db_file, "r", encoding="utf-8") as f:
            db_data_after = json.load(f)
        self.assertEqual(len(db_data_after["flour"]["quarantine_batches"]), 0)

    def test_scenario_5_friendly_errors_on_invalid_inputs(self):
        """Scenario 5: Verify that friendly error messages are printed and exit code is non-zero on failure."""
        self.run_cmd(["--init"])

        # Invalid quantity type
        res1 = self.run_cmd(["add", "flour", "abc", "--exp", "2026-12-31", "--limit", "15.0"])
        self.assertNotEqual(res1.returncode, 0)
        self.assertNotIn("traceback", res1.stdout.lower() + res1.stderr.lower())

        # Invalid date format
        res2 = self.run_cmd(["add", "flour", "10.0", "--exp", "31-12-2026", "--limit", "15.0"])
        self.assertNotEqual(res2.returncode, 0)
        self.assertNotIn("traceback", res2.stdout.lower() + res2.stderr.lower())

        # Update non-existent ingredient
        res3 = self.run_cmd(["update", "yeast", "-5.0"])
        self.assertNotEqual(res3.returncode, 0)
        self.assertIn("yeast", res3.stdout.lower() + res3.stderr.lower())
        self.assertNotIn("traceback", res3.stdout.lower() + res3.stderr.lower())

        # Consume more than available stock
        self.run_cmd(["add", "yeast", "2.0", "--exp", "2026-12-31", "--limit", "1.0"])
        res4 = self.run_cmd(["update", "yeast", "-10.0"])
        self.assertNotEqual(res4.returncode, 0)
        self.assertIn("insuficiente", res4.stdout.lower() + res4.stderr.lower())
        self.assertNotIn("traceback", res4.stdout.lower() + res4.stderr.lower())

    def test_scenario_6_global_executable_command(self):
        """Scenario 6: Verify that the global 'estocapao' command executes successfully or skips if not installed."""
        cmd_name = "estocapao.exe" if sys.platform == "win32" else "estocapao"
        
        user_scripts = ""
        if sys.platform == "win32":
            user_scripts = os.path.join(
                os.environ.get("APPDATA", ""),
                "Python",
                f"Python{sys.version_info.major}{sys.version_info.minor}",
                "Scripts"
            )
        else:
            import shutil
            bin_path = shutil.which(cmd_name)
            if bin_path:
                user_scripts = os.path.dirname(bin_path)

        executable_path = os.path.join(user_scripts, cmd_name) if user_scripts else cmd_name
        
        if not os.path.exists(executable_path):
            import shutil
            bin_path = shutil.which(cmd_name)
            if bin_path:
                executable_path = bin_path
            else:
                self.skipTest("Global 'estocapao' command not found in PATH. Please run 'pip install -e .' first.")

        res = subprocess.run(
            [executable_path, "--init"],
            cwd=self.cwd,
            env=self.env,
            capture_output=True,
            text=True
        )
        self.assertEqual(res.returncode, 0)
        self.assertIn("Inicializado", res.stdout)

if __name__ == "__main__":
    unittest.main()
