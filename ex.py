import json

with open('test.json', 'rt', encoding='UTF8') as f:
    email = json.load(f)

email_list = []

for i in email['omnidoc']:
    contact = i['contact']
    for j in contact:
        email_list.append(j.get('email'))

email_list = list(set(email_list))

print(email_list)