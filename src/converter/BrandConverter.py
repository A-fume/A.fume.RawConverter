import os

from src.common.data.Brand import Brand
from src.common.repository.BrandRepository import update_brand
from src.converter.Converter import Converter
from src.common.repository.SQLUtil import SQLUtil
from src.common.util.ExcelParser import ExcelColumn, ExcelParser


class BrandConverter(Converter):

    def __init__(self):
        super().__init__("{}_brands_raw".format(os.getenv('MYSQL_DB')))

    def get_data_list(self):
        SQLUtil.instance().execute(
            sql="SELECT brand_idx AS '{}', name AS '{}', english_name AS '{}', first_initial AS '{}', image_url"
                " AS '{}', description AS {} FROM brands"
                .format(ExcelColumn.COL_IDX, ExcelColumn.COL_NAME, ExcelColumn.COL_ENGLISH_NAME,
                        ExcelColumn.COL_FIRST_INITIAL, ExcelColumn.COL_IMAGE_URL, ExcelColumn.COL_DESCRIPTION))

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
            brand = ExcelParser.get_brand(row, columns_list)
            update_brand(brand)
            i += 1
