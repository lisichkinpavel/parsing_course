# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    _id = scrapy.Field()
    item_authors_title = scrapy.Field()
    item_old_price = scrapy.Field()
    item_new_price = scrapy.Field()
    item_price = scrapy.Field()
    item_rate = scrapy.Field()
    item_authors = scrapy.Field()
    item_title = scrapy.Field()
    item_source = scrapy.Field()


