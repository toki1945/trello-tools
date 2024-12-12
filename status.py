#!/usr/bin/env python3
import json
import logging
import logging.config
from pathlib import Path

import yaml

from cardInformation import CardInformation
from checklist import CheckList
from trelloclient import TrelloClient


WORK_DIR = Path.cwd()
LOG_DIR = WORK_DIR / "log"


SETTINGS_FILE = "settings.json"


LOG_CONFIG = "logger.yaml"
LOGGER_NAME = "my_module"


if __name__ == "__main__":
    if not LOG_DIR.exists():
        LOG_DIR.mkdir()
        print("#### create log dir")

    with open(LOG_CONFIG, "r", encoding="utf-8") as l:
        yml = yaml.safe_load(l)

    logging.config.dictConfig(yml)
    logger = logging.getLogger(LOGGER_NAME)

    with open(SETTINGS_FILE, mode="r", encoding="utf-8") as f:
        settings = json.load(f)

    trello_user_name = settings["trelloId"]["name"]
    target_board_name = settings["board"]["myBoard"]["name"]
    target_list_name = settings["board"]["myBoard"]["list"][1]["name"]

    trello_client = TrelloClient(settings["api"]["key"], settings["api"]["token"])

    trello_id = trello_client.get_user_id(trello_user_name)

    for board_id in trello_client.get_board_id(trello_user_name):
        if target_board_name == trello_client.get_board_name(board_id):
            logger.debug(f"target board: {target_board_name}")
            lists_on_board = trello_client.get_lists_on_board(board_id)
            break

    check_lists = []
    for board_list in lists_on_board:
        for target in [card for card in trello_client.get_cards(board_list["id"]) if trello_id in card['idMembers']]:
            card_information = CardInformation(target["id"], target["name"])
            check_lists.extend(card_information.get_check_list(trello_client, target["idChecklists"]))

    check_list: CheckList
    for check_list in check_lists:
        check_list.print_check_list()