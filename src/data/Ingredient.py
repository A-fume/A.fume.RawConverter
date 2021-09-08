from src.util.excelParser import get_idx, get_changed_cell_value, ExcelColumn


class Ingredient:

    def __init__(self, ingredient_idx, name, english_name, description, image_url):
        self.ingredient_idx = ingredient_idx
        self.name = name
        self.english_name = english_name
        self.description = description
        self.image_url = image_url

    def get_json(self):
        json = {'ingredient_idx': self.ingredient_idx}
        if self.name is not None:
            json['name'] = self.name
        if self.english_name is not None:
            json['english_name'] = self.english_name
        if self.description is not None:
            json['description'] = self.description
        if self.image_url is not None:
            json['image_url'] = self.image_url
        if len(json.keys()) == 1:
            return
        return json

    def __eq__(self, other):
        return self.ingredient_idx == other.ingredient_idx \
               and self.name == other.name \
               and self.english_name == other.english_name \
               and self.description == other.description \
               and self.image_url == other.image_url

    @staticmethod
    def create(row, column_list):
        idx = row[get_idx(column_list, ExcelColumn.COL_IDX)].value
        name = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_NAME))
        english_name = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_ENGLISH_NAME))
        description = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_DESCRIPTION))
        image_url = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_IMAGE_URL))
        return Ingredient(ingredient_idx=idx, name=name, english_name=english_name, description=description,
                          image_url=image_url)

    def __hash__(self):
        return hash((self.ingredient_idx, self.name, self.english_name, self.description, self.image_url))

    def __str__(self):
        return 'Ingredient({}, {}, {}, {}, {})'.format(self.ingredient_idx, self.name, self.english_name,
                                                       self.description, self.image_url)
