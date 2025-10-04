#!/usr/bin/env python3
"""
https://developer.atlassian.com/cloud/trello/rest/api-group-actions/#api-group-actions
"""
import asyncio
from datetime import datetime, timedelta
import logging
import logging.config

import httpx
import yaml

from card import Card
from checklist import CheckList


LOG_CONFIG = "logger.yaml"
LOGGER_NAME = "trelloClient"

HEADER = {"Accept": "application/json"}


class TrelloManager:

    def __init__(self, api, token):
        self.api_key = api
        self.token = token
        self.client = httpx.AsyncClient(headers=HEADER)
        self.end_point = "https://api.trello.com/1"
        self.query = {'key': self.api_key,'token': self.token}

        with open(LOG_CONFIG, "r", encoding="utf-8") as l:
            yml = yaml.safe_load(l)

        logging.config.dictConfig(yml)
        self.logger = logging.getLogger(LOGGER_NAME)


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
        self.logger.info("update card")
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

