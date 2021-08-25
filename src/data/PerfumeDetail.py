from src.util.excelParser import ExcelColumn, get_idx, get_changed_cell_value


class PerfumeDetail:
    abundance_rate_list = ['', '코롱', '오 드 코롱', '코롱 인텐스', '오 드 퍼퓸', '오 드 뚜왈렛']

    def __init__(self, idx, story, volume_and_price, abundance_rate):
        self.idx = idx
        self.story = story
        self.volume_and_price = volume_and_price
        self.abundance_rate = abundance_rate

    def get_json(self):
        json = {'idx': self.idx}
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
        story = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_STORY))
        volume_and_price = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_VOLUME_AND_PRICE))
        abundance_rate_str = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_ABUNDANCE_RATE))
        abundance_rate = PerfumeDetail.abundance_rate_list.index(abundance_rate_str) if abundance_rate_str is not None else None
        if abundance_rate == -1:
            raise RuntimeError("abundance_rate_str is not invalid: " + abundance_rate_str)
        return PerfumeDetail(idx=idx, story=story, volume_and_price=volume_and_price, abundance_rate=abundance_rate)

    def __str__(self):
        return 'PerfumeDetail({}, {}, {}, {})'.format(self.idx, self.story, self.volume_and_price, self.abundance_rate)
