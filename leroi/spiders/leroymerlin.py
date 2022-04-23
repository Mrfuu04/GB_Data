import scrapy
from scrapy.http import HtmlResponse

from leroi.items import LeroiItem
from scrapy.loader import ItemLoader



class LeroymerlinSpider(scrapy.Spider):
    handle_httpstatus_list = [301, 302]
    name = 'leroymerlin'
    allowed_domains = ['castorama.ru']
    start_urls = ['https://www.castorama.ru/bathroom/toilets-and-installation-systems']

    def parse(self, response:HtmlResponse):
        links = response.css('.product-card').xpath('a[@class="product-card__img-link"]/@href').getall()
        next_page = response.css('.next::attr(href)').extract_first()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in links:
            yield response.follow(link, callback=self.parse_item)


    def parse_item(self, response:HtmlResponse):
        item = ItemLoader(item=LeroiItem(), response=response)
        item.add_css('name', 'h1::text')
        item.add_value('link', response.url)
        item.add_xpath('price', '//span[@class="price"]//text()')
        item.add_xpath('photos', '//div[@class="js-zoom-container"]//@data-src')

        yield item.load_item()