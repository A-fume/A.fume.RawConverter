import os

import openpyxl
from dotenv import load_dotenv

from src.common.data.Brand import Brand
from src.common.repository.BrandRepository import update_brand
from src.common.repository.SQLUtil import SQLUtil

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)


def main():
    file_nm = "../../input/{}_brands_raw.xlsx".format(os.getenv('MYSQL_DB'))
    xlxs_dir = os.path.join(BASE_DIR, file_nm)

    excel_file = openpyxl.load_workbook(xlxs_dir)
    sheet1 = excel_file.active
    columns_list = [cell.value for cell in sheet1['A2:AK2'][0]]
    i = 3

    while True:
        row = sheet1['A{}:AK{}'.format(i, i)][0]

        filtered = list(filter(lambda x: x is not None and len(str(x)) > 0, [cell.value for cell in row]))
        if len(filtered) == 0:
            break
        brand = Brand.create(row, columns_list)
        update_brand(brand)
        i += 1


if __name__ == '__main__':
    SQLUtil.instance().logging = True
    main()
    SQLUtil.instance().commit()
