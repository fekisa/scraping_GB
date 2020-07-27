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
main_link = 'https://hh.ru'

#запрос данных
response = requests.get(f'{main_link}/search/vacancy?clusters=true&area=1&enable_snippets=true&salary=&st=searchVacancy&text={occupation}', headers=headers)

#преобразование в DOM
soup = bs(response.text, 'lxml')

#основа для списка
hh_vacancy_list = []

#кнопка "Дальше"
pages = soup.find_all('a', {'class': 'bloko-button HH-Pager-Control'})
print(int(pages[-1].text))

#цикл для сбора

if response.ok:
    for page in range(int(pages[-1].text)):
        hh_vacancies_block = soup.find_all('div', {'class': 'vacancy-serp'})
        hh_vacancies_list = hh_vacancies_block[0].find_all('div', {'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_premium'}) + \
                  hh_vacancies_block[0].find_all('div', {'data-qa': 'vacancy-serp__vacancy'})

        for vacancy in hh_vacancies_list: #цикл для сборки словаря
            vacancy_data = {}
            vacancy_data['name'] = vacancy.find_all('a', {'class': 'bloko-link HH-LinkModifier'})[0].text
            vacancy_data['link'] = vacancy.find_all('a', {'class': 'bloko-link HH-LinkModifier'})[0]['href']
            vacancy_data['employer'] = vacancy.find_all('a', {'data-qa': 'vacancy-serp__vacancy-employer'})[0].text

            try:
                salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).text
            except AttributeError:
                salary = None

            if salary is None:
                salary_min = None
                salary_max = None
                salary_curr = None
            else:
                salary = salary.replace('\xa0', '')
                salary = salary.replace(' ', '-')
                salary = salary.split('-')
                if salary[0] == 'от':
                    salary_min = int(salary[1])
                    salary_max = None
                elif salary[0] == 'до':
                    salary_min = None
                    salary_max = int(salary[1])
                else:
                    salary_min = int(salary[0])
                    salary_max = int(salary[1])
                salary_curr = salary[2]

            vacancy_data['salary_min'] = salary_min
            vacancy_data['salary_max'] = salary_max
            vacancy_data['salary_currency'] = salary_curr

            hh_vacancy_list.append(vacancy_data)

#сохраняем датафрейм и json
df = pd.DataFrame(hh_vacancy_list)
print(df)
df.to_csv(f'hh_{occupation}.csv', encoding='utf-8')
with open(f'hh_{occupation}.json', 'w', encoding='utf-8') as outfile:
    json.dump(hh_vacancy_list, outfile)