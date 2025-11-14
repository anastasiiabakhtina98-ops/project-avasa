"""Note class for representing a single note."""


class Note:
    """Class representing a single note."""

    def __init__(self, title, content, tags=None):
        if not self.validate_title(title):
            raise ValueError("Note title cannot be empty.")
        if not self.validate_content(content):
            raise ValueError("Note content cannot be empty.")

        self.title = title.strip()
        self.content = content.strip()
        self.tags = [t.strip().lower() for t in tags if t.strip()] if tags else []

    @staticmethod
    def validate_title(value):
        """Validates that title is not empty."""
        return isinstance(value, str) and len(value.strip()) > 0

    @staticmethod
    def validate_content(value):
        """Validates that content is not empty."""
        return isinstance(value, str) and len(value.strip()) > 0

    def to_dict(self):
        """Convert Note object to dict."""
        return {
            "title": self.title,
            "content": self.content,
            "tags": self.tags
        }

    @classmethod
    def from_dict(cls, data):
        """Create object Note from dict."""
        return cls(data["title"], data["content"], data.get("tags", []))

    def __str__(self):
        """Returns formatted string representation of the note."""
        tags_str = f"[{', '.join(self.tags)}]" if self.tags else "[no tags]"
        return f"{self.title}\n  📝 {self.content}\n  {tags_str}"