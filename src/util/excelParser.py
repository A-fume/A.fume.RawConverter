class ExcelColumn:
    COL_IDX = 'idx'
    COL_NAME = '이름'
    COL_ENGLISH_NAME = '영어_이름'
    COL_BRAND = '브랜드'
    COL_MAIN_IMAGE = '향수_대표_이미지'
    COL_STORY = '조향_스토리'
    COL_VOLUME_AND_PRICE = '용량_가격'
    COL_ABUNDANCE_RATE = '부향률'
    COL_TOP_NOTE = '탑노트'
    COL_MIDDLE_NOTE = '미들노트'
    COL_BASE_NOTE = '베이스노트'
    COL_SINGLE_NOTE = '싱글노트'
    COL_DEFAULT_KEYWORD = '키워드_default'
    COL_DEFAULT_SCORE = '별점_default'
    COL_DEFAULT_SEASONAL = '계절감_default_봄/여름/가을/겨울'
    COL_DEFAULT_SILLAGE = '잔향감_default_가벼움/중간/무거움'
    COL_DEFAULT_LONGEVITY = '지속감_default_매우약함/약함/보통/강함/매우강함'
    COL_DEFAULT_GENDER = '성별감_default_남성/중성/여성'

    COL_IMAGE_URL = '이미지'
    COL_DESCRIPTION = '설명'
    COL_FIRST_INITIAL = '시작 초성'


def get_idx(columns_list, column):
    _idx = columns_list.index(column)
    if _idx == -1:
        raise Exception("Error Exception")
    return _idx


def get_changed_cell_value(row, idx):
    cell = row[idx]
    if cell.fill.start_color.rgb == '00000000':
        return None
    if cell.fill.start_color.rgb == 'FFFFC000':
        return cell.value
    if cell.fill.start_color.rgb != 'FFFFFF00':
        print("Un Expected Color :" + str(cell.fill.start_color.rgb))

    return cell.value
