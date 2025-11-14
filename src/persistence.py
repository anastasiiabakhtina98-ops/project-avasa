"""Data persistence functions for saving and loading data."""

import json
import os
from src.addressbook import AddressBook
from src.record import Record
from src.notebook import NoteBook
from src.note import Note
from src.config import ADDRESSBOOK_FILE, NOTEBOOK_FILE


def save_data(book, notebook, addressbook_file=ADDRESSBOOK_FILE, notebook_file=NOTEBOOK_FILE):
    """Saves address book and notebook to JSON files."""
    # Save address book
    addressbook_data = [record.to_dict() for record in book.data.values()]
    with open(addressbook_file, "w", encoding="utf-8") as f:
        json.dump(addressbook_data, f, indent=4, ensure_ascii=False)

    # Save notebook
    notebook_data = [note.to_dict() for note in notebook.data.values()]
    with open(notebook_file, "w", encoding="utf-8") as f:
        json.dump(notebook_data, f, indent=4, ensure_ascii=False)


def load_data(addressbook_file=ADDRESSBOOK_FILE, notebook_file=NOTEBOOK_FILE):
    """Loads address book and notebook from JSON files."""
    # Load address book
    book = AddressBook()
    if os.path.exists(addressbook_file):
        try:
            with open(addressbook_file, "r", encoding="utf-8") as f:
                try:
                    data_list = json.load(f)
                except json.JSONDecodeError:
                    print(f"Warning: Can't read {addressbook_file}. Created new Address book.")
                    data_list = []

                for record_dict in data_list:
                    record = Record.from_dict(record_dict)
                    book.add_record(record)
        except Exception as e:
            print(f"Error during Address book loading: {e}. Created new Address book.")

    # Load notebook
    notebook = NoteBook()
    if os.path.exists(notebook_file):
        try:
            with open(notebook_file, "r", encoding="utf-8") as f:
                try:
                    data_list = json.load(f)
                except json.JSONDecodeError:
                    print(f"Warning: Can't read {notebook_file}. Created new Notebook.")
                    data_list = []

                for note_dict in data_list:
                    note = Note.from_dict(note_dict)
                    notebook.add_note(note)
        except Exception as e:
            print(f"Error during Notebook loading: {e}. Created new Notebook.")

    return book, notebook