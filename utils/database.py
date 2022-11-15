import pymysql
import os


class DbBooksSystem:
    """ This class is a helper class to connect to the system DB """
    @staticmethod
    def get_connection():
        user = os.environ['DB_USER_NAME']
        password = os.environ['DB_PASS']
        host = os.environ['DB_RDS_HOST']

        connection = pymysql.connect(user=user,
                                     password=password,
                                     host=host,
                                     cursorclass=pymysql.cursors.DictCursor,
                                     autocommit=True)
        return connection


DB_CONNECTION = DbBooksSystem.get_connection()
