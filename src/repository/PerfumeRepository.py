from src.data.Perfume import Perfume
from src.data.PerfumeDefaultReview import PerfumeDefaultReview
from src.repository.SQLUtil import SQLUtil


def update_perfume(perfume):
    if not isinstance(perfume, Perfume):
        raise RuntimeError("update_perfume(): only allow Perfume class as parameter")

    perfume_idx = perfume.idx
    json = perfume.get_json()
    if json is None:
        return
    json.pop('idx')
    set_condition = ', '.join(['{} = %s'.format(it) for it in json.keys()])
    values = [json[it] for it in json.keys()]

    sql = 'UPDATE perfumes SET {} WHERE perfume_idx = {}'.format(set_condition, perfume_idx)
    SQLUtil.instance().execute(sql=sql, args=values)


def update_perfume_default_review(perfume_default_review):
    if not isinstance(perfume_default_review, PerfumeDefaultReview):
        raise RuntimeError("update_perfume(): only allow PerfumeDefaultReview class as parameter")

    perfume_idx = perfume_default_review.idx
    json = perfume_default_review.get_json()
    if json is None:
        return

    json.pop('idx')
    set_condition = ', '.join(['{} = "{}"'.format(it, json[it]) for it in json.keys()])

    sql = 'UPDATE perfume_default_reviews SET {} WHERE perfume_idx = {}'.format(set_condition, perfume_idx)
    SQLUtil.instance().execute(sql=sql)


def main():
    from dotenv import load_dotenv
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)

    SQLUtil.instance().logging = True

    testPerfume = Perfume(idx=1, name='154 코롱 조말론 런던',
                          english_name='154 Cologne Jo Malone London for women and men', image_url=None)
    update_perfume(testPerfume)

    testPerfumeDefaultReview = PerfumeDefaultReview(idx=1, rating=5.0, seasonal=None, sillage=None, longevity=None,
                                                    gender='2/2/2')
    update_perfume_default_review(testPerfumeDefaultReview)


if __name__ == '__main__':
    main()
    SQLUtil.instance().rollback()

