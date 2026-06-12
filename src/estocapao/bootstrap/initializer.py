"""This module sets up and links different parts of the application together when it starts up.
It connects our core business logic to the actual components that handle files or terminal commands.
"""
import os
import stat
import json
import configparser
from estocapao.shared.logger import log_action

DEFAULT_CONFIG_CONTENT = """[system_defaults]
alert_color_enabled = true
automatic_backup_generations = 5
passcode_sha256_hash = e99a18c428cb38d5f260853678922e03f88ef685652e00845a72233f520b2241

[alerts_threshold]
expiration_alert_days_window = 3
low_stock_default_kg_limit = 5.0
"""


class InvalidSchemaError(ValueError):
    """Raised when the database JSON file structure is malformed or invalid."""
    pass


class SystemConfig:
    """Object holding the configuration settings for the system."""

    def __init__(
        self,
        alert_color_enabled: bool = True,
        automatic_backup_generations: int = 5,
        passcode_sha256_hash: str = "e99a18c428cb38d5f260853678922e03f88ef685652e00845a72233f520b2241",
        expiration_alert_days_window: int = 3,
        low_stock_default_kg_limit: float = 5.0
    ):
        self.alert_color_enabled = alert_color_enabled
        self.automatic_backup_generations = automatic_backup_generations
        self.passcode_sha256_hash = passcode_sha256_hash
        self.expiration_alert_days_window = expiration_alert_days_window
        self.low_stock_default_kg_limit = low_stock_default_kg_limit


def secure_file_permissions(file_path: str) -> None:
    """Applies restrictive permissions (chmod 600 / owner read-write only) on POSIX environments."""
    if os.name == "posix":
        try:
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR)
        except Exception:
            pass  # Clean fallback if permissions cannot be set


