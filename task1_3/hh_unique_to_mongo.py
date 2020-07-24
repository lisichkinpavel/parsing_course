from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import requests
import re
import json

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies_mng_db']
vacancies_mng = db.vacancies_mng

vacancy_for_search = 'программист'
page = 0
main_link = 'https://hh.ru'
vacancies = []


def salaries(salary_string):  # Преобразовывает строку с зарплатами и валютой
    min_sal = None
    max_sal = None
    curr = None
    salary_string = ''.join(salary_string.split('\xa0'))

    if salary_string[:2] == 'до':
        max_sal = int(re.findall(r'(\d+)', salary_string)[0])
        curr = re.findall(r'до \d+ (\w+)', salary_string)[0]
    elif salary_string[:2] == 'от':
        min_sal = int(re.findall(r'(\d+)', salary_string)[0])
        curr = re.findall(r'от \d+ (\w+)', salary_string)[0]
    elif '-' in salary_string:
        min_sal = int(re.findall(r'(\d+)-', salary_string)[0])
        max_sal = int(re.findall(r'-(\d+)', salary_string)[0])
        curr = re.findall(r'\d+-\d+ (\w+)', salary_string)[0]

    return min_sal, max_sal, curr


def duplicate_check(vacancy_dict):
    try:  # добавляем в бд документ из полученного словаря
        vacancies_mng.insert_one(vacancy_dict)
    except DuplicateKeyError:
        pass  # Если документ с таким id уже есть, переходим дальше


while True:
    params = {'L_save_area': True,
              'clusters': True,
              'enable_snippets': True,
              'showClusters': True,
              'search_field': 'name',
              'text': vacancy_for_search,
              'page': page}

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

    response = requests.get(main_link + '/search/vacancy', params=params, headers=headers)
    soup = bs(response.text, 'lxml')
    vacancy_list = soup.find_all('div', {'class': 'vacancy-serp-item'})

    for vacancy in vacancy_list:
        vacancy_data = {}
        url = vacancy.find('a', {'class': 'bloko-link'})['href']
        vacancy_data['_id'] = int(re.findall(r'/(\d+)', url)[0])  # уникальный id вакансии
        vacancy_data['vacancy'] = vacancy.find('div', {'class': 'vacancy-serp-item__info'}).getText()
        vacancy_data['url'] = url
        salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()
        next_button = soup.find_all('a', {'class': 'bloko-button', 'data-qa': 'pager-next'})

        min_sal, max_sal, curr = salaries(salary)

        vacancy_data['min_salary'] = min_sal
        vacancy_data['max_salary'] = max_sal
        vacancy_data['currency'] = curr
        vacancy_data['vacancy_from'] = main_link

        vacancies.append(vacancy_data)  # список заполняем всеми вакансиями, даже дублирующимися

        duplicate_check(vacancy_data)  # в БД добавляем уникальные записи
    print(page + 1)
    page += 1

    if not next_button:
        break

with open('hh_vacancies.json', 'w') as f:
    json.dump(vacancies, f)

print(f'Всего вакансий: {len(vacancies)}')
print(f'Уникальные вакансии, записанные в БД: {db.vacancies_mng.count_documents({})}')
