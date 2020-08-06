import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader

class LeroymerlinruSpider(scrapy.Spider):
    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super().__init__()
        self.start_urls = [f'http://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        next_button = response.xpath("//div[@class='next-paginator-button-wrapper']//@href").extract_first()
        links = response.xpath("//product-card/@data-product-url").extract()
        for link in links:
            yield response.follow(link, callback=self.item_parse)
        if next_button:
            yield response.follow(next_button, callback=self.parse)


    def item_parse(self, response:HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_xpath('title', "//h1/text()")
        loader.add_xpath('pictures', "//img[@slot='thumbs']/@src")
        loader.add_xpath('price', "//meta[@itemprop='price']/@content")
        loader.add_value('url', response.url)
        loader.add_xpath('specs_params', "//dt[@class='def-list__term']//text()")
        loader.add_xpath('specs_values', "//dd[@class='def-list__definition']//text()")

        yield loader.load_item()



