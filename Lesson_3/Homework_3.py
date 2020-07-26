#terminal - brew services start mongodb-community@4.2

from pymongo import MongoClient
import json


with open('../Lesson_2/hh_Аналитик.json') as f:
    file_data = json.load(f)

client = MongoClient('localhost', 27017) #создаем клиент
db = client['vacancy_db'] #создаем БД, [] - имя БД
hh_vacancies = db.vacancies #создаем привязку к коллекции vacancy в БД

hh_vacancies.insert_many(file_data)

# поиск по БД (зарплата)
x = int(input('Введите заработную плату для поиска: '))
for vacancy in hh_vacancies.find({'$or':[
                                      {'salary_min': {'$gt': x}}, {'salary_max': {'$gt': x}}
                                     ]},
                                      {'_id':0, 'employer': 1, 'name': 1, 'salary_min': 1, 'salary_max': 1}):
    print(vacancy)

# в виде функции

def find_salary():
    salary = int(input('Введите заработную плату для поиска: '))
    vacancy = hh_vacancies.find({'salary':{'$gte': salary}}, {'id':0, 'employer': 1, 'name': 1, 'salary_min': 1, 'salary_max': 1})
    for i in vacancy:
        print(i)

# запись в БД новых вакансий

def add_to_db(data):
    def is_existed_vacancy(vac):
        a=hh_vacancies.find_one(vac)
        if a:
            return True
        return False
    n, o =0, 0
    for i in data:
        existed_vacancy = is_existed_vacancy(i)
        if not existed_vacancy:
            n+=1
            hh_vacancies.insert_one(i)
        else:
            o+-1
    print(f'Got {len(data)} vacancies, {n} new, {o} are not written in db')