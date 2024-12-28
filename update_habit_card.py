#!/usr/bin/env python3
import logging
import logging.config
from pathlib import Path

import yaml

from cardInformation import CardInformation
from trelloclient import TrelloClient


WORK_DIR = Path.cwd()
LOG_DIR = WORK_DIR / "log"

TARGET_LIST = "habit"

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

    target_list_information = lists_on_board[TARGET_LIST]
    cards_on_list = trello_client.get_cards(target_list_information["id"])

    print_card_information(cards_on_list, logger, trello_client)


def print_card_information(card_list, logger: logging, client: TrelloClient):
    for card_on_list in card_list:
        card_information = CardInformation(name=card_on_list["name"], information=card_on_list)
        logger.info(f"card name = {card_information.name}")
        update_due_date(card_information, logger, client)


def update_due_date(card: CardInformation, logger: logging, client: TrelloClient):
    new_due_date = card.update_due_date_for_habit_card()
    if new_due_date:
        client.update_card(card.information["id"], due=new_due_date)
        logger.info(f">>>> update due date: {new_due_date}")
    else:
        logger.info(f"not update due date")

# main
if __name__ == "__main__":
    main()