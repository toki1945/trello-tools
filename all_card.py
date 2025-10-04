#!/usr/bin/env python3
import asyncio

from checklist import CheckList
from configmanager import LoggerConfigManager
from trellomanager import TrelloManager


LOGGER_NAME = "my_module"


async def main():
    trello_manager = None
    logger = LoggerConfigManager(LOGGER_NAME).setup_logger()

    args = TrelloManager.parse_argument()
    target_board_name = args.board
    target_list = args.list_name

    try:

        logger.info("ボード名: {}, 対象リスト = {}".format(target_board_name, target_list))
        trello_manager = TrelloManager()

        user_information = await trello_manager.get_user_information(trello_manager.user_id)

        board_information: dict = await trello_manager.get_board_information(user_information["idBoards"])

        target_board = board_information[target_board_name]

        lists_on_board: dict = await trello_manager.get_lists_on_board(target_board["id"])

        for list_on_board in lists_on_board.values():
            logger.info("====================== リスト名: {} ======================".format(list_on_board["name"]))

            cards_on_list = await trello_manager.get_cards_on_list(list_on_board["id"])

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

    except KeyError as e:
        logger.error(f"エラーが発生しました] {e}は存在しません")

    except Exception as e:
        logger.error(e)

    finally:
        if trello_manager:
            await trello_manager.client.aclose()


if __name__ == "__main__":
    asyncio.run(main())