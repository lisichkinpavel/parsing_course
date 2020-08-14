# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstaparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    id = scrapy.Field()
    photo = scrapy.Field()
    status = scrapy.Field()
    account = scrapy.Field()


