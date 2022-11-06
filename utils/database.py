import pymysql


# TODO: changing the connection to the AWS
class DbBooksSystem:
    """ This class is a helper class to connect to the system DB """
    @staticmethod
    def get_connection():
        user = "root"  # "admin"
        password = "dbuserdbuser" #"the_warriors"
        host = "localhost"  #"books.ci6gsofoisc0.us-east-1.rds.amazonaws.com"

        connection = pymysql.connect(user=user,
                                     password=password,
                                     host=host,
                                     cursorclass=pymysql.cursors.DictCursor,
                                     autocommit=True)
        return connection


DB_CONNECTION = DbBooksSystem.get_connection()