from src.common.data.Brand import Brand
from src.common.data.Ingredient import Ingredient
from src.common.data.Note import Note
from src.common.data.Perfume import Perfume
from src.common.data.PerfumeDefaultReview import PerfumeDefaultReview
from src.common.repository import KeywordRepository
from src.common.repository.IngredientRepository import get_ingredient_idx_by_name


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


def parse_note_str(note_str: str, perfume_idx: int, note_type: int) -> [Note]:
    note_list = []

    ingredient_list = [it.strip() for it in note_str.split(',')]

    for ingredient_name in ingredient_list:
        ingredient_idx = get_ingredient_idx_by_name(ingredient_name)
        note_list.append(Note(perfume_idx=perfume_idx, ingredient_idx=ingredient_idx, type=note_type))

    return note_list


class ExcelParser:

    @staticmethod
    def get_idx(columns_list, column):
        _idx = columns_list.index(column)
        if _idx == -1:
            raise Exception("Error Exception")
        return _idx

    @staticmethod
    def get_cell_value(row: [any], column_list: [str], column: str) -> any:
        idx = ExcelParser.get_idx(column_list, column)
        return row[idx].value

    @staticmethod
    def get_ingredient(row: [str], column_list: [str]) -> Ingredient:
        idx = row[ExcelParser.get_idx(column_list, ExcelColumn.COL_IDX)].value
        name = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_NAME)
        english_name = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_ENGLISH_NAME)
        description = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_DESCRIPTION)
        image_url = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_IMAGE_URL)
        return Ingredient(ingredient_idx=idx, name=name, english_name=english_name, description=description,
                          image_url=image_url)

    @staticmethod
    def get_brand(row: [str], column_list: [str]) -> Brand:
        idx = row[ExcelParser.get_idx(column_list, ExcelColumn.COL_IDX)].value
        name = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_NAME)
        english_name = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_ENGLISH_NAME)
        first_initial = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_FIRST_INITIAL)
        description = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_DESCRIPTION)
        image_url = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_IMAGE_URL)
        return Brand(brand_idx=idx, name=name, english_name=english_name, first_initial=first_initial,
                     description=description, image_url=image_url)

    @staticmethod
    def get_perfume(row: [str], column_list: [str]) -> Perfume:
        idx = row[ExcelParser.get_idx(column_list, ExcelColumn.COL_IDX)].value
        name = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_NAME)
        english_name = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_ENGLISH_NAME)
        image_url = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_MAIN_IMAGE)
        story = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_STORY)
        volume_and_price = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_VOLUME_AND_PRICE)
        abundance_rate_str = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_ABUNDANCE_RATE)
        abundance_rate = Perfume.abundance_rate_list.index(
            abundance_rate_str) if abundance_rate_str is not None else None

        if abundance_rate == -1:
            raise RuntimeError("abundance_rate_str is not invalid: " + abundance_rate_str)
        return Perfume(idx=idx, name=name, english_name=english_name, image_url=image_url, story=story,
                       volume_and_price=volume_and_price, abundance_rate=abundance_rate)

    @staticmethod
    def get_perfumeDefaultReview(row: [str], column_list: [str]) -> PerfumeDefaultReview:
        idx = row[ExcelParser.get_idx(column_list, ExcelColumn.COL_IDX)].value
        rating = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_DEFAULT_SCORE)
        seasonal = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_DEFAULT_SEASONAL)
        sillage = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_DEFAULT_SILLAGE)
        longevity = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_DEFAULT_LONGEVITY)
        gender = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_DEFAULT_GENDER)
        keyword = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_DEFAULT_KEYWORD)
        if keyword is not None:
            keyword_list = list(filter(lambda x: len(x) > 0, keyword.split(',')) if keyword is not None else [])
            for it in keyword_list:
                if it.isnumeric():
                    KeywordRepository.get_keyword_by_idx(int(it))
                else:
                    KeywordRepository.get_keyword_idx_by_name(it)
            keyword = ",".join(keyword_list)
        return PerfumeDefaultReview(idx=idx, rating=rating, seasonal=seasonal, sillage=sillage, longevity=longevity,
                                    gender=gender, keyword=keyword)

    @staticmethod
    def get_note_list(row: [str], column_list: [str]) -> any:
        perfume_idx = row[ExcelParser.get_idx(column_list, ExcelColumn.COL_IDX)].value

        top_note_str = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_TOP_NOTE)
        top_note_list = parse_note_str(top_note_str, perfume_idx, Note.TYPE_TOP)

        middle_note_str = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_MIDDLE_NOTE)
        middle_note_list = parse_note_str(middle_note_str, perfume_idx, Note.TYPE_MIDDLE)

        base_note_str = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_BASE_NOTE)
        base_note_list = parse_note_str(base_note_str, perfume_idx, Note.TYPE_BASE)

        single_note_str = ExcelParser.get_cell_value(row, column_list, ExcelColumn.COL_SINGLE_NOTE)
        single_note_list = parse_note_str(single_note_str, perfume_idx, Note.TYPE_SINGLE)

        return {top_note_list, middle_note_list, base_note_list, single_note_list}
