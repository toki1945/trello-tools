#!/usr/bin/env python3
import logging
import logging.config
from pathlib import Path

import yaml

from cardInformation import CardInformation
from trello_operations import get_user_information, get_board_information, get_lists_on_board, get_cards_on_board
from trelloclient import TrelloClient


WORK_DIR = Path.cwd()
LOG_DIR = WORK_DIR / "log"


SETTINGS_FILE = "settings.yaml"
LOG_CONFIG = "logger.yaml"
LOGGER_NAME = "my_module"

# 処理開始
if __name__ == "__main__":
    if not LOG_DIR.exists():
        LOG_DIR.mkdir()
        print("#### create log dir")

    with open(LOG_CONFIG, "r", encoding="utf-8") as l:
        yml = yaml.safe_load(l)

    logging.config.dictConfig(yml)
    logger = logging.getLogger(LOGGER_NAME)

    with open(SETTINGS_FILE, mode="r", encoding="utf-8") as f:
        settings = yaml.safe_load(f)

    trello_client = TrelloClient(settings["api"]["key"], settings["api"]["token"])

    user_information = get_user_information(trello_client, settings["user"])

    board_information: dict = get_board_information(trello_client, user_information["idBoards"])

    target_board = board_information[settings["board"]["myBoard"]["name"]]

    lists_on_board: dict = get_lists_on_board(trello_client, target_board["id"])

    all_card = []
    for list_on_board in lists_on_board.values():
        cards_on_list = get_cards_on_board(trello_client, list_on_board["id"])
        all_card.extend(cards_on_list)

    for card_on_list in all_card:
        card = CardInformation(name=card_on_list["name"], information=card_on_list)
        check_list = trello_client.get_check_list(card.information["idChecklists"])
        print(check_list)