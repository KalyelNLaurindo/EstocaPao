"""This module reads commands typed by the user in the terminal and runs the matching actions in our application."""
import argparse
import sys
import os
import time
from datetime import date
from typing import List

from estocapao.bootstrap.initializer import initialize_dependencies
from estocapao.modules.inventory.infra.repo import LocalJsonRepositoryAdapter
from estocapao.modules.inventory.app.usecase import UpdateStockUseCase, GetInventoryStatusUseCase
from estocapao.modules.inventory.app.quarantine import QuarantineManager
from estocapao.modules.inventory.domain.entity import IngredientEntity, InsufficientStockError
from estocapao.modules.inventory.domain.value import DomainValidationError, InvalidQuantityError, InvalidDateError
from estocapao.shared.logger import log_action


class CommandLineInterfaceParser:
    """Reads typed terminal commands and turns them into actions our application can execute."""

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="EstocaPão — High-Performance In-Memory Local CLI Inventory Engine"
        )
        self._setup_arguments()

    def _setup_arguments(self) -> None:
        """Sets up the sub-options and flags (like 'add flour' or 'check status') that a user can type."""
        # Top-level flags
        self.parser.add_argument(
            "--init",
            action="store_true",
            help="Bootstraps configuration files, logs, and initial JSON databases."
        )

        subparsers = self.parser.add_subparsers(dest="subcommand", help="Available subcommands")

        # add command
        parser_add = subparsers.add_parser("add", help="Registers a new ingredient lot.")
        parser_add.add_argument("name", type=str, help="Name of the ingredient.")
        parser_add.add_argument("qty", type=float, help="Quantity of the ingredient.")
        parser_add.add_argument("--exp", type=str, required=True, help="Expiration date (YYYY-MM-DD).")
        parser_add.add_argument("--limit", type=float, required=True, help="Low stock safety limit.")
        parser_add.add_argument("--received", type=str, default=None, help="Received date (YYYY-MM-DD).")

        # update command
        parser_update = subparsers.add_parser("update", help="Increments or decrements active stock levels.")
        parser_update.add_argument("id", type=str, help="Ingredient ID.")
        parser_update.add_argument("qty", type=float, help="Quantity to update (negative to consume).")
        parser_update.add_argument("--exp", type=str, default=None, help="Expiration date (YYYY-MM-DD) for additions.")
        parser_update.add_argument("--received", type=str, default=None, help="Received date (YYYY-MM-DD) for additions.")

        # status command
        subparsers.add_parser("status", help="Renders active stock levels and warnings.")

        # discard command
        parser_discard = subparsers.add_parser("discard", help="Removes a batch from quarantine.")
        parser_discard.add_argument("batch_id", type=str, help="The ID of the batch to discard.")

    def parse_and_execute(self, args: List[str] = None) -> None:
        """Processes the input arguments from the terminal and triggers the requested feature."""
        if args is None:
            args = sys.argv[1:]

        parsed_args = self.parser.parse_args(args)

        # Scenario 1: Initialise
        if getattr(parsed_args, "init", False):
            try:
                initialize_dependencies()
                # Ensure db_backup.json is physically initialized if missing
                if not os.path.exists("db_backup.json"):
                    with open("db_backup.json", "w", encoding="utf-8") as f:
                        f.write("{}")
                print("Sistema Inicializado com sucesso.")
                return
            except Exception as e:
                print(f"Erro ao inicializar o sistema: {e}", file=sys.stderr)
                sys.exit(1)

        # For other commands, we must ensure dependencies are initialised
        try:
            _ = initialize_dependencies()
        except Exception as e:
            print(f"Erro ao inicializar dependências: {e}", file=sys.stderr)
            sys.exit(1)

        # Create repo and use cases
        repo = LocalJsonRepositoryAdapter("db_backup.json")
        quarantine_mgr = QuarantineManager(repo)
        update_usecase = UpdateStockUseCase(repo)
        status_usecase = GetInventoryStatusUseCase(repo, quarantine_mgr)

        if not hasattr(parsed_args, "subcommand") or parsed_args.subcommand is None:
            self.parser.print_help()
            sys.exit(0)

        try:
            if parsed_args.subcommand == "add":
                name = parsed_args.name.strip()
                qty = parsed_args.qty
                limit = parsed_args.limit
                exp_str = parsed_args.exp.strip()
                received_str = parsed_args.received

                if qty <= 0:
                    raise ValueError("A quantidade deve ser maior que zero ao adicionar estoque.")
                if limit < 0:
                    raise ValueError("O limite mínimo de segurança não pode ser negativo.")

                try:
                    exp_date = date.fromisoformat(exp_str)
                except ValueError:
                    raise ValueError("Data de validade deve seguir o formato YYYY-MM-DD.")

                received_date = None
                if received_str:
                    try:
                        received_date = date.fromisoformat(received_str.strip())
                    except ValueError:
                        raise ValueError("Data de recebimento deve seguir o formato YYYY-MM-DD.")

                ingredient_id = name.lower()
                ingredient = repo.find_by_id(ingredient_id)
                if not ingredient:
                    ingredient = IngredientEntity(ingredient_id, name.capitalize(), limit)
                    repo.save(ingredient)

                batch_id = f"LOT-{int(time.time() * 1000)}"

                update_usecase.execute(
                    ingredient_id=ingredient_id,
                    quantity=qty,
                    batch_id=batch_id,
                    expiration_date=exp_date,
                    received_date=received_date
                )
                print(f"Ingrediente '{name}' adicionado com sucesso no lote {batch_id}.")
                log_action("INFO", f"Ingrediente '{name}' adicionado com sucesso no lote {batch_id}.")

            elif parsed_args.subcommand == "update":
                ing_id = parsed_args.id.strip().lower()
                qty = parsed_args.qty
                exp_str = parsed_args.exp
                received_str = parsed_args.received

                if qty == 0.0:
                    raise ValueError("A quantidade de atualização não pode ser zero.")

                ingredient = repo.find_by_id(ing_id)
                if not ingredient:
                    raise ValueError(f"Ingrediente com ID '{ing_id}' não encontrado.")

                if qty > 0.0:
                    if not exp_str:
                        raise ValueError("Data de validade (--exp) é obrigatória ao adicionar estoque.")

                    try:
                        exp_date = date.fromisoformat(exp_str.strip())
                    except ValueError:
                        raise ValueError("Data de validade deve seguir o formato YYYY-MM-DD.")

                    received_date = None
                    if received_str:
                        try:
                            received_date = date.fromisoformat(received_str.strip())
                        except ValueError:
                            raise ValueError("Data de recebimento deve seguir o formato YYYY-MM-DD.")

                    batch_id = f"LOT-{int(time.time() * 1000)}"
                    update_usecase.execute(
                        ingredient_id=ing_id,
                        quantity=qty,
                        batch_id=batch_id,
                        expiration_date=exp_date,
                        received_date=received_date
                    )
                    print(f"Estoque atualizado com sucesso. Adicionado lote {batch_id}.")
                    log_action("INFO", f"Estoque de '{ing_id}' atualizado com sucesso. Adicionado lote {batch_id}.")
                else:
                    update_usecase.execute(
                        ingredient_id=ing_id,
                        quantity=qty
                    )
                    print(f"Estoque atualizado com sucesso. Consumido {abs(qty)} unidades.")
                    log_action("INFO", f"Estoque de '{ing_id}' atualizado com sucesso. Consumido {abs(qty)} unidades.")

            elif parsed_args.subcommand == "status":
                report = status_usecase.execute()
                if not report:
                    print("Nenhum ingrediente cadastrado no estoque.")
                    return

                print(f"{'ID':<10} | {'Nome':<25} | {'Quantidade':<12} | {'Limite Mín':<10} | {'Status':<10}")
                print("-" * 72)
                for details in report.values():
                    print(f"{details['id']:<10} | {details['name']:<25} | {details['total_quantity']:<12.1f} | {details['safety_threshold']:<10.1f} | {details['status']:<10}")

            elif parsed_args.subcommand == "discard":
                batch_id = parsed_args.batch_id.strip()
                quarantine_mgr.discard_quarantined_batch(batch_id)
                print(f"Lote {batch_id} descartado com sucesso.")
                log_action("INFO", f"Lote {batch_id} descartado da quarentena com sucesso.")

        except InsufficientStockError:
            print("Erro: Estoque insuficiente.", file=sys.stderr)
            sys.exit(1)
        except DomainValidationError as e:
            print(f"Erro de validação: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Erro: {e}", file=sys.stderr)
            sys.exit(1)


def main():
    """Starts the command line application by reading arguments from the system terminal."""
    cli = CommandLineInterfaceParser()
    cli.parse_and_execute(sys.argv[1:])
