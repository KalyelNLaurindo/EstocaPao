"""This module handles saving and loading the inventory data directly to a local JSON file on the computer's hard drive."""
import os
import json
from typing import Dict, Optional
from estocapao.modules.inventory.domain.entity import IngredientEntity
from estocapao.modules.inventory.domain.ports import IInventoryRepository
from estocapao.modules.inventory.domain.value import BatchValueObject
from estocapao.bootstrap.initializer import secure_file_permissions, validate_database_schema, InvalidSchemaError
from estocapao.shared.logger import log_action


class LocalJsonRepositoryAdapter(IInventoryRepository):
    """Responsible for reading and writing our inventory state to a text file on the local computer."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._memory_cache: Dict[str, IngredientEntity] = {}  # Holds inventory data temporarily in memory for high speed
        self._load_from_disk()

    def _load_from_disk(self) -> None:
        """Loads repository state from the JSON file on disk, if it exists."""
        if not os.path.exists(self.db_path):
            return

        try:
            validate_database_schema(self.db_path)
        except InvalidSchemaError:
            log_action("WARNING", "Banco de dados principal corrompido. Tentando restaurar a partir do backup.")
            bak_path = self.db_path + ".bak"
            bak_valid = False
            if os.path.exists(bak_path):
                try:
                    validate_database_schema(bak_path)
                    bak_valid = True
                except InvalidSchemaError:
                    pass
            
            if bak_valid:
                try:
                    os.replace(bak_path, self.db_path)
                    log_action("INFO", "Banco de dados restaurado com sucesso a partir do backup.")
                except Exception:
                    bak_valid = False
            
            if not bak_valid:
                try:
                    with open(self.db_path, "w", encoding="utf-8") as f:
                        f.write("{}")
                    log_action("ERROR", "Banco de dados e backup corrompidos/ausentes. Inicializando banco de dados limpo.")
                except Exception:
                    pass

        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            for ing_id, ing_data in data.items():
                entity = IngredientEntity(
                    ingredient_id=ing_data["id"],
                    name=ing_data["name"],
                    safety_threshold=ing_data["safety_threshold"]
                )
                
                # Deserialise active batches
                for batch_dict in ing_data["batches"]:
                    entity.add_batch(BatchValueObject(
                        batch_id=batch_dict["batch_id"],
                        quantity=batch_dict["quantity"],
                        expiration_date=batch_dict["expiration_date"],
                        received_date=batch_dict["received_date"]
                    ))
                
                # Deserialise quarantined batches if present
                if "quarantine_batches" in ing_data:
                    for batch_dict in ing_data["quarantine_batches"]:
                        entity.add_quarantine_batch(BatchValueObject(
                            batch_id=batch_dict["batch_id"],
                            quantity=batch_dict["quantity"],
                            expiration_date=batch_dict["expiration_date"],
                            received_date=batch_dict["received_date"]
                        ))
                
                self._memory_cache[ing_id] = entity
        except Exception as e:
            log_action("ERROR", f"Falha ao desserializar dados do banco de dados: {e}")

    def save(self, ingredient: IngredientEntity) -> None:
        """Saves the ingredient details to the JSON file safely, avoiding data loss if the computer crashes."""
        # 1. Update in-memory cache
        self._memory_cache[ingredient.id] = ingredient

        # 2. Serialize all entities to dict
        serialized_data = {}
        for ing_id, ing in self._memory_cache.items():
            serialized_data[ing_id] = {
                "id": ing.id,
                "name": ing.name,
                "safety_threshold": ing.safety_threshold,
                "batches": [
                    {
                        "batch_id": b.batch_id,
                        "quantity": b.quantity,
                        "expiration_date": b.expiration_date.isoformat(),
                        "received_date": b.received_date.isoformat()
                    } for b in ing.batches
                ],
                "quarantine_batches": [
                    {
                        "batch_id": b.batch_id,
                        "quantity": b.quantity,
                        "expiration_date": b.expiration_date.isoformat(),
                        "received_date": b.received_date.isoformat()
                    } for b in ing.quarantine_batches
                ]
            }

        # 3. Write atomically
        tmp_path = self.db_path + ".tmp"
        
        # Write to tmp file first
        try:
            # Create directories if needed
            dir_name = os.path.dirname(self.db_path)
            if dir_name:
                os.makedirs(dir_name, exist_ok=True)
                
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(serialized_data, f, indent=4)
            
            # Secure permissions on tmp file
            secure_file_permissions(tmp_path)
            
            # If the current file exists, rename it to .bak for safety backup
            if os.path.exists(self.db_path):
                bak_path = self.db_path + ".bak"
                os.replace(self.db_path, bak_path)
            
            # Swap tmp to final db_path
            os.replace(tmp_path, self.db_path)
        except Exception:
            # Clean up tmp file if it was created
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
            raise

    def find_by_id(self, ingredient_id: str) -> Optional[IngredientEntity]:
        """Searches the fast in-memory inventory list for an ingredient matching the given ID."""
        return self._memory_cache.get(ingredient_id)

    def get_all(self) -> Dict[str, IngredientEntity]:
        """Returns the entire list of ingredients we currently have loaded in memory."""
        return self._memory_cache.copy()
