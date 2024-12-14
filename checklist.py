#!/usr/bin/env python3
import logging
import logging.config

import yaml

LOG_CONFIG = "logger.yaml"
LOGGER_NAME = "checkList"


class CheckList:

    def __init__(self, name, items):
        self.name = name
        self.items = items

        with open(LOG_CONFIG, "r", encoding="utf-8") as l:
            yml = yaml.safe_load(l)

        logging.config.dictConfig(yml)
        self.logger = logging.getLogger(LOGGER_NAME)

    def print_check_list(self):
        self.logger.info(f"#### check list name: {self.name}")
        check_items = [item for item in self.items]
        check_items.sort(key=lambda k: k["pos"])

        for check_item in check_items:
            self.logger.info(f'items: {check_item["name"]}, status: {check_item["state"]}')