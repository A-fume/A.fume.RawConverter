import os

import openpyxl
from dotenv import load_dotenv

from src.data.Note import Note
from src.data.Perfume import Perfume
from src.data.PerfumeDefaultReview import PerfumeDefaultReview
from src.data.PerfumeDetail import PerfumeDetail
from src.repository.IngredientRepository import get_ingredient_idx_by_name
from src.repository.NoteRepository import update_note_list
from src.repository.PerfumeRepository import update_perfume_default_review, update_perfume, update_perfume_detail
from src.repository.SQLUtil import SQLUtil
from src.util.excelParser import get_changed_cell_value, get_idx, ExcelColumn

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../.env'), verbose=True)

abundance_rate_arr = "코롱/오 드 코롱/코롱 인텐스/오 드 퍼퓸/오 드 뚜왈렛".split('/')
note_arr = "top/middle/base/single".split('/')


def main():
    file_nm = "../input/{}_raw_update.xlsx".format(os.getenv('MYSQL_DB'))
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
        i += 1

        perfume = Perfume.create(row, columns_list)
        update_perfume(perfume)

        perfumeDetail = PerfumeDetail.create(row, columns_list)
        update_perfume_detail(perfumeDetail)

        perfumeDefaultReview = PerfumeDefaultReview.create(row, columns_list)
        update_perfume_default_review(perfumeDefaultReview)

        update_note(row, columns_list)


def update_note(row, column_list):
    perfume_idx = row[get_idx(column_list, ExcelColumn.COL_IDX)].value

    top_note_str = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_TOP_NOTE))
    if top_note_str is not None:
        top_note_list = parse_note_str(top_note_str, perfume_idx, Note.TYPE_TOP)
        update_note_list(perfume_idx=perfume_idx, update_list=top_note_list, note_type=Note.TYPE_TOP)

    middle_note_str = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_MIDDLE_NOTE))
    if middle_note_str is not None:
        middle_note_list = parse_note_str(middle_note_str, perfume_idx, Note.TYPE_MIDDLE)
        update_note_list(perfume_idx=perfume_idx, update_list=middle_note_list, note_type=Note.TYPE_MIDDLE)

    base_note_str = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_BASE_NOTE))
    if base_note_str is not None:
        base_note_list = parse_note_str(base_note_str, perfume_idx, Note.TYPE_BASE)
        update_note_list(perfume_idx=perfume_idx, update_list=base_note_list, note_type=Note.TYPE_BASE)

    single_note_str = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_SINGLE_NOTE))
    if single_note_str is not None:
        single_note_list = parse_note_str(single_note_str, perfume_idx, Note.TYPE_SINGLE)
        update_note_list(perfume_idx=perfume_idx, update_list=single_note_list, note_type=Note.TYPE_SINGLE)

    return


def parse_note_str(note_str, perfume_idx, type):
    note_list = []

    ingredient_list = [it.strip() for it in note_str.split(',')]

    for ingredient_name in ingredient_list:
        ingredient_idx = get_ingredient_idx_by_name(ingredient_name)
        note_list.append(Note(perfume_idx=perfume_idx, ingredient_idx=ingredient_idx, type=type))

    return note_list


if __name__ == '__main__':
    SQLUtil.instance().logging = True
    main()
    SQLUtil.instance().commit()
