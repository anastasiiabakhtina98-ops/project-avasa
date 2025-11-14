"""Command handlers for notebook operations."""

from src.decorators import input_error
from src.note import Note
from src.notebook import NoteBook


@input_error
def add_tag(args, notebook: NoteBook):
    """Adds tags to an existing note."""
    if isinstance(args, str):
        args_str = args.strip()
    else:
        args_str = " ".join(args)

    if not args_str:
        raise IndexError(
            "Not enough arguments.\n"
            "Usage: add tag [title], [#tag1 #tag2 ...]\n"
            "Example: add tag To Do, #urgent #important")

    if "," not in args_str:
        raise ValueError(
            "Missing comma separator!\n"
            "Usage: add tag [title], [#tag1 #tag2 ...]\n"
            "Example: add tag To Do, #urgent #important")

    parts = args_str.split(",", 1)
    title = parts[0].strip()
    tags_input = parts[1].strip()

    if not title:
        raise ValueError("Note title cannot be empty.")
    if not tags_input:
        raise ValueError("Please provide at least one tag.")

    note = notebook.find(title)
    if note is None:
        raise KeyError(f"Note '{title}' not found")

    new_tags = []
    for word in tags_input.split():
        if word.startswith("#"):
            new_tags.append(word.lstrip("#").lower())
        else:
            new_tags.append(word.lower())

    if not new_tags:
        raise ValueError("Please provide at least one tag (starting with #)")

    existing_tags = set(note.tags)
    existing_tags.update(new_tags)
    note.tags = sorted(list(existing_tags))

    return f"Added {len(new_tags)} tag(s) to '{title}'. Total tags: {len(note.tags)}"


@input_error
def remove_tag(args, notebook: NoteBook):
    """Removes tags from a note."""
    if isinstance(args, str):
        args_str = args.strip()
    else:
        args_str = " ".join(args)

    if not args_str:
        raise IndexError(
            "Not enough arguments.\n"
            "Usage: remove tag [title], [#tag1 #tag2 ...]\n"
            "Example: remove tag To Do, #urgent")

    if "," not in args_str:
        raise ValueError(
            "Missing comma separator!\n"
            "Usage: remove tag [title], [#tag1 #tag2 ...]\n"
            "Example: remove tag To Do, #urgent")

    parts = args_str.split(",", 1)
    title = parts[0].strip()
    tags_input = parts[1].strip()

    if not title:
        raise ValueError("Note title cannot be empty.")
    if not tags_input:
        raise ValueError("Please provide at least one tag to remove.")

    note = notebook.find(title)
    if note is None:
        raise KeyError(f"Note '{title}' not found")

    tags_to_remove = []
    for word in tags_input.split():
        tag = word.lstrip("#").lower()
        tags_to_remove.append(tag)

    initial_count = len(note.tags)
    note.tags = [tag for tag in note.tags if tag not in tags_to_remove]
    removed_count = initial_count - len(note.tags)

    if removed_count == 0:
        return f"No tags were removed from '{title}'."

    return f"Removed {removed_count} tag(s) from '{title}'. Remaining tags: {len(note.tags)}"


@input_error
def add_note(args, notebook: NoteBook):
    """Adds a new note with optional tags using comma as separator."""
    if isinstance(args, str):
        args_str = args.strip()
    else:
        args_str = " ".join(args)

    if not args_str:
        raise IndexError(
            "Not enough arguments.\n"
            "Usage: add note [title], [content] [#tag1 #tag2 ...]\n"
            "Example: add note To Do, Complete project #important")

    if "," not in args_str:
        raise ValueError(
            "Missing comma separator!\n"
            "Usage: add note [title], [content] [#tag1 #tag2 ...]\n"
            "Example: add note To Do, Complete project #important")

    parts = args_str.split(",", 1)
    title = parts[0].strip()
    rest = parts[1].strip()

    if not title:
        raise ValueError("Note title cannot be empty.")
    if not rest:
        raise ValueError("Note content cannot be empty.")

    tags = []
    content_parts = []

    for word in rest.split():
        if word.startswith("#"):
            tags.append(word.lstrip("#"))
        else:
            content_parts.append(word)

    content = " ".join(content_parts)

    if not content:
        raise ValueError("Note content cannot be empty.")

    note = Note(title, content, tags)
    notebook.add_note(note)
    return f"Note added: '{title}' with {len(tags)} tag(s)."


@input_error
def view_notes(args, notebook: NoteBook):
    """Displays all notes with their content and tags."""
    if not notebook.data:
        return "No notes saved."

    result = "All notes:\n" + "="*50 + "\n"
    for i, note in enumerate(notebook.data.values(), 1):
        result += f"{i}. {note}\n" + "-"*50 + "\n"

    return result.strip()


@input_error
def search_notes(args, notebook: NoteBook):
    """Searches notes by keyword or tag."""
    if isinstance(args, str):
        query = args.strip()
    else:
        query = " ".join(args)

    if not query:
        raise IndexError("Please provide a search term.\n"
                        "Usage: search note [keyword or #tag]\n"
                        "Example: search note #todo")

    query_lower = query.lstrip("#").lower()
    results = notebook.search(query_lower)

    if not results:
        return f"No notes found matching '{query}'."

    output = f"🔍 Search results for '{query}':\n"
    for note in results:
        output += f"  • {note}\n"

    return output.strip()


@input_error
def edit_note(args, notebook: NoteBook):
    """Edits an existing note's content and/or tags using comma as separator."""
    if isinstance(args, str):
        args_str = args.strip()
    else:
        args_str = " ".join(args)

    if not args_str:
        raise IndexError(
            "Not enough arguments.\n"
            "Usage: edit note [title], [new_content] [#tag1 #tag2 ...]\n"
            "Example: edit note To Do, Complete project and prepare #urgent")

    if "," not in args_str:
        raise ValueError(
            "Missing comma separator!\n"
            "Usage: edit note [title], [new_content] [#tag1 #tag2 ...]\n"
            "Example: edit note To Do, Complete project and prepare #urgent")

    parts = args_str.split(",", 1)
    title = parts[0].strip()
    rest = parts[1].strip()

    if not title:
        raise ValueError("Note title cannot be empty.")
    if not rest:
        raise ValueError("Note content cannot be empty.")

    tags = []
    content_parts = []

    for word in rest.split():
        if word.startswith("#"):
            tags.append(word.lstrip("#"))
        else:
            content_parts.append(word)

    new_content = " ".join(content_parts) if content_parts else None
    new_tags = tags if tags else None

    notebook.edit(title, new_content=new_content, new_tags=new_tags)
    return f"Note updated: '{title}'"


@input_error
def delete_note(args, notebook: NoteBook):
    """Deletes a note."""
    if len(args) < 1:
        raise IndexError("Not enough arguments. Usage: delete note [title]")

    title = args[0]
    notebook.delete(title)
    return f"Note '{title}' deleted."


@input_error
def sort_notes(args, notebook: NoteBook):
    """Displays notes sorted by tag."""
    if not notebook.data:
        return "No notes saved."

    sorted_notes = sorted(
        notebook.data.values(),
        key=lambda n: n.tags[0] if n.tags else "zzz"
    )

    result = "Notes sorted by tag:\n"
    for i, note in enumerate(sorted_notes, 1):
        result += f"{i}. {note}\n"

    return result.strip()