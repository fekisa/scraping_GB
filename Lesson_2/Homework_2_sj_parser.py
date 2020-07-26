from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
import json
import re
from pprint import pprint

#user_agent
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

#параметры
occupation = 'Аналитик'
#pages = 5
main_link = 'https://superjob.ru'

sj_params = {'pages': 1,
             'keywords': occupation,
             'noGeo': 1}

#запрос данных
response = requests.get(main_link + '/vacancy/search/', headers=headers, params=sj_params)
#преобразование в DOM
soup = bs(response.text, 'lxml')
#основа для списка
sj_vacancy_list = []

#цикл для сбора
if response.ok:
    sj_vacancies_block = soup.find('div', {'class': 'iJCa5'})
    sj_vacancies_list = sj_vacancies_block.find_all('div', {'class': 'LvoDO'})
    print(len(sj_vacancies_list))

    for vacancy in sj_vacancies_list: #цикл для сборки словаря
        vacancy_data = {}
        vacancy_data['name'] = vacancy.find('a', {'class': 'icMQ_'}).getText()
        vacancy_data['link'] = main_link + vacancy.find('a', {'class': 'icMQ_'})['href']

        a = vacancy.find('span', {'class': 'PlM3e'}).getText()
        if a == 'По договорённости':
            a = None
        else:
            a = re.split('[\xa0 -]', a)
            a = [i for i in a if i != '—']

            if len(a) == 4 and a[0] == 'от':
                vacancy_data['min_salary'] = int(a[1] + a[2])
            if len(a) == 4 and a[0] == 'до':
                vacancy_data['max_salary'] = int(a[1] + a[2])
            if len(a) > 4:
                vacancy_data['min_salary'] = int(a[0] + a[1])
                vacancy_data['max_salary'] = int(a[2] + a[3])

            vacancy_data['currency'] = a[-1]

        b = vacancy.find('span', {'class': 'clLH5'}).find_next_sibling().getText()
        vacancy_data['city'] = b.split(',')[0]
        vacancy_data['main_link'] = main_link
        vacancy_data['vacancy_id'] = str(''.join(re.findall('[0-9]+', vacancy_data['link'])))

        sj_vacancy_list.append(vacancy_data)

#сохраняем датафрейм и json
df = pd.DataFrame(sj_vacancy_list)
print(df)
df.to_csv(f'sj_{occupation}.csv', encoding='utf-8')
with open(f'sj_{occupation}.json', 'w', encoding='utf-8') as outfile:
    json.dump(sj_vacancy_list, outfile)