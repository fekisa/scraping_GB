# Изучить список открытых API.
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию.
# Ответ сервера записать в файл.

import requests
import json
from pprint import pprint

main_link = "http://ws.audioscrobbler.com/2.0/"
user = "Fekisa"
api_key = '7a1309626e9b5a8d25e4b85686b1068d'
method = "user.getLovedTracks"

params = {'user': user,
          'api_key': api_key,
          'method': method}
response = requests.get(main_link, params=params)
pprint(response.text)
