from src.repository.SQLUtil import SQLUtil


def get_ingredient_idx_by_name(name):
    sql = 'SELECT ingredient_idx FROM ingredients WHERE name="{}"'.format(name)
    SQLUtil.instance().execute(sql=sql)
    result = SQLUtil.instance().fetchall()
    if len(result) == 0:
        raise "Wrong Ingredient name:[{}]".format(name)
    return result[0]['ingredient_idx']


def main():
    from dotenv import load_dotenv
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)

    SQLUtil.instance().logging = True
    idx = get_ingredient_idx_by_name('그레이프프루트')
    if idx > 0:
        print('success getIngredientIdx() : {}'.format(idx))
    else:
        print('failed getIngredientIdx()')


if __name__ == '__main__':
    main()
    SQLUtil.instance().rollback()
