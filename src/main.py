"""Main entry point for the Bot Assistant application."""

from src.persistence import load_data, save_data
from src.parser import parse_input
from src.help import display_help
from src.contact_handlers import (
    add_contact,
    change_contact,
    delete_contact,
    show_all,
    add_birthday,
    change_birthday,
    show_birthday,
    birthdays,
    add_email,
    change_email,
    add_address,
    change_address,
    search_contacts,
)
from src.note_handlers import (
    add_tag,
    remove_tag,
    add_note,
    view_notes,
    search_notes,
    edit_note,
    delete_note,
    sort_notes,
)


def setup_commands():
    """Sets up command mappings to handler functions."""
    return {
        "hello": lambda args, book, notebook: "How can I help you?",
        "help": lambda args, book, notebook: display_help(),
        # Contact commands
        "add contact": lambda args, book, notebook: add_contact(args, book),
        "change contact": lambda args, book, notebook: change_contact(args, book),
        "delete contact": lambda args, book, notebook: delete_contact(args, book),
        "show all": lambda args, book, notebook: show_all(args, book),
        "add birthday": lambda args, book, notebook: add_birthday(args, book),
        "show birthday": lambda args, book, notebook: show_birthday(args, book),
        "change birthday": lambda args, book, notebook: change_birthday(args, book),
        "add email": lambda args, book, notebook: add_email(args, book),
        "change email": lambda args, book, notebook: change_email(args, book),
        "add address": lambda args, book, notebook: add_address(args, book),
        "change address": lambda args, book, notebook: change_address(args, book),
        "birthdays": lambda args, book, notebook: birthdays(args, book),
        "search": lambda args, book, notebook: search_contacts(args, book),
        # Note commands
        "add note": lambda args, book, notebook: add_note(args, notebook),
        "view notes": lambda args, book, notebook: view_notes(args, notebook),
        "search note": lambda args, book, notebook: search_notes(args, notebook),
        "edit note": lambda args, book, notebook: edit_note(args, notebook),
        "delete note": lambda args, book, notebook: delete_note(args, notebook),
        "sort notes": lambda args, book, notebook: sort_notes(args, notebook),
        "add tag": lambda args, book, notebook: add_tag(args, notebook),
        "remove tag": lambda args, book, notebook: remove_tag(args, notebook),
    }


def display_welcome():
    """Displays welcome message to the user."""
    print("\n" + "=" * 50)
    print("WELCOME TO ADDRESS BOOK & NOTEBOOK ASSISTANT BOT")
    print("=" * 50)
    print("Type 'help' to see all available commands\n")


def main():
    """Main function to run the address book and notebook bot."""
    book, notebook = load_data()
    commands = setup_commands()

    display_welcome()

    while True:
        try:
            user_input = input("Enter a command: ").strip()
            if not user_input:
                continue

            command, args = parse_input(user_input)

            if command in ["close", "exit"]:
                save_data(book, notebook)
                print("\n" + "=" * 50)
                print("Data saved. Good bye!")
                print("=" * 50 + "\n")
                break

            if command in commands:
                result = commands[command](args, book, notebook)
                if result:
                    print(f"\n{result}\n")
            else:
                print(f"\nInvalid command: '{command}'. Type 'help' for assistance.\n")

        except KeyboardInterrupt:
            print("\n\nExiting... (Data will be saved)")
            save_data(book, notebook)
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}\n")


if __name__ == "__main__":
    main()