from typing import Dict

from src.common.Strings import CommandInfo, CommandStr
from src.converter.BrandConverter import BrandConverter
from src.converter.Converter import Converter
from src.converter.IngredientConverter import IngredientConverter
from src.converter.PerfumeConverter import PerfumeConverter
from src.converter.SeriesConverter import SeriesConverter

converter_map: Dict[str, Converter] = {
    CommandInfo.ingredient: IngredientConverter(),
    CommandInfo.perfume: PerfumeConverter(),
    CommandInfo.brand: BrandConverter(),
    CommandInfo.series: SeriesConverter()
}


def main(name, command_str):
    if '*' == name:
        for key in converter_map.keys():
            converter_map[key].do_command(command_str)
        return

    converter = converter_map[name]
    converter.do_command(command_str)


if __name__ == '__main__':
    main(CommandInfo.ingredient, CommandStr.db2excel)
