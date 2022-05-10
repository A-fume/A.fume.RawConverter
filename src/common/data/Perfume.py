class Perfume:
    abundance_rate_list = ['', '코롱', '오 드 코롱', '오 드 뚜왈렛', '오 드 퍼퓸', '퍼퓸', '기타']

    def __init__(self, idx, name, english_name, image_url, story, volume_and_price, abundance_rate):
        self.idx = idx
        self.name = name
        self.english_name = english_name
        self.image_url = image_url
        self.story = story
        self.volume_and_price = volume_and_price
        self.abundance_rate = abundance_rate

    def get_json(self):
        json = {'idx': self.idx}
        if self.name is not None:
            json['name'] = self.name
        if self.english_name is not None:
            json['english_name'] = self.english_name
        if self.image_url is not None:
            json['image_url'] = self.image_url
        if self.story is not None:
            json['story'] = self.story
        if self.volume_and_price is not None:
            json['volume_and_price'] = self.volume_and_price
        if self.abundance_rate is not None:
            json['abundance_rate'] = self.abundance_rate
        if len(json.keys()) == 1:
            return
        return json

    def __str__(self):
        return 'Perfume({}, {}, {}, {}, {}, {}, {})'.format(self.idx, self.name, self.english_name, self.image_url,
                                                            self.story, self.volume_and_price, self.abundance_rate)
