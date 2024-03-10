from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, value):      
        if len(value) != 0:
            super().__init__(value)
        else:
            raise ValueError ("Incorrect Name!")
        
class Phone(Field):
    def __init__(self, value):      
        if len(value) == 10:
            super().__init__(value)
        else:
            raise ValueError ("Incorrect Phone!")
        
class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, '%d.%m.%Y')
            self.value = value                                                  
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
		
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None        

    def add_phone(self, phone):
        self.phones.append(Phone(phone))
                
    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
    
    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                    
    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
    
    def add_birthday(self, birthday):           
        self.birthday = Birthday(birthday)                             
        
    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
    
    def find (self, name):
        return self.data.get(name)
            
    def delete(self, name):
        if name in self.data:
            record = self.data[name]
            for phone in record.phones:
                record.remove_phone(phone.value)
            del self.data[name]
            print(f"Запис {name} видалено")
        else:
            print(f"Запис {name} не знайдено")

    def get_upcoming_birthdays(self):

        today = datetime.today()
        upcoming_birthdays = []

        for record in self.data.values():
            birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y")
            birthday_this_year = birthday.replace(year=today.year)
            
            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            days_until_birthday = (birthday_this_year - today).days

            if days_until_birthday <= 7:
                if birthday_this_year.weekday() == 5:
                    birthday_this_year += timedelta(days=+2)
                elif birthday_this_year.weekday() == 6:
                    birthday_this_year += timedelta(days=+1)           

                upcoming_birthdays.append({"name": record.name.value, "congratulation_date": birthday_this_year.strftime("%d.%m.%Y")})

        return upcoming_birthdays















# # Створення нової адресної книги
# book = AddressBook()

# # Створення запису для John
# john_record = Record("John")
# john_record.add_phone("1234567890")
# john_record.add_phone("5555555555")

# # Додавання запису John до адресної книги
# book.add_record(john_record)

# # Створення та додавання нового запису для Jane
# jane_record = Record("Jane")
# jane_record.add_phone("9876543210")
# book.add_record(jane_record)

# # Виведення всіх записів у книзі
# for name, record in book.data.items():
#     print(record)

# # Знаходження та редагування телефону для John
# john = book.find("John")
# john.edit_phone("1234567890", "1112223333")

# print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

# # Пошук конкретного телефону у записі John
# found_phone = john.find_phone("5555555555")
# print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

# # Видалення запису Jane
# book.delete("Jane")