import re


class PerfumeDefaultReview:
    def __init__(self, idx, rating, seasonal, sillage, longevity, gender, keyword):
        self.idx = idx
        self.rating = rating
        self.keyword = keyword

        if seasonal is not None and re.match(r'^\d+/\d+/\d+/\d+$', seasonal) is None:
            raise RuntimeError("Invalid Seasonal format: " + seasonal)
        self.seasonal = seasonal
        if sillage is not None and re.match(r'^\d+/\d+/\d+$', sillage) is None:
            raise RuntimeError("Invalid Sillage format: " + sillage)
        self.sillage = sillage
        if longevity is not None and re.match(r'^\d+/\d+/\d+/\d+/\d+$', longevity) is None:
            raise RuntimeError("Invalid Longevity format: " + longevity)
        self.longevity = longevity
        if gender is not None and re.match(r'^\d+/\d+/\d+$', gender) is None:
            raise RuntimeError("Invalid Gender format: " + gender)
        self.gender = gender

    def get_json(self):
        json = {'idx': self.idx}
        if self.rating is not None:
            json['rating'] = self.rating
        if self.seasonal is not None:
            json['seasonal'] = self.seasonal
        if self.sillage is not None:
            json['sillage'] = self.sillage
        if self.longevity is not None:
            json['longevity'] = self.longevity
        if self.gender is not None:
            json['gender'] = self.gender
        if self.keyword is not None:
            json['keyword'] = self.keyword
        if len(json.keys()) == 1:
            return
        return json

    def __str__(self):
        return 'PerfumeDefaultReview({}, {}, {}, {}, {}, {}, {})'.format(self.idx, self.rating, self.seasonal,
                                                                         self.sillage,
                                                                         self.longevity, self.gender, self.keyword)
