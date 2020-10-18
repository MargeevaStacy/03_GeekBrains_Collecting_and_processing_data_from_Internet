import requests
main_link = 'http://www.mail.ru'

response = requests.get(main_link)

response.status_code
response.headers

if response.status_code == 200:
    pass

if response.ok:
    pass

response.text
response.content

print(1)
