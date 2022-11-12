import pymysql


class DbBooksSystem:
    """ This class is a helper class to connect to the system DB """
    @staticmethod
    def get_connection():
        user = "admin"
        password = "the_warriors"
        host = "books.c4m5teyjg8v7.us-east-1.rds.amazonaws.com"

        connection = pymysql.connect(user=user,
                                     password=password,
                                     host=host,
                                     cursorclass=pymysql.cursors.DictCursor,
                                     autocommit=True)
        return connection


DB_CONNECTION = DbBooksSystem.get_connection()