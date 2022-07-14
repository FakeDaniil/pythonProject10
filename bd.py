import psycopg2

host = "localhost" # 127.0.0.1
user = "postgres"
password = "admin"
db_name = "postgres"

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
	# 		"""CREATE TABLE q(
	# 		id serial PRIMARY KEY,
	# 		name varchar(50) NOT NULL,
	# 		password varchar(50) NOT NULL);"""
	# 	)
	# 	print("[INFO] Table created successfully")

    # Вставка данных в таблицу
	with connection.cursor() as cursor:
		cursor.execute(
			"""INSERT INTO q (name, password) VALUES
			('Oleg', 'admin');"""
		)
		print("[INFO] Data was succefully inserted")

	with connection.cursor() as cursor:
		cursor.execute(
			"""SELECT name, password FROM q WHERE name = 'Oleg';"""
		)
		print(cursor.fetchone())

    # Пример функции, которая должна быть вместо write_csv
	# def write_to_db(connection, data):
	# 	with connection.cursor() as cursor:
	# 		cursor.execute(
	# 			f"""INSERT INTO vacancies(name, salary) VALUES
	# 			({data['name']}, {data['zp']});"""
	# 		)
	# 		print("[INFO] Data was succefully inserted")

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