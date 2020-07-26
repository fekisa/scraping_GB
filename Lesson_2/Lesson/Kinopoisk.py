from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint


params = {'quick_filters':'serials',
         'tab':'all'}
main_link = 'https://www.kinopoisk.ru'
response = requests.get(main_link+'/popular/films',params=params)
soup = bs(response.text,'lxml')

serials_block = soup.find('div',{'class':'selection-list'})
serials_list = serials_block.findChildren(recursive=False)
serials_list2 = serials_block.find_all('div',{'class':'desktop-rating-selection-film-item'})


serials = []
for serial in serials_list:
    serial_data = {}
    serial_data['name'] = serial.find('p').getText()
    serial_data['link'] = main_link + serial.find('a',{'class':'selection-film-item-meta__link'})['href']
    serial_data['genre'] = serial.find('span',{'class':'selection-film-item-meta__meta-additional-item'}).find_next_sibling().getText()
    rating = serial.find('span',{'class':'rating__value'}).getText()
    if rating == '—':
        rating = 0
    serial_data['rating'] = float(rating)

    serials.append(serial_data)

pprint(serials)