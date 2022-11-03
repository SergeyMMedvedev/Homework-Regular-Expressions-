from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
# pprint(contacts_list)

contacts_list_dict = {}

def merge_contacts(row1, row2):
    result = []
    for value1, value2 in zip(row1, row2):
        result += [value1] if value1 else [value2]
    return result


for i, contact in enumerate(contacts_list):
    full_name = []
    for el in contact[:2]:
        full_name += el.split()
    contact[:3] = full_name[:3]

    name_key = (contact[0], contact[1])
    duplicate = contacts_list_dict.get(name_key)
    if duplicate:
        contacts_list_dict[name_key] = merge_contacts(contact, duplicate)
    else:
        contacts_list_dict[name_key] = contact


with open("phonebook.csv", "w", encoding='utf-8') as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(contacts_list_dict.values())