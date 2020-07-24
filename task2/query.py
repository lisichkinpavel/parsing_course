from pymongo import MongoClient
from pprint import pprint
import json

client = MongoClient('127.0.0.1', 27017)
db = client['vacancies_db']
vacancies = db.vacancies

with open('hh_vacancies.json', 'r') as f:
    vacancies_data = json.load(f)

vacancies.insert_many(vacancies_data)


def search_by_salary(salary):
    for vacancy in vacancies.find({'$or': [{'max_salary': {'$gt': salary}}, {'min_salary': {'$gt': salary}}]},
                                  {'vacancy': 1, 'min_salary': 1, 'max_salary': 1, 'url': 1, '_id': 1}):
        pprint(vacancy)


search_by_salary(100000)
