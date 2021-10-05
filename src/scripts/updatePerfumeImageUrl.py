import os

from dotenv import load_dotenv

from src.data.Perfume import Perfume
from src.repository.PerfumeRepository import update_perfume
from src.repository.SQLUtil import SQLUtil

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, '../../.env'), verbose=True)


def main(perfume_idx_list):
    for perfume_idx in perfume_idx_list:
        image_url = "https://afume-release.s3.ap-northeast-2.amazonaws.com/perfumes/{}_1.png".format(perfume_idx)
        perfume = Perfume(idx=perfume_idx, name=None, english_name=None, story=None, volume_and_price=None,
                          abundance_rate=None, image_url=image_url)
        update_perfume(perfume)


if __name__ == '__main__':
    perfume_idx_list = []
    SQLUtil.instance().logging = True
    main(perfume_idx_list)
    SQLUtil.instance().commit()
