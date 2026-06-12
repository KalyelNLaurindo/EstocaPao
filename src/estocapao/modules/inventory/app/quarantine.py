"""This module handles the logic of logic quarantine of batches, checking expiration and discarding lots."""
from datetime import date
from typing import Dict, List

from estocapao.modules.inventory.domain.ports import IInventoryRepository
from estocapao.modules.inventory.domain.value import BatchValueObject


class QuarantineManager:
    """Manages logical quarantine of expired stock batches, removing them from active use and handling audit discards."""

    def __init__(self, repository: IInventoryRepository):
        self.repository = repository

    def quarantine_expired_batches(self, system_date: date) -> Dict[str, List[BatchValueObject]]:
        """Scans all ingredients in the repository, isolates expired batches, saves them, and returns them."""
        if not isinstance(system_date, date):
            raise TypeError("System date must be a datetime.date instance.")

        quarantined_report: Dict[str, List[BatchValueObject]] = {}
        ingredients = self.repository.get_all()

        for ing_id, ingredient in ingredients.items():
            newly_quarantined = ingredient.quarantine_expired_batches(system_date)
            if newly_quarantined:
                quarantined_report[ing_id] = newly_quarantined
                self.repository.save(ingredient)

        return quarantined_report

    def discard_quarantined_batch(self, batch_id: str) -> None:
        """Permanently removes a batch from quarantine list of whichever ingredient owns it and saves it."""
        if not batch_id:
            raise ValueError("Batch ID is required for discard.")

        ingredients = self.repository.get_all()
        found = False

        for ingredient in ingredients.values():
            removed_batch = ingredient.remove_quarantine_batch(batch_id)
            if removed_batch is not None:
                self.repository.save(ingredient)
                found = True
                break

        if not found:
            raise ValueError(f"Quarantined batch with ID '{batch_id}' not found.")
