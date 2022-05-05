from src.common.repository.SQLUtil import SQLUtil
from src.converter.PerfumeConverter import PerfumeConverter


def main():
    PerfumeConverter().excel2db()


if __name__ == '__main__':
    SQLUtil.instance().logging = True
    main()
    SQLUtil.instance().rollback()
