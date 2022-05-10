import os

from src.common.data.Note import Note
from src.common.data.Perfume import Perfume
from src.common.repository.KeywordRepository import get_keyword_by_idx
from src.common.repository.NoteRepository import update_note_list
from src.common.repository.PerfumeRepository import update_perfume_default_review, update_perfume
from src.common.repository.SQLUtil import SQLUtil
from src.common.util.ExcelParser import ExcelColumn, ExcelParser
from src.converter.Converter import Converter


def update_note(row, column_list):
    perfume_idx = row[ExcelParser.get_idx(column_list, ExcelColumn.COL_IDX)].value
    top_note_list, middle_note_list, single_note_list, base_note_list = ExcelParser.get_note_list(row, column_list)

    update_note_list(perfume_idx=perfume_idx, update_list=top_note_list, note_type=Note.TYPE_TOP)
    update_note_list(perfume_idx=perfume_idx, update_list=middle_note_list, note_type=Note.TYPE_MIDDLE)
    update_note_list(perfume_idx=perfume_idx, update_list=base_note_list, note_type=Note.TYPE_BASE)
    update_note_list(perfume_idx=perfume_idx, update_list=single_note_list, note_type=Note.TYPE_SINGLE)

    return


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
        i = 3

        while True:
            row = sheet1['A{}:AK{}'.format(i, i)][0]

            filtered = list(filter(lambda x: x is not None and len(str(x)) > 0, [cell.value for cell in row]))
            if len(filtered) == 0:
                break
            i += 1

            perfume = ExcelParser.get_perfume(row, columns_list)
            update_perfume(perfume)

            perfumeDefaultReview = ExcelParser.get_perfumeDefaultReview(row, columns_list)
            update_perfume_default_review(perfumeDefaultReview)

            update_note(row, columns_list)
