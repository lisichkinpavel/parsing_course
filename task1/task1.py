# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для
# конкретного пользователя, сохранить JSON-вывод в файле *.json.
import requests
import json

service = 'https://api.github.com'
user_name = 'octocat'
responce = requests.get(f'{service}/users/{user_name}/repos')
if responce.ok:
    data = responce.json()
    with open('repos.json', 'w') as f:                              # save full responce to .json
        json.dump(data, f, indent=2)
    for i in range(len(data)):                                      # output just repositories names and it's urls
        print(f'{i+1}){data[i]["name"]}, url:{data[i]["html_url"]}')
else:
    print('Responce is NOT ok!')