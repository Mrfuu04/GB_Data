from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from leroi import settings
from leroi.spiders.leroymerlin import LeroymerlinSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinSpider)
    process.start()
