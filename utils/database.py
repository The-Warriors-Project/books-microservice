import os

import pymysql


class DbBooksSystem:
    """ This class is a helper class to connect to the system DB """
    @staticmethod
    def get_connection():
        try:
            user = os.environ['DB_USER_NAME']
            password = os.environ['DB_PASS']
            host = os.environ['DB_RDS_HOST']

            connection = pymysql.connect(user=user,
                                         password=password,
                                         host=host,
                                         cursorclass=pymysql.cursors.DictCursor,
                                         autocommit=True)
        except Exception:
            return False
        return connection


DB_CONNECTION = DbBooksSystem.get_connection()


def check_db_connection():
    """
    This function make check whether the RDS is connected or not.
    By having the function, the app stays up even though the RDS is off.
    :return: the connection
    """
    db_connection = DB_CONNECTION
    if not DB_CONNECTION:
        db_connection = DbBooksSystem.get_connection()
    return db_connection
