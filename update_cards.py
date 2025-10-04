#!/usr/bin/env python3
"""
特定のリストにあるカードの期限を本日に設定、チェックリストw初期化
"""
import asyncio
from datetime import datetime, timezone

from checklist import CheckList
from configmanager import LoggerConfigManager
from trellomanager import TrelloManager


LOGGER_NAME = "my_module"


async def main():
    trello_manager = None
    
    today = datetime.now()
    new_due = datetime(today.year, today.month, today.day, 22, 0).astimezone(timezone.utc)

    logger = LoggerConfigManager(LOGGER_NAME).setup_logger()

    args = TrelloManager.parse_argument()
    target_board_name = args.board
    target_list = args.list_name
    if not target_list:
        logger.info("引数にリスト名を渡してください")
        exit(2)

    try:

        logger.info("ボード名: {}, 対象リスト = {}".format(target_board_name, target_list))
        trello_manager = TrelloManager()

        user_information = await trello_manager.get_user_information(trello_manager.user_id)

        board_information: dict = await trello_manager.get_board_information(user_information["idBoards"])

        target_board = board_information[target_board_name]

        lists_on_board: dict = await trello_manager.get_lists_on_board(target_board["id"])


        target_list_information = lists_on_board[target_list]

        cards_on_list = await trello_manager.get_cards_on_list(target_list_information["id"])

        tasks = []
        post_tasks = []
        for card in cards_on_list:
            logger.info(f"----------- カード名: {card.name}, id = {card.id}-----------")

            tasks.append(trello_manager.update_card(card.id, due=new_due.strftime("%Y-%m-%dT%H:%M:%S.000Z")))

            checklist_ids = card.checklist_ids()
            if checklist_ids:

                checklists = await trello_manager.get_checklists(checklist_ids)

                checklist: CheckList
                for checklist in checklists:
                    tasks.append(trello_manager.create_checklists(card.id, checklist.id, checklist.name))

                    post_tasks.append(trello_manager.delete_checklists(checklist.id))

        await asyncio.gather(*tasks)
        await asyncio.gather(*post_tasks)


    except Exception as e:
        logger.error(e)

    finally:
        if trello_manager:
            await trello_manager.client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
