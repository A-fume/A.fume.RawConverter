from src.common.data.Brand import Brand
from src.common.repository.SQLUtil import SQLUtil


def update_brand(brand):
    if not isinstance(brand, Brand):
        raise RuntimeError("update_brand(): only allow Brand class as parameter")

    json = brand.get_json()
    if json is None:
        return
    brand_idx = json.pop('brand_idx')
    set_condition = ', '.join(['{} = "{}"'.format(it, str(json[it]).replace('"', '""')) for it in json.keys()])

    sql = 'UPDATE brands SET {} WHERE brand_idx = {}'.format(set_condition, brand_idx)
    print(sql)
    SQLUtil.instance().execute(sql=sql)


def main():
    from dotenv import load_dotenv
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../../.env'), verbose=True)

    SQLUtil.instance().logging = True


if __name__ == '__main__':
    main()
    SQLUtil.instance().rollback()
