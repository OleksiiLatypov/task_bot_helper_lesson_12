from addressbook import AddressBook, Record


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Enter Correct Name!'
        except ValueError as exception:
            return exception.args[0]
        except IndexError:
            return 'Bot: Please use whitespace when entering name and phone'
        except TypeError:
            return 'Wrong Command !'
    return wrapper


contacts = AddressBook()


@input_error
def hello():
    return f'Bot: Hello, how can I help you?'


@input_error
def add(user_input):
    if len(user_input.split()) != 3:
         raise ValueError('Please provide data info in format "add <name> <phone>" example add Harry 0999999999.')
    data = user_input.split()
    if data[1] in contacts:
        raise ValueError('Bot: This contact is already exist')
    record = Record(data[1])
    for phone in data[2:]:
        record.add_phone(phone)
    contacts.add_record(record)
    return f'Bot: You successfully added contacts'


@input_error
def birthday(user_input):
    if len(user_input.split()) != 5:
        raise ValueError('Please provide birthday info in format "birthday <name> <year month day>"/'
                         'example birthday Harry 1994 01 01')
    name = user_input.split()[1]
    data = '.'.join(user_input.split()[2:])
    record = contacts[name]
    record.add_birthday(data)
    return f'You added birthday for name {name.title()}'


@input_error
def days_to_birthday(user_input):
    name = user_input.split()[3]
    record = contacts[name]
    return f'{name.title()} has birthday after {record.days_to_next_birthday()} days'


@input_error
def show_all(user_input):
    if len(user_input.split()) != 2:
        raise ValueError('Please provide data info in format "show all".')
    all_contacts = 'List of contacts:\n'
    page_number = 1

    for page in contacts.iterator():
        all_contacts += f'Page #{page_number}\n'

        for record in page:
            all_contacts += f'{record.get_info()}\n'
        page_number += 1
    return all_contacts


@input_error
def change_addition(user_input):
    if len(user_input.split()) != 3:
        raise ValueError('Please provide data info in format "change <name> <phone>" example "change Harry 0999999999".')
    name, phones = user_input.split()[1], user_input.split()[2]
    record = contacts[name]
    record.change_phones(phones)
    return f'Additional phone {phones} with name {name.title()} was added'


@input_error
def update(user_input):
    if len(user_input.split()) != 3:
        raise ValueError('Please provide data info in format "update <name> <phone>" example "update Harry 0999999999".')
    name, new_phone = user_input.split()[1], user_input.split()[2]
    record = contacts[name]
    record.update_phone(new_phone)
    return f'Phone with name {name.title()} were updated to {new_phone}'


@input_error
def delete_phone_name(user_input):
    if len(user_input.split()) != 2 and ' '.join(user_input.split()[:2]) != 'delete phone':
        raise ValueError('Please provide data info in format "delete <name> <phone>" example "delete Harry".')
    name = user_input.split()[1]
    contacts.remove_record(name)
    return f'Success delete contact {name.title()}'


@input_error
def phone(user_input):
    if len(user_input.split()) != 2:
        raise ValueError('Please provide data info in format "phone <name>" example "phone Harry".')
    value = user_input.split()[1]
    return contacts.search(value).get_info()


@input_error
def delete_phone_number(user_input):
    phone, name = user_input.split()[3], user_input.split()[2]
    record = contacts[name]
    if record.delete_phone(phone):
        return f'Phone {phone} for {name} contact deleted.'
    return f'{name} contact does not have this number'


@input_error
def search_record(user_input):
    value = user_input.split()[1]
    search_records = ''
    records = contacts.search(value)
    for record in records:
        search_records += f'{record.get_info()}\n'
    return search_records


def wrong_input():
    return f'Bot: Wrong enter'


command = {
    'add': add,   # add new contact
    'hello': hello,  # hello func
    'show all': show_all,  # show list of all contacts
    'change': change_addition,  # addition of extra phone
    'phone': phone,  # find contact number using name
    'wrong_input': wrong_input,  # func to process wrong input
    'delete': delete_phone_name,  # delete contact using name
    'delete phone': delete_phone_number,  # delete phone number
    'update': update,  # remove old phone and create new for contact
    'birthday': birthday,  # add birthday to contact
    'days to birthday':  days_to_birthday,  # to find amount of days to next birthday
    'search': search_record
}


def main():
    key_words = ['good bye', 'bye', 'close', 'thank you', 'exit']
    try:
        while True:
            user_input = input('User: ').lower()
            if user_input.split()[0] == 'hello':
                print(command[user_input.split()[0]]())
            if user_input.split()[0] == 'add':
                print(command[user_input.split()[0]](user_input))
            if ' '.join(user_input.split()[:2]) == 'show all':
                print(command[' '.join(user_input.split()[:2])](user_input))
            if user_input.split()[0] == 'change':
                print(command[user_input.split()[0]](user_input))
            if user_input.split()[0] == 'update':
                print(command[user_input.split()[0]](user_input))
            if user_input.split()[0] == 'phone':
                print(command[user_input.split()[0]](user_input))
            if user_input.split()[0] == 'delete':
                print(command[user_input.split()[0]](user_input))
            if ' '.join(user_input.split()[:2]) == 'delete phone':
                print(command[' '.join(user_input.split()[:2])](user_input))
            if user_input.split()[0] == 'birthday':
                print(command[user_input.split()[0]](user_input))
            if ' '.join(user_input.split()[:3]) == 'days to birthday':
                print(command[' '.join(user_input.split()[:3])](user_input))
            if user_input.split()[0] == 'search':
                print(command[user_input.split()[0]](user_input))

            if (user_input.split()[0] not in key_words and user_input.split()[0] not in command)\
                    and (' '.join(user_input.split()[:2]) not in key_words and ' '.join(user_input.split()[:2]) not in command)\
                    and (' '.join(user_input.split()[:3]) not in key_words and ' '.join(user_input.split()[:3]) not in command):
                print(wrong_input())

            if user_input in key_words:
                print(f'Bot: Goodbye see you next time')
                break
    finally:
        contacts.save_to_file()


if __name__ == '__main__':
    main()