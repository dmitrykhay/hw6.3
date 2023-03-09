import requests
import re
import json
from pprint import pprint
from fake_headers import Headers
from bs4 import BeautifulSoup

HOST = "https://spb.hh.ru"
MAIN = f"{HOST}/search/vacancy?text=python&area=1&area=2"


def get_headers():
    return Headers(browser='firefox', os='win').generate()


main_page = requests.get(MAIN, headers=get_headers()).text
bs = BeautifulSoup(main_page, 'lxml')
vacancy_list = bs.find_all(class_='vacancy-serp-item-body')

parsed_data = {}
parsed_data['vacancy_list'] = []

django_flask_vacancy_list = {}
django_flask_vacancy_list['vacancy_list'] = []

USD_vacancy_list ={}
USD_vacancy_list['USD_vacancy_list'] = []

for vacancy in vacancy_list:
    name = vacancy.find('a', class_="serp-item__title").text
    link = vacancy.find('a', class_="serp-item__title")['href']
    salary = vacancy.find('span', class_="bloko-header-section-3")
    #salary = ""
    #for i in salary_tag:
       #i = i.find_all("!-- --")
        #for j in i:
            #salary += (j.get_text())
    #print(salary)
    company_name = vacancy.find('a', class_="bloko-link bloko-link_kind-tertiary").text
    city = vacancy.find('div', class_="vacancy-serp-item__info").text
    parsed_data['vacancy_list'].append({
            'name': name,
            'link': link,
            'salary': salary,
            'company_name': company_name,
            'city': city
        })
    pprint(parsed_data)

    description_html = requests.get(link, headers=get_headers()).text
    description_bs = BeautifulSoup(description_html, "html.parser")
    description = description_bs.find_all('div', class_="vacancy-branded-user-content")
    description_text = ""

    for i in description:
        #ps = i.find_all('p')
        for j in i:
            description_text += (j.get_text())
    if re.findall('django', description_text, re.IGNORECASE) or re.findall('flask', description_text, re.IGNORECASE) is True:
        django_flask_vacancy_list['vacancy_list'].append({
            'name': name,
            'link': link,
            'salary': salary,
            'company_name': company_name,
            'city': city
        })

pprint(django_flask_vacancy_list)

    #if re.findall('usd', salary, re.IGNORECASE) is True:
        #USD_vacancy_list['USD_vacancy_list'].append({
            #'name': name,
            #'link': link,
            #'salary': salary,
            #'company_name': company_name,
            #'city': city
        #})

#pprint(USD_vacancy_list)

with open("django_flask_vacancy_list.json", "w", encoding="utf-8") as outfile:
    json.dump(parsed_data, outfile, ensure_ascii=False, indent=2)
#with open("USD_vacancy_list.json", "w", encoding="utf-8") as outfile:
    #json.dump(parsed_data, outfile, ensure_ascii=False, indent=2)
