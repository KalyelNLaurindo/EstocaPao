"""This module represents a specific batch or shipment lot of an ingredient."""
from datetime import date

class BatchValueObject:
    """A single batch of an ingredient received from a supplier on a specific date with an expiration date.
    Once created, the details of this batch cannot be changed (immutable).
    """

    def __init__(self, batch_id: str, quantity: float, expiration_date: date, received_date: date):
        self._batch_id = batch_id
        self._quantity = quantity
        self._expiration_date = expiration_date
        self._received_date = received_date

    @property
    def batch_id(self) -> str:
        return self._batch_id

    @property
    def quantity(self) -> float:
        return self._quantity

    @property
    def expiration_date(self) -> date:
        return self._expiration_date

    @property
    def received_date(self) -> date:
        return self._received_date
