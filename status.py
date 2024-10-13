#!/usr/bin/env python3
import json

from commonlogger import Commonlogger
from trellomanager import TrelloManager
from cardInformation import CardInfoWithCheckList


SETTINGS_FILE = "settings.json"
with open(SETTINGS_FILE, mode="r", encoding="utf-8") as f:
    settings = json.load(f)

trello_user_name = settings["trelloId"]["name"]
target_board_name = settings["board"]["myBoard"]["name"]
target_list_name = settings["board"]["myBoard"]["list"][1]["name"]

if __name__ == "__main__":
    logger = Commonlogger(__name__).setup()
    trello = TrelloManager(settings["api"]["key"], settings["api"]["token"])

    trello_id = trello.get_user_id(trello_user_name)

    for board_id in trello.get_board_id(trello_user_name):
        if target_board_name == trello.get_board_name(board_id):
            logger.debug(f"target board: {target_board_name}")
            lists_on_board = trello.get_lists_on_board(board_id)
            break

    cards_list_with_list_name = []
    for board_list in lists_on_board:
        if board_list["name"] == target_list_name:
            for target in [card for card in trello.get_cards(board_list["id"]) if trello_id in card['idMembers']]:
                check_items_list = [trello.get_check_list(check_list_id) for check_list_id in target["idChecklists"]]
                CardInfoWithCheckList(target["id"], target["name"], check_items_list).print_check_list()