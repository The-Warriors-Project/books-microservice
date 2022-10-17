from typing import Optional
from db_books_system import DbBooksSystem
import consts


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


def get_by_book_name(book_name: str, field: str, filters: Optional[dict] = None) -> [dict]:
    """
    This function retrieves data from the DB
    :param book_name: the name of the book
    :param field: the needed field for the query (etc. name)
    :param filters: optional filters for query
    :return: a list of books
    """

    sql = "SELECT {filter_} FROM {db_name}.{table_name} WHERE {field}=%s".format(filter_='*',
                                                                                 db_name=consts.DATABASE_NAME,
                                                                                 table_name=consts.TABLE_NAME,
                                                                                 field=field)

    final_result = get_data(sql=sql, argument=book_name)
    return final_result


def get_by_book_author(author_name: str, field: str, filters: Optional[dict] = None) -> [dict]:
    """
    This function retrieves data from the DB.
    :param author_name: the author of the book
    :param field: the needed field for the query (etc. author)
    :param filters: optional filters for query
    :return: a list of books
    """

    sql = "SELECT {filter_} FROM {db_name}.{table_name} WHERE {field}=%s".format(filter_='*',
                                                                                 db_name=consts.DATABASE_NAME,
                                                                                 table_name=consts.TABLE_NAME,
                                                                                 field=field)

    final_result = get_data(sql=sql, argument=author_name)
    return final_result
