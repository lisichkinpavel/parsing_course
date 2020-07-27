from pprint import pprint
from pymongo import MongoClient
from lxml import html
import requests
import re

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/84.0.4147.89 Safari/537.36'}
main_link = 'https://news.mail.ru'

response = requests.get(main_link, headers=header)
dom = html.fromstring(response.text)

link = dom.xpath("//table[@class = 'daynews__inner']//td[position()<3]//@href")
link.extend(dom.xpath("//ul[@class='list list_type_square list_half js-module']/li[position()>2]//@href"))

# Некоторые новости на мэйлру имеют относительные ссылки, поэтому нужно привести их к нормальному виду.
# Ссылки на новсоти с других источников абсолютные, их оставляем как есть.
result_link = [main_link + i if i[0] == '/' else i for i in link]

text = dom.xpath(
    "//span[@class = 'photo__title photo__title_new photo__title_new_hidden js-topnews__notification']/text()")
text.extend(dom.xpath("//ul[@class='list list_type_square list_half js-module']/li[position()>2]//text()"))

# Удвляем лишние символы
result_text = [s.replace('\xa0', ' ') for s in text]


# Функция для обработки даты и ресурса новости из запроса
def date_source(url):
    date_source_response = requests.get(url, headers=header)
    date_source_dom = html.fromstring(date_source_response.text)

    get_date = date_source_dom.xpath("//span[@class='note__text breadcrumbs__text js-ago']/@datetime")[0]
    get_source = date_source_dom.xpath("//span[@class='breadcrumbs__item']//span[@class='link__text']/text()")[0]
    return re.findall(r'(\d+-\d+-\d+)', get_date)[0], get_source


result_date = []
result_source = []

for i in result_link:
    news_date, news_source = date_source(i)
    result_date.append(news_date)
    result_source.append(news_source)


# В итоге получаем 4 списка из которых нужно собрать список словарей
mail_news = []

for i in range(len(result_link)):
    mail_news_dict = {}
    mail_news_dict['title'] = result_text[i]
    mail_news_dict['link'] = result_link[i]
    mail_news_dict['date'] = result_date[i]
    mail_news_dict['source'] = result_source[i]
    mail_news.append(mail_news_dict)


client = MongoClient('127.0.0.1', 27017)
db = client['news_db']
news = db.news
news.insert_many(mail_news)

pprint(mail_news)
