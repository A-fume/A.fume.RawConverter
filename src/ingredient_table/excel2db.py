from src.common.repository.SQLUtil import SQLUtil
from src.converter.IngredientConverter import IngredientConverter


def main():
    IngredientConverter().excel2db()


if __name__ == '__main__':
    SQLUtil.instance().logging = True
    main()
    SQLUtil.instance().rollback()
