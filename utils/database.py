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
            return None
        return connection
