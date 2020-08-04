import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem

class Book24ruSpider(scrapy.Spider):
    name = 'book24ru'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/novie-knigi']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='catalog-pagination__item _text js-pagination-catalog-item']/@href").extract_first()
        books_links = response.xpath("//div[@class='catalog-products__list js-catalog-products']//div[@class='book__image-block']//@href").extract()
        for link in books_links:
            yield response.follow(link, callback=self.book_parse)
        if next_page:
            yield response.follow(next_page, callback=self.parse)


    def book_parse(self, response: HtmlResponse):
        title = response.xpath("//h1/text()").extract_first()
        authors = response.xpath("//div[@class='item-tab__chars-item'][1]//a[@class='item-tab__chars-link']/text()").extract_first()
        old_price = response.xpath("//div[@class='item-actions__price-old']//text()").extract_first()
        new_price = response.xpath("//div[@class='item-actions__price']//text()").extract_first()
        rate = response.xpath("//span[@class='rating__rate-value']/text()").extract_first()
        yield BookparserItem(item_title=title, item_old_price=old_price, item_authors=authors,
                             item_new_price=new_price, item_rate=rate)

