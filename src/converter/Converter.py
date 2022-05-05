import os
from abc import abstractmethod

import openpyxl
import pandas as pd
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)


class Converter:
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_data_list(self):
        pass

    @abstractmethod
    def update_excel(self, excel_file):
        pass

    def db2excel(self):
        data_list = self.get_data_list()

        result = pd.DataFrame(data_list)
        print(result)

        if os.path.exists('../output') is False:
            os.makedirs('../output')

        file_nm = "../../output/{}.xlsx".format(self.name)
        xlxs_dir = os.path.join(BASE_DIR, file_nm)

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
        file_nm = "../../input/{}.xlsx".format(self.name)
        xlxs_dir = os.path.join(BASE_DIR, file_nm)

        excel_file = openpyxl.load_workbook(xlxs_dir)
        self.update_excel(excel_file)
