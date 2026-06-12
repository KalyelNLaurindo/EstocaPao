"""This is the main entry point to start the EstocaPão application.
It launches the Command Line Interface (CLI) so users can interact with the system.
"""
from estocapao.modules.inventory.infra.cli import main

if __name__ == "__main__":
    main()
