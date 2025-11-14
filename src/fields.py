"""Field classes for contact information validation and storage."""

import re
from datetime import datetime
from src.config import PHONE_DIGITS_LENGTH, EMAIL_PATTERN, DATE_FORMAT


class Field:
    """Base class for contact fields."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    """Class for contact name."""
    pass


class Phone(Field):
    """Class for phone number with validation."""

    def __init__(self, value):
        if not self.validate(value):
            raise ValueError(
                f"Phone number must contain {PHONE_DIGITS_LENGTH} digits. Use format like 0931112233."
            )
        super().__init__(value)

    @staticmethod
    def validate(value):
        """Validates phone number format (10 digits)."""
        return value.isdigit() and len(value) == PHONE_DIGITS_LENGTH


class Email(Field):
    """Class for email with validation."""

    def __init__(self, value):
        value = value.strip().lower()
        if not self.validate(value):
            raise ValueError("Invalid email format. Must contain '@' and domain.")
        super().__init__(value)

    @staticmethod
    def validate(value):
        """Validates email format using regex."""
        return re.match(EMAIL_PATTERN, value) is not None


class Address(Field):
    """Class for address with validation."""

    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Address cannot be empty.")
        super().__init__(value)

    @staticmethod
    def validate(value):
        """Validates that address is not empty."""
        return isinstance(value, str) and len(value.strip()) > 0


class Birthday(Field):
    """Class for birthday with validation."""

    def __init__(self, value):
        try:
            birthday_date = datetime.strptime(value, DATE_FORMAT)
            super().__init__(birthday_date)
        except ValueError:
            raise ValueError(f"Invalid date format. Use {DATE_FORMAT}")