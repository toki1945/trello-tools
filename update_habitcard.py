#!/usr/bin/env python3
"""
毎日使うカードの期限を更新、チェックリストを初期化する
"""
import asyncio
from datetime import datetime, timezone
import logging
import logging.config
from pathlib import Path

import yaml

from checklist import CheckList, CheckItem
from trellomanager import TrelloManager


WORK_DIR = Path.cwd()
LOG_DIR = WORK_DIR / "log"

SETTINGS_FILE = "settings.yaml"
LOG_CONFIG = "logger.yaml"
LOGGER_NAME = "my_module"

TARGET_LIST = "habit"

trello_manager = None


def pretreatment():

    with open(LOG_CONFIG, "r", encoding="utf-8") as l:
        yml = yaml.safe_load(l)

    logging.config.dictConfig(yml)
    logger = logging.getLogger(LOGGER_NAME)

    with open(SETTINGS_FILE, mode="r", encoding="utf-8") as f:
        settings = yaml.safe_load(f)

    LOG_DIR.mkdir(exist_ok=True)

    return logger, settings


async def main(logger: logging.Logger, settings: dict):
    today = datetime.now()

    new_due = datetime(today.year, today.month, today.day, 22, 0).astimezone(timezone.utc)

    try:

        logger.info("更新対象リスト = {}".format(TARGET_LIST))
        trello_manager = TrelloManager(settings["api"]["key"], settings["api"]["token"])

        user_information = await trello_manager.get_user_information(settings["user"])

        board_information: dict = await trello_manager.get_board_information(user_information["idBoards"])

        board_name = board_information[settings["targetboard"]["name"]]

        lists_on_board: dict = await trello_manager.get_lists_on_board(board_name["id"])

        target_list_information = lists_on_board[TARGET_LIST]

        cards_on_list = await trello_manager.get_cards_on_list(target_list_information["id"])

        tasks = []
        post_tasks = []
        for card in cards_on_list:
            logger.info(f"----------- カード名: {card.name}, id = {card.id}-----------")

            tasks.append(trello_manager.update_card(card.id, due=new_due.strftime("%Y-%m-%dT%H:%M:%S.000Z")))

            checklist_ids = card.checklist_ids()
            if checklist_ids:

                cheklists = await trello_manager.get_checklists(checklist_ids)

                cheklist: CheckList
                for cheklist in cheklists:
                    tasks.append(trello_manager.create_checklists(card.id, cheklist.id, cheklist.name))

                    post_tasks.append(trello_manager.delete_checklists(cheklist.id))

        await asyncio.gather(*tasks)
        await asyncio.gather(*post_tasks)


    except Exception as e:
        logger.error(e)

    finally:
        if trello_manager:
            await trello_manager.client.aclose()


# main
if __name__ == "__main__":

    logger, settings = pretreatment()

    asyncio.run(main(logger, settings))