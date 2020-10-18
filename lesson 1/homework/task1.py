""" Задание 1: Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного
пользователя, сохранить JSON-вывод в файле *.json. """

# request template - https://docs.github.com/en/free-pro-team@latest/rest/reference/repos#list-repositories-for-a-user
# https://api.github.com/users/{username}/repos

import requests
# from pprint import pprint
import json

git_api = 'https://api.github.com/users/'
username = 'MargeevaStacy'
params = {
    'accept': 'application/vnd.github.v3+json',
    'type': 'owner',
    'sort': 'full_name'
    }

response = requests.get(git_api + username + '/repos', params=params)
result = response.json()
# pprint(result)

with open('response_from_git.json', 'w', encoding='UTF-8') as file:
    json.dump(result, file)

print(f'Список Git репозиториев пользователя {username}:')

for el in result:
    print(f'{el["full_name"]}')
