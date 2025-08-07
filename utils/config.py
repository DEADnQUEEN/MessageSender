import json
import os


TIMEDIFF = 0.1
TIMEOUT = 50 * (1 / TIMEDIFF)

CSV_DATA_FILE = os.path.join(os.getcwd(), 'config', 'table.csv')


with open(os.path.join(os.getcwd(), 'config', 'image_config.json'), 'r', encoding="utf-8") as file:
    CONFIG = json.load(file)

with open(os.path.join(os.getcwd(), 'config', 'text.txt'), 'r', encoding='utf-8') as f:
    BASE_TEXT = ""
    for line in f.readlines():
        BASE_TEXT += line

with open(os.path.join(os.getcwd(), 'config', 'replaces.json'), 'r', encoding="utf-8") as file:
    TEXT_REPLACES = json.load(file)


LOG_PATH = os.path.join(os.getcwd(), 'log')
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)


TMP_PATH = os.path.join(os.getcwd(), CONFIG['tmp_folder'])
if not os.path.exists(TMP_PATH):
    os.mkdir(TMP_PATH)

COLUMN_PATH = os.path.join(os.getcwd(), "config", "csv_load.json")
with open(COLUMN_PATH, encoding="utf-8", newline='') as json_file:
    CSV_CONFIG = json.load(json_file)
    COLUMN_DATA = CSV_CONFIG['columns']
    CSV_HAS_TITLE = CSV_CONFIG['title']

