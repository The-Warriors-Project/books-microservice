from typing import Optional

from fastapi import status, Response

import consts
from utils.database import DbBooksSystem
from utils.google_books_api import get_books_from_google_by_title


def execute_query(sql: str, argument: Optional[str] = None):
    """
    This function takes sql query and returns its result
    :param sql: the sql statement
    :param argument: the needed argument
    :return: data
    """
    connection = DbBooksSystem.get_connection()
    if not connection:
        return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                        content="DB service is unavailable")
    cursor = connection.cursor()
    _ = cursor.execute(sql, args=argument)  # provide the number of results
    final_result = cursor.fetchone()  # provide the actual result (with data)

    return final_result


def get_books(field_name_: str, field_data_: str) -> dict:
    """
    This function retrieves data from the DB, if the book does not exist -> get from google API
    :param field_name_: the name of the field in the database
    :param field_data_: the field data
    :return: a list of books
    """

    sql = "SELECT {filter} FROM {db_name}.{table_name} " \
          "WHERE {field_name}=%s AND isbn=%s".format(filter='*',
                                                     db_name=consts.DATABASE_NAME,
                                                     table_name=consts.TABLE_NAME,
                                                     field_name=field_name_)

    sql_fetch_id = "SELECT {filter} FROM {db_name}.{table_name} " \
                   "WHERE {field_name}=%s AND isbn=%s".format(filter='_id',
                                                              db_name=consts.DATABASE_NAME,
                                                              table_name=consts.TABLE_NAME,
                                                              field_name=field_name_)

    books_to_return = {}
    google_result = get_books_from_google_by_title(data=field_data_, field=field_name_)
    for i in range(6):
        final_result = execute_query(sql=sql, argument=(google_result[i].get('title'), google_result[i].get('isbn')))
        if not final_result:

            # A book can have a list of author but the DB does not accept type list -> join it.
            if type(google_result[i].get("author")) == list:
                google_result[i]["author"] = ', '.join(google_result[i].get("author"))

            insert_book(title=google_result[i].get('title'), author=google_result[i].get('author'),
                        description=google_result[i].get('description'),
                        isbn=google_result[i].get('isbn'), picture=google_result[i].get('picture'))

        # get the _id number
        _id = execute_query(sql=sql_fetch_id, argument=(google_result[i].get('title'), google_result[i].get('isbn')))
        books_to_return[i] = {'title': google_result[i].get('title'),
                              'author': google_result[i].get('author'),
                              'description': google_result[i].get('description'),
                              'isbn': google_result[i].get('isbn'),
                              'picture': google_result[i].get('picture'),
                              '_id': _id.get('_id')}

    return books_to_return


def get_book_by_id(_id: str):
    """
    This function get a book by its id
    :return: dict of information
    """
    sql = "SELECT {filter} FROM {db_name}.{table_name} " \
          "WHERE {field_name}=%s".format(filter='*',
                                         db_name=consts.DATABASE_NAME,
                                         table_name=consts.TABLE_NAME,
                                         field_name=consts.BOOK_ID)
    book_info = execute_query(sql=sql, argument=_id)
    return book_info


def insert_book(title: str, author: str, description: str, isbn: str, picture: str) -> [dict]:
    """
    This function inserts book properties into the DB
    :param title: the name of the book
    :param author: the name of the author
    :param description: the description of the book
    :param isbn: the isbn of the book
    :param picture: the picture url of the book
    :return: a list of books
    """

    sql = "INSERT INTO `books_db`.books (title, author, description, isbn, picture, likes_count) VALUES (%s,%s,%s,%s,%s,%s)"

    final_result = execute_query(sql=sql, argument=(title, author, description, isbn, picture, 0))
    return final_result


def get_likes_book(book_id: str):
    """
    This function get a book's count_like using its id
    :param book_id: the book _id
    :return: the count likes of a book
    """
    sql = "SELECT {filter} FROM {db_name}.{table_name} " \
          "WHERE {field_name}=%s".format(filter='likes_count',
                                         db_name=consts.DATABASE_NAME,
                                         table_name=consts.TABLE_NAME,
                                         field_name=consts.BOOK_ID)
    final_result = execute_query(sql=sql, argument=book_id)
    return final_result


def update_likes_book(book_id: str, operator: int):
    """
    This function updates the like count accorsing to the request (+1/-1)
    :param book_id: the book id
    :param operator: +1/-1
    :return: None
    """

    if operator > 0:
        sql = "UPDATE {db_name}.{table_name} " \
              "SET likes_count = likes_count+({operator}) WHERE " \
              "_id={_id}".format(db_name=consts.DATABASE_NAME,
                                 table_name=consts.TABLE_NAME,
                                 operator=str(operator),
                                 _id=book_id)
    else:  # in case of removing like, making sure it cannot be less than 0.
        sql = "UPDATE {db_name}.{table_name} " \
              "SET likes_count = likes_count+({operator}) WHERE " \
              "_id={_id} AND likes_count > 0".format(db_name=consts.DATABASE_NAME,
                                                     table_name=consts.TABLE_NAME,
                                                     operator=str(operator),
                                                     _id=book_id)
    execute_query(sql=sql)
