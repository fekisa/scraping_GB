import scrapy
from scrapy.http import HtmlResponse
from avito.items import AvitoItem
from scrapy.loader import ItemLoader

class AvitoruSpider(scrapy.Spider):
    name = 'avitoru'
    allowed_domains = ['avito.ru']


    def __init__(self, search):
        super().__init__()
        self.start_urls = [f'https://www.avito.ru/rossiya?q={search}']

    # def start_requests(self):
    #     scrapy.Request()

    def parse(self, response:HtmlResponse):
        ads_links = response.xpath("//a[@class='snippet-link']")
        for link in ads_links:
            yield response.follow(link,callback=self.parse_ads)

    def parse_ads(self,response:HtmlResponse):
        loader = ItemLoader(item=AvitoItem(),response=response)
        loader.add_xpath('name',"//span[@class='title-info-title-text']/text()")
        loader.add_xpath('photos',"//div[contains(@class,'gallery-img-frame')]/@data-url")
        # loader.add_css()
        # loader.add_value('url',response.url)
        yield loader.load_item()

        # name = response.xpath("//span[@class='title-info-title-text']/text()").extract_first()
        # photos=response.xpath("//div[contains(@class,'gallery-img-frame')]/@data-url").extract()
        # yield AvitoItem(name=name,photos=photos)