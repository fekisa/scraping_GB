from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser import settings
from jobparser.spiders.hhru import HhruSpider
from jobparser.spiders.sjru import SjruSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    # answer = input('Введите вакансию')

    process.crawl(HhruSpider,vacansy = 'python')
    process.crawl(SjruSpider, vacansy='python')

    process.start()