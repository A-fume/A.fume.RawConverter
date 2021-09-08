import os

from dotenv import load_dotenv

from src.repository.SQLUtil import SQLUtil

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)


def substitute(ingredient_idx, substitute_ingredient_idx):
    note_query = "SELECT *, type, count(perfume_idx) AS count FROM notes " \
                 "WHERE ingredient_idx = {} OR ingredient_idx = {} " \
                 "GROUP BY perfume_idx " \
        .format(ingredient_idx, substitute_ingredient_idx)
    SQLUtil.instance().execute(note_query)
    note_list = SQLUtil.instance().fetchall()
    for note in note_list:
        if note['count'] == 1:
            if note['ingredient_idx'] != substitute_ingredient_idx:
                query = "UPDATE notes SET ingredient_idx = {} " \
                        "WHERE ingredient_idx = {} AND perfume_idx = {} AND type = {}" \
                    .format(substitute_ingredient_idx, note['ingredient_idx'], note['perfume_idx'], note['type'])
                SQLUtil.instance().execute(query)
        elif note['count'] == 2:
            query = "DELETE FROM notes WHERE ingredient_idx = {} AND perfume_idx = {} AND type = {}".format(
                note['ingredient_idx'], note['perfume_idx'], note['type'])
            SQLUtil.instance().execute(query)
        else:
            raise Exception("???")

    remove_ingredient_query = "DELETE FROM ingredients WHERE ingredient_idx = {}".format(ingredient_idx)
    SQLUtil.instance().execute(remove_ingredient_query)


def main():
    query = "SELECT english_name FROM ingredients GROUP BY english_name HAVING COUNT(english_name) > 1"
    SQLUtil.instance().execute(query)
    duplicated_english_name_list = SQLUtil.instance().fetchall()
    for item in duplicated_english_name_list:
        english_name = item['english_name']
        if len(english_name) == 0:
            continue
        query = "SELECT ingredient_idx, name, english_name FROM ingredients WHERE english_name = '{}'".format(
            english_name)
        SQLUtil.instance().execute(query)
        ingredient_list = SQLUtil.instance().fetchall()
        idx_list = [item['ingredient_idx'] for item in ingredient_list]
        idx_list.sort()
        correct_idx = idx_list.pop(0)
        for duplicated_idx in idx_list:
            print("{} -> {}".format(duplicated_idx, correct_idx))
            substitute(duplicated_idx, correct_idx)


if __name__ == '__main__':
    main()
    SQLUtil.instance().commit()
