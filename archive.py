#!/usr/bin/env python3
from datetime import datetime, timedelta
import logging
import logging.config
from pathlib import Path
import re

import yaml

from cardInformation import CardInformation
from trelloclient import TrelloClient


WORK_DIR = Path.cwd()
LOG_DIR = WORK_DIR / "log"

TARGET_LIST = "completed"

SETTINGS_FILE = "settings.yaml"
LOG_CONFIG = "logger.yaml"
LOGGER_NAME = "my_module"


TODAY = datetime.now()
DATE_FORMAT = re.compile(r"^[0-9]+-[0-9]+-[0-9]+")


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

    target_list_information = lists_on_board[TARGET_LIST]
    cards_on_list = trello_client.get_cards(target_list_information["id"])

    archieve_cards(cards_on_list, trello_client, logger)


def archieve_cards(cards_list, client: TrelloClient, logger: logging):
    for card in cards_list:
        card_information = CardInformation(name=card["name"], information=card)
        logger.info(f"=============== card name = {card_information.name} ===============")

        _last_activity = DATE_FORMAT.match(card_information.information["dateLastActivity"])
        last_activity = datetime.strptime(_last_activity.group(), "%Y-%m-%d")

        if last_activity + timedelta(days=60) < TODAY:
            client.update_card(card_information.information["id"], closed=True)
            logger.info(f"{card_information.name} was archived")

# main
if __name__ == "__main__":
    main()