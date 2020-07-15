# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import requests
import json

key = 'Iauj4k413w8jnan7xykibj4yVUbrcVBSE19abBGY'
service = 'https://api.nasa.gov/planetary/apod'     # service provide Astronomy Picture of the Day
parameters = {
    'date': '2020-07-10',
    'hd': False,
    'api_key': key
}

responce = requests.get(service, params=parameters)
if responce.ok:
    data = responce.json()
    pic_title = f"{data['title']}.jpg"
    pic_url = data['url']
    with open(pic_title, 'wb') as f:                 # save picture
        f.write(requests.get(pic_url).content)
    with open('responce_out.json', 'w') as f:        # save responce
        json.dump(data, f, indent=2)
