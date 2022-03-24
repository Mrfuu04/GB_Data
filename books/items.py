# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksItem(scrapy.Item):
    _id = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    name = scrapy.Field()
    old_price = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
