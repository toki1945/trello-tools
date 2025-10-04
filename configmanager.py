import logging
import logging.config
from pathlib import Path

import yaml


WORK_DIR = Path.cwd()
LOG_DIR = WORK_DIR / "log"


LOG_CONFIG = "logger.yaml"
TRELLO_CONFIG = "settings.yaml"


class LoggerConfigManager:

    def __init__(self, name):
        self.name = name

    def setup_logger(self):
        LOG_DIR.mkdir(exist_ok=True)
        with open(LOG_CONFIG, "r", encoding="utf-8") as l:
            yml = yaml.safe_load(l)

        logging.config.dictConfig(yml)
        return logging.getLogger(self.name)


class TrelloConfigManager:
    def __init__(self):
        with open(TRELLO_CONFIG, mode="r", encoding="utf-8") as f:
            settings = yaml.safe_load(f)

        self.settings = settings
