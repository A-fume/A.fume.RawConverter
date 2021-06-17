import os
import pandas as pd

from dotenv import load_dotenv

from src.repository.SQLUtil import SQLUtil

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../.env'), verbose=True)

abundance_rate_arr = "코롱/오 드 코롱/코롱 인텐스/오 드 퍼퓸/오 드 뚜왈렛".split('/')
note_arr = "top/middle/base/single".split('/')

if __name__ == '__main__':
    base_columns = ['idx', '이름', '제품_영어_이름', '브랜드', '조향_스토리', '용량_가격', '부향률']
    columns = base_columns + ['탑노트', '미들 노트', '베이스 노트', '싱글 노트']

    perfume_list = SQLUtil.instance().execute(sql='SELECT p.perfume_idx AS idx, '
                                                  'p.name AS 이름,'
                                                  'p.english_name AS 영어_이름, '
                                                  'b.name AS 브랜드, '
                                                  'p.image_url AS 향수_대표_이미지, '
                                                  
                                                  'pd.story AS 조향_스토리, '
                                                  'pd.volume_and_price AS 용량_가격, '
                                                  'pd.abundance_rate AS 부향률, '

                                                  '(SELECT GROUP_CONCAT(name) FROM notes AS n INNER JOIN ingredients '
                                                  'AS i ON n.ingredient_idx = i.ingredient_idx WHERE n.perfume_idx = '
                                                  'p.perfume_idx AND n.`type` = 1 ) AS 탑노트, '

                                                  '(SELECT GROUP_CONCAT(name) FROM notes AS n INNER JOIN ingredients '
                                                  'AS i ON n.ingredient_idx = i.ingredient_idx WHERE n.perfume_idx = '
                                                  'p.perfume_idx AND n.`type` = 2 ) AS 미들노트, '

                                                  '(SELECT GROUP_CONCAT(name) FROM notes AS n INNER JOIN ingredients '
                                                  'AS i ON n.ingredient_idx = i.ingredient_idx WHERE n.perfume_idx = '
                                                  'p.perfume_idx AND n.`type` = 3 ) AS 베이스노트, '
    
                                                  '(SELECT GROUP_CONCAT(name) FROM notes AS n INNER JOIN ingredients '
                                                  'AS i ON n.ingredient_idx = i.ingredient_idx WHERE n.perfume_idx = '
                                                  'p.perfume_idx AND n.`type` = 4 ) AS 싱글노트, '

                                                  '(SELECT GROUP_CONCAT(k.name) FROM keywords AS k INNER JOIN '
                                                  'join_perfume_keywords AS jpk ON k.id = jpk.perfume_idx '
                                                  'WHERE jpk.perfume_idx = p.perfume_idx) AS 키워드, ' 

                                                  'IFNULL(pdr.seasonal, "") AS 계절감_default, '
                                                  'IFNULL(pdr.sillage, "") AS 잔향감_default, ' 
                                                  'IFNULL(pdr.longevity, "") AS 지속감_default, '
                                                  
                                                  'AVG(r.score) AS `[평균점수]`, '
                                                  '(SELECT COUNT(lp.user_idx) FROM like_perfumes AS lp WHERE '
                                                  'lp.perfume_idx = p.perfume_idx) AS 좋아요, '
                                                  
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
                                                  'AND longevity = 5) AS `[지속감_매우_강함]` '
                                                   
                                                  'FROM perfumes AS p '
                                                  'INNER JOIN perfume_details AS pd '
                                                  'ON p.perfume_idx = pd.perfume_idx '
                                                  'INNER JOIN brands AS b '
                                                  'ON p.perfume_idx = pd.perfume_idx '
                                                  'LEFT JOIN reviews AS r '
                                                  'ON p.perfume_idx = r.perfume_idx '
                                                  'LEFT JOIN perfume_default_reviews AS pdr '
                                                  'ON p.perfume_idx = pdr.perfume_idx '
                                                  'GROUP BY p.perfume_idx')
    for perfume in perfume_list:
        perfume['부향률'] = abundance_rate_arr[perfume['부향률']]

    result = pd.DataFrame(perfume_list)
    print(result)

    file_nm = "{}_raw.xlsx".format(os.getenv('MYSQL_DB'))
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
