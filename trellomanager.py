#!/usr/bin/env python3
"""
https://developer.atlassian.com/cloud/trello/rest/api-group-actions/#api-group-actions
"""
import argparse
import asyncio

import httpx

from card import Card
from checklist import CheckList
from configmanager import LoggerConfigManager, TrelloConfigManager


LOG_CONFIG = "logger.yaml"
LOGGER_NAME = "trelloManager"

HEADER = {"Accept": "application/json"}


class TrelloManager:

    def __init__(self):
        congig_manager = TrelloConfigManager()

        self.user_id = congig_manager.settings["user"]
        self.api_key = congig_manager.settings["api"]["key"]
        self.token = congig_manager.settings["api"]["token"]
        self.client = httpx.AsyncClient(headers=HEADER)
        self.end_point = "https://api.trello.com/1"
        self.query = {'key': self.api_key,'token': self.token}
        self.logger = LoggerConfigManager(LOGGER_NAME).setup_logger()


    @staticmethod
    def parse_argument():
        parser = argparse.ArgumentParser()
        parser.add_argument("board", type=str)
        parser.add_argument("-l","--list_name", type=str)
        return parser.parse_args()

    async def send_requests(self, url, method, data=None):
        try:

            response = await self.client.request(
                    method,
                    url,
                    params=self.query,
                    json=data
                )

            response.raise_for_status()
            return response.json()

        except Exception as e:
            self.logger.error(f"エラーが発生しました: {e}")
            return


    async def get_user_information(self, trello_id):
        return await self.send_requests(f"{self.end_point}/members/{trello_id}", "GET")


    async def get_board_information(self, board_ids: list) -> dict:
        tasks = [self.send_requests(f"{self.end_point}/boards/{board_id}", "GET") for board_id in board_ids]
        board_information_list = await asyncio.gather(*tasks)
        return {board["name"]: board for board in board_information_list}


    async def get_lists_on_board(self, board_id: str) -> dict:
        url = f"{self.end_point}/boards/{board_id}/lists"

        board_lists = await self.send_requests(url, "GET")

        return {board_list["name"]: board_list for board_list in board_lists}


    async def get_cards_on_list(self, list_id):
        url = f"{self.end_point}/lists/{list_id}/cards"

        cards_on_list = await self.send_requests(url, "GET")

        cards = [Card(card["id"], card["name"], card) for card in cards_on_list]

        return cards


    async def get_card(self, card_id):
        card = await self.send_requests(f"{self.end_point}/cards/{card_id}", "GET")
        return Card(card["id"], card["name"], card)


    async def update_card(self, card_id, **kwargs):
        result = await self.send_requests(f"{self.end_point}/cards/{card_id}", "PUT", kwargs)
        self.logger.info("カード情報を更新しました")
        return result


    async def get_checklists(self, checklist_ids: list) -> list:
        tasks = [self.send_requests(f"{self.end_point}/checklists/{checklist_id}", "GET") for checklist_id in checklist_ids]

        checklist_informations = await asyncio.gather(*tasks)

        checklist_informations.sort(key=lambda x: x["pos"])

        return [CheckList(checklist_information["id"], checklist_information["name"], checklist_information) for checklist_information in checklist_informations]


    async def delete_checklists(self, checklist_id):
        await self.send_requests(f"{self.end_point}/checklists/{checklist_id}", "DELETE")


    async def create_checklists(self, card_id, checklist_id, name):
        result = await self.send_requests(f"{self.end_point}/checklists", "POST", {"idCard": card_id, "name": name, "idChecklistSource": checklist_id})

        return result

