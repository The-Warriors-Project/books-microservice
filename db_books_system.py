import pymysql
from typing import Optional


class DbBooksSystem:
    """ This class is a helper class to connect to the system DB """
    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        user = "root"  # "admin"
        password =  "dbuserdbuser" #"the_warriors"
        host = "localhost"  #"books.ci6gsofoisc0.us-east-1.rds.amazonaws.com"

        connection = pymysql.connect(user=user,
                                     password=password,
                                     host=host,
                                     cursorclass=pymysql.cursors.DictCursor,
                                     autocommit=True)
        return connection

    @staticmethod
    def get_data(sql: str, argument: Optional[str] = None):
        """
        This function takes sql query and returns its result
        :param sql: the sql statement
        :param argument: the needed argument
        :return: data
        """
        connection = DbBooksSystem._get_connection()
        cursor = connection.cursor()
        _ = cursor.execute(sql, args=argument)  # provide the number of results
        final_result = cursor.fetchone()  # provide the actual result (with data)

        return final_result
