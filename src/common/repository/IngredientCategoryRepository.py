from src.common.repository.SQLUtil import SQLUtil


def get_category_idx_by_name(name):
    sql = 'SELECT idx FROM ingredient_categories WHERE name="{}"'.format(name)
    SQLUtil.instance().execute(sql=sql)
    result = SQLUtil.instance().fetchall()
    if len(result) == 0:
        raise RuntimeError("Wrong IngredientCategory name:[{}]".format(name))
    return result[0]['idx']


def carate_ingredient_category(name):
    sql = 'INSERT ingredient_categories(name) VALUES({})'.format(name)
    print(sql)
    SQLUtil.instance().execute(sql=sql)
