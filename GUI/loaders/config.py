import json
import utils.config


with open(utils.config.get_file_path('previewer.json'), 'r', encoding='utf-8') as json_config:
    UI_CONF = json.load(json_config)
