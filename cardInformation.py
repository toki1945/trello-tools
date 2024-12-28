#!/usr/bin/env python3
from dataclasses import dataclass

from checklist import CheckList
from trelloclient import TrelloClient

@dataclass
class CardInformation:
    name: str
    information: dict

    def get_check_list_items(self, client: TrelloClient, cheklist_ids: list):
        check_items_list = []
        for check_list_id in cheklist_ids:
            check_items = client.get_check_list(check_list_id)
            check_items_list.append(CheckList(check_items["name"], check_items["checkItems"]))

        return check_items_list