import os
from abc import abstractmethod, ABCMeta

import openpyxl
import pandas as pd

from Config import Config
from src.common.Strings import CommandStr
from src.common.repository.SQLUtil import SQLUtil


class Converter(metaclass=ABCMeta):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_data_list(self):
        pass

    def db2excel(self):
        data_list = self.get_data_list()

        result = pd.DataFrame(data_list)
        print(result)

        if os.path.exists(Config.instance().OUTPUT_DIR_PATH) is False:
            os.makedirs(Config.instance().OUTPUT_DIR_PATH)

        file_nm = "{}.xlsx".format(self.name)
        xlxs_dir = os.path.join(Config.instance().OUTPUT_DIR_PATH, file_nm)

        result.to_excel(xlxs_dir,
                        sheet_name=self.name,
                        na_rep='',
                        float_format="%.2f",
                        header=True,
                        index=False,
                        index_label="id",
                        startrow=1,
                        startcol=1,
                        # engine = 'xlsxwriter',
                        freeze_panes=(2, 0)
                        )

    def excel2db(self):
        file_nm = "{}.xlsx".format(self.name)
        xlxs_dir = os.path.join(Config.instance().INPUT_DIR_PATH, file_nm)

        excel_file = openpyxl.load_workbook(xlxs_dir)

        sheet1 = excel_file.active
        columns_list = [cell.value for cell in sheet1['A2:AK2'][0]]
        self.prepare_parser(columns_list)
        i = 3
        while True:
            row = sheet1['A{}:AK{}'.format(i, i)][0]

            filtered = list(filter(lambda x: x is not None and len(str(x)) > 0, [cell.value for cell in row]))
            if len(filtered) == 0:
                break
            self.read_line(row)
            i += 1

    @abstractmethod
    def prepare_parser(self, columns_list):
        pass

    @abstractmethod
    def read_line(self, row):
        pass

    def do_command(self, command_str):
        SQLUtil.instance().logging = True
        if command_str == CommandStr.db2excel:
            self.db2excel()
        elif command_str == CommandStr.excel2db:
            self.excel2db()
            if Config.instance().DEBUG:
                SQLUtil.instance().rollback()
            else:
                SQLUtil.instance().commit()
        else:
            raise RuntimeError('Unknown Command')
