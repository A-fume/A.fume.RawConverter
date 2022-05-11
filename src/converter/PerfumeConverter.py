import os

from src.common.data.Note import Note
from src.common.data.Perfume import Perfume
from src.common.data.PerfumeDefaultReview import PerfumeDefaultReview
from src.common.repository import KeywordRepository
from src.common.repository.IngredientRepository import get_ingredient_idx_by_name
from src.common.repository.KeywordRepository import get_keyword_by_idx
from src.common.repository.NoteRepository import update_note_list
from src.common.repository.PerfumeRepository import update_perfume_default_review, update_perfume
from src.common.repository.SQLUtil import SQLUtil
from src.common.util.ExcelParser import ExcelColumn, ExcelParser
from src.converter.Converter import Converter


class PerfumeConverter(Converter):
    def __init__(self):
        super().__init__("{}_perfumes_raw".format(os.getenv('MYSQL_DB')))

    def get_data_list(self):
        SQLUtil.instance().execute(sql='SELECT p.perfume_idx AS {}, '.format(ExcelColumn.COL_IDX) +
                                       'p.name AS {},'.format(ExcelColumn.COL_NAME) +
                                       'p.english_name AS {},'.format(ExcelColumn.COL_ENGLISH_NAME) +
                                       'b.name AS {},'.format(ExcelColumn.COL_BRAND) +
                                       'p.image_url AS {},'.format(ExcelColumn.COL_MAIN_IMAGE) +

                                       'p.story AS {},'.format(ExcelColumn.COL_STORY) +
                                       'p.volume_and_price AS {},'.format(ExcelColumn.COL_VOLUME_AND_PRICE) +
                                       'p.abundance_rate AS {},'.format(ExcelColumn.COL_ABUNDANCE_RATE) +

                                       '(SELECT GROUP_CONCAT(name) FROM notes AS n INNER JOIN ingredients '
                                       'AS i ON n.ingredient_idx = i.ingredient_idx WHERE n.perfume_idx = '
                                       'p.perfume_idx AND n.`type` = 1 ) AS {},'.format(ExcelColumn.COL_TOP_NOTE) +

                                       '(SELECT GROUP_CONCAT(name) FROM notes AS n INNER JOIN ingredients '
                                       'AS i ON n.ingredient_idx = i.ingredient_idx WHERE n.perfume_idx = '
                                       'p.perfume_idx AND n.`type` = 2 ) AS {},'.format(ExcelColumn.COL_MIDDLE_NOTE) +

                                       '(SELECT GROUP_CONCAT(name) FROM notes AS n INNER JOIN ingredients '
                                       'AS i ON n.ingredient_idx = i.ingredient_idx WHERE n.perfume_idx = '
                                       'p.perfume_idx AND n.`type` = 3 ) AS {},'.format(ExcelColumn.COL_BASE_NOTE) +

                                       '(SELECT GROUP_CONCAT(name) FROM notes AS n INNER JOIN ingredients '
                                       'AS i ON n.ingredient_idx = i.ingredient_idx WHERE n.perfume_idx = '
                                       'p.perfume_idx AND n.`type` = 4 ) AS {},'.format(ExcelColumn.COL_SINGLE_NOTE) +

                                       'IFNULL(pdr.keyword, "") AS {},'.format(ExcelColumn.COL_DEFAULT_KEYWORD) +
                                       'IFNULL(pdr.rating, "") AS {},'.format(ExcelColumn.COL_DEFAULT_SCORE) +
                                       'IFNULL(pdr.seasonal, "") AS `{}`,'.format(ExcelColumn.COL_DEFAULT_SEASONAL) +
                                       'IFNULL(pdr.sillage, "") AS  `{}`,'.format(ExcelColumn.COL_DEFAULT_SILLAGE) +
                                       'IFNULL(pdr.longevity, "") AS `{}`,'.format(ExcelColumn.COL_DEFAULT_LONGEVITY) +
                                       'IFNULL(pdr.gender, "") AS `{}`,'.format(ExcelColumn.COL_DEFAULT_GENDER) +

                                       # 'AVG(r.score) AS `[평균점수]`, '
                                       # '(SELECT COUNT(lp.user_idx) FROM like_perfumes AS lp WHERE '
                                       # 'lp.perfume_idx = p.perfume_idx) AS `[좋아요]`, '

                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx) '
                                       # 'AS `[리뷰개수]`, '
                                       # 
                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND seasonal = 0) AS `[계절감_평가X]`, '
                                       # 
                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND seasonal = 1) AS `[봄]` ,'
                                       # 
                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND seasonal = 2) AS `[여름]`, '
                                       # 
                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND seasonal = 3) AS `[가을]`, '
                                       # 
                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND seasonal = 4) AS `[겨울]`, '
                                       # 
                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND sillage = 0) AS `[잔향감_평가X]`, '
                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND sillage = 1) AS `[잔향감_가벼움]`, '
                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND sillage = 2) AS `[잔향감_보통]`, '
                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND sillage = 3) AS `[잔향감_무거움]`, '

                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND longevity = 0) AS `[지속감_평가X]`, '
                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND longevity = 1) AS `[지속감_매우_약함]`, '
                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND longevity = 2) AS `[지속감_약함]`, '
                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND longevity = 3) AS `[지속감_보통]`, '
                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND longevity = 4) AS `[지속감_강함]`, '
                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND longevity = 5) AS `[지속감_매우_강함]`, '

                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND gender = 1) AS `[성별감_남성]`, '
                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND gender = 2) AS `[성별감_중성]`, '
                                       # '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                       # 'AND gender = 3) AS `[성별감_여성]`, '

                                       # '(SELECT GROUP_CONCAT(k.name) FROM keywords AS k INNER JOIN '
                                       # 'join_perfume_keywords AS jpk ON k.id = jpk.perfume_idx '
                                       # 'WHERE jpk.perfume_idx = p.perfume_idx) AS `[키워드]`,'

                                       '" " AS `[국내 출시]` '

                                       'FROM perfumes AS p '
                                       'INNER JOIN brands AS b '
                                       'ON p.brand_idx = b.brand_idx '
                                       # 'LEFT JOIN reviews AS r '
                                       # 'ON p.perfume_idx = r.perfume_idx '
                                       'LEFT JOIN perfume_default_reviews AS pdr '
                                       'ON p.perfume_idx = pdr.perfume_idx '
                                       'GROUP BY p.perfume_idx')

        perfume_list = SQLUtil.instance().fetchall()

        for perfume in perfume_list:
            perfume[ExcelColumn.COL_ABUNDANCE_RATE] = Perfume.abundance_rate_list[
                perfume[ExcelColumn.COL_ABUNDANCE_RATE]]
            # print(perfume[ExcelColumn.COL_DEFAULT_KEYWORD])
            keyword_idx_list = list(filter(lambda x: len(x) > 0, perfume[ExcelColumn.COL_DEFAULT_KEYWORD].split(",")))
            # print(keyword_idx_list)
            perfume[ExcelColumn.COL_DEFAULT_KEYWORD] = ', '.join(
                [get_keyword_by_idx(keyword_idx)['name'] for keyword_idx in
                 keyword_idx_list]) if len(keyword_idx_list) > 0 else ''
            # print(perfume[ExcelColumn.COL_DEFAULT_KEYWORD])

        return perfume_list

    def update_excel(self, excel_file):
        sheet1 = excel_file.active
        columns_list = [cell.value for cell in sheet1['A2:AK2'][0]]

        def doTaskPerfume(json) -> Perfume:
            abundance_rate = Perfume.abundance_rate_list.index(
                json['abundance_rate_str']) if json['abundance_rate_str'] is not None else None
            if abundance_rate == -1:
                raise RuntimeError("abundance_rate_str is not invalid: " + json['abundance_rate_str'])
            return Perfume(idx=json['perfume_idx'], name=json['name'], english_name=json['english_name'],
                           image_url=json['image_url'], story=json['story'],
                           volume_and_price=json['volume_and_price'], abundance_rate=abundance_rate)

        def doTaskDefaultReview(json) -> PerfumeDefaultReview:
            if json['keyword'] is not None:
                keyword_list = list(
                    filter(lambda x: len(x) > 0, json['keyword'].split(',')) if json['keyword'] is not None else [])
                for it in keyword_list:
                    if it.isnumeric():
                        KeywordRepository.get_keyword_by_idx(int(it))
                    else:
                        KeywordRepository.get_keyword_idx_by_name(it)
                json['keyword'] = ",".join(keyword_list)
            return PerfumeDefaultReview(idx=json['idx'], rating=json['rating'], seasonal=json['seasonal'],
                                        sillage=json['sillage'], longevity=json['longevity'],
                                        gender=json['gender'], keyword=json['keyword'])

        def doTaskNoteList(json) -> dict:
            perfume_idx = json['perfume_idx']

            def parse_note_str(note_str: str, note_type: int) -> [Note]:
                if note_str is None:
                    return []

                note_list = []
                ingredient_list = [it.strip() for it in note_str.split(',')]

                for ingredient_name in ingredient_list:
                    ingredient_idx = get_ingredient_idx_by_name(ingredient_name)
                    note_list.append(Note(perfume_idx=perfume_idx, ingredient_idx=ingredient_idx, type=note_type))

                return note_list

            ret = {Note.TYPE_TOP: parse_note_str(json['top_note_str'], Note.TYPE_TOP),
                   Note.TYPE_MIDDLE: parse_note_str(json['middle_note_str'], Note.TYPE_MIDDLE),
                   Note.TYPE_BASE: parse_note_str(json['base_note_str'], Note.TYPE_BASE),
                   Note.TYPE_SINGLE: parse_note_str(json['single_note_str'], Note.TYPE_SINGLE)}
            return ret

        perfume_parser = ExcelParser(columns_list, {
            'perfume_idx': ExcelColumn.COL_IDX,
            'name': ExcelColumn.COL_NAME,
            'english_name': ExcelColumn.COL_ENGLISH_NAME,
            'image_url': ExcelColumn.COL_MAIN_IMAGE,
            'story': ExcelColumn.COL_STORY,
            'volume_and_price': ExcelColumn.COL_VOLUME_AND_PRICE,
            'abundance_rate_str': ExcelColumn.COL_ABUNDANCE_RATE
        }, doTaskPerfume)

        default_review_parser = ExcelParser(columns_list, {
            'idx': ExcelColumn.COL_IDX,
            'rating': ExcelColumn.COL_DEFAULT_SCORE,
            'seasonal': ExcelColumn.COL_DEFAULT_SEASONAL,
            'sillage': ExcelColumn.COL_DEFAULT_SILLAGE,
            'longevity': ExcelColumn.COL_DEFAULT_LONGEVITY,
            'gender': ExcelColumn.COL_DEFAULT_GENDER,
            'keyword': ExcelColumn.COL_DEFAULT_KEYWORD
        }, doTaskDefaultReview)

        note_parser = ExcelParser(columns_list, {
            'perfume_idx': ExcelColumn.COL_IDX,
            'top_note_str': ExcelColumn.COL_TOP_NOTE,
            'middle_note_str': ExcelColumn.COL_MIDDLE_NOTE,
            'base_note_str': ExcelColumn.COL_BASE_NOTE,
            'single_note_str': ExcelColumn.COL_SINGLE_NOTE
        }, doTaskNoteList)

        i = 3

        while True:
            row = sheet1['A{}:AK{}'.format(i, i)][0]

            filtered = list(filter(lambda x: x is not None and len(str(x)) > 0, [cell.value for cell in row]))
            if len(filtered) == 0:
                break
            i += 1

            perfume = perfume_parser.parse(row)
            update_perfume(perfume)

            perfumeDefaultReview = default_review_parser.parse(row)
            update_perfume_default_review(perfumeDefaultReview)

            note_dict = note_parser.parse(row)
            for note_type, note_list in note_dict.items():
                update_note_list(perfume_idx=perfume.idx, update_list=note_list, note_type=note_type)
