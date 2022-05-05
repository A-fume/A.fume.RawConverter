class Note:
    TYPE_TOP = 1
    TYPE_MIDDLE = 2
    TYPE_BASE = 3
    TYPE_SINGLE = 4

    def __init__(self, perfume_idx, ingredient_idx, type):
        self.perfume_idx = perfume_idx
        self.ingredient_idx = ingredient_idx
        self.type = type

    def update(self):
        json = {'perfume_idx': self.perfume_idx}
        if self.ingredient_idx is not None:
            json['ingredient_idx'] = self.ingredient_idx
        if self.type is not None:
            json['type'] = self.type
        if len(json.keys()) == 1:
            return
        print(json)

    def __eq__(self, other):
        return self.perfume_idx == other.perfume_idx and self.ingredient_idx == other.ingredient_idx and self.type == other.type

    def __hash__(self):
        return hash((self.perfume_idx, self.ingredient_idx, self.type))

    def __str__(self):
        return 'Note({}, {}, {})'.format(self.perfume_idx, self.ingredient_idx, self.type)
