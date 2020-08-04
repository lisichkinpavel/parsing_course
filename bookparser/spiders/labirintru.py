import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/genres/2993/?page=1']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//div[@class='pagination-next']//@href").extract_first()
        books_links = response.xpath("//div[@class='inner-catalog']//a[@class='product-title-link']/@href").extract()
        for link in books_links:
            yield response.follow(link, callback=self.book_parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def book_parse(self, response: HtmlResponse):
        authors_title = response.xpath("//h1/text()").extract_first()
        old_price = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        new_price = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        price = response.xpath("//span[@class='buying-price-val-number']/text()").extract_first()
        rate = response.xpath("//div[contains(@id,'rate')]/text()").extract_first()
        yield BookparserItem(item_authors_title=authors_title, item_old_price=old_price, item_new_price=new_price,
                             item_price=price, item_rate=rate)


