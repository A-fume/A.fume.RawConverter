import os

import pandas as pd
from dotenv import load_dotenv

from src.repository.SQLUtil import SQLUtil
from src.util.excelParser import ExcelColumn

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)


def main():
    SQLUtil.instance().logging = True
    SQLUtil.instance().execute(
        sql="SELECT i.ingredient_idx AS {}, i.name AS {}, i.english_name AS {}, i.description AS {}, "
            "i.image_url AS {}, i.series_idx AS {}, s.name AS {} "
            "FROM ingredients i INNER JOIN series s ON s.series_idx = i.series_idx"
            .format(ExcelColumn.COL_IDX, ExcelColumn.COL_NAME, ExcelColumn.COL_ENGLISH_NAME,
                    ExcelColumn.COL_DESCRIPTION, ExcelColumn.COL_IMAGE_URL,
                    ExcelColumn.COL_SERIES_IDX, ExcelColumn.COL_SERIES_NAME))

    perfume_list = SQLUtil.instance().fetchall()

    result = pd.DataFrame(perfume_list)
    print(result)

    file_nm = "../../output/{}_ingredients_raw.xlsx".format(os.getenv('MYSQL_DB'))
    xlxs_dir = os.path.join(BASE_DIR, file_nm)

    result.to_excel(xlxs_dir,
                    sheet_name='ingredients',
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
