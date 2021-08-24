from src.repository.SQLUtil import SQLUtil


def get_keyword_idx_by_name(name):
    sql = 'SELECT id FROM keywords WHERE name="{}"'.format(name)
    SQLUtil.instance().execute(sql=sql)
    result = SQLUtil.instance().fetchall()
    if len(result) == 0:
        raise "Wrong keyword name:[{}]".format(name)
    return result[0]['id']


def main():
    from dotenv import load_dotenv
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)

    SQLUtil.instance().logging = True
    idx = get_keyword_idx_by_name('톡 쏘는')
    if idx > 0:
        print('success getKeywordIdx() : {}'.format(idx))
    else:
        print('failed getKeywordIdx()')


if __name__ == '__main__':
    main()
    SQLUtil.instance().rollback()
