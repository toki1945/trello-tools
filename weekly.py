#!/usr/bin/env python3
import asyncio

from configmanager import LoggerConfigManager
from trellomanager import TrelloManager


LOGGER_NAME = "my_module"


async def main():
    trello_manager = None
    logger = LoggerConfigManager(LOGGER_NAME).setup_logger()

    args = TrelloManager.parse_argument()
    target_board_name = args.board
    if not args.list_name:
        logger.error("リスト名を指定してください")
        return

    target_list_name = args.list_name

    try:

        logger.info("ボード名: {}".format(target_board_name))
        trello_manager = TrelloManager()

        user_information = await trello_manager.get_user_information(trello_manager.user_id)

        board_information: dict = await trello_manager.get_board_information(user_information["idBoards"])

        target_board = board_information[target_board_name]

        lists_on_board: dict = await trello_manager.get_lists_on_board(target_board["id"])

        all_cards = []
        for list_on_board in lists_on_board.values():
            cards_on_list = await trello_manager.get_cards_on_list(list_on_board["id"])
            all_cards.extend(cards_on_list)

        my_cards = [card for card in all_cards if card.information["idMembers"] and user_information["id"] in card.information["idMembers"]]

        tasks = []
        for my_card in my_cards:
            if "【週次】" not in my_card.name:
                continue
            tasks.append(trello_manager.create_card(lists_on_board[target_list_name]["id"], dueComplete=False, idCardSource=my_card.information["id"]))

        await asyncio.gather(*tasks)

    except KeyError as e:
        logger.error(f"エラーが発生しました] {e}は存在しません")

    except Exception as e:
        logger.error(e)

    finally:
        if trello_manager:
            await trello_manager.client.aclose()


if __name__ == "__main__":
    asyncio.run(main())