from ClassesAddressBook import AddressBook, Record
import pickle

def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()                        
    
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "No such name found"
        except IndexError:
            return "Not found"
        except Exception:
            return "Error"
        
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, phone = args
    if name in book:
        book[name] = phone
        return "Contact updated."
    else:
        return "Contact not found."

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    if name in book:
        return book[name]
    else:
        return "Contact not found."

@input_error    
def show_all(book: AddressBook):
    if len(book) == 0:
        return "No contacts found."
    else:
        return "\n".join([f"{name}: {phone}" for name, phone in book.items()])

@input_error     
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.data.get(name)
    print(record.name)
    if record is None:
        return "Contact not found."
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        return "Contact not found."
    if not record.birthday:
        return "Birthday not available."
    return record.birthday.value

@input_error                                                    
def show_upcoming_birthdays(book: AddressBook):
    birthdays = book.get_upcoming_birthdays()
    if not birthdays:
        return "Birthday not"
    result = ""
    for el in birthdays:
        result += f"name: {el.get('name')} - date: {el.get('congratulation_date')}"
    return birthdays
        
def main(): 

    book = load_data()

    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(book))
        elif command == "add-birthday":         
            print(add_birthday(args, book))
        elif command == "show-birthday":        
            print(show_birthday(args, book))
        elif command == "birthdays":                       
            print(show_upcoming_birthdays(book))
        else:
            print("Invalid command.")

    save_data(book)  
  
if __name__ == "__main__":
    main()