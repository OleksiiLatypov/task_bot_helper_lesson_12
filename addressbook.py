from collections import UserDict
from datetime import datetime
import pickle


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if len(value) != 10:
            raise ValueError('Length of phone must be 10 digits')
        if not value.isnumeric() or not value.startswith('0'):
            raise ValueError('Wrong phones.')
        self._value = value


class Birthday(Field):
    @Field.value.setter
    def value(self, value):
        today = datetime.now().date()
        birth_date = datetime.strptime(value, '%Y.%m.%d').date()
        if birth_date > today:
            raise ValueError("Wrong birthday. Please check date.")
        self._value = value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def get_info(self):
        phone_number = ' '
        birth_info = ' '

        for phone in self.phones:
            phone_number += f'{phone.value}, '

        if self.birthday:
            birth_info = f'(Birthday: {self.birthday.value})'

        return f'{self.name.value.title()}: {phone_number[:-2]}; {birth_info}'

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, data):
        self.birthday = (Birthday(data))

    def days_to_next_birthday(self):
        if not self.birthday:
            raise ValueError('Birthday not found')
        today = datetime.now().date()
        birth_date = datetime.strptime(self.birthday.value, '%Y.%m.%d').date()
        data = datetime(year=datetime.today().year, month=birth_date.month, day=birth_date.day).date()
        if data < today:
            data = datetime(year=datetime.today().year + 1, month=birth_date.month, day=birth_date.day).date()
            return (data - today).days
        return (data - today).days

    def delete_phone(self, phone):
        for record_phone in self.phones:
            if record_phone.value == phone or f'{record_phone.value}, ' == phone:
                self.phones.remove(record_phone)
                return True
        return False

    def change_phones(self, phones):
        for phone in phones:
            if not self.delete_phone(phone):
                self.add_phone(phones)
                break

    def update_phone(self, new_phone):
        self.phones.clear()
        self.phones.append(Phone(new_phone))


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.load_data()

    def add_record(self, record):
        self.data[record.name.value] = record

    def get_all_record(self):
        return self.data

    def has_record(self, name):
        return bool(self.data.get(name))

    def get_record(self, name):
        return self.data.get(name)

    def remove_record(self, name):
        del self.data[name]

    def search(self, value):
        record_result = []
        for record in self.get_all_record().values():
            if value in record.name.value:
                record_result.append(record)
                continue

            for phone in record.phones:
                if value in phone.value:
                    record_result.append(record)
        if not record_result:
            raise ValueError('Contact does not exist')
        return record_result

    def iterator(self, amount_of_records=5):
        page = []
        counter = 0
        for record in self.data:
            page.append(self.data[record])
            counter += 1

            if counter == amount_of_records:
                yield page
                page = []
                counter = 0
        if page:
            yield page

    def save_to_file(self):
        with open('addressbook.pickle', 'wb') as file:
            pickle.dump(self.data, file)

    def load_data(self):
        try:
            with open('addressbook.pickle', 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            pass






