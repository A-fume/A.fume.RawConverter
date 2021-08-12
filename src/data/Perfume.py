from src.util.excelParser import ExcelColumn, get_idx, get_changed_cell_value


class Perfume:
    def __init__(self, idx, name, english_name, image_url):
        self.idx = idx
        self.name = name
        self.english_name = english_name
        self.image_url = image_url

    def update(self):
        json = {'idx': self.idx}
        if self.name is not None:
            json['name'] = self.name
        if self.english_name is not None:
            json['englishName'] = self.english_name
        if self.image_url is not None:
            json['image_url'] = self.image_url
        if len(json.keys()) == 1:
            return
        print(json)

    @staticmethod
    def create(row, column_list):
        idx = row[get_idx(column_list, ExcelColumn.COL_IDX)].value
        name = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_NAME))
        english_name = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_ENGLISH_NAME))
        image_url = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_MAIN_IMAGE))
        return Perfume(idx=idx, name=name, english_name=english_name, image_url=image_url)

    def __str__(self):
        return 'Perfume({}, {}, {}, {})'.format(self.idx, self.name, self.english_name, self.image_url)
