import csv
import requests
from bs4 import BeautifulSoup


def get_html(url):
    r = requests.get(url)
    return r.text


def write_csv(data):
    with open('plugins.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([data['name'],
                         data['url'],
                         data['employer'],
                         data["zp"]])


def get_data(html):
    soup = BeautifulSoup(html, 'lxml')

    vakansii = soup.find('div', class_="result-list").find_all('div', class_='snippet__inner')
    # print(vakansii)
    for vakansia in vakansii:
        name = vakansia.find("div", class_="snippet__body").find("h2", class_="snippet__title").find("a",
                                                                                                     class_="snippet__title-link link an-vc").text
        url = vakansia.find("div", class_="snippet__body").find("h2", class_="snippet__title").find("a",
                                                                                                    class_="snippet__title-link link an-vc").get(
            "href")
        employer = vakansia.find("div", class_="snippet__body").find("div", class_="snippet__meta-wrapper").find("ul",
                                                                                                                 class_="snippet__meta-list list list_horizontal-slasher").find(
            "li", class_="snippet__meta-item snippet__meta-item_company").find("span",
                                                                               class_="snippet__meta-value").text
        employer_ = employer.replace(' ', '').replace('\n', '')
        zp = vakansia.find("div", class_="snippet__body").find("div", class_="snippet__salary-group").find("span",
                                                                                                           class_="snippet__salary").text
        zp_ = zp.replace(' ', '').replace('\n', '').replace('xa', '')

        data = {
            'name': name,
            'url': url,
            'employer': employer_,
            'zp': zp_
        }
        write_csv(data)


def main():
    url = "https://moskva.gorodrabot.ru/"
    html = get_html(url)
    get_data(html)


main()