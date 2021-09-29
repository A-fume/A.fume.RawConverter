import os

import pandas as pd
from dotenv import load_dotenv

from src.repository.SQLUtil import SQLUtil
from src.util.excelParser import ExcelColumn

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)


def main():
    SQLUtil.instance().execute(
        sql="SELECT brand_idx AS '{}', name AS '{}', english_name AS '{}', first_initial AS '{}', image_url AS '{}', "
            "description AS {} FROM brands"
            .format(ExcelColumn.COL_IDX, ExcelColumn.COL_NAME, ExcelColumn.COL_ENGLISH_NAME,
                    ExcelColumn.COL_FIRST_INITIAL, ExcelColumn.COL_IMAGE_URL, ExcelColumn.COL_DESCRIPTION))

    perfume_list = SQLUtil.instance().fetchall()

    result = pd.DataFrame(perfume_list)
    print(result)

    file_nm = "../../output/{}_brands_raw.xlsx".format(os.getenv('MYSQL_DB'))
    xlxs_dir = os.path.join(BASE_DIR, file_nm)

    result.to_excel(xlxs_dir,
                    sheet_name='brands',
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


if __name__ == '__main__':
    main()
