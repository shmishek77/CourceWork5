import psycopg2
from config import config

def get_connection():
    return psycopg2.connect(dbname="hh", **config())

class DBManager:
    '''Класс для подключения к БД'''

    def get_companies_and_vacancies_count(self):
        '''получает список всех компаний и количество вакансий у каждой компании.'''

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT company_name, COUNT(vacancies_name) AS count_vacancies "
                            f"FROM employers "
                            f"JOIN vacancies USING (employer_id) "
                            f"GROUP BY employers.company_name")
                result = cur.fetchall()
            conn.commit()
            for item in result:
                for i in item:
                    print(i, end=' ')
                print("")

    def get_all_vacancies(self):
        ''' получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.'''

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT employers.company_name, vacancies.vacancies_name, "
                            f"vacancies.payment, vacancies_url "
                            f"FROM employers "
                            f"JOIN vacancies USING (employer_id)")
                result = cur.fetchall()
            conn.commit()
            for item in result:
                for i in item:
                    print(i, end=' ')
                print("")

    def get_avg_salary(self):
        '''получает среднюю зарплату по вакансиям'''

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT AVG(payment) as avg_payment FROM vacancies ")
                result = cur.fetchall()
            conn.commit()
            for item in result:
                for i in item:
                    print(i, end=' ')
                print("")

    def get_vacancies_with_higher_salary(self):
        '''получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.'''
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT vacancies_name, payment, requirement, vacancies_url FROM vacancies "
                            f"WHERE payment > (SELECT AVG(payment) FROM vacancies) ")
                result = cur.fetchall()
            conn.commit()
            for item in result:
                for i in item:
                    print(i, end=' ')
                print("")

    def get_vacancies_with_keyword(self, keyword):
        '''получает список всех вакансий, в названии которых
        содержатся переданные в метод слова, например python.'''

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM vacancies "
                            f"WHERE lower(vacancies_name) LIKE '%{keyword}%' "
                            f"OR lower(vacancies_name) LIKE '%{keyword}'"
                            f"OR lower(vacancies_name) LIKE '{keyword}%';")
                result = cur.fetchall()
            conn.commit()
            for item in result:
                for i in item:
                    print(i, end=' ')
                print("")
