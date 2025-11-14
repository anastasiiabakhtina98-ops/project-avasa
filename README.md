# Bot Assistant - Address Book & Notebook

A modular Python assistant bot that manages contacts and notes with advanced search, validation, and data persistence features.

## Features

### Address Book
- **Contact Management**: Add, edit, delete contacts
- **Phone Management**: Add/edit multiple phone numbers with validation
- **Email Management**: Store and update email addresses
- **Address Management**: Store and update addresses
- **Birthday Management**: Track birthdays and get notifications
- **Search**: Search contacts by name, phone, email, address, or birthday

### Notebook
- **Note Management**: Create, edit, delete notes
- **Tags**: Organize notes with hashtags
- **Search**: Find notes by keywords or tags
- **Sorting**: Sort notes by tags

## Project Structure

```
project-fantastic5/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── config.py                # Configuration & constants
│   ├── fields.py                # Field classes (Name, Phone, Email, etc.)
│   ├── record.py                # Contact Record class
│   ├── addressbook.py           # AddressBook collection class
│   ├── note.py                  # Note class
│   ├── notebook.py              # NoteBook collection class
│   ├── persistence.py           # save_data, load_data functions
│   ├── decorators.py            # input_error decorator
│   ├── parser.py                # parse_input function
│   ├── contact_handlers.py      # Contact command handlers (13 functions)
│   ├── note_handlers.py         # Note command handlers (8 functions)
│   ├── help.py                  # display_help function
│   └── main.py                  # Main entry point (command loop)
├── .gitignore
├── README.md
├── pyproject.toml
└── requirements.txt
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the bot:
```bash
python -m src.main
```

Or if installed as package:
```bash
bot-assistant
```

### Available Commands

#### Contact Management
- `add contact [name] [phone]` - Add new contact
- `change contact [name] [old] [new]` - Change phone number
- `delete contact [name]` - Delete contact
- `show all` - Display all contacts
- `search [query]` - Search contacts by name/phone/email/address/birthday

#### Email & Address
- `add email [name] [email]` - Add email to contact
- `change email [name] [new_email]` - Change contact email
- `add address [name] [address]` - Add address to contact
- `change address [name] [new_address]` - Change contact address

#### Birthday Management
- `add birthday [name] [DD.MM.YYYY]` - Add birthday to contact
- `change birthday [name] [DD.MM.YYYY]` - Change contact birthday
- `show birthday [name]` - Display contact birthday
- `birthdays [N]` - Show birthdays in exactly N days (default: 7)

#### Note Management
- `add note [title], [content] [#tags]` - Add new note
- `view notes` - Display all notes with content
- `search note [query]` - Search notes by keyword/tag
- `edit note [title], [new_content]` - Edit note content
- `delete note [title]` - Delete note
- `add tag [title], [#tag1 #tag2]` - Add tags to existing note
- `remove tag [title], [#tag1]` - Remove tags from note
- `sort notes` - Sort notes by tag

#### General
- `hello` - Start bot
- `help` - Show all commands
- `close` or `exit` - Save and exit

## Design Patterns

### OOP Implementation

1. **Inheritance**: `Field` → `Name`, `Phone`, `Email`, `Address`, `Birthday`
2. **Composition**: `Record` contains multiple `Field` objects
3. **Collections**: `AddressBook` and `NoteBook` extend `UserDict`
4. **Decorators**: `input_error` for centralized error handling
5. **Factory Pattern**: `from_dict()` for object deserialization

### Modularity

- **Separation of Concerns**: Each module has a single responsibility
- **Configuration**: All constants in `config.py`
- **Data Persistence**: Isolated in `persistence.py`
- **Command Handlers**: Grouped by domain (`contact_handlers.py`, `note_handlers.py`)
- **Easy Testing**: Each component can be tested independently

## Data Persistence

- Address book saved to `addressbook.json`
- Notebook saved to `notes.json`
- Automatic loading on startup
- Automatic saving on exit

## Requirements

- Python 3.8+

## Development

For development, install development dependencies:
```bash
pip install -r requirements.txt
```

To format code:
```bash
black src/
isort src/
```

To check types:
```bash
mypy src/
```

## Team

- **Anastasiia Bakhtina** - Team Lead, Code Review
- **Sergi Alekseiuk** - Notebook, Tags
- **Andrii Borodin** - Data Models, Persistence
- **Anton Glazkov** - Birthdays
- **Valeriia Bogdan-Koretska** - Documentation

## License

MIT
