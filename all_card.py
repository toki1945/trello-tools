#!/usr/bin/env python3
import logging
import logging.config
from pathlib import Path

import yaml

from trelloclient import TrelloClient


WORK_DIR = Path.cwd()
LOG_DIR = WORK_DIR / "log"


SETTINGS_FILE = "settings.yaml"
LOG_CONFIG = "logger.yaml"
LOGGER_NAME = "my_module"


def main():
    with open(LOG_CONFIG, "r", encoding="utf-8") as l:
        yml = yaml.safe_load(l)

    logging.config.dictConfig(yml)
    logger = logging.getLogger(LOGGER_NAME)

    with open(SETTINGS_FILE, mode="r", encoding="utf-8") as f:
        settings = yaml.safe_load(f)

    # create log dir
    if not LOG_DIR.exists():
        LOG_DIR.mkdir()
        logger.info("#### create log dir")

    trello_client = TrelloClient(settings["api"]["key"], settings["api"]["token"])

    user_information = trello_client.get_user_information(settings["user"])

    board_information: dict = trello_client.get_board_information(user_information["idBoards"])

    target_board = board_information[settings["board"]["myBoard"]["name"]]

    lists_on_board: dict = trello_client.get_lists_on_board(target_board["id"])

    cards_on_list = trello_client.get_all_cards(lists_on_board)
    for card in cards_on_list:
        logger.info(f"card name: {card['name']}")

# main
if __name__ == "__main__":
    main()