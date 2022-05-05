from typing import Dict

from src.converter.BrandConverter import BrandConverter
from src.converter.Converter import Converter
from src.converter.IngredientConverter import IngredientConverter
from src.converter.PerfumeConverter import PerfumeConverter

converter_map: Dict[str, Converter] = {
    'ingredient_info': IngredientConverter(),
    'perfume_info': PerfumeConverter(),
    'brand_info': BrandConverter()
}


def main(name, command_str):
    converter = converter_map[name]
    converter.do_command(command_str)


if __name__ == '__main__':
    main('perfume_info', 'db2excel')
