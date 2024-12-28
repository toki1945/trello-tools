#!/usr/bin/env python3
import logging
import logging.config
from pathlib import Path

import yaml

from cardInformation import CardInformation
from checklist import CheckList
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

    target_list_information = lists_on_board[settings["board"]["myBoard"]["board_list"][1]]
    cards_on_list = trello_client.get_cards(target_list_information["id"])

    print_card_information(cards_on_list, trello_client, logger)


def print_card_information(card_list, trello_client: TrelloClient, logger: logging):
    for card_on_list in card_list:
        card = CardInformation(name=card_on_list["name"], information=card_on_list)
        logger.info(f"=============== card name = {card.name} ===============")

        check_lists = trello_client.get_check_list(card.information["idChecklists"])
        print_checklist_status(check_lists, logger)


def print_checklist_status(check_items_list: dict, logger: logging):
    for check_list_name, check_list_information in check_items_list.items():
        check_items_list = CheckList(check_list_name, check_list_information)
        logger.info(f"checkListName: {check_items_list.name}")

        check_items_list: CheckList
        for check_items in check_items_list.check_items_status():
            logger.info(f'check_items: {check_items["name"]}, status: {check_items["state"]}')

# main
if __name__ == "__main__":
    main()