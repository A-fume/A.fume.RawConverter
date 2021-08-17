from src.repository.SQLUtil import SQLUtil


def get_ingredient_idx_by_name(name):
    result = SQLUtil.instance().execute(sql='SELECT ingredient_idx FROM ingredients WHERE name="{}"'.format(name))
    if len(result) == 0:
        raise "Wrong Ingredient name:[{}]".format(name)
    return result[0]['ingredient_idx']


if __name__ == '__main__':
    from dotenv import load_dotenv
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)

    if get_ingredient_idx_by_name('Grapefruit') > 0:
        print('success getIngredientIdx()')
    else:
        print('failed getIngredientIdx()')
