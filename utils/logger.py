import datetime
import os.path
from utils import config
from typing import Optional


def collect_log(text, filename: Optional[str] = None):
    log_name = datetime.datetime.now().strftime("%d-%m-%YT%H-%M") + ".txt"
    if filename:
        log_name = filename + "__" + log_name
    with open(
        os.path.join(
            config.LOG_PATH,
            log_name
        ), "w"
    ) as logfile:
        logfile.write(text)
