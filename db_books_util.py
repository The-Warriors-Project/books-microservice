from typing import Optional

import consts
from db_books_system import DbBooksSystem

DB_CONNECTION = DbBooksSystem.get_connection()


def get_data(sql: str, argument: Optional[str] = None):
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


def get_by_book_field(field_name_: str, field_data_: str) -> [dict]:
    """
    This function retrieves data from the DB
    :param field_name_: the name of the field in the database
    :param field_data_: the field data
    :return: a list of books
    """

    sql = "SELECT {filter} FROM {db_name}.{table_name} " \
          "WHERE {field_name}=%s".format(filter='*',
                                         db_name=consts.DATABASE_NAME,
                                         table_name=consts.TABLE_NAME,
                                         field_name=field_name_)

    final_result = get_data(sql=sql, argument=field_data_)
    return final_result
