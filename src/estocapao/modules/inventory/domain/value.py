"""This module represents a specific batch or shipment lot of an ingredient."""
from datetime import date, datetime

class DomainValidationError(ValueError):
    """Base exception class for domain validation errors."""
    pass

class InvalidQuantityError(DomainValidationError):
    """Exception raised when an invalid batch quantity is provided."""
    pass

class InvalidDateError(DomainValidationError):
    """Exception raised when batch dates are invalid or incorrectly formatted."""
    pass

class BatchValueObject:
    """A single batch of an ingredient received from a supplier on a specific date with an expiration date.
    Once created, the details of this batch cannot be changed (immutable).
    """

    __slots__ = ('_batch_id', '_quantity', '_expiration_date', '_received_date')

    def __init__(self, batch_id: str, quantity: float, expiration_date: str | date, received_date: str | date):
        # Validate quantity
        if not isinstance(quantity, (int, float)):
            raise TypeError("Quantity must be a numeric value.")
        if quantity <= 0:
            raise InvalidQuantityError("Quantity must be a positive number greater than zero.")

        self._batch_id = batch_id
        self._quantity = float(quantity)
        self._expiration_date = self._parse_date(expiration_date, "expiration_date")
        self._received_date = self._parse_date(received_date, "received_date")

        # Validate chronological order
        if self._expiration_date < self._received_date:
            raise InvalidDateError("Expiration date cannot be earlier than received date.")

    def _parse_date(self, value: str | date, field_name: str) -> date:
        if isinstance(value, date) and not isinstance(value, datetime):
            return value
        if isinstance(value, datetime):
            return value.date()
        if isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except ValueError as e:
                raise InvalidDateError(
                    f"Invalid date format for '{field_name}': '{value}'. Expected YYYY-MM-DD format."
                ) from e
        raise TypeError(
            f"Invalid type for '{field_name}'. Expected a YYYY-MM-DD ISO string or datetime.date instance."
        )

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

    def __eq__(self, other) -> bool:
        if not isinstance(other, BatchValueObject):
            return NotImplemented
        return (
            self._batch_id == other._batch_id and
            self._quantity == other._quantity and
            self._expiration_date == other._expiration_date and
            self._received_date == other._received_date
        )

    def __hash__(self) -> int:
        return hash((self._batch_id, self._quantity, self._expiration_date, self._received_date))

    def __repr__(self) -> str:
        return (
            f"BatchValueObject(batch_id={self._batch_id!r}, quantity={self._quantity}, "
            f"expiration_date={self._expiration_date.isoformat()}, received_date={self._received_date.isoformat()})"
        )
