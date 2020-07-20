from bs4 import BeautifulSoup as bs
import requests
import re
import json

vacancy_for_search = 'Системный администратор'
page = 1
main_link = 'https://russia.superjob.ru'
vacancies = []

while True:
    params = {'keywords': vacancy_for_search,
              'page': page}
    response = requests.get(main_link + '/vacancy/search/', params=params)
    soup = bs(response.text,'lxml')
    vacancy_list = soup.find_all('div', {'class':'iJCa5 f-test-vacancy-item _1fma_ _1JhPh _2gFpt _1znz6 _2nteL'})
    pages_list = soup.find_all('span',{'class': 'qTHqo _1mEoj _2h9me DYJ1Y _2FQ5q _2GT-y'})

    for vacancy in vacancy_list:
        vacancy_data = {}
        vacancy_data['vacancy'] = vacancy.find('a', {'class': 'icMQ_'}).getText()
        vacancy_data['url'] = main_link + vacancy.find('a', {'class': 'icMQ_'})['href']
        salary = vacancy.find('span', {'class': '_3mfro'}).getText()


        def salaries(salary):
            min_sal = None
            max_sal = None
            curr = None
            salary = ''.join(salary.split('\xa0'))

            if salary[:2] == 'По':
                pass
            elif salary[:2] == 'до':
                max_sal = int(re.findall(r'(\d+)', salary)[0])
                curr = re.findall(r'до\d+(\w+)', salary)[0]
            elif salary[:2] == 'от':
                min_sal = int(re.findall(r'(\d+)', salary)[0])
                curr = re.findall(r'от\d+(\w+)', salary)[0]
            elif '—' in salary:
                min_sal = int(re.findall(r'(\d+)—', salary)[0])
                max_sal = int(re.findall(r'—(\d+)', salary)[0])
                curr = re.findall(r'\d+—\d+(\w+)', salary)[0]
            else:
                min_sal = int(re.findall(r'(\d+)', salary)[0])
                max_sal = min_sal
                curr = re.findall(r'\d+(\w+)', salary)[0]

            return min_sal, max_sal, curr


        min_sal, max_sal, curr = salaries(salary)
        vacancy_data['min_salary'] = min_sal
        vacancy_data['max_salary'] = max_sal
        vacancy_data['currency'] = curr
        vacancy_data['vacancy_from'] = main_link

        vacancies.append(vacancy_data)

    page += 1
    if pages_list[-1].find('span', {'class': '_3IDf-'}).getText() != 'Дальше':
        break

with open('superjob_vacancies.json', 'w') as f:
    json.dump(vacancies, f)
