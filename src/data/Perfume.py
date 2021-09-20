from src.util.excelParser import ExcelColumn, get_idx, get_changed_cell_value


class Perfume:
    abundance_rate_list = ['', '코롱', '오 드 코롱', '코롱 인텐스', '오 드 퍼퓸', '오 드 뚜왈렛']

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

    @staticmethod
    def create(row, column_list):
        idx = row[get_idx(column_list, ExcelColumn.COL_IDX)].value
        name = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_NAME))
        english_name = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_ENGLISH_NAME))
        image_url = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_MAIN_IMAGE))
        story = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_STORY))
        volume_and_price = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_VOLUME_AND_PRICE))
        abundance_rate_str = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_ABUNDANCE_RATE))
        abundance_rate = Perfume.abundance_rate_list.index(
            abundance_rate_str) if abundance_rate_str is not None else None
        if abundance_rate == -1:
            raise RuntimeError("abundance_rate_str is not invalid: " + abundance_rate_str)
        return Perfume(idx=idx, name=name, english_name=english_name, image_url=image_url, story=story,
                       volume_and_price=volume_and_price, abundance_rate=abundance_rate)

    def __str__(self):
        return 'Perfume({}, {}, {}, {}, {}, {}, {})'.format(self.idx, self.name, self.english_name, self.image_url,
                                                            self.story, self.volume_and_price, self.abundance_rate)
