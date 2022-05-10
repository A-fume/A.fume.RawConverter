from typing import Dict

from src.converter.BrandConverter import BrandConverter
from src.converter.Converter import Converter
from src.converter.IngredientConverter import IngredientConverter
from src.converter.PerfumeConverter import PerfumeConverter
from src.converter.SeriesConverter import SeriesConverter

converter_map: Dict[str, Converter] = {
    'ingredient_info': IngredientConverter(),
    'perfume_info': PerfumeConverter(),
    'brand_info': BrandConverter(),
    'series_info': SeriesConverter()
}


def main(name, command_str):
    if '*' == name:
        for key in converter_map.keys():
            converter_map[key].do_command(command_str)
        return

    converter = converter_map[name]
    converter.do_command(command_str)


if __name__ == '__main__':
    main('series_info', 'db2excel')
