from src.common.data.Ingredient import Ingredient
from src.common.repository.SQLUtil import SQLUtil


def get_ingredient_idx_by_name(name):
    sql = 'SELECT ingredient_idx FROM ingredients WHERE name="{}"'.format(name)
    SQLUtil.instance().execute(sql=sql)
    result = SQLUtil.instance().fetchall()
    if len(result) == 0:
        raise RuntimeError("Wrong Ingredient name:[{}]".format(name))
    return result[0]['ingredient_idx']


def update_ingredient(ingredient):
    if not isinstance(ingredient, Ingredient):
        raise RuntimeError("update_ingredient(): only allow Ingredient class as parameter")

    json = ingredient.get_json()
    if json is None:
        return
    ingredient_idx = json.pop('ingredient_idx')
    set_condition = ', '.join(['{} = "{}"'.format(it, str(json[it]).replace('"', '""')) for it in json.keys()])

    sql = 'UPDATE ingredients SET {} WHERE ingredient_idx = {}'.format(set_condition, ingredient_idx)
    print(sql)
    SQLUtil.instance().execute(sql=sql)


def main():
    SQLUtil.instance().logging = True
    idx = get_ingredient_idx_by_name('그레이프프루트')
    if idx > 0:
        print('success getIngredientIdx() : {}'.format(idx))
    else:
        print('failed getIngredientIdx()')


if __name__ == '__main__':
    main()
    SQLUtil.instance().rollback()
