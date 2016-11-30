import pymysql


class DatabaseConnection(object):
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db

    def __enter__(self):
        self.connection = pymysql.connect(host=self.host,
                                          user=self.user,
                                          password=self.password,
                                          db=self.db,
                                          cursorclass=pymysql.cursors.DictCursor)
        return self.connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def create_connection():
    return DatabaseConnection('SandSpider2234.mysql.pythonanywhere-services.com',
                              'SandSpider2234',
                              '***REMOVED***',
                              'SandSpider2234$users')
