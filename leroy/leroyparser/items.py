# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst


def pic_resolution(url):
    for r in (("w_82", "w_600"), ("h_82", "h_600")):
        url = url.replace(*r)
    return url


class LeroyparserItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    pictures = scrapy.Field(input_processor=MapCompose(pic_resolution))
    price = scrapy.Field(input_processor=MapCompose(lambda x: float(x.replace(' ', ''))), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    specs_params = scrapy.Field(input_processor=MapCompose())
    specs_values = scrapy.Field(input_processor=MapCompose(lambda x: x.strip()))
    specs = scrapy.Field()
