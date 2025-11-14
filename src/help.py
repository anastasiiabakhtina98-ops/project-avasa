"""Help and display utilities."""


def display_help():
    """Displays the help menu with all available commands."""
    help_text = """
                BOT ASSISTANT - AVAILABLE COMMANDS



CONTACT MANAGEMENT:
  add contact [name] [phone]           - Add new contact
  change contact [name] [old] [new]    - Change phone number
  delete contact [name]                - Delete contact
  show all                             - Display all contacts
  search [query]                       - Search contacts by name/phone/email/address/birthday



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



NOTE MANAGEMENT:
  add note [title], [content] [#tags]  - Add new note
  view notes                           - Display all notes with content
  search note [query]                  - Search notes by keyword/tag
  edit note [title], [new_content]     - Edit note content
  delete note [title]                  - Delete note
  add tag [title], [#tag1 #tag2 ...]   - Add tags to existing note
  remove tag [title], [#tag1 ...]      - Remove tags from note
  sort notes                           - Sort notes by tag



GENERAL:
  hello                                - Launch bot
  help                                 - Show this menu
  close/exit                           - Save and exit



    """
    return help_text.strip()