"""Command handlers for address book operations."""

from src.decorators import input_error
from src.record import Record
from src.addressbook import AddressBook
from src.config import DEFAULT_BIRTHDAY_DAYS


@input_error
def add_contact(args, book: AddressBook):
    """Adds a new contact with name and phone."""
    if len(args) < 2:
        raise IndexError("Not enough arguments. Usage: add contact [name] [phone]")

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
        raise IndexError("Not enough arguments. Usage: add birthday [name] [DD.MM.YYYY]")
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
        days = DEFAULT_BIRTHDAY_DAYS
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
        raise IndexError("Not enough arguments. Usage: change email [name] [new_email]")
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
        raise IndexError("Not enough arguments. Usage: add address [name] [address]")
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