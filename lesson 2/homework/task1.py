import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint
import pandas as pd

# HeadHunter
hh_link = 'https://hh.ru'
# job_title = input('Введите название должности: ')
job_title = 'Анестезиолог'

hh_params = {
    'clusters': 'true',
    'enable_snippets': 'true',
    # 'search_field': 'name',
    'text': job_title
    # 'showClusters': 'true'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}

hh_response = requests.get(hh_link + '/search/vacancy', params=hh_params, headers=headers)
hh_dom = bs(hh_response.text, 'html.parser')
hh_next_page = hh_dom.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
hh_total_pages = int(hh_next_page.findPrevious('a', {'class': 'bloko-button HH-Pager-Control'}).text)

hh_page = 1
hh_vacancies = []

while hh_page <= hh_total_pages:

    hh_vacancies_list = hh_dom.findAll('div', {'class': 'vacancy-serp-item__row vacancy-serp-item__row_header'})

    for vacancy in hh_vacancies_list:
        vacancy_data = {}

        a = vacancy.find('a')
        vacancy_data['name'] = a.getText()
        vacancy_data['link'] = a['href']
        vacancy_data['source'] = 'HH'

        salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()
        salary = salary.replace(u'\xa0', '').replace('-', ' ').split()
        if not salary:
            vacancy_data['min_salary'] = None
            vacancy_data['max_salary'] = None
            vacancy_data['currency'] = None
        elif salary[0] == 'от':
            vacancy_data['min_salary'] = int(salary[1])
            vacancy_data['max_salary'] = None
            vacancy_data['currency'] = salary[-1]
        elif salary[0] == 'до':
            vacancy_data['min_salary'] = None
            vacancy_data['max_salary'] = int(salary[1])
            vacancy_data['currency'] = salary[-1]
        else:
            vacancy_data['min_salary'] = int(salary[0])
            vacancy_data['max_salary'] = int(salary[1])
            vacancy_data['currency'] = salary[-1]

        hh_vacancies.append(vacancy_data)

    # pprint(hh_vacancies)

    if hh_page != hh_total_pages:
        hh_next_page = hh_dom.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})
        hh_response = requests.get(hh_link + hh_next_page['href'], headers=headers)
        hh_dom = bs(hh_response.text, 'html.parser')
        hh_page += 1
    else:
        break

pprint(f'Число вакансий на позицию {job_title} на сайте HeadHunter - {len(hh_vacancies)}')


# SuperJob
sj_link = 'https://www.superjob.ru'

sj_params = {
    'keywords': job_title,
    'noGeo': 1
}

sj_response = requests.get(sj_link + '/vacancy/search/', params=sj_params, headers=headers)
sj_dom = bs(sj_response.text, 'html.parser')

sj_next_page = sj_dom.find('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'})
sj_total_pages = int(sj_next_page.findPrevious('span', {'class': '_3IDf-'}).text)

sj_page = 1
sj_vacancies = []

while sj_page <= sj_total_pages:

    sj_vacancies_list = sj_dom.findAll('div', {'class': '_3mfro PlM3e _2JVkc _3LJqf'})

    for vacancy in sj_vacancies_list:
        sj_vacancy_data = {}

        a = vacancy.find('a')
        sj_vacancy_data['name'] = a.getText()
        sj_vacancy_data['link'] = sj_link + a['href']
        sj_vacancy_data['source'] = 'SJ'

        sj_salary = a.findNext('span', {'class': '_1OuF_'}).getText()

        if not sj_salary or sj_salary[0] == 'П':
            sj_vacancy_data['min_salary'] = None
            sj_vacancy_data['max_salary'] = None
            sj_vacancy_data['currency'] = None

        elif sj_salary[0] == 'о':
            temp = sj_salary.replace(u'\xa0', '')
            min_salary = ''
            for el in temp:
                if el.isdigit():
                    min_salary += el
            sj_vacancy_data['min_salary'] = int(min_salary)
            sj_vacancy_data['max_salary'] = None
            sj_vacancy_data['currency'] = sj_salary.split()[-1].split('/')[-2]

        elif sj_salary[0] == 'д':
            temp = sj_salary.replace(u'\xa0', '')
            max_salary = ''
            for el in temp:
                if el.isdigit():
                    max_salary += el
            sj_vacancy_data['min_salary'] = None
            sj_vacancy_data['max_salary'] = int(max_salary)
            sj_vacancy_data['currency'] = sj_salary.split()[-1].split('/')[-2]

        elif '—' in sj_salary:
            temp = sj_salary.replace(u'\xa0', '').split('—')
            max_salary = ''
            for el in temp[1]:
                if el.isdigit():
                    max_salary += el
            sj_vacancy_data['min_salary'] = int(temp[0])
            sj_vacancy_data['max_salary'] = int(max_salary)
            sj_vacancy_data['currency'] = sj_salary.split()[-1].split('/')[-2]

        else:
            temp = sj_salary.replace(u'\xa0', '')
            salary = ''
            for el in temp:
                if el.isdigit():
                    salary += el
            sj_vacancy_data['min_salary'] = int(salary)
            sj_vacancy_data['max_salary'] = int(salary)
            sj_vacancy_data['currency'] = sj_salary.split()[-1].split('/')[-2]

        sj_vacancies.append(sj_vacancy_data)

    # pprint(sj_vacancies)

    if sj_page != sj_total_pages:
        sj_next_page = sj_dom.find('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'})
        sj_response = requests.get(sj_link + sj_next_page['href'], headers=headers)
        sj_dom = bs(sj_response.text, 'html.parser')
        sj_page += 1
    else:
        break

pprint(f'Число вакансий на позицию {job_title} на сайте SuperJob - {len(sj_vacancies)}')

df = pd.DataFrame(hh_vacancies).append(sj_vacancies, ignore_index=True)
pd.set_option('display.max_columns', 6)
print(df)
