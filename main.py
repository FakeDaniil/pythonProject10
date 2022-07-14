import requests
from bs4 import BeautifulSoup
import psycopg2

host = "localhost" # 127.0.0.1
user = "postgres"
password = "admin"
db_name = "postgres"
def bd(data):

    try:
        # connect to exist database
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        connection.autocommit = True

        # Создание курсора для выполнения запросов к базам данных
        # cursor = connection.cursor()

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT version();"
            )
            print(f"Server version: {cursor.fetchone()}")


        # with connection.cursor() as cursor:
        # 	cursor.execute(
        # 		"""CREATE TABLE vacancies(
        # 			id serial PRIMARY KEY,
        # 			name varchar(100) NOT NULL,
        # 		    url varchar(100)  NOT NULL,
        # 		    employer varchar(100)  NOT NULL,
        # 		    zp varchar(100)  NOT NULL);"""
        # 	)
        # 	print("[INFO] Table created successfully")

        # with connection.cursor() as cursor:
        #     cursor.execute(
        #         """DROP TABLE vacancies;"""
        #     )
        #     print("[INFO] Table was deleted")

        # Вставка данных в таблицу
        # 	with connection.cursor() as cursor:
        # 		cursor.execute(
        # 			f"""INSERT INTO vacancies(name, salary) VALUES
        # 			({data['name']}, {data['zp']});"""
        # 		)
        # 		print("[INFO] Data was succefully inserted")




        with connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO vacancies(name, url, employer, zp) VALUES
                ('{data['name']}', '{data['url']}', '{data['employer']}', '{data['zp']}');"""
            )
            print("[INFO] Data was succefully inserted")


        # Получение данных из таблицы
        # with connection.cursor() as cursor:
        #     cursor.execute(
        #         """SELECT nick_name FROM users WHERE first_name = 'Oleg';"""
        #     )

        #     print(cursor.fetchone())

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL", _ex)
    finally:
        if connection:
            # cursor.close()
            connection.close()
            print("[INFO] PostgreSQL connection closed")



def get_html(url):
    r = requests.get(url)
    return r.text

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


        bd(data)


def main():
    url = "https://moskva.gorodrabot.ru/"
    html = get_html(url)
    get_data(html)


main()