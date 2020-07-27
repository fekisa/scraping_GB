from lxml import html
import requests
from datetime import timedelta, datetime
from pprint import pprint
from pymongo import MongoClient


header = {'User-Agent': 'Chrome/80.0.4150.1'}

site = 'https://m.lenta.ru/parts/news'
response = requests.get(site, headers=header)
dom = html.fromstring(response.text)
results = dom.xpath("//div[@class='parts-page__item']")
news = []
for result in results:
    item = {}
    news_link = result.xpath(".//@href")[0]
    news_link = news_link if news_link.find('http') != -1 else 'https://lenta.ru' + news_link
    item['source'] = 'https://m.lenta.ru/parts/news'
    item['title'] = result.xpath(".//div[@class='card-mini__title']/text()")[0]
    item['link'] = news_link
    item['date'] = result.xpath(".//time/text()")[0]
    news.append(item)
pprint(news)

site = 'https://news.mail.ru'
response = requests.get(site, headers=header)
dom = html.fromstring(response.text)
results = dom.xpath('//ul/li | //a[@class="newsitem__title link-holder"]')
news = []
for result in results:
    item = {}
    news_link = result.xpath(".//@href")[0]
    news_link = news_link if news_link.find('http') != -1 else site + news_link
    item['link'] = news_link if news_link.find('http') != -1 else site + news_link
    item['title'] = result.xpath(".//text()")[0].replace("\xa0", " ")
    response1 = requests.get(news_link, headers=header)
    dom1 = html.fromstring(response1.text)
    date_time = dom1.xpath('..//@datetime')[0] if dom1.xpath('..//@datetime')[0] else 'Новость без даты'
    item['date'] = date_time.replace("T", " ").replace("+03:00", "") if date_time else 'Новость без даты'
    item['source'] = dom1.xpath('//span[@class="note"]//span[@class="link__text"]/text()')[0]
    news.append(item)
pprint(news)

site = 'https://yandex.ru'
response = requests.get(site + '/news', headers=header)
dom = html.fromstring(response.text)
results = dom.xpath("//tr/td")
news = []
for result in results:
    item = {}
    news_link = result.xpath(".//h2//@href")[0]
    item['link'] = site + news_link
    source_date = result.xpath('.//div[@class="story__date"]/text()')[0].replace("\xa0", " ")
    if source_date.find(' вчера в ') > -1:
        pos = source_date.find(' вчера в ')
        item['source'] = source_date[:pos]
        item['pos'] = pos
        item['date'] = source_date[pos + 9:] + ' ' + (datetime.now() - timedelta(days=1)).strftime('%d-%m-%Y')
    else:
        item['source'] = source_date[:-6]
        item['date'] = source_date[-5:]

    item['title'] = result.xpath(".//h2//text()")[0]
    news.append(item)
pprint(news)

client = MongoClient('localhost', 27017)
db = client['news']
news_db = db.news_db
news_db.insert_many(news)