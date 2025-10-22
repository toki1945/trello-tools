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
    target_cards = args.card_name.split(",")

    try:

        logger.info("ボード名: {}, 対象カード = {}".format(target_board_name, target_cards))
        trello_manager = TrelloManager()

        user_information = await trello_manager.get_user_information(trello_manager.user_id)

        board_information: dict = await trello_manager.get_board_information(user_information["idBoards"])

        target_board = board_information[target_board_name]

        lists_on_board: dict = await trello_manager.get_lists_on_board(target_board["id"])

        tasks = []

        for list_on_board in lists_on_board.values():

            cards_on_list = await trello_manager.get_cards_on_list(list_on_board["id"])

            for card in cards_on_list:
                if card.name in target_cards:
                    tasks.append(trello_manager.archive_card(card.id))

        if tasks:
            await asyncio.gather(*tasks)
            logger.info("指定されたカードをアーカイブしました")


    except KeyError as e:
        logger.error(f"エラーが発生しました] {e}は存在しません")

    except Exception as e:
        logger.error(e)

    finally:
        if trello_manager:
            await trello_manager.client.aclose()


if __name__ == "__main__":
    asyncio.run(main())