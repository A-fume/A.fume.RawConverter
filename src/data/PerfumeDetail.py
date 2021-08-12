from src.util.excelParser import ExcelColumn, get_idx, get_changed_cell_value


class PerfumeDetail:
    def __init__(self, idx, story, volume_and_price, abundance_rate):
        self.idx = idx
        self.story = story
        self.volume_and_price = volume_and_price
        self.abundance_rate = abundance_rate

    def update(self):
        json = {'idx': self.idx}
        if self.story is not None:
            json['story'] = self.story
        if self.volume_and_price is not None:
            json['volumeAndPrice'] = self.volume_and_price
        if self.abundance_rate is not None:
            json['abundanceRate'] = self.abundance_rate
        if len(json.keys()) == 1:
            return
        print(json)

    @staticmethod
    def create(row, column_list):
        idx = row[get_idx(column_list, ExcelColumn.COL_IDX)].value
        story = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_STORY))
        volume_and_price = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_VOLUME_AND_PRICE))
        abundance_rate = get_changed_cell_value(row, get_idx(column_list, ExcelColumn.COL_ABUNDANCE_RATE))
        return PerfumeDetail(idx=idx, story=story, volume_and_price=volume_and_price, abundance_rate=abundance_rate)

    def __str__(self):
        return 'PerfumeDetail({}, {}, {}, {})'.format(self.idx, self.story, self.volume_and_price, self.abundance_rate)
