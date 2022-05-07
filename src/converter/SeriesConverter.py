import os

from src.common.repository.SQLUtil import SQLUtil
from src.common.util.excelParser import ExcelColumn
from src.converter.Converter import Converter


class SeriesConverter(Converter):

    def __init__(self):
        super().__init__("{}_series_raw".format(os.getenv('MYSQL_DB')))

    def get_data_list(self):
        SQLUtil.instance().execute(
            sql="SELECT s.series_idx AS {}, s.name AS {}, s.english_name AS {}, s.description AS {}, "
                "s.image_url AS {} FROM series AS s"
                .format(ExcelColumn.COL_IDX, ExcelColumn.COL_NAME, ExcelColumn.COL_ENGLISH_NAME,
                        ExcelColumn.COL_DESCRIPTION, ExcelColumn.COL_IMAGE_URL))

        return SQLUtil.instance().fetchall()

    def update_excel(self, excel_file):
        pass
