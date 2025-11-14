"""NoteBook class for managing notes."""

from collections import UserDict
from src.note import Note


class NoteBook(UserDict):
    """Class representing the notebook (collection of notes)."""

    def add_note(self, note):
        """Adds a note to the notebook."""
        self.data[note.title] = note

    def find(self, title):
        """Finds a note by title."""
        return self.data.get(title)

    def delete(self, title):
        """Deletes a note by title."""
        if title in self.data:
            del self.data[title]
        else:
            raise KeyError(f"Note '{title}' not found")

    def edit(self, title, new_title=None, new_content=None, new_tags=None):
        """Edits a note."""
        note = self.find(title)
        if note is None:
            raise KeyError(f"Note '{title}' not found")

        if new_title:
            if not Note.validate_title(new_title):
                raise ValueError("Note title cannot be empty.")
            del self.data[title]
            note.title = new_title.strip()
            self.add_note(note)

        if new_content:
            if not Note.validate_content(new_content):
                raise ValueError("Note content cannot be empty.")
            note.content = new_content.strip()

        if new_tags is not None:
            note.tags = [t.strip().lower() for t in new_tags if t.strip()]

    def search(self, query):
        """Searches notes by keyword (title, content, or tag)."""
        query_lower = query.lower()
        results = []

        for note in self.data.values():
            # Search by title
            if query_lower in note.title.lower():
                results.append(note)
            # Search by content
            elif query_lower in note.content.lower():
                results.append(note)
            # Search by tags
            elif any(query_lower in tag.lower() for tag in note.tags):
                results.append(note)

        return results

    def get_by_tag(self, tag):
        """Returns all notes with a specific tag."""
        tag_lower = tag.lower()
        return [note for note in self.data.values() if tag_lower in note.tags]
    