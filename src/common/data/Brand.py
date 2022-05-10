class Brand:

    def __init__(self, brand_idx, name, english_name, first_initial, description, image_url):
        self.brand_idx = brand_idx
        self.name = name
        self.english_name = english_name
        self.first_initial = first_initial
        self.description = description
        self.image_url = image_url

    def get_json(self):
        json = {'brand_idx': self.brand_idx}
        if self.name is not None:
            json['name'] = self.name
        if self.english_name is not None:
            json['english_name'] = self.english_name
        if self.first_initial is not None:
            json['first_initial'] = self.first_initial
        if self.description is not None:
            json['description'] = self.description
        if self.image_url is not None:
            json['image_url'] = self.image_url
        if len(json.keys()) == 1:
            return
        return json

    def __eq__(self, other):
        return self.brand_idx == other.brand_idx \
               and self.name == other.name \
               and self.english_name == other.english_name \
               and self.first_initial == other.first_initial \
               and self.description == other.description \
               and self.image_url == other.image_url

    def __hash__(self):
        return hash(
            (self.brand_idx, self.name, self.english_name, self.first_initial, self.description, self.image_url))

    def __str__(self):
        return 'Brand({}, {}, {}, {}, {}, {})'.format(self.brand_idx, self.name, self.english_name,
                                                      self.first_initial, self.description, self.image_url)
