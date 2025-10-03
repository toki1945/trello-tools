#!/usr/bin/env python3
import asyncio
import logging
import logging.config
from pathlib import Path

import yaml

from checklist import CheckList
from trellomanager import TrelloManager


WORK_DIR = Path.cwd()
LOG_DIR = WORK_DIR / "log"

TARGET_LIST = "study"

SETTINGS_FILE = "settings.yaml"
LOG_CONFIG = "logger.yaml"
LOGGER_NAME = "my_module"

trello_manager = None


async def main():

    with open(SETTINGS_FILE, mode="r", encoding="utf-8") as f:
        settings = yaml.safe_load(f)

    with open(LOG_CONFIG, "r", encoding="utf-8") as l:
        yml = yaml.safe_load(l)

    logging.config.dictConfig(yml)
    logger = logging.getLogger(LOGGER_NAME)

    LOG_DIR.mkdir(exist_ok=True)

    try:

        logger.info("対象リスト名 = {}".format(TARGET_LIST))
        trello_manager = TrelloManager(settings["api"]["key"], settings["api"]["token"])

        user_information = await trello_manager.get_user_information(settings["user"])

        board_information: dict = await trello_manager.get_board_information(user_information["idBoards"])

        board_name = board_information[settings["targetboard"]["name"]]

        lists_on_board: dict = await trello_manager.get_lists_on_board(board_name["id"])

        target_list_information = lists_on_board[TARGET_LIST]

        cards_on_list = await trello_manager.get_cards_on_list(target_list_information["id"])

        for card in cards_on_list:
            logger.info(f"----------- カード名: {card.name}, id = {card.id}-----------")
            checklist_ids = card.checklist_ids()
            if not checklist_ids:
                continue

            cheklists = await trello_manager.get_checklists(checklist_ids)

            cheklist: CheckList
            for cheklist in cheklists:
                logger.info("チェックリスト名: {}".format(cheklist.name))
                check_items = cheklist.items_status()
                logger.info("アイテム一覧")
                logger.info(check_items)


    except Exception as e:
        logger.error(e)

    finally:
        if trello_manager:
            await trello_manager.client.aclose()

# main
if __name__ == "__main__":
    asyncio.run(main())