class Series:

    def __init__(self, series_idx, name, english_name, description, image_url):
        self.series_idx = series_idx
        self.name = name
        self.english_name = english_name
        self.description = description
        self.image_url = image_url

    def get_json(self):
        json = {'series_idx': self.series_idx}
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
        return self.series_idx == other.series_idx \
               and self.name == other.name \
               and self.english_name == other.english_name \
               and self.description == other.description \
               and self.image_url == other.image_url

    def __hash__(self):
        return hash((self.series_idx, self.name, self.english_name, self.description, self.image_url))

    def __str__(self):
        return 'Series({}, {}, {}, {}, {})'.format(self.series_idx, self.name, self.english_name,
                                                   self.description, self.image_url)

    def get_set_query(self):
        json = self.get_json()
        json.pop('series_idx')
        return ', '.join(['{} = "{}"'.format(it, str(json[it]).replace('"', '""')) for it in json.keys()])
