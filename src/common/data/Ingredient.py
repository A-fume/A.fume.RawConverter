class Ingredient:

    def __init__(self, ingredient_idx, name, english_name, description, image_url, series_idx):
        self.ingredient_idx = ingredient_idx
        self.name = name
        self.english_name = english_name
        self.description = description
        self.image_url = image_url
        self.series_idx = series_idx

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
        if self.series_idx is not None:
            json['series_idx'] = self.series_idx
        if len(json.keys()) == 1:
            return
        return json

    def __eq__(self, other):
        return self.ingredient_idx == other.ingredient_idx \
               and self.name == other.name \
               and self.english_name == other.english_name \
               and self.description == other.description \
               and self.image_url == other.image_url \
               and self.series_idx == other.series_idx

    def __hash__(self):
        return hash(
            (self.ingredient_idx, self.name, self.english_name, self.description, self.image_url, self.series_idx))

    def __str__(self):
        return 'Ingredient({}, {}, {}, {}, {}, {})'.format(self.ingredient_idx, self.name, self.english_name,
                                                           self.description, self.image_url, self.series_idx)
