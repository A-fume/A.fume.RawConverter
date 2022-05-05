import os

from dotenv import load_dotenv

from src.common.repository.SQLUtil import SQLUtil
from src.converter.BrandConverter import BrandConverter

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)


def main():
    BrandConverter().excel2db()


if __name__ == '__main__':
    SQLUtil.instance().logging = True
    main()
    SQLUtil.instance().rollback()
