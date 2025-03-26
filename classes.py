"""
This script implements a contact management system using OOP principles.
It includes classes for storing and validating contact names and phone numbers,
and allows adding, editing, finding, and deleting contacts in an address book.
"""

from collections import UserDict
from dataclasses import dataclass            # Буду використовувати цей декоратор, щоб зменшити кількість коду

@dataclass
class Field:                                 # Змінила клас лише, щоб застосувати @dataclass
    value: str
    def __str__(self):
        return str(self.value)


@dataclass
class Name(Field):                           # Клас просто наслідує Field без змін
    pass


@dataclass
class Phone(Field):
    def __post_init__(self):                 # Забираємо телефон як value з класу Field та валідуємо його
        self.validate(self.value)

    def validate(self, value):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits.")
        if len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")


class Record:                                # Тут @dataclass не використовую, щоб вказати, щоб конкретизувати, що name приймає str, інакше перевірка з умови завдання не працює
    def __init__(self, name: str):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))     # Вказуємо, що введений рядок, це об'єкт класу Phone
    
    def remove_phone(self, phone: str):
        try:
            self.phones.remove(Phone(phone))
            return f"Phone {phone} was removed from contact {self.name.value}."
        except ValueError:
            return f"Phone {phone} not found in contact {self.name.value}."

    def edit_phone(self, old_phone: str, new_phone: str):
        for idx, p in enumerate(self.phones):          # Перебираємо номери телефонів, щоб знайти, що треба відредагувати (old_phone)
            if p == Phone(old_phone):
                self.phones[idx] = Phone(new_phone)    # Перезаписуємо старий номер на новий, якщо було співпадіння
                return f"Phone {old_phone} was updated to {new_phone} for contact {self.name.value}."
        return f"Phone {old_phone} not found in contact {self.name.value}."

    def find_phone(self, phone: str):
        if Phone(phone) in self.phones:
            return f"{self.name.value}: {phone}"
        return f"Phone {phone} not found for contact {self.name.value}."


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    def find(self, name: str):
        return self.data.get(name, f"No contact with the name {name} found.")

    def delete(self, name: str):
        if name in self.data:
            del self.data[name]
            return f"Contact {name} has been deleted."
        return f"No contact with the name {name} was found."
       

if __name__=='__main__':             # Перевірка взята з умови завдання
    book = AddressBook()

    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    book.add_record(john_record)

    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    book.add_record(jane_record)

    for name, record in book.data.items():
        print(record)

    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")

    print(john)

    found_phone = john.find_phone("5555555555")
    print(f"{john.name}: {found_phone}")

    book.delete("Jane")