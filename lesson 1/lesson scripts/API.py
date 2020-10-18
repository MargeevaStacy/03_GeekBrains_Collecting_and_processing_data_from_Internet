#e5e4cd692a72b0b66ea0a6b80255d1c3
#api.openweathermap.org/data/2.5/weather?q=paris&appid=e5e4cd692a72b0b66ea0a6b80255d1c3
import requests
from pprint import pprint
import json
main_link = 'http://api.openweathermap.org/data/2.5/weather'
city = 'Moscow,US'
params = {
    'q':city,
    'appid':'e5e4cd692a72b0b66ea0a6b80255d1c3'
}

response = requests.get(main_link,params=params)
# print(response.text)
j_data = response.json()
pprint(j_data)

with open('response.json','w') as f:
    json.dump(j_data,f)

print(f'В городе {j_data["name"]} температура {j_data["main"]["temp"]-273.15} градусов')



