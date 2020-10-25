from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint

main_link = 'http://127.0.0.1:5000/'
response = requests.get(main_link)

soup = bs(response.text,'html.parser')

tag_a = soup.find('a')
grandfather_tag_a = tag_a.parent.parent
parents_tag_a = tag_a.findParents()

# children = len(list(grandfather_tag_a.children))      #Свойство для просмотра детей
# pprint(list(grandfather_tag_a.children))

# children = grandfather_tag_a.findChildren(recursive=False)
# pprint(children)
# pprint(len(children))

# pprint(soup.findAll(attrs={'class':'paragraph'}))
# pprint(soup.findAll('p',{'class':['red paragraph','red paragraph left']}))

# elems = soup.findAll('p',limit=3)
# pprint(elems)

elem = soup.find(text='Шестой параграф')
pprint(elem.parent)
