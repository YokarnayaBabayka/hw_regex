from pprint import pprint
import re

# читаем адресную книгу в формате CSV в список contacts_list
import csv

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
# pprint(contacts_list)

# Сохраняем заголовки 
headers = contacts_list[0]


# Приводим имена к надлежащему виду:
for i in contacts_list:
    full_name = " ".join(i[:3])
    i[0] = full_name.split()[0]
    i[1] = full_name.split()[1]
    if len(full_name.split()) == 3:
        i[2] = full_name.split()[2]
    

# Объединение повторяющихся контактов
result_contacts_list = []
for i in contacts_list:
    for j in contacts_list:
        if " ".join(i[:2]) == " ".join(j[:2]) and " ".join(i) != " ".join(j):
            person = []
            for k in range(7):
                if i[k] == j[k]:
                    person.append(i[k])
                elif i[k] != j[k] and j[k] == "":
                    person.append(i[k])
                elif i[k] != j[k] and i[k] == "":
                    person.append(j[k])
            if person in result_contacts_list:
                continue
            else:
                result_contacts_list.append(person)

                
#  Создаем временный список из фамилий и имен (критерий уникальности)
temp_list = []
for i in contacts_list[1:]:
    temp_list.append(" ".join(i[:2]))


#  Добавляем в результирующий список уникальные записи
for i in contacts_list:
    if temp_list.count(" ".join(i[:2])) == 1:
        result_contacts_list.append(i)


#  Приводим запись телефона в надлежащий вид
pattern = r'\+?(\d)\s?\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})'
for i in result_contacts_list:
    i[5] = re.sub(pattern, r'+7(\2)\3-\4-\5', i[5])


#  Приводим запись доб. телефона в надлежащий вид
pattern = r'\(?доб.\s(\d{4})\)?'
for i in result_contacts_list:
    i[5] = re.sub(pattern, r'доб.\1', i[5])


#  Добавляем заголовки
result_contacts_list[0] = headers
pprint(result_contacts_list)

# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  # Вместо contacts_list подставьте свой список
  datawriter.writerows(result_contacts_list)
