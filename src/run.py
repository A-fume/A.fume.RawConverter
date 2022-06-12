import os
from datetime import datetime
from typing import Dict

from Config import Config
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


def execute(name, command_str, out_folder_path):
    converter = converter_map[name]
    converter.do_command(command_str, out_folder_path)


def run():
    command = Config.instance().COMMAND
    target_list = Config.instance().get_target_list()
    out_folder_path = None
    if command == CommandStr.db2excel:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        out_folder_path = os.path.join(Config.instance().OUTPUT_DIR_PATH, timestamp)
        os.mkdir(out_folder_path)

    for target in target_list:
        execute(target, command, out_folder_path)
