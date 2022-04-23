import scrapy
from scrapy.http import HtmlResponse

from books.items import BooksItem


class BookerSpider(scrapy.Spider):
    name = 'booker'
    allowed_domains = ['book24.ru']
    start_urls = ['http://book24.ru/']

    def parse(self, response: HtmlResponse):
        # Пагинация
        for i in range(2, 40):
            yield response.follow(f'https://book24.ru/knigi-bestsellery/page-{i}/', callback=self.parse,
                                  dont_filter=True)

        items = response.xpath(
            "//a[contains(@class, 'product-card__image-link') and contains(@class, 'smartLink')]//@href").extract()
        for link in items:
            yield response.follow(link, callback=self.parse_item, dont_filter=True)

    def parse_item(self, response: HtmlResponse):
        item_link = response.url
        try:
            author, name = response.css("h1::text").get().split(':')
        except:
            name = response.css("h1::text").get()
            author = None
        _price = response.xpath(
            "//span[contains(@class, 'app-price') and contains(@class, 'product-sidebar-price__price') and not(contains(@class, 'product-sidebar-price__price-old'))]/text()").get()
        price = int(''.join([x for x in _price if x.isdigit()]))
        _old_price = response.xpath(
            "//span[contains(@class, 'app-price') and contains(@class, 'product-sidebar-price__price-old')]/text()").get()
        try:
            old_price = int(''.join([x for x in _old_price if x.isdigit()]))
        except:
            old_price = None
        _rating = response.xpath("//span[@class='rating-widget__other-text']").get()
        rating = int(''.join([x for x in _rating if x.isdigit()]))

        yield BooksItem(url=item_link, author=author, name=name, price=price, old_price=old_price, rating=rating)
