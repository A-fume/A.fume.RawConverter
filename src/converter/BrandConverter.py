import os

from src.common.data.Brand import Brand
from src.common.repository.BrandRepository import update_brand
from src.converter.Converter import Converter
from src.common.repository.SQLUtil import SQLUtil
from src.common.util.ExcelParser import ExcelColumn, ExcelParser


class BrandConverter(Converter):

    def __init__(self):
        super().__init__("{}_brands_raw".format(os.getenv('MYSQL_DB')))
        self.parser = None

    def get_data_list(self):
        SQLUtil.instance().execute(
            sql="SELECT brand_idx AS '{}', name AS '{}', english_name AS '{}', first_initial AS '{}', image_url"
                " AS '{}', description AS {} FROM brands"
                .format(ExcelColumn.COL_IDX, ExcelColumn.COL_NAME, ExcelColumn.COL_ENGLISH_NAME,
                        ExcelColumn.COL_FIRST_INITIAL, ExcelColumn.COL_IMAGE_URL, ExcelColumn.COL_DESCRIPTION))

        return SQLUtil.instance().fetchall()

    def prepare_parser(self, columns_list):
        self.parser = ExcelParser(columns_list=columns_list, column_dict={
            'idx': ExcelColumn.COL_IDX,
            'name': ExcelColumn.COL_NAME,
            'english_name': ExcelColumn.COL_ENGLISH_NAME,
            'first_initial': ExcelColumn.COL_FIRST_INITIAL,
            'description': ExcelColumn.COL_DESCRIPTION,
            'image_url': ExcelColumn.COL_IMAGE_URL
        }, doTask=lambda json: Brand(brand_idx=json['idx'], name=json['name'], english_name=json['english_name'],
                                     first_initial=json['first_initial'],
                                     description=json['description'], image_url=json['image_url']))

    def read_line(self, row: any):
        brand = self.parser.parse(row)
        update_brand(brand)
