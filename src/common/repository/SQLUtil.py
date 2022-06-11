import pymysql
from src.Config import Config


class SQLUtil:
    def __init__(self):
        self.db = self.get_db()
        self.cursor = self.get_cursor(self.db)
        self.logging = False

    def execute(self, sql, args=None):
        if self.logging:
            print(sql + " // " + str(args))
        if args is not None:
            result = self.cursor.execute(sql, tuple(args))
        else:
            result = self.cursor.execute(sql)
        if self.logging:
            print(result)
        return result

    def fetchall(self):
        return self.cursor.fetchall()

    def commit(self):
        self.db.commit()
        return

    def rollback(self):
        self.db.rollback()
        return

    @staticmethod
    def get_db():
        db = pymysql.connect(
            user=Config.instance().MYSQL_USER,
            passwd=Config.instance().MYSQL_PASSWD,
            host=Config.instance().MYSQL_HOST,
            db=Config.instance().MYSQL_DB,
            charset=Config.instance().MYSQL_CHARSET,
            port=Config.instance().MYSQL_PORT,
        )
        return db

    @staticmethod
    def get_cursor(db):
        return db.cursor(pymysql.cursors.DictCursor)

    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls):
        cls.__instance = cls()
        cls.instance = cls.__getInstance
        return cls.__instance


if __name__ == '__main__':
    print(SQLUtil.instance().execute(sql='select * from perfumes'))
