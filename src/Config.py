import os
from dotenv import load_dotenv


def getenvNonNull(key) -> any:
    x = os.getenv(key)
    if x is None:
        raise RuntimeError('{} must be not null'.format(key))
    return x


class Config:

    def __init__(self):
        import os

        BASE_DIR = os.path.abspath(os.path.dirname(__file__))
        load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../.env'), verbose=True)

        self.MYSQL_USER = getenvNonNull('MYSQL_USER')
        self.MYSQL_PASSWD = getenvNonNull('MYSQL_PASSWD')
        self.MYSQL_DB = getenvNonNull('MYSQL_DB')
        self.MYSQL_HOST = getenvNonNull('MYSQL_HOST')
        self.MYSQL_CHARSET = getenvNonNull('MYSQL_CHARSET')
        self.MYSQL_PORT = int(getenvNonNull('MYSQL_PORT'))
        self.INPUT_DIR_PATH = os.getenv('INPUT_DIR_PATH') or './input'
        self.OUTPUT_DIR_PATH = os.getenv('OUTPUT_DIR_PATH') or './output'

    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls):
        cls.__instance = cls()
        cls.instance = cls.__getInstance
        return cls.__instance
