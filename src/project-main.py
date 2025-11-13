from collections import UserDict
from datetime import datetime, timedelta
import json
import re
import os


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
            raise ValueError("Phone number must contain 10 digits. Use format like 0931112233.")
        super().__init__(value)

    @staticmethod
    def validate(value):
        """Validates phone number format (10 digits)."""
        return value.isdigit() and len(value) == 10


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
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, value) is not None


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
            birthday_date = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(birthday_date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


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
        """Covert Record object to dict"""
        return {
            "name": self.name.value,
            "phones": [phone.value for phone in self.phones],
            "email": self.email.value if self.email else None,
            "address": self.address.value if self.address else None,
            "birthday": self.birthday.value.strftime("%d.%m.%Y") if self.birthday else None,
        }

    @classmethod
    def from_dict(cls, data):
        """Create object Record from dict"""
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
        birthday_str = (f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}"
                        if self.birthday else "")
        email_str = f", email: {self.email.value}" if self.email else ""
        address_str = f", address: {self.address.value}" if self.address else ""
        return (f"Contact name: {self.name.value}, phones: {phones_str}"
                f"{email_str}{address_str}{birthday_str}")


class AddressBook(UserDict):
    """Class representing the address book."""
    def add_record(self, record):
        """Adds a record to the address book."""
        self.data[record.name.value] = record

    def find(self, name):
        """Finds a record by name."""
        return self.data.get(name)

    def delete(self, name):
        """Deletes a record by name."""
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact '{name}' not found")

    def get_birthdays_in_days(self, days: int):
        """Returns contacts with birthday exactly in `days` days from today."""
        if days < 0:
            raise ValueError("Number of days cannot be negative.")
        today = datetime.today().date()
        target_date = today + timedelta(days=days)
        result = []
        for record in self.data.values():
            if not record.birthday:
                continue
            bday = record.birthday.value.date()
            bday_this_year = bday.replace(year=today.year)
            if bday_this_year < today:
                bday_this_year = bday_this_year.replace(year=today.year + 1)
            if bday_this_year == target_date:
                date = bday_this_year
                wd = date.weekday()
                if wd == 5:  # Субота → Понеділок
                    date += timedelta(days=2)
                elif wd == 6:  # Неділя → Понеділок
                    date += timedelta(days=1)
                result.append({
                    "name": record.name.value,
                    "congratulation_date": date.strftime("%d.%m.%Y")
                })
        result.sort(key=lambda x: x["name"])
        return result

    def get_upcoming_birthdays(self):
        """Keeps backward compatibility — returns birthdays in 7 days."""
        return self.get_birthdays_in_days(7)

    def search(self, query):
        """Searches contacts by name, phone, email, address, or birthday."""
        found_records = []
        query_lower = query.lower()

        for record in self.data.values():
            # Search by name
            if query_lower in record.name.value.lower():
                found_records.append(record)
                continue

            # Search by phone
            phone_found = False
            for phone in record.phones:
                if query_lower in phone.value:
                    found_records.append(record)
                    phone_found = True
                    break

            if phone_found:
                continue

            # Search by email
            if record.email and query_lower in record.email.value.lower():
                found_records.append(record)
                continue

            # Search by address
            if record.address and query_lower in record.address.value.lower():
                found_records.append(record)
                continue

            # Search by birthday
            if (record.birthday and
                    query_lower in record.birthday.value.strftime("%d.%m.%Y")):
                found_records.append(record)

        return found_records


def save_data(book, filename="addressbook.json"):
    """Saves address book to JSON file."""
    data_to_save = [record.to_dict() for record in book.data.values()]

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, indent=4, ensure_ascii=False)


def load_data(filename="addressbook.json"):
    """Loads address book from JSON file."""
    if not os.path.exists(filename):
        return AddressBook()

    try:
        with open(filename, "r", encoding="utf-8") as f:
            try:
                data_list = json.load(f)
            except json.JSONDecodeError:
                print(f"Error: Can't read {filename}. Created new Adress book.")
                return AddressBook()

        book = AddressBook()
        for record_dict in data_list:
            record = Record.from_dict(record_dict)
            book.add_record(record)
        return book

    except FileNotFoundError:
        return AddressBook()
    except Exception as e:
        print(f"Error during data loading: {e}. Created new Adress book.")
        return AddressBook()


