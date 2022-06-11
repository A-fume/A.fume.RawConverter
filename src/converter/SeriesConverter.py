from src.Config import Config
from src.common.data.Series import Series
from src.common.repository.SQLUtil import SQLUtil
from src.common.repository.SeriesRepository import update_series
from src.common.util.ExcelParser import ExcelColumn, ExcelParser
from src.converter.Converter import Converter


class SeriesConverter(Converter):

    def __init__(self):
        super().__init__("{}_series_raw".format(Config.instance().MYSQL_DB))
        self.parser = None

    def get_data_list(self):
        SQLUtil.instance().execute(
            sql="SELECT s.series_idx AS {}, s.name AS {}, s.english_name AS {}, s.description AS {}, "
                "s.image_url AS {} FROM series AS s"
                .format(ExcelColumn.COL_IDX, ExcelColumn.COL_NAME, ExcelColumn.COL_ENGLISH_NAME,
                        ExcelColumn.COL_DESCRIPTION, ExcelColumn.COL_IMAGE_URL))

        return SQLUtil.instance().fetchall()

    def prepare_parser(self, columns_list):
        self.parser = ExcelParser(columns_list, {
            'series_idx': ExcelColumn.COL_IDX,
            'name': ExcelColumn.COL_NAME,
            'english_name': ExcelColumn.COL_ENGLISH_NAME,
            'image_url': ExcelColumn.COL_IMAGE_URL,
            'description': ExcelColumn.COL_DESCRIPTION
        }, lambda result_json: Series(series_idx=result_json['series_idx'], name=result_json['name'],
                                      english_name=result_json['english_name'], image_url=result_json['image_url'],
                                      description=result_json['description']))

    def read_line(self, row):
        series = self.parser.parse(row)
        if series.get_json() is None:
            return
        update_series(series)
