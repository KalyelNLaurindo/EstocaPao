"""Color codes used to style and paint text in the command line terminal (e.g., green for success, red for alerts)."""
import sys

RESET = "\033[0m"
BOLD = "\033[1m"

# UI Color Palette
CRITICAL_ALERT = "\033[91m"  # Bright Red
SUCCESS = "\033[92m"         # Vibrant Green
WARNING = "\033[93m"         # Yellow
INFO = "\033[96m"            # Soft Cyan


class TerminalAnsiFormatter:
    """Formatter to wrap text with ANSI escape codes for colored terminal displays."""

    def __init__(self, color_enabled: bool = True):
        # Color is enabled only if configured AND stdout is a TTY
        self.color_enabled = color_enabled and sys.stdout.isatty()

    def format(self, text: str, color_code: str) -> str:
        """Applies bold styling and color coding to text if formatting is enabled."""
        if self.color_enabled:
            return f"{BOLD}{color_code}{text}{RESET}"
        return text
