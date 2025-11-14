"""Configuration and constants for the bot assistant."""

# File paths for data persistence
ADDRESSBOOK_FILE = "addressbook.json"
NOTEBOOK_FILE = "notes.json"

# Date format
DATE_FORMAT = "%d.%m.%Y"

# Phone validation
PHONE_DIGITS_LENGTH = 10

# Email validation pattern
EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# Default days for upcoming birthdays
DEFAULT_BIRTHDAY_DAYS = 7

# Two-word commands
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
    "delete contact",
    "add note",
    "search note",
    "edit note",
    "delete note",
    "view notes",
    "sort notes",
    "add tag",
    "remove tag",
]