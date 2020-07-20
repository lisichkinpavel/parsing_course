from bs4 import BeautifulSoup as bs
import requests
import re
import json

vacancy_for_search = 'Системный администратор'
page = 0
main_link = 'https://hh.ru'
params = {'L_is_autosearch': False,
          'area': 113,
          'clusters': True,
          'enable_snippets': True,
          'search_field': 'name',
          'text': vacancy_for_search,
          'page': page}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

response = requests.get(main_link + '/search/vacancy', params=params, headers=headers)
soup = bs(response.text, 'lxml')
vacancy_list = soup.find_all('div', {'class': 'vacancy-serp-item'})


vacancies = []

for vacancy in vacancy_list:
    vacancy_data = {}
    vacancy_data['vacancy'] = vacancy.find('div', {'class': 'vacancy-serp-item__info'}).getText()
    vacancy_data['url'] = vacancy.find('a', {'class': 'bloko-link'})['href']
    salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()


    def salaries(salary):
        min_sal = None
        max_sal = None
        curr = None
        salary = ''.join(salary.split('\xa0'))

        if salary[:2] == 'до':
            max_sal = int(re.findall(r'(\d+)', salary)[0])
            curr = re.findall(r'до \d+ (\w+)', salary)[0]
        elif salary[:2] == 'от':
            min_sal = int(re.findall(r'(\d+)', salary)[0])
            curr = re.findall(r'от \d+ (\w+)', salary)[0]
        elif '-' in salary:
            min_sal = int(re.findall(r'(\d+)-', salary)[0])
            max_sal = int(re.findall(r'-(\d+)', salary)[0])
            curr = re.findall(r'\d+-\d+ (\w+)', salary)[0]

        return min_sal, max_sal, curr


    min_sal, max_sal, curr = salaries(salary)
    vacancy_data['min_salary'] = min_sal
    vacancy_data['max_salary'] = max_sal
    vacancy_data['currency'] = curr
    vacancy_data['vacancy_from'] = main_link

    vacancies.append(vacancy_data)

with open('hh_vacancies.json', 'w') as f:
    json.dump(vacancies, f)