def validate_database_schema(db_path: str) -> None:
    """Validates the structural integrity of the database JSON file.
    Raises InvalidSchemaError if the schema is malformed or missing mandatory fields.
    """
    if not os.path.exists(db_path):
        return  # Missing file is fine, it will be created empty

    try:
        with open(db_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        
        # Empty file is malformed (should be at least {} if initialized, or non-empty if it exists)
        if not content:
            raise InvalidSchemaError("Database file is empty.")
            
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise InvalidSchemaError(f"Database contains malformed JSON: {e}") from e
    except InvalidSchemaError:
        raise
    except Exception as e:
        raise InvalidSchemaError(f"Failed to read database file: {e}") from e

    if not isinstance(data, dict):
        raise InvalidSchemaError("Database root must be a JSON object (dict).")

    for ing_id, ing in data.items():
        if not isinstance(ing, dict):
            raise InvalidSchemaError(f"Ingredient '{ing_id}' must be a JSON object (dict).")
        
        for key in ("id", "name", "safety_threshold", "batches"):
            if key not in ing:
                raise InvalidSchemaError(f"Ingredient '{ing_id}' is missing mandatory key: '{key}'.")
        
        if not isinstance(ing["id"], str):
            raise InvalidSchemaError(f"Ingredient '{ing_id}' id must be a string.")
        if not isinstance(ing["name"], str):
            raise InvalidSchemaError(f"Ingredient '{ing_id}' name must be a string.")
        if not isinstance(ing["safety_threshold"], (int, float)):
            raise InvalidSchemaError(f"Ingredient '{ing_id}' safety_threshold must be a number.")
        if not isinstance(ing["batches"], list):
            raise InvalidSchemaError(f"Ingredient '{ing_id}' batches must be a list (array).")

        # Validate batches structure
        for i, batch in enumerate(ing["batches"]):
            if not isinstance(batch, dict):
                raise InvalidSchemaError(f"Batch {i} in ingredient '{ing_id}' must be a JSON object (dict).")
            for bkey in ("batch_id", "quantity", "expiration_date", "received_date"):
                if bkey not in batch:
                    raise InvalidSchemaError(f"Batch {i} in ingredient '{ing_id}' is missing key: '{bkey}'.")

        # Validate quarantine_batches if present
        if "quarantine_batches" in ing:
            if not isinstance(ing["quarantine_batches"], list):
                raise InvalidSchemaError(f"Ingredient '{ing_id}' quarantine_batches must be a list (array).")
            for i, batch in enumerate(ing["quarantine_batches"]):
                if not isinstance(batch, dict):
                    raise InvalidSchemaError(f"Quarantined batch {i} in ingredient '{ing_id}' must be a JSON object (dict).")
                for bkey in ("batch_id", "quantity", "expiration_date", "received_date"):
                    if bkey not in batch:
                        raise InvalidSchemaError(f"Quarantined batch {i} in ingredient '{ing_id}' is missing key: '{bkey}'.")


def load_config(config_path: str = "config.ini") -> SystemConfig:
    """Loads system configuration settings from the ini file. Auto-heals if missing or malformed."""
    config = configparser.ConfigParser()

    # Auto-heal: If file does not exist, create it with defaults
    if not os.path.exists(config_path):
        dir_name = os.path.dirname(config_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                f.write(DEFAULT_CONFIG_CONTENT)
            secure_file_permissions(config_path)
        except Exception:
            # If writing fails, return standard default configuration object
            return SystemConfig()

    try:
        config.read(config_path, encoding="utf-8")

        # Parse defaults with fallbacks
        alert_color = True
        if config.has_option("system_defaults", "alert_color_enabled"):
            try:
                alert_color = config.getboolean("system_defaults", "alert_color_enabled")
            except ValueError:
                pass

        backup_gens = 5
        if config.has_option("system_defaults", "automatic_backup_generations"):
            try:
                backup_gens = config.getint("system_defaults", "automatic_backup_generations")
            except ValueError:
                pass

        passcode_hash = config.get(
            "system_defaults",
            "passcode_sha256_hash",
            fallback="e99a18c428cb38d5f260853678922e03f88ef685652e00845a72233f520b2241"
        )

        exp_window = 3
        if config.has_option("alerts_threshold", "expiration_alert_days_window"):
            try:
                exp_window = config.getint("alerts_threshold", "expiration_alert_days_window")
            except ValueError:
                pass

        low_stock_limit = 5.0
        if config.has_option("alerts_threshold", "low_stock_default_kg_limit"):
            try:
                low_stock_limit = config.getfloat("alerts_threshold", "low_stock_default_kg_limit")
            except ValueError:
                pass

        return SystemConfig(
            alert_color_enabled=alert_color,
            automatic_backup_generations=backup_gens,
            passcode_sha256_hash=passcode_hash,
            expiration_alert_days_window=exp_window,
            low_stock_default_kg_limit=low_stock_limit
        )

    except Exception:
        # If parsing completely fails, return safe defaults
        return SystemConfig()


def initialize_dependencies(config_path: str = "config.ini", db_path: str = "db_backup.json") -> SystemConfig:
    """Prepares and connects all system modules so the application is ready to run."""
    config = load_config(config_path)
    secure_file_permissions(config_path)

    # Guarantee the database file exists with a minimal valid structure.
    # NOTE: Schema validation and self-healing recovery are the sole responsibility
    # of LocalJsonRepositoryAdapter._load_from_disk(). Performing it here as well
    # causes the .bak file to be consumed before the repo adapter can use it,
    # triggering a spurious double-recovery cycle logged on every invocation.
    if db_path and not os.path.exists(db_path):
        try:
            dir_name = os.path.dirname(db_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
            with open(db_path, "w", encoding="utf-8") as f:
                f.write("{}")
            log_action("INFO", f"Arquivo de banco de dados criado em: {db_path}")
        except Exception as e:
            log_action("CRITICAL", f"Falha ao criar arquivo de banco de dados inicial: {e}")

    if db_path and os.path.exists(db_path):
        secure_file_permissions(db_path)

    return config
