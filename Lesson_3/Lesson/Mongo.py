from pymongo import MongoClient
from pprint import pprint

client = MongoClient('127.0.0.1',27017)
db = client['users_db']

users = db.users
books = db.books

#Добавляет один словарь в БД
# users.insert_one({"author": "Peter",
#                "age" : 78,
#                "text": "is cool! Wildberry",
#                "tags": ['cool','hot','ice'],
#                "date": '14.06.1983'})
#CRUD

#Добавляет несколько словарей в БД
# users.insert_many(
#     [{"author": "John",
#                "age" : 29,
#                "text": "Too bad! Strawberry",
#                "tags": ['ice'],
#                "date": '04.08.1971'},
#
#                     {"author": "Anna",
#                "age" : 36,
#                "title": "Hot Cool!!!",
#                "text": "easy too!",
#                "date": '26.01.1995'},
#
#                    {"author": "Jane",
#                "age" : 43,
#                "title": "Nice book",
#                "text": "Pretty text not long",
#                "date": '08.08.1975',
#                "tags":['fantastic','criminal']}
#      ]
# )

#Выведет все, что есть в БД
for user in users.find({}):
    print(user)

#Найдет всех Jane
for user in users.find({'author':'Jane'}):
    print(user)

#Оператор ИЛИ
for user in users.find({'$or':[{'author':'Peter'},{'age':21}]}):
    print(user)

#Выбрать поля для вывода (нужно проставить число больше 0 для полей, которые хотим вывести)
for user in users.find({'author':'Peter'} , {'author':1,'age':1,'date':1, '_id':0}):
    print(user)

#Добавляем сортировку и лимит вывода, поле ID убираем из вывода
#sort('age') - от меньшего к большему
#sort('age', -1) - обратный порядок сортировки
for user in users.find({} , {'author':1,'age':1,'date':1, '_id':0}).sort('age',-1).limit(3):
    print(user)

# '$gt' - greater then, символьная форма знака >
# '$lt' - less then, <
# '$gte', '$lte' - >= , <=
# '$ne' -  - не равно

for user in users.find({'author':'Peter','age':{'$gte':43}}):
    print(user)

# замена одного документа другим
doc = {'age': 18,
 'author': 'Anna',
 'date': '26.01.1998',
 'text': 'easy too!',
 'title': 'Hot Cool!!!'}

# users.replace_one({'author':'Peter','age':22},doc)
# users.replace_many()

# обновление записи
users.update_many({},{'$set':{'new_field':47}})
# users.update_one()

# удаление записи
# users.delete_one({'author':'Anna'})
# users.delete_many({})
# users.drop()


users.find()
books.find()


for user in users.find({}):
     print(user)

#показатель все коллекции БД
print(db.collection_names())