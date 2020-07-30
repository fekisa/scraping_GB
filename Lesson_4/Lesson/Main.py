from pprint import pprint
from lxml import html
import requests

header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
main_link = 'https://ru.ebay.com/b/Nike-Free-Sneakers-for-Men/15709/bn_58770'

response = requests.get(main_link,headers=header)
dom = html.fromstring(response.text)

items = dom.xpath("//ul[@class='b-list__items_nofooter']/li")

boots = []
for item in items:
    boot = {}
    name = item.xpath(".//h3[@class='s-item__title']/text()")[0]
    price = item.xpath(".//span[@class='s-item__price']//text()")[0].replace('\xa0','')
    image = item.xpath(".//img[@class='s-item__image-img']/@src")[0]
    review = item.xpath(".//span[@class='s-item__reviews-count']/../@href")

    boot['name'] = name
    boot['price'] = price
    boot['image'] = image
    boot['review'] = review

    boots.append(boot)


pprint(boots)