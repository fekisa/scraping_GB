from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import json
from time import sleep
from pprint import pprint

#user_agent
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

#параметры
occupation = 'DataScientist'
main_link = 'https://hh.ru'

#запрос данных
response = requests.get(f'{main_link}/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text={occupation}', headers=headers).text

#преобразование в DOM
soup = bs(response,'lxml')

#кнопка "Дальше"
pages = soup.find_all('a', {'class': 'bloko-button HH-Pager-Control'})
print(int(pages[-1].text))

#основа для списка
hh_vacancy_list = []

#цикл для сбора

for page in range(int(pages[-1].text)): #ограничение страниц для поиска
    link = f'{main_link}/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text={occupation}&page={page}'
    response = requests.get(link, headers=headers).text
    soup = bs(response, 'lxml')
    hh_vac_block = soup.find_all('div', {'class': 'vacancy-serp'}) #находим div со списком вакансий
    hh_vac_list = hh_vac_block[0].find_all('div', {'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_premium'}) + \
                  hh_vac_block[0].find_all('div', {'data-qa': 'vacancy-serp__vacancy'}) #выделяем блоки с информацией по каждой вакансии
    for i in hh_vac_list: #цикл для сборки словаря
        dict = {}
        if not i.find_all('a', {'class': 'bloko-link HH-LinkModifier'}): #обработка нулевых значений
            dict['name'] = None
            dict['link'] = None
        else:
            dict['name'] = i.find_all('a', {'class': 'bloko-link HH-LinkModifier'})[0].text #название
            dict['link'] = i.find_all('a', {'class': 'bloko-link HH-LinkModifier'})[0]['href'] #ссылка
        if not i.find_all('a', {'data-qa': 'vacancy-serp__vacancy-employer'}):
            dict['employer'] = None
        else:
            dict['employer'] = i.find_all('a', {'data-qa': 'vacancy-serp__vacancy-employer'})[0].text #компания
        sal = i.find_all('span', {'class': 'bloko-section-header-3 bloko-section-header-3_lite'}) #зарплата
        if len(sal) == 1:
            dict['sal_min'] = None
            dict['sal_max'] = None
            dict['sal_cur'] = None
        else:
            dict['sal_min'] = ''
            dict['sal_max'] = ''
            dict['sal_cur'] = ''
            spec_sal = sal[1].text
            spec_sal = spec_sal.replace(' ', "\xa0") #убираем пробелы
            spec_sal = spec_sal.replace('-', "\xa0-\xa0") #убираем дефис
            sal_list = spec_sal.split("\xa0")
            if 'от' in sal_list:  #проверка написания зарплаты и обработка
                for elem in sal_list[1:len(sal_list) - 1]:
                    dict['sal_min'] += elem
            elif 'до' in sal_list:
                for elem in sal_list[1:len(sal_list) - 1]:
                    dict['sal_max'] += elem
            elif '-' in sal_list:
                pos = sal_list.index('-')
                for elem in sal_list[:pos]:
                    dict['sal_min'] += elem
                for elem in sal_list[pos + 1:len(sal_list) - 1]:
                    dict['sal_max'] += elem
            else:
                for elem in sal_list[1:len(sal_list) - 1]:
                    dict['sal_min'] += elem
                    dict['sal_max'] += elem
            dict['sal_min'] = None if dict['sal_min'] == '' else dict['sal_min']
            dict['sal_max'] = None if dict['sal_max'] == '' else dict['sal_max']
            dict['sal_cur'] = None if 'По договорённости' in sal_list else sal_list[-1]
        hh_vacancy_list.append(dict)

#сохраняем датафрейм и json
df = pd.DataFrame(hh_vacancy_list)
print(df)
df.to_csv(f'hh_{occupation}.csv', encoding='utf-8')
with open(f'hh_{occupation}.json', 'w', encoding='utf-8') as outfile:
    json.dump(hh_vacancy_list, outfile)

#На SJ не хватило времени