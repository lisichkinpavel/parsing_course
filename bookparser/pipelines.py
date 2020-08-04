# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class BookparserPipeline:
    def __init__(self):
        client = MongoClient('localhost',27017)
        self.mongo_base = client.books

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]

        if spider.name == 'labirintru':
            item['item_old_price'], item['item_new_price'] = self.price(item['item_old_price'],item['item_new_price'],item['item_price'])
            item['item_authors'], item['item_title'] = self.author_title(item['item_authors_title'])
            item.pop('item_price')
            item.pop('item_authors_title')
        elif spider.name == 'book24ru':
            item['item_old_price'] = self.book24price(item['item_new_price'], item['item_old_price'])
        item['item_source'] = spider.name

        collection.insert_one(item)
        return item

    def author_title(self, string):
        if string.find(':') != -1:
            authors = string.split(':')[0]
            title = string.split(':')[1]
        else:
            authors = None
            title = string
        return authors, title

    def price(self, old_price, new_price, price):
        if price:
            old_price = price
            new_price = price
        return old_price, new_price

    def book24price(self, price, old_price):
        if not old_price:
            old_price = price
        else:
            old_price = ''.join(x for x in old_price if x.isdigit())
        return old_price


