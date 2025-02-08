from collections import UserDict


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return f"{e} error"
            
    return inner

class WrongFormatOfField(Exception):
    def __init__(self, message="Wrong format of field"):
        self.message = message
        super().__init__(self.message)

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def __eq__(self, other):
        if isinstance(other, Field):
            return self.value == other.value
        return False

class Name(Field):
    pass


class Phone(Field):
     def __init__(self, value):
        if len(value) == 10 and value.isdecimal():
            super().__init__(value)
        else:
             raise WrongFormatOfField("The phone number should contain 10 numeric characters")

class Record:
    def __init__(self, name, phones = []):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones]

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        if phone in self.phones:
            self.phones.remove(phone)
        else:
            raise ValueError(f"Phone number {phone} not found")

    def edit_phone(self, old_number, new_number):
        self.add_phone(new_number)
        self.remove_phone(self.find_phone(old_number))

    def find_phone(self, number):
        return next((phone for phone in self.phones 
                     if phone == Phone(number)), None)
    
    def __str__(self):
        return f"Contact: {self.name}, tel.: {self.phones}"


class AddressBook(UserDict):
    def __init__(self, path):
        self.path = path
        self.data = {}
        with open(self.path, "r", encoding="utf-8") as file:
            lines = [el.strip() for el in file.readlines()]
            for line in lines:
                name, numbers = line.split(",")
                self.data[name] = Record(name,[number.strip() for number in numbers.split(";")])
    
    def add_record(self, record: Record):
        if not str(record.name) in self.data.keys():
            self.data[str(record.name)] = record
            with open(self.path,"a",encoding="utf-8") as file:
                file.write(f"{record.name},{'; '.join(map(str, record.phones))}\n")
        else:
            raise ValueError("Record with this name already exists")
        
    def update_record(self, record:Record):
        if str(record.name) in self.data.keys():
            self.data[str(record.name)] = record
        else:
            raise ValueError(f"Record {record.name} not found")
        
    def find(self, name):
        if name in self.data.keys():
            return self.data[name]
        else:
             raise ValueError(f"Record {name} not found")
        
    
    def check_record(self, record):
        return record in self.data.keys()

    def delete(self, name):
        if name in self.data.keys():
            del self.data[name]
        else:  
            raise KeyError(f"Record {name} not found")
        
    def save_records(self):
        with open(self.path,"w",encoding="utf-8") as file:
            for key, value in self.data.items():
                file.write(f"{key},{'; '.join(map(str, value.phones))}\n")
    
    def __str__(self):
        return [f"{value}" for key,value in self.data]


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split(" ")
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, contacts:AddressBook):
    name, phone = args
    if contacts.check_record(name):
        record = contacts.find(name)
        record.add_phone(phone)
        contacts.update_record(record)
        contacts.save_records()
        return "Contact updated"
    record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, contacts:AddressBook):
    name, old_phone, new_phone = args
    record = contacts.find(name)
    record.edit_phone(old_phone, new_phone)
    contacts.update_record(record)
    contacts.save_records()
    return "Contact changed."


@input_error
def show_phone(args, contacts:AddressBook):
    name = args[0]
    record = contacts.find(name)
    return f"tel: {'; '.join(map(str, record.phones))}"


@input_error
def show_all(contacts):
    listOfContacts = list()
    for key, record in contacts.items():
       listOfContacts.append(f"{key}, tel: {'; '.join(map(str, record.phones))}")
    return listOfContacts


def main():
    contacts = AddressBook("contacts.txt")
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
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            listOfContacts = show_all(contacts)
            for item in listOfContacts:
                print(item)
        elif command == "help":
            print("'close', 'exit' to stop the program")
            print("'add' to create new contact")
            print("'change' to change a contact")
            print("'phone' to see a phone number of person")
            print("'all' to print all contacts")
        else:
            print("Invalid command.")
            print("Try 'help' command")

if __name__ == "__main__":
    main()


