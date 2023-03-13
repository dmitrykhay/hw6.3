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

USD_vacancy_list = {}
USD_vacancy_list['vacancy_list'] = []

for vacancy in vacancy_list:
    name = vacancy.find('a', class_="serp-item__title").text
    link = vacancy.find('a', class_="serp-item__title")['href']
    try:
        salary = vacancy.find('span', class_="bloko-header-section-3").text
        salary = re.sub("\u202f", "", salary)
    except AttributeError:
        salary = "Зарплата не указана"
    company_name = vacancy.find('a', class_="bloko-link bloko-link_kind-tertiary").text
    city = vacancy.find(attrs={"data-qa": "vacancy-serp__vacancy-address"}).text
    parsed_data['vacancy_list'].append({'name': name, 'link': link, 'salary': salary, 'company_name': company_name, 'city': city})
    description_html = requests.get(link, headers=get_headers()).text
    description_bs = BeautifulSoup(description_html, "html.parser")
    description = description_bs.find_all('div', class_="vacancy-branded-user-content")
    description_text = ""
    for i in description:
        texts_p = i.find_all('p')
        texts_li = i.find_all('li')
        for text in texts_p:
            description_text += (text.get_text())
        for text in texts_li:
            description_text += (text.get_text())
    if re.findall('django', description_text, re.IGNORECASE) or re.findall('flask', description_text, re.IGNORECASE) is True:
        django_flask_vacancy_list['vacancy_list'].append({'name': name, 'link': link, 'salary': salary, 'company_name': company_name, 'city': city})
    if re.findall('usd', salary, re.IGNORECASE) is True:
        USD_vacancy_list['vacancy_list'].append({'name': name, 'link': link, 'salary': salary, 'company_name': company_name, 'city': city})

pprint(parsed_data)
with open("django_flask_vacancy_list.json", "w", encoding="utf-8") as outfile:
    json.dump(django_flask_vacancy_list, outfile, ensure_ascii=False, indent=2)
with open("USD_vacancy_list.json", "w", encoding="utf-8") as outfile:
    json.dump(USD_vacancy_list, outfile, ensure_ascii=False, indent=2)
