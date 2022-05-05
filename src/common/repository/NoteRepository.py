from src.common.data.Note import Note
from src.common.repository.SQLUtil import SQLUtil


def get_note_list_by_perfume_idx(perfume_idx, note_type):
    sql = 'SELECT perfume_idx, ingredient_idx, type FROM notes WHERE perfume_idx={} AND type={}' \
        .format(perfume_idx, note_type)
    SQLUtil.instance().execute(sql=sql)
    return [Note(perfume_idx=it['perfume_idx'], ingredient_idx=it['ingredient_idx'], type=it['type']) for it in
            SQLUtil.instance().fetchall()]


def update_note(note):
    sql = 'UPDATE notes SET type = {} WHERE perfume_idx = {} AND ingredient_idx = {}' \
        .format(note.type,
                note.perfume_idx,
                note.ingredient_idx)
    result = SQLUtil.instance().execute(sql=sql)
    return result


def create_note(note):
    sql = 'INSERT notes(perfume_idx, ingredient_idx, type) VALUES({}, {}, {}) ON DUPLICATE KEY UPDATE type = {}' \
        .format(note.perfume_idx,
                note.ingredient_idx, note.type, note.type)
    result = SQLUtil.instance().execute(sql=sql)
    return result


def delete_note(note):
    sql = 'DELETE FROM notes WHERE perfume_idx = {} AND ingredient_idx = {}' \
        .format(note.perfume_idx,
                note.ingredient_idx)
    result = SQLUtil.instance().execute(sql=sql)
    return result


def update_note_list(perfume_idx, note_type, update_list):
    for note in update_list:
        if note.perfume_idx != perfume_idx or note.type != note_type:
            raise RuntimeError("Logic Error")

    db_list = get_note_list_by_perfume_idx(perfume_idx=perfume_idx, note_type=note_type)
    note_set = set(update_list)
    db_set = set(db_list)

    intersection_set = note_set.intersection(db_set)
    note_set = note_set - intersection_set
    db_set = db_set - intersection_set

    added_set = note_set.difference(db_set)
    removed_set = db_set.difference(note_set)

    [create_note(note) for note in added_set]
    [delete_note(note) for note in removed_set]


def main():
    from dotenv import load_dotenv
    import os

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../../.env'), verbose=True)

    SQLUtil.instance().logging = True

    result = get_note_list_by_perfume_idx(1, 1)

    for x in result:
        print(x)

    create_note(Note(100, 100, 100))
    update_note(Note(1, 2, 1))

    update_note_list(1, 1,
                     [])

    update_note_list(1, 1,
                     [Note(1, 2, 1), Note(1, 8, 1), Note(1, 12, 1), Note(1, 11, 1), Note(1, 241, 1), Note(1, 3, 1),
                      Note(1, 13, 1), Note(1, 151, 1), Note(1, 14, 1), Note(1, 9, 1)])


if __name__ == '__main__':
    main()
    SQLUtil.instance().rollback()