def input_error(func):
    """Decorator for handling errors in command functions."""
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {e}"
        except KeyError as e:
            return f"Error: {e}"
        except IndexError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Unexpected error: {e}"
    return inner


def parse_input(user_input):
    """Parses user input to extract command and arguments."""
    parts = user_input.split()
    if len(parts) == 0:
        return "", []

    TWO_WORD_COMMANDS = [
        "show all",
        "add contact",
        "change contact",
        "add birthday",
        "change birthday",
        "show birthday",
        "add email",
        "change email",
        "add address",
        "change address",
        "delete contact"
    ]

    if len(parts) >= 2:
        two_word_command = f"{parts[0]} {parts[1]}".lower()
        if two_word_command in TWO_WORD_COMMANDS:
            return two_word_command, parts[2:]

    cmd = parts[0].strip().lower()
    return cmd, parts[1:]


@input_error
def add_contact(args, book: AddressBook):
    """Adds a new contact with name and phone."""
    if len(args) < 2:
        raise IndexError(
            "Not enough arguments. Usage: add contact [name] [phone]")

    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    """Changes phone number for an existing contact."""
    if len(args) < 3:
        raise IndexError(
            "Not enough arguments. Usage: change contact [name] [old_phone] [new_phone]")
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def delete_contact(args, book: AddressBook):
    """Deletes a contact from the address book."""
    if len(args) < 1:
        raise IndexError("Not enough arguments. Usage: delete contact [name]")
    name = args[0]
    book.delete(name)
    return f"Contact '{name}' deleted."


@input_error
def show_all(args, book: AddressBook):
    """Displays all contacts in the address book."""
    if not book.data:
        return "No contacts saved."

    result = "All contacts:\n"
    for record in book.data.values():
        result += f"{record}\n"

    return result.strip()


@input_error
def add_birthday(args, book: AddressBook):
    """Adds a birthday to an existing contact."""
    if len(args) < 2:
        raise IndexError(
            "Not enough arguments. Usage: add birthday [name] [DD.MM.YYYY]")
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def change_birthday(args, book: AddressBook):
    """Changes the birthday for an existing contact."""
    if len(args) < 2:
        raise IndexError(
            "Not enough arguments. Usage: change birthday [name] [new_DD.MM.YYYY]")
    name, new_birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    if record.birthday is None:
        raise ValueError(f"Contact '{name}' has no birthday. Use 'add birthday' first.")

    record.add_birthday(new_birthday)
    return "Birthday updated."


@input_error
def show_birthday(args, book: AddressBook):
    """Displays the birthday for a contact."""
    if len(args) < 1:
        raise IndexError("Not enough arguments. Usage: show birthday [name]")
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    if record.birthday is None:
        return f"{name} has no birthday set."
    return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"


@input_error
def birthdays(args, book: AddressBook):
    """Show birthdays in exactly N days (default: 7)."""
    if not args:
        days = 7
    else:
        try:
            days = int(args[0])
            if days < 0:
                raise ValueError
        except ValueError:
            return "Error: Enter a valid number (e.g., 'birthdays 5')"

    upcoming = book.get_birthdays_in_days(days)
    if not upcoming:
        return f"No birthdays in {days} day{'s' if days != 1 else ''}."

    result = f"Birthdays in {days} day{'s' if days != 1 else ''}:\n"
    for item in upcoming:
        result += f"• {item['name']} → {item['congratulation_date']}\n"
    return result.strip()


@input_error
def add_email(args, book: AddressBook):
    """Adds an email to an existing contact."""
    if len(args) < 2:
        raise IndexError("Not enough arguments. Usage: add email [name] [email]")
    name, email, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    record.add_email(email)
    return "Email added."


@input_error
def change_email(args, book: AddressBook):
    """Changes the email for an existing contact."""
    if len(args) < 2:
        raise IndexError(
            "Not enough arguments. Usage: change email [name] [new_email]")
    name, new_email, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    if record.email is None:
        raise ValueError(f"Contact '{name}' has no email. Use 'add email' first.")
    record.edit_email(new_email)
    return "Email updated."


