#!/usr/bin/env python3
from checklist import CheckList
from trelloclient import TrelloClient


class CardInformation:

    def __init__(self, card_id, name):
        self.card_id = card_id
        self.name = name

    def get_check_list(self, client: TrelloClient, cheklist_ids: list):
        check_items_list = []
        for check_list_id in cheklist_ids:
            check_items = client.get_check_list(check_list_id)
            check_items_list.append(CheckList(check_items["name"], check_items["checkItems"]))

        return check_items_list