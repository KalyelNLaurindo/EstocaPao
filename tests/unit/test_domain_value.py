import unittest
from datetime import date
from estocapao.modules.inventory.domain.value import (
    BatchValueObject,
    InvalidQuantityError,
    InvalidDateError,
    DomainValidationError
)

class TestBatchValueObject(unittest.TestCase):
    """Unit tests for the BatchValueObject domain value object."""

    def test_valid_instantiation_with_strings(self):
        """Should successfully instantiate BatchValueObject when valid ISO date strings are provided."""
        batch = BatchValueObject(
            batch_id="LOT-001",
            quantity=15.5,
            expiration_date="2026-12-31",
            received_date="2026-06-12"
        )
        self.assertEqual(batch.batch_id, "LOT-001")
        self.assertEqual(batch.quantity, 15.5)
        self.assertEqual(batch.expiration_date, date(2026, 12, 31))
        self.assertEqual(batch.received_date, date(2026, 6, 12))

    def test_valid_instantiation_with_date_objects(self):
        """Should successfully instantiate BatchValueObject when date objects are provided directly."""
        exp = date(2026, 10, 15)
        rcv = date(2026, 5, 20)
        batch = BatchValueObject(
            batch_id="LOT-002",
            quantity=5.0,
            expiration_date=exp,
            received_date=rcv
        )
        self.assertEqual(batch.batch_id, "LOT-002")
        self.assertEqual(batch.quantity, 5.0)
        self.assertEqual(batch.expiration_date, exp)
        self.assertEqual(batch.received_date, rcv)

    def test_immutability(self):
        """Should enforce strict immutability. Attributes cannot be modified or added dynamically."""
        batch = BatchValueObject(
            batch_id="LOT-003",
            quantity=10.0,
            expiration_date="2026-09-01",
            received_date="2026-06-01"
        )
        
        # Test modifying existing properties
        with self.assertRaises(AttributeError):
            batch.batch_id = "NEW-LOT" # type: ignore
        with self.assertRaises(AttributeError):
            batch.quantity = 20.0 # type: ignore
        with self.assertRaises(AttributeError):
            batch.expiration_date = date(2027, 1, 1) # type: ignore
        with self.assertRaises(AttributeError):
            batch.received_date = date(2026, 6, 2) # type: ignore

        # Test setting a new attribute not defined in slots
        with self.assertRaises(AttributeError):
            batch.new_attr = "forbidden" # type: ignore

    def test_invalid_quantity_raises_error(self):
        """Should raise InvalidQuantityError (subclass of ValueError) for zero or negative quantities."""
        with self.assertRaises(InvalidQuantityError):
            BatchValueObject(
                batch_id="LOT-004",
                quantity=0.0,
                expiration_date="2026-12-31",
                received_date="2026-06-12"
            )
        with self.assertRaises(InvalidQuantityError):
            BatchValueObject(
                batch_id="LOT-005",
                quantity=-2.5,
                expiration_date="2026-12-31",
                received_date="2026-06-12"
            )
        # Verify it inherits from ValueError and DomainValidationError
        try:
            BatchValueObject(
                batch_id="LOT-005",
                quantity=-1.0,
                expiration_date="2026-12-31",
                received_date="2026-06-12"
            )
        except InvalidQuantityError as e:
            self.assertTrue(isinstance(e, ValueError))
            self.assertTrue(isinstance(e, DomainValidationError))

    def test_invalid_date_format_raises_error(self):
        """Should raise InvalidDateError (subclass of ValueError) for malformed date strings."""
        invalid_formats = [
            "2026/12/31",
            "31-12-2026",
            "not-a-date",
            "",
            "2026-13-45"
        ]
        for bad_date in invalid_formats:
            with self.assertRaises(InvalidDateError):
                BatchValueObject(
                    batch_id="LOT-006",
                    quantity=10.0,
                    expiration_date=bad_date,
                    received_date="2026-06-12"
                )
            with self.assertRaises(InvalidDateError):
                BatchValueObject(
                    batch_id="LOT-007",
                    quantity=10.0,
                    expiration_date="2026-12-31",
                    received_date=bad_date
                )

    def test_invalid_date_chronology_raises_error(self):
        """Should raise InvalidDateError when expiration date is chronologically before received date."""
        with self.assertRaises(InvalidDateError):
            BatchValueObject(
                batch_id="LOT-008",
                quantity=8.0,
                expiration_date="2026-06-01",  # Expired before received
                received_date="2026-06-12"
            )

    def test_equality_and_hash(self):
        """Should equate and hash objects by their value attributes instead of reference identity."""
        batch_1 = BatchValueObject(
            batch_id="LOT-009",
            quantity=12.0,
            expiration_date="2026-12-31",
            received_date="2026-06-12"
        )
        batch_2 = BatchValueObject(
            batch_id="LOT-009",
            quantity=12.0,
            expiration_date="2026-12-31",
            received_date="2026-06-12"
        )
        batch_different = BatchValueObject(
            batch_id="LOT-010",
            quantity=12.0,
            expiration_date="2026-12-31",
            received_date="2026-06-12"
        )

        self.assertEqual(batch_1, batch_2)
        self.assertNotEqual(batch_1, batch_different)
        self.assertEqual(hash(batch_1), hash(batch_2))
        
        # Test hash set uniqueness/identity
        batches_set = {batch_1, batch_2}
        self.assertEqual(len(batches_set), 1)

if __name__ == "__main__":
    unittest.main()
