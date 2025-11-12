import json
import os

# -----------------------------
# Console NoteBook App
# Features: add, view, search, edit, delete, sort notes by tags
# -----------------------------

class NoteBook:
    def __init__(self, filename="notes.json"):
        self.filename = filename
        self.notes = self.load_notes()

    # ---------- Data Handling ----------
    def load_notes(self):
        """Load notes from a JSON file."""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def save_notes(self):
        """Save all notes to a JSON file."""
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.notes, f, indent=4, ensure_ascii=False)

    # ---------- Core Features ----------
    def add_note(self, title, content, tags):
        """Add a new note with title, content, and tags."""
        note = {
            "title": title.strip(),
            "content": content.strip(),
            "tags": [t.strip().lower() for t in tags if t.strip()]
        }
        self.notes.append(note)
        self.save_notes()
        print("✅ Note added!")

    def view_notes(self):
        """List all notes and allow opening them in a loop."""
        if not self.notes:
            print("📭 No notes found.")
            return

        while True:
            print("\nAll notes:")
            for i, note in enumerate(self.notes, 1):
                tags = ", ".join(note["tags"])
                print(f"{i}. {note['title']}  [tags: {tags}]")

            choice = input("\nEnter note number/title to open (Enter or 'q' to return): ").strip()
            if not choice or choice.lower() == "q":
                break  # exit view mode

            # Determine if user entered number or title
            note = None
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(self.notes):
                    note = self.notes[index]
            else:
                note = next((n for n in self.notes if n["title"].lower() == choice.lower()), None)

            if note:
                tags = ", ".join(note["tags"])
                print(f"\n📝 {note['title']}  [tags: {tags}]\n{'-'*40}\n{note['content']}\n{'-'*40}")
                input("\nPress Enter to go back to the list...")
            else:
                print("❌ Note not found.")

    def search_notes(self, keyword):
        """Search for notes by keyword (title, content, or tag)."""
        keyword = keyword.lower()
        results = [
            n for n in self.notes
            if keyword in n["title"].lower()
            or keyword in n["content"].lower()
            or keyword in [t.lower() for t in n["tags"]]
        ]
        if results:
            print(f"\n🔎 Found {len(results)} note(s):")
            for note in results:
                tags = ", ".join(note["tags"])
                print(f"\n📝 {note['title']}  [tags: {tags}]\n{note['content']}")
        else:
            print("❌ No matching notes found.")

    def edit_note(self, title):
        """Edit a note by title."""
        for note in self.notes:
            if note["title"].lower() == title.lower():
                new_title = input("New title (Enter to keep): ").strip()
                new_content = input("New content (Enter to keep): ").strip()
                new_tags = input("New tags (comma-separated, Enter to keep): ").strip()

                if new_title:
                    note["title"] = new_title
                if new_content:
                    note["content"] = new_content
                if new_tags:
                    note["tags"] = [t.strip().lower() for t in new_tags.split(",") if t.strip()]

                self.save_notes()
                print("✏️ Note updated!")
                return
        print("❌ Note not found.")

    def delete_note(self, title):
        """Delete a note by title."""
        for note in self.notes:
            if note["title"].lower() == title.lower():
                self.notes.remove(note)
                self.save_notes()
                print("🗑️ Note deleted!")
                return
        print("❌ Note not found.")

    def sort_by_tag(self):
        """Sort and display notes alphabetically by their first tag."""
        sorted_notes = sorted(self.notes, key=lambda n: n["tags"][0] if n["tags"] else "")
        for i, note in enumerate(sorted_notes, 1):
            tags = ", ".join(note["tags"])
            print(f"{i}. {note['title']}  [tags: {tags}]")

# -----------------------------
# Console Interface
# -----------------------------
def main():
    nb = NoteBook()

    while True:
        print("\n--- 📒 NoteBook Menu ---")
        print("1. Add note")
        print("2. View notes (list + open mode)")
        print("3. Search notes")
        print("4. Edit note")
        print("5. Delete note")
        print("6. Sort notes by tags")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            title = input("Note title: ")
            content = input("Note content: ")
            tags = input("Tags (comma-separated): ").split(",")
            nb.add_note(title, content, tags)

        elif choice == "2":
            nb.view_notes()

        elif choice == "3":
            keyword = input("Enter keyword or tag: ")
            nb.search_notes(keyword)

        elif choice == "4":
            title = input("Enter note title to edit: ")
            nb.edit_note(title)

        elif choice == "5":
            title = input("Enter note title to delete: ")
            nb.delete_note(title)

        elif choice == "6":
            nb.sort_by_tag()

        elif choice == "0":
            print("👋 Goodbye!")
            break

        else:
            print("❗ Invalid choice, try again.")

if __name__ == "__main__":
    main()
