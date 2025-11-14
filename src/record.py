"""Record class for representing a contact."""

from src.fields import Name, Phone, Email, Address, Birthday
from src.config import DATE_FORMAT


class Record:
    """Class representing a contact record."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.address = None
        self.birthday = None

    def add_phone(self, phone):
        """Adds a phone number to the contact."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        """Removes a phone number from the contact."""
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone number {phone} not found")

    def edit_phone(self, old_phone, new_phone):
        """Edits an existing phone number."""
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            if not Phone.validate(new_phone):
                raise ValueError("New phone number must contain 10 digits. Use format like 0931112233.")
            index = self.phones.index(phone_to_edit)
            self.phones[index] = Phone(new_phone)
        else:
            raise ValueError(f"Phone number {old_phone} not found")

    def find_phone(self, phone):
        """Finds a phone number in the contact's phone list."""
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_email(self, email):
        """Adds or updates email address."""
        self.email = Email(email)

    def edit_email(self, new_email):
        """Edits the email address."""
        if not Email.validate(new_email):
            raise ValueError("Invalid email format.")
        self.email = Email(new_email)

    def add_address(self, address):
        """Adds or updates address."""
        self.address = Address(address)

    def edit_address(self, new_address):
        """Edits the address."""
        if not Address.validate(new_address):
            raise ValueError("Address cannot be empty.")
        self.address = Address(new_address)

    def add_birthday(self, birthday):
        """Adds or updates birthday."""
        self.birthday = Birthday(birthday)

    def to_dict(self):
        """Convert Record object to dict."""
        return {
            "name": self.name.value,
            "phones": [phone.value for phone in self.phones],
            "email": self.email.value if self.email else None,
            "address": self.address.value if self.address else None,
            "birthday": self.birthday.value.strftime(DATE_FORMAT) if self.birthday else None,
        }

    @classmethod
    def from_dict(cls, data):
        """Create object Record from dict."""
        record = cls(data["name"])

        for phone in data.get("phones", []):
            record.add_phone(phone)

        if data.get("email"):
            record.add_email(data["email"])

        if data.get("address"):
            record.add_address(data["address"])

        if data.get("birthday"):
            record.add_birthday(data["birthday"])

        return record

    def __str__(self):
        """Returns formatted string representation of the contact."""
        phones_str = "; ".join(p.value for p in self.phones) if self.phones else "No phones"
        birthday_str = (
            f", birthday: {self.birthday.value.strftime(DATE_FORMAT)}"
            if self.birthday
            else ""
        )
        email_str = f", email: {self.email.value}" if self.email else ""
        address_str = f", address: {self.address.value}" if self.address else ""
        return (
            f"Contact name: {self.name.value}, phones: {phones_str}"
            f"{email_str}{address_str}{birthday_str}"
        )