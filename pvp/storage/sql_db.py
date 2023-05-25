from logging import info as logging_info
from sqlite3 import connect, Connection

from ..entity.vacancy import Vacancy


__all__ = ['DBSaverSQLite', 'new_sqlite_db_conn']


def new_sqlite_db_conn(memory: bool, file_path: str = 'default_db.sqlite') -> Connection:
    """
    New DB.
    :param memory: choice of storage method
    :param file_path: filename/path to store
    :return: db-object
    """
    if memory:
        file_path = ':memory:'
        logging_info('Connection DB: Database is created in memory')
        return connect(file_path)

    logging_info('Connection DB: Database is created in file')
    return connect(file_path)


class DBSaverSQLite:
    __slots__ = 'db_conn', 'cursor'

    def __init__(self, db_conn: Connection):
        self.db_conn = db_conn
        self.cursor = self.db_conn.cursor()

    def create_table(self):
        # create table if not exists
        pass

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """
        Save vacancy in DB.
        :param vacancy: Vacancy object
        """
        query = '''
        INSERT INTO student
        (title, url, date_published, city, requirements, salary_min, salary_max, currency) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        self.cursor.execute(query, *vacancy.make_dict().values())
        self.db_conn.commit()

    def get_vacancies_by_salary(self, salary_min: int) -> list:
        """
        Get vacancies "like by" salary_min attr.
        :param salary_min: salary_min attr
        :return: Vacancy-objects
        """
        query = f'SELECT title, url, date_published, city, requirements, salary_min, salary_max, currency ' \
                f'FROM student WHERE salary_min <= {salary_min}'

        all_rows = self.cursor.execute(query).fetchall()
        return [Vacancy(*row) for row in all_rows]

    def delete_vacancy(self, vacancy_url: str) -> None:
        """
        Delete vacancy.
        :param vacancy_url: url
        """
        self.cursor.execute(f'DELETE FROM student WHERE url={vacancy_url}')
        self.db_conn.commit()
