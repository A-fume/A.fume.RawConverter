from src.common.data.Brand import Brand
from src.common.data.Ingredient import Ingredient


class ExcelColumn:
    COL_IDX = 'idx'
    COL_NAME = '이름'
    COL_ENGLISH_NAME = '영어_이름'
    COL_BRAND = '브랜드'
    COL_MAIN_IMAGE = '향수_대표_이미지'
    COL_STORY = '조향_스토리'
    COL_VOLUME_AND_PRICE = '용량_가격'
    COL_ABUNDANCE_RATE = '부향률'
    COL_TOP_NOTE = '탑노트'
    COL_MIDDLE_NOTE = '미들노트'
    COL_BASE_NOTE = '베이스노트'
    COL_SINGLE_NOTE = '싱글노트'
    COL_DEFAULT_KEYWORD = '키워드_default'
    COL_DEFAULT_SCORE = '별점_default'
    COL_DEFAULT_SEASONAL = '계절감_default_봄/여름/가을/겨울'
    COL_DEFAULT_SILLAGE = '잔향감_default_가벼움/중간/무거움'
    COL_DEFAULT_LONGEVITY = '지속감_default_매우약함/약함/보통/강함/매우강함'
    COL_DEFAULT_GENDER = '성별감_default_남성/중성/여성'

    COL_IMAGE_URL = '이미지'
    COL_DESCRIPTION = '설명'
    COL_FIRST_INITIAL = '시작 초성'
    COL_SERIES_IDX = "계열_id"
    COL_SERIES_NAME = "계열_이름"


CELL_COLOR_NONE = '00000000'
CELL_COLOR_UPDATE = 'FFFFFF00'
CELL_COLOR_SKIP = 'FFFFC000'
CELL_COLOR_DELETED = 'FF'
CELL_COLOR_ADDED = 'FF'


def get_idx(columns_list, column):
    _idx = columns_list.index(column)
    if _idx == -1:
        raise Exception("Error Exception")
    return _idx


def get_changed_cell_value(row, column_list: [str], column: str):
    idx = get_idx(column_list, column)
    cell = row[idx]
    return get_cell_value(cell)


def get_cell_value(cell):
    if cell.fill.start_color.rgb == CELL_COLOR_NONE:
        return None
    if cell.fill.start_color.rgb == CELL_COLOR_SKIP:
        return None
    if cell.fill.start_color.rgb == CELL_COLOR_UPDATE:
        return cell.value
    raise RuntimeError("Unexpected cell background color {}".format(cell.fill.start_color.rgb))


class ExcelParser:

    def __init__(self, columns_list: [str], column_dict: dict, doTask: any):
        self.columns_list = columns_list
        self.columns_idx_dict = {
            prop: columns_list.index(column)
            for prop, column in column_dict.items()
        }
        self.doTask = doTask

    def get_json(self, row: [str]) -> any:
        ret = {}
        for prop, idx in self.columns_idx_dict.items():
            cell = row[idx]
            ret[prop] = get_cell_value(cell) if idx != 1 else cell.value
        return ret

    def parse(self, row: [str]) -> any:
        json = self.get_json(row)
        if self.doTask:
            json = self.doTask(json)
        return json

    @staticmethod
    def get_ingredient(row: [str], column_list: [str]) -> Ingredient:
        idx = row[get_idx(column_list, ExcelColumn.COL_IDX)].value
        name = get_changed_cell_value(row, column_list, ExcelColumn.COL_NAME)
        english_name = get_changed_cell_value(row, column_list, ExcelColumn.COL_ENGLISH_NAME)
        description = get_changed_cell_value(row, column_list, ExcelColumn.COL_DESCRIPTION)
        image_url = get_changed_cell_value(row, column_list, ExcelColumn.COL_IMAGE_URL)
        return Ingredient(ingredient_idx=idx, name=name, english_name=english_name, description=description,
                          image_url=image_url)

    @staticmethod
    def get_brand(row: [str], column_list: [str]) -> Brand:
        idx = row[get_idx(column_list, ExcelColumn.COL_IDX)].value
        name = get_changed_cell_value(row, column_list, ExcelColumn.COL_NAME)
        english_name = get_changed_cell_value(row, column_list, ExcelColumn.COL_ENGLISH_NAME)
        first_initial = get_changed_cell_value(row, column_list, ExcelColumn.COL_FIRST_INITIAL)
        description = get_changed_cell_value(row, column_list, ExcelColumn.COL_DESCRIPTION)
        image_url = get_changed_cell_value(row, column_list, ExcelColumn.COL_IMAGE_URL)
        return Brand(brand_idx=idx, name=name, english_name=english_name, first_initial=first_initial,
                     description=description, image_url=image_url)