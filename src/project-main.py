from collections import UserDict
from datetime import datetime, timedelta
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must contain 10 digits.")
        super().__init__(value)

    @staticmethod
    def validate(value):
        return value.isdigit() and len(value) == 10


class Birthday(Field):
    def __init__(self, value):
        try:
            birthday_date = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(birthday_date)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f"Phone number {phone} not found")

    def edit_phone(self, old_phone, new_phone):
        phone_to_edit = self.find_phone(old_phone)
        if phone_to_edit:
            if not Phone.validate(new_phone):
                raise ValueError("New phone number must contain 10 digits.")
            index = self.phones.index(phone_to_edit)
            self.phones[index] = Phone(new_phone)
        else:
            raise ValueError(f"Phone number {old_phone} not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones_str = "; ".join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact {name} not found")

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday is None:
                continue
            birthday_date = record.birthday.value.date()
            birthday_this_year = birthday_date.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_date.replace(year=today.year + 1)
            days_until_birthday = (birthday_this_year - today).days

            if 0 <= days_until_birthday <= 7:
                congratulation_date = birthday_this_year
                if birthday_this_year.weekday() == 5:
                    congratulation_date = birthday_this_year + timedelta(days=2)
                elif birthday_this_year.weekday() == 6:
                    congratulation_date = birthday_this_year + timedelta(days=1)

                upcoming_birthdays.append({
                    "name": record.name.value,
                    "congratulation_date": congratulation_date.strftime("%d.%m.%Y")
                })
        return upcoming_birthdays

    def search(self, query):
        found_records = []
        query_lower = query.lower()

        for record in self.data.values():
            if query_lower in record.name.value.lower():
                found_records.append(record)
                continue

            for phone in record.phones:
                if query_lower in phone.value:
                    found_records.append(record)
                    break

        return found_records

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return f"Error: {e}"
        except KeyError as e:
            return f"Error: {e}"
        except IndexError:
            return "Error: Not enough arguments provided."
        except Exception as e:
            return f"Unexpected error: {e}"
    return inner


def parse_input(user_input):
    parts = user_input.split()
    if len(parts) == 0:
        return "", []
    
    TWO_WORD_COMMANDS = [
        "add contact",
        "change contact", 
        "show phone",
        "show all",
        "add birthday",
        "show birthday"
    ]

    if len(parts) >= 2:
        two_word_command = f"{parts[0]} {parts[1]}".lower()
        if two_word_command in TWO_WORD_COMMANDS:
            return two_word_command, parts[2:]
        
    cmd = parts[0].strip().lower()
    return cmd, parts[1:]


@input_error
def add_contact(args, book: AddressBook):
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
    if len(args) < 3:
        raise IndexError("Not enough arguments. Usage: change [name] [old_phone] [new_phone]")
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError("Not enough arguments. Usage: phone [name]")
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    return str(record)


@input_error
def show_all(args, book: AddressBook):
    if not book.data:
        return "No contacts saved."
    
    result = "All contacts:\n"
    for record in book.data.values():
        result += f"{record}\n"
    
    return result.strip()


@input_error
def add_birthday(args, book: AddressBook):
    if len(args) < 2:
        raise IndexError("Not enough arguments. Usage: add-birthday [name] [DD.MM.YYYY]")
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook):
    if len(args) < 1:
        raise IndexError("Not enough arguments. Usage: show-birthday [name]")
    name = args[0]
    record = book.find(name)
    if record is None:
        raise KeyError(f"Contact '{name}' not found")
    if record.birthday is None:
        return f"{name} has no birthday set."
    return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"


@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays in the next week."
    
    result = "Upcoming birthdays:\n"
    for item in upcoming:
        result += f"{item['name']}: {item['congratulation_date']}\n"
    
    return result.strip()


@input_error
def search_contacts(args, book: AddressBook):
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

def main():
    book = load_data()
    
    commands = {
        "hello": lambda args, book: "How can I help you?",
        "add contact": lambda args, book: add_contact(args, book),
        "change contact": lambda args, book: change_contact(args, book),
        "show phone": lambda args, book: show_phone(args, book),
        "show all": lambda args, book: show_all(args, book),
        "add birthday": lambda args, book: add_birthday(args, book),
        "show birthday": lambda args, book: show_birthday(args, book),
        "birthdays": lambda args, book: birthdays(args, book),
        "search": lambda args, book: search_contacts(args, book),
    }
    print("Welcome to the assistant bot!")
    
    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            continue
        
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break

        if command in commands:
            result = commands[command](args, book)
            if result:
                print(f"{result}\n")
        else:
            print(f"Invalid command: '{command}'.\n")


if __name__ == "__main__":
    main()