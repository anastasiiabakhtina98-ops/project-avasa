"""Input parsing for commands."""

from src.config import TWO_WORD_COMMANDS


def parse_input(user_input):
    """Parses user input to extract command and arguments."""
    parts = user_input.split()
    if len(parts) == 0:
        return "", []

    # Check for two-word commands
    if len(parts) >= 2:
        two_word_command = f"{parts[0]} {parts[1]}".lower()
        if two_word_command in TWO_WORD_COMMANDS:
            return two_word_command, parts[2:]

    cmd = parts[0].strip().lower()
    return cmd, parts[1:]