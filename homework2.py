import requests
import json
import transliterate
from bs4 import BeautifulSoup
import lxml
import pandas as pd

header = {
    'USER-AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.135 YaBrowser/21.6.2.855 Yowser/2.5 Safari/537.36 '
}

all_vacancies = []


# Функция, которая добавляет новые элементы в словарь
def vac(name, salary, link):
    for num, item in enumerate(name):
        all_vacancies.append(
            {
                'Name': item,
                'Salary': salary[num],
                'Link': link[num]
            }
        )


# Функция, которая создает bs4 элементы
def parse(url):
    request = requests.get(url, headers=header)
    soup = BeautifulSoup(request.text, 'lxml')
    return soup


# Пользователь вводит откуда и сколько страниц парсить
pages = int(input('Сколько страниц смотрим: '))
source = input('Откуда смотрим (superjob/hh): ')

# Superjob

if source == 'superjob':
    # Пользователь вводит интересующую профессию
    # Ньюанс. Используя библиотеку transliterate чтобы преобразовать кирилицу в латиницу, не использовать такие буквы
    # как: я, ц, ь, ъ. Словарь не совпадает с superjob
    position = input('Введите должность с мал. буквы (если есть пробел, то вместо него поставьте "-"): ')
    position = transliterate.translit(position, reversed=True)
    a = 1

    # Пагинация
    for page in range(1, pages + 1):
        url = f'https://ufa.superjob.ru/vakansii/{position}.html?page={a}'
        a += 1
    # Создаем соуп элемент главной страницы
        soup = parse(url)
    # Извлекаем оттуда нужную информацию
        name = [i.text for i in soup.select('div._1h3Zg a')]
        salary = [i.text.strip() for i in soup.select('div.jNMYr span._1h3Zg')]
        link = ['https://www.superjob.ru' + i['href'] for i in soup.select('div._1h3Zg a')]
    # Редактируем список salary (убираем слово месяц и меняем кодировку пробела на пробел)
        for i in salary:
            if i == 'месяц':
                salary.remove(i)
        salary = [el.replace('\xa0', ' ') for el in salary]
    # Добавляем нужные элементы в словарь список all_vacancies
        vac(name, salary, link)

# HH
else:

    position = input('Введите должность с мал. буквы (если есть пробел, то вместо него поставьте "_"): ')
    position = transliterate.translit(position, reversed=True)
    a = 0
    # Пагинация
    for page in range(1, pages + 1):
        url = f'https://ufa.hh.ru/vacancies/{position}?page={a}'
        a += 1
        soup = parse(url)
    # Забираем нужную информацию
        name = [i.text for i in soup.select('div.vacancy-serp-item__info span a')]
        link = [i['href'] for i in soup.select('span.g-user-content a.bloko-link')]
    # На hh с зарплатой сложнее, на главной странице з/п может быть не указана, поэтому я брал з/п, заходя на каждую
    # страницу вакансии
        salary = []

        for i in link:
            soup = parse(i)
            a = soup.find('p', class_='vacancy-salary')
            if not a:
                salary.append('З/П не указана')
            else:
                salary.append(a.text)
        salary = [el.replace('\xa0', ' ') for el in salary]
        salary = [el.replace('на руки', '') for el in salary]
    # Добавляем нужные элементы в словарь список all_vacancies
        vac(name, salary, link)

# Запись финального списка в файл vacancies.csv
pd.DataFrame(all_vacancies).to_csv('vacancies.csv')