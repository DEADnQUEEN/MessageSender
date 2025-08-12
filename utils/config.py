import json
import os


TIMEDIFF = 0.1
TIMEOUT = 50 * (1 / TIMEDIFF)

LOGS = "log"
TEMPORARY = "tmp"
CONFIG_DIR = "configs"


def get_file_path(filename: str) -> str:
    """
    Note! Files need to be stored relative to the current working directory.
    :param filename: name of the file
    :return: full file path
    """

    return os.path.join(os.getcwd(), 'configs', filename)


with open(get_file_path('files.json'), 'r') as json_file:
    FILES = json.load(json_file)


with open(get_file_path('image_config.json'), 'r', encoding="utf-8") as file:
    CONFIG = json.load(file)


with open(get_file_path('replaces.json'), 'r', encoding="utf-8") as file:
    TEXT_REPLACES = json.load(file)


for directory in [LOGS, TEMPORARY]:
    if not os.path.exists(FILES[directory]):
        os.mkdir(FILES[directory])


LOG_PATH = os.path.join(os.getcwd(), LOGS)
TMP_PATH = os.path.join(os.getcwd(), TEMPORARY)
