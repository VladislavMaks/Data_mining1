import requests
import json

# 1) Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

header = {
    'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36 '
}

user = 'VladislavMaks'

url = f'https://api.github.com'

request = requests.get(f'{url}/users/{user}/repos', headers=header)

a = []

for i in request.json():
    a.append(i['name'])

with open('repos.json', 'w') as f:
    json.dump(a, f)

for i in a:
    print(i)

# 2) Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему,
# пройдя авторизацию. Ответ сервера записать в файл.

header = {
    'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36 '
}

# Я нашел сервис, который требует авторизацию с помощью API Key

APIKey = '0ac5ded4-edf9-4420-ac88-2870bb452304'

url = 'https://holidayapi.com'

request = requests.get(f'{url}/v1/holidays?pretty&key={APIKey}&country=RU&year=2020', headers=header)

holidays = []

for i in request.json()['holidays']:
    holidays.append(i['name'])

with open('holidays.json', 'w') as f:
    json.dump(holidays, f)
