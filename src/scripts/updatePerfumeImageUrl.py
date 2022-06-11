from src.common.data.Perfume import Perfume
from src.common.repository.PerfumeRepository import update_perfume
from src.common.repository.SQLUtil import SQLUtil


def main(perfume_idx_list):
    for perfume_idx in perfume_idx_list:
        image_url = "https://afume-release.s3.ap-northeast-2.amazonaws.com/perfumes/{}_1.png".format(perfume_idx)
        perfume = Perfume(idx=perfume_idx, name=None, english_name=None, story=None, volume_and_price=None,
                          abundance_rate=None, image_url=image_url)
        update_perfume(perfume)


if __name__ == '__main__':
    SQLUtil.instance().logging = True
    main([])
    SQLUtil.instance().commit()
