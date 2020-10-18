""" Задание 2: Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
Найти среди них любое, требующее авторизацию (любого типа). Выполнить запросы к нему, пройдя авторизацию.
Ответ сервера записать в файл."""

""" Для выполнения задачи был взят следующий API - https://www.programmableweb.com/api/lastfm-rest-api-v20 
Last.fm — сайт, посвящённый музыке. С помощью плагинов к медиаплеерам собирает информацию о музыке, которую слушают 
пользователи, и на основе полученных данных автоматически составляет индивидуальные и общие хит-парады (чарты). 
На сайте существует возможность прослушивания музыки.

Выведем список избранных треков пользователя.

API key = __ """

import requests
# from pprint import pprint
import json

last_fm_api = 'http://ws.audioscrobbler.com/2.0/'
username = '__'
api_key = '__'

params = {
    'method': 'user.getlovedtracks',
    'user': username,
    'api_key': api_key,
    'format': 'json'
    }

response = requests.get(last_fm_api, params=params)
result = response.json()
# pprint(result)

with open('response_from_last_fm.json', 'w', encoding='UTF-8') as file:
    json.dump(result, file)

print(f'Список избранных треков пользователя {username}:')

for el in result['lovedtracks']['track']:
    print(f'{el["artist"]["name"]} - {el["name"]}')
