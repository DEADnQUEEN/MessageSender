import json
import utils.config

with open(utils.config.get_file_path("translates.json"), 'r', encoding='utf-8') as json_translations:
    TRANSLATES = json.load(json_translations)
