from pprint import pprint
from lxml import html
import requests
from datetime import date, timedelta
import re
from pymongo import MongoClient

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
main_link = 'https://yandex.ru/news'

response = requests.get(main_link, headers=header)
dom = html.fromstring(response.text)

items = dom.xpath("//div[@class='page-content__fixed']//tr[@class='stories-set__items-group']/td | //div[@class='story__content']")


ya_news = []

for item in items:
    ya_news_dict = {}
    title = item.xpath(".//h2//text()")[0]
    link = 'https://yandex.ru' + item.xpath(".//h2//@href")[0]

    # ресурс и время новости передаются в одной строке
    source_time = item.xpath(".//div[@class='story__date']/text()")[0]
    source = re.search(r'.*(?=вчера)|.*(?= \d)', source_time)
    if 'вчера' in source_time:
        news_date = date.today() - timedelta(days=1)
    else:
        news_date = date.today()

    ya_news_dict['title'] = title
    ya_news_dict['link'] = link
    ya_news_dict['date'] = news_date.strftime('%Y-%m-%d')
    ya_news_dict['source'] = source.group()
    ya_news.append(ya_news_dict)

client = MongoClient('127.0.0.1', 27017)
db = client['news_db']
news = db.news
news.insert_many(ya_news)

pprint(ya_news)
