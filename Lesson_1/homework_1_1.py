import json
import requests
from pprint import pprint

#1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

#https://developer.github.com/v3/repos/

user = "fekisa"
main_link = f'https://api.github.com/users/{user}/repos'

response = requests.get(main_link)

data = response.json()
with open('user_reps.json', 'w') as outfile:
    json.dump(data, outfile)

#красивый вывод списка
for i in range(0, len(data)):
    print("Project Number:", i+1)
    print("Project Name:", data[i]['name'])
    print("Project URL:", data[i]['svn_url'], "\n")