import datetime
import os.path
from utils import config


def collect_log(text):
    with open(os.path.join(config.LOG_PATH, datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + ".txt"), "w") as logfile:
        logfile.write(text)
