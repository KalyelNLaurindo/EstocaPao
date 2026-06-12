"""This module writes history logs of actions (like adding stock or warnings) to a local text file called 'estocapao.log'."""
import datetime

def log_action(category: str, message: str) -> None:
    """Appends a time-stamped log message to our history file (estocapao.log) so we have a record of what happened."""
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    log_line = f"[{timestamp}] [{category}] {message}\n"
    try:
        with open("estocapao.log", "a", encoding="utf-8") as f:
            f.write(log_line)
    except OSError:
        # Silently ignore write failures so the main application does not crash
        pass
