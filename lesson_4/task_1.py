from pymongo import MongoClient
from lxml import html
from requests import get


class NewsParse:
    def __init__(self):
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/98.0.4758.102 Safari/537.36'}
        self.URL = 'https://yandex.ru/news/'


    def parse(self,db_name, collection_name):
        response = get(self.URL, headers=self.header)
        root = html.fromstring(response.text)

        block = root.xpath('//section[@aria-labelledby="top-heading"]//div[@class="mg-card__inner"]')
        other_block = root.xpath('//section[@aria-labelledby="top-heading"]//div[contains(@class,"mg-card_flexible-single")]')
        result = []

        # get main news
        for top_info in block:
            post = {}
            title = top_info.xpath('.//h2/a/text()')
            post['title'] = title
            post['link'] = top_info.xpath('.//h2/a/@href')
            post['definition'] = top_info.xpath('.//div[@class="mg-card__annotation"]/text()')
            post['source'] = top_info.xpath('.//span[@class="mg-card-source__source"]/a/text()')
            result.append(post)

        # get other news
        for info in other_block:
            post = {}
            post['title'] = info.xpath('.//h2/a/text()')
            post['link'] = info.xpath('.//h2/a/@href')
            post['definition'] = info.xpath('.//div[@class="mg-card__annotation"]/text()')
            post['source'] = info.xpath('.//span[@class="mg-card-source__source"]//a/text()')
            result.append(post)

        self._put_in_mongo(db_name, collection_name, result)


    def __init_db(self, db_name, collection_name):
        client = MongoClient('localhost', 27017)
        db = client[db_name]
        collection = db[collection_name]
        return db, collection


    def _put_in_mongo(self,db_name, collection_name, data):
        db, collection = self.__init_db(db_name, collection_name)

        for vacancy in data:
            collection.insert_one(vacancy)


if __name__ == '__main__':
    parser = NewsParse()
    parser.parse('test_news', 'test_news')
