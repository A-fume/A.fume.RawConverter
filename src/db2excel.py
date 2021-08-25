import os
import pandas as pd

from dotenv import load_dotenv

from src.data.PerfumeDetail import PerfumeDetail
from src.repository.KeywordRepository import get_keyword_by_idx
from src.repository.SQLUtil import SQLUtil
from src.util.excelParser import ExcelColumn

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../.env'), verbose=True)

note_arr = "top/middle/base/single".split('/')


def main():
    SQLUtil.instance().execute(sql='SELECT p.perfume_idx AS {}, '.format(ExcelColumn.COL_IDX) +
                                   'p.name AS {},'.format(ExcelColumn.COL_NAME) +
                                   'p.english_name AS {},'.format(ExcelColumn.COL_ENGLISH_NAME) +
                                   'b.name AS {},'.format(ExcelColumn.COL_BRAND) +
                                   'p.image_url AS {},'.format(ExcelColumn.COL_MAIN_IMAGE) +

                                   'pd.story AS {},'.format(ExcelColumn.COL_STORY) +
                                   'pd.volume_and_price AS {},'.format(ExcelColumn.COL_VOLUME_AND_PRICE) +
                                   'pd.abundance_rate AS {},'.format(ExcelColumn.COL_ABUNDANCE_RATE) +

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

                                   'AVG(r.score) AS `[평균점수]`, '
                                   '(SELECT COUNT(lp.user_idx) FROM like_perfumes AS lp WHERE '
                                   'lp.perfume_idx = p.perfume_idx) AS `[좋아요]`, '

                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx) '
                                   'AS `[리뷰개수]`, '

                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND seasonal = 0) AS `[계절감_평가X]`, '

                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND seasonal = 1) AS `[봄]` ,'

                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND seasonal = 2) AS `[여름]`, '

                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND seasonal = 3) AS `[가을]`, '

                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND seasonal = 4) AS `[겨울]`, '

                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND sillage = 0) AS `[잔향감_평가X]`, '
                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND sillage = 1) AS `[잔향감_가벼움]`, '
                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND sillage = 2) AS `[잔향감_보통]`, '
                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND sillage = 3) AS `[잔향감_무거움]`, '

                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND longevity = 0) AS `[지속감_평가X]`, '
                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND longevity = 1) AS `[지속감_매우_약함]`, '
                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND longevity = 2) AS `[지속감_약함]`, '
                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND longevity = 3) AS `[지속감_보통]`, '
                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND longevity = 4) AS `[지속감_강함]`, '
                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND longevity = 5) AS `[지속감_매우_강함]`, '

                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND gender = 1) AS `[성별감_남성]`, '
                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND gender = 2) AS `[성별감_중성]`, '
                                   '(SELECT COUNT(id) FROM reviews WHERE perfume_idx = p.perfume_idx '
                                   'AND gender = 3) AS `[성별감_여성]`, '

                                   '(SELECT GROUP_CONCAT(k.name) FROM keywords AS k INNER JOIN '
                                   'join_perfume_keywords AS jpk ON k.id = jpk.perfume_idx '
                                   'WHERE jpk.perfume_idx = p.perfume_idx) AS `[키워드]`,'

                                   '" " AS `[국내 출시]` '

                                   'FROM perfumes AS p '
                                   'INNER JOIN perfume_details AS pd '
                                   'ON p.perfume_idx = pd.perfume_idx '
                                   'INNER JOIN brands AS b '
                                   'ON p.brand_idx = b.brand_idx '
                                   'LEFT JOIN reviews AS r '
                                   'ON p.perfume_idx = r.perfume_idx '
                                   'LEFT JOIN perfume_default_reviews AS pdr '
                                   'ON p.perfume_idx = pdr.perfume_idx '
                                   'GROUP BY p.perfume_idx')

    perfume_list = SQLUtil.instance().fetchall()

    for perfume in perfume_list:
        perfume[ExcelColumn.COL_ABUNDANCE_RATE] = PerfumeDetail.abundance_rate_list[
            perfume[ExcelColumn.COL_ABUNDANCE_RATE]]
        print(perfume[ExcelColumn.COL_DEFAULT_KEYWORD])
        keyword_idx_list = list(filter(lambda x: len(x) > 0, perfume[ExcelColumn.COL_DEFAULT_KEYWORD].split(",")))
        print(keyword_idx_list)
        perfume[ExcelColumn.COL_DEFAULT_KEYWORD] = ', '.join([get_keyword_by_idx(keyword_idx)['name'] for keyword_idx in
                                                    keyword_idx_list]) if len(keyword_idx_list) > 0 else ''
        print(perfume[ExcelColumn.COL_DEFAULT_KEYWORD])

    result = pd.DataFrame(perfume_list)
    print(result)

    file_nm = "../output/{}_raw.xlsx".format(os.getenv('MYSQL_DB'))
    xlxs_dir = os.path.join(BASE_DIR, file_nm)

    result.to_excel(xlxs_dir,
                    sheet_name='Sheet1',
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
