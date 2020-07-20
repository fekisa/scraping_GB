from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

response = requests.get('http://127.0.0.1:5000/')
soup = bs(response.text,'lxml')   # или можно использовать встроенный html.parser

link = soup.find_all('a') # найти все теги "а" (find - работает только до первого вхождения)
parent_a = link[0].parent.parent #найти родителя + уровень выше

children = parent_a.findChildren(recursive=False) #поиск детей (без recursive=False выдаст и детей и внуков)
child = parent_a.findChild()

#child.find_next_sibling()   -s #соседи
#child.find_previous_sibling()    -s

link[0].getText() #забрать текст из ссылки a

elem = soup.find_all(attrs={'class':'red'}) #поиск с атрибутами, работает только один параметр (не учитывает частичное совпадение при двух классах)
elem2 = soup.find_all(attrs={'class':'paragraph'})

elem3 = soup.find('div',{'id':'d2'})
top3 = soup.find_all('p',limit=3)


text_tag = soup.find(text='Шестой параграф')
pprint(text_tag.parent.findNextSibling())