@input_error
def add_address(args, book: AddressBook):
    """Adds an address to an existing contact."""
    if len(args) < 2:
        raise IndexError(
            "Not enough arguments. Usage: add address [name] [address]")
    name = args[0]
    address = " ".join(args[1:])
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    record.add_address(address)
    return "Address added."


@input_error
def change_address(args, book: AddressBook):
    """Changes the address for an existing contact."""
    if len(args) < 2:
        raise IndexError(
            "Not enough arguments. Usage: change address [name] [new_address]")
    name = args[0]
    new_address = " ".join(args[1:])
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    if record.address is None:
        raise ValueError(f"Contact '{name}' has no address. Use 'add address' first.")
    record.edit_address(new_address)
    return "Address updated."


@input_error
def search_contacts(args, book: AddressBook):
    """Searches contacts by name, phone, email, address, or birthday."""
    if not args:
        raise IndexError("Please provide a search term. Usage: search [query]")

    query = " ".join(args)
    results = book.search(query)

    if not results:
        return f"No contacts found matching '{query}'."

    output = f"Search results for '{query}':\n"
    for record in results:
        output += f"{record}\n"

    return output.strip()


def display_help():
    """Displays the help menu with all available commands."""
    help_text = """
            ADDRESS BOOK BOT - AVAILABLE COMMANDS                

CONTACT MANAGEMENT:
  add contact [name] [phone]           - Add new contact
  change contact [name] [old] [new]    - Change phone number
  delete contact [name]                - Delete contact
  show all                             - Display all contacts
  search [query]                       - Search by name/phone/email/address/birthday

EMAIL MANAGEMENT:
  add email [name] [email]             - Add email to contact
  change email [name] [new_email]      - Change contact email

ADDRESS MANAGEMENT:
  add address [name] [address]         - Add address to contact
  change address [name] [new_address]  - Change contact address

BIRTHDAY MANAGEMENT:
  add birthday [name] [DD.MM.YYYY]     - Add birthday to contact
  change birthday [name] [DD.MM.YYYY]  - Change contact birthday
  show birthday [name]                 - Display contact birthday
  birthdays [N]                        - Show birthdays in exactly N days (default: 7)
                                       Examples: birthdays 0 (today), birthdays 3, birthdays 30

GENERAL:
  hello                                - launch bot
  help                                 - Show this menu
  close/exit                           - Save and exit

"""
    return help_text.strip()


def main():
    """Main function to run the address book bot."""
    book = load_data()

    commands = {
        "hello": lambda args, book: "How can I help you?",
        "help": lambda args, book: display_help(),
        "add contact": lambda args, book: add_contact(args, book),
        "change contact": lambda args, book: change_contact(args, book),
        "delete contact": lambda args, book: delete_contact(args, book),
        "show all": lambda args, book: show_all(args, book),
        "add birthday": lambda args, book: add_birthday(args, book),
        "show birthday": lambda args, book: show_birthday(args, book),
        "change birthday": lambda args, book: change_birthday(args, book),
        "add email": lambda args, book: add_email(args, book),
        "change email": lambda args, book: change_email(args, book),
        "add address": lambda args, book: add_address(args, book),
        "change address": lambda args, book: change_address(args, book),
        "birthdays": lambda args, book: birthdays(args, book),
        "search": lambda args, book: search_contacts(args, book),
    }

    print("\nWELCOME TO ADDRESS BOOK ASSISTANT BOT")
    print("Type 'help' to see all available commands")

    while True:
        try:
            user_input = input("Enter a command: ").strip()
            if not user_input:
                continue

            command, args = parse_input(user_input)

            if command in ["close", "exit"]:
                save_data(book)
                print("\nData saved. Good bye!")
                break

            if command in commands:
                result = commands[command](args, book)
                if result:
                    print(f"\n{result}\n")
            else:
                print(f"\nInvalid command: '{command}'. Type 'help' for assistance.\n")

        except KeyboardInterrupt:
            print("\n\nExiting... (Data will be saved)")
            save_data(book)
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}\n")


if __name__ == "__main__":
    main()