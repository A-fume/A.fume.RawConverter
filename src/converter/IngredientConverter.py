import os

from src.common.data.Ingredient import Ingredient
from src.common.repository.IngredientRepository import update_ingredient
from src.common.repository.SQLUtil import SQLUtil
from src.common.util.ExcelParser import ExcelColumn, ExcelParser
from src.converter.Converter import Converter


class IngredientConverter(Converter):

    def __init__(self):
        super().__init__("{}_ingredients_raw".format(os.getenv('MYSQL_DB')))

    def get_data_list(self):
        SQLUtil.instance().execute(
            sql="SELECT i.ingredient_idx AS {}, i.name AS {}, i.english_name AS {}, i.description AS {}, "
                "i.image_url AS {}, i.series_idx AS {}, s.name AS {} "
                "FROM ingredients i INNER JOIN series s ON s.series_idx = i.series_idx ORDER BY i.ingredient_idx"
                .format(ExcelColumn.COL_IDX, ExcelColumn.COL_NAME, ExcelColumn.COL_ENGLISH_NAME,
                        ExcelColumn.COL_DESCRIPTION, ExcelColumn.COL_IMAGE_URL,
                        ExcelColumn.COL_SERIES_IDX, ExcelColumn.COL_SERIES_NAME))

        return SQLUtil.instance().fetchall()

    def update_excel(self, excel_file):
        sheet1 = excel_file.active
        columns_list = [cell.value for cell in sheet1['A2:AK2'][0]]
        i = 3

        while True:
            row = sheet1['A{}:AK{}'.format(i, i)][0]

            filtered = list(filter(lambda x: x is not None and len(str(x)) > 0, [cell.value for cell in row]))
            if len(filtered) == 0:
                break
            ingredient = ExcelParser.get_ingredient(row, columns_list)
            update_ingredient(ingredient)
            i += 1
