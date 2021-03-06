from src.common.repository.SQLUtil import SQLUtil


def get_keyword_idx_by_name(name):
    sql = 'SELECT id FROM keywords WHERE name="{}"'.format(name)
    SQLUtil.instance().execute(sql=sql)
    result = SQLUtil.instance().fetchall()
    if len(result) == 0:
        raise RuntimeError("Wrong keyword name:[{}]".format(name))
    return result[0]['id']


def get_keyword_by_idx(keyword_idx):
    sql = 'SELECT * FROM keywords WHERE id={}'.format(keyword_idx)
    SQLUtil.instance().execute(sql=sql)
    result = SQLUtil.instance().fetchall()
    if len(result) == 0:
        raise RuntimeError("Wrong keyword idx:[{}]".format(keyword_idx))
    return result[0]


def get_keywords_by_idx_list(keyword_idx_list) -> str:
    sql = "SELECT name FROM keywords WHERE id IN ({})".format(','.join(map(str, keyword_idx_list)))
    SQLUtil.instance().execute(sql=sql)
    result = SQLUtil.instance().fetchall()
    return ','.join(map(lambda x: x['name'], result))


def main():
    SQLUtil.instance().logging = True
    idx = get_keyword_idx_by_name('톡 쏘는')
    if idx > 0:
        print('success getKeywordIdx() : {}'.format(idx))
    else:
        print('failed getKeywordIdx()')

    name = get_keyword_by_idx(idx)
    print(name)


if __name__ == '__main__':
    main()
    SQLUtil.instance().rollback()
