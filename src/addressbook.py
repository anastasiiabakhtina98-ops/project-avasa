"""AddressBook class for managing contacts."""

from collections import UserDict
from datetime import datetime, timedelta
from src.config import DATE_FORMAT


class AddressBook(UserDict):
    """Class representing the address book."""

    def add_record(self, record):
        """Adds a record to the address book."""
        self.data[record.name.value] = record

    def find(self, name):
        """Finds a record by name."""
        return self.data.get(name)

    def delete(self, name):
        """Deletes a record by name."""
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError(f"Contact '{name}' not found")

    def get_birthdays_in_days(self, days: int):
        """Returns contacts with birthday exactly in `days` days from today."""
        if days < 0:
            raise ValueError("Number of days cannot be negative.")
        today = datetime.today().date()
        target_date = today + timedelta(days=days)
        result = []
        for record in self.data.values():
            if not record.birthday:
                continue
            bday = record.birthday.value.date()
            bday_this_year = bday.replace(year=today.year)
            if bday_this_year < today:
                bday_this_year = bday_this_year.replace(year=today.year + 1)
            if bday_this_year == target_date:
                date = bday_this_year
                wd = date.weekday()
                if wd == 5:  # Saturday -> Monday
                    date += timedelta(days=2)
                elif wd == 6:  # Sunday -> Monday
                    date += timedelta(days=1)
                result.append({
                    "name": record.name.value,
                    "congratulation_date": date.strftime(DATE_FORMAT)
                })
        result.sort(key=lambda x: x["name"])
        return result

    def get_upcoming_birthdays(self):
        """Keeps backward compatibility — returns birthdays in 7 days."""
        return self.get_birthdays_in_days(7)

    def search(self, query):
        """Searches contacts by name, phone, email, address, or birthday."""
        found_records = []
        query_lower = query.lower()

        for record in self.data.values():
            # Search by name
            if query_lower in record.name.value.lower():
                found_records.append(record)
                continue

            # Search by phone
            phone_found = False
            for phone in record.phones:
                if query_lower in phone.value:
                    found_records.append(record)
                    phone_found = True
                    break

            if phone_found:
                continue

            # Search by email
            if record.email and query_lower in record.email.value.lower():
                found_records.append(record)
                continue

            # Search by address
            if record.address and query_lower in record.address.value.lower():
                found_records.append(record)
                continue

            # Search by birthday
            if (record.birthday and
                    query_lower in record.birthday.value.strftime(DATE_FORMAT)):
                found_records.append(record)

        return found_records