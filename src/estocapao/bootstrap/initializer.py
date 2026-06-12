"""This module sets up and links different parts of the application together when it starts up.
It connects our core business logic to the actual components that handle files or terminal commands.
"""
import os
import configparser

DEFAULT_CONFIG_CONTENT = """[system_defaults]
alert_color_enabled = true
automatic_backup_generations = 5
passcode_sha256_hash = e99a18c428cb38d5f260853678922e03f88ef685652e00845a72233f520b2241

[alerts_threshold]
expiration_alert_days_window = 3
low_stock_default_kg_limit = 5.0
"""


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


def initialize_dependencies(config_path: str = "config.ini") -> SystemConfig:
    """Prepares and connects all system modules so the application is ready to run."""
    return load_config(config_path)
