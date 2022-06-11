from typing import Dict

from Config import Config
from src.common.Strings import CommandInfo
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


def execute(name, command_str):
    converter = converter_map[name]
    converter.do_command(command_str)


def run():
    command = Config.instance().COMMAND
    target_list = Config.instance().get_target_list()
    for target in target_list:
        execute(target, command)
