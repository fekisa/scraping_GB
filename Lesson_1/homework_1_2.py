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

#with open('last_fm_response.json', 'w') as outfile:
    #json.dump(response, outfile)

#Вариант API vk.com (access token)

access_token = 'fe5e997115afaea1dfe3b4ed4d87be9db95dd5f88e5be140a2c88d25cac4a81f411af1c108f6bb4edecaf'

vk_response = requests.get(f'https://api.vk.com/method/friends.getOnline?v=5.52&access_token={access_token}')
pprint(vk_response.text)