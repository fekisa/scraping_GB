import requests
from pprint import pprint #для удобного отображения словарей

main_link = 'http://www.google.ru'
response = requests.get(main_link)

print(1)

# запуск в дебагере
# response.headers - заголовки
# response.headers['Content-Type'] - заголовки хранятся в словаре, обращение конкретно к типу содержимого
# response.status_code - число статус-кода (200 - ок, 300 - редирект, 400 - ошибка клиента, 500 - ошибка сервера

# if response.ok:  - если все подключилось (статус код от 200 до 399), то ...

# response.text - содержимое (html-верстка и текст сайта)
# response.content - то же самое, но только в бинарном виде
# response.url - возвращает ссылку на которую был сделлан последний get запрос

# пример сохранения содержимого
# wb - режим записи файла в бинарном виде
main_link = 'https://img.gazeta.ru/files3/845/7947845/upload-shutterstock_117062077-pic905v-895x505-99863.jpg'
response = requests.get(main_link)

if response.ok:
    with open('sea.jpg', 'wb') as f:
        f.write(response.content)

#пример запроса на ресурс с API (openweather.com)

city = 'Moscow,ru'
appid = 'e5e4cd692a72b0b66ea0a6b80255d1c3'

#main_link = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}'
# до знака вопроса - основная ссылка, после - параметры через &
#или

#  создадим словарь
weather_params = {'q':city,
          'appid':appid}
# убираем знак вопроса
main_link = 'https://api.openweathermap.org/data/2.5/weather'

#объединяем ссылку и параметры в самом запросе
response = requests.get(main_link,params=weather_params)

#выводим результат
pprint(response.text)  #str, не ообработать

#преобразуем в json
pprint(response.json())

#красивый вывод для пользователя

data = response.json()
print(f'В городе {data["name"]} температура {data["main"]["temp"] - 273.15} градусов')
