from typing import Optional

import consts
from utils.database import DB_CONNECTION
from utils.google_books_api import get_book_from_google_by_title


def execute_query(sql: str, argument: Optional[str] = None):
    """
    This function takes sql query and returns its result
    :param sql: the sql statement
    :param argument: the needed argument
    :return: data
    """
    connection = DB_CONNECTION
    cursor = connection.cursor()
    _ = cursor.execute(sql, args=argument)  # provide the number of results
    final_result = cursor.fetchone()  # provide the actual result (with data)

    return final_result


def get_book(field_name_: str, field_data_: str) -> [dict]:
    """
    This function retrieves data from the DB, if the book does not exist -> get from google API
    :param field_name_: the name of the field in the database
    :param field_data_: the field data
    :return: a list of books
    """

    sql = "SELECT {filter} FROM {db_name}.{table_name} " \
          "WHERE {field_name}=%s".format(filter='*',
                                         db_name=consts.DATABASE_NAME,
                                         table_name=consts.TABLE_NAME,
                                         field_name=field_name_)

    final_result = execute_query(sql=sql, argument=field_data_)

    if not final_result:
        google_result = get_book_from_google_by_title(data=field_data_, field=field_name_)
        insert_book(name=google_result[0], author=google_result[1], description=google_result[2],
                    isbn=google_result[3], picture=google_result[4])
        final_result = execute_query(sql=sql, argument=google_result[0])

    return final_result


def insert_book(name: str, author: str, description: str, isbn: str, picture: str) -> [dict]:
    """
    This function inserts book properties into the DB
    :param name: the name of the book
    :param author: the name of the author
    :param description: the description of the book
    :param isbn: the isbn of the book
    :param picture: the picture url of the book
    :return: a list of books
    """

    sql = "INSERT INTO `books_testing`.books (name, author, description, isbn, picture) VALUES (%s,%s,%s,%s,%s)"

    final_result = execute_query(sql=sql, argument=(name, author, description, isbn, picture))
    return final_result
