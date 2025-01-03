#!/usr/bin/env python3
from datetime import datetime, timedelta
import logging
import logging.config

import requests
import yaml


LOG_CONFIG = "logger.yaml"
LOGGER_NAME = "trelloClient"

GET = "GET"
PUT = "PUT"
POST = "POST"

class TrelloClient:
    def __init__(self, api, token):
        self.api_key = api
        self.token = token

        with open(LOG_CONFIG, "r", encoding="utf-8") as l:
            yml = yaml.safe_load(l)

        logging.config.dictConfig(yml)
        self.logger = logging.getLogger(LOGGER_NAME)

    def send_requests(self, url, data, method):
        try:
            headers = {"Accept": "application/json"}
            query = {'key': self.api_key,'token': self.token}
            if data:
                response = requests.request(
                method,
                url,
                headers=headers,
                params=query,
                json=data
                )
            else:
                response = requests.request(
                method,
                url,
                headers=headers,
                params=query,
            )
            status_code = response.status_code
        except Exception:
            self.logger.error(f"#### send_requests was not succeeded, status code = {status_code}")
            return

        return response.json()

    def get_user_information(self, trello_id):
        url = f"https://api.trello.com/1/members/{trello_id}"
        result = self.send_requests(url, None, GET)

        return result

    def get_board_information(self, board_ids: list) -> dict:
        board_information_list = []
        for board_id in board_ids:
            url = f"https://api.trello.com/1/boards/{board_id}"
            result = self.send_requests(url, None, GET)
            board_information_list.append(result)

        board_dict = {board["name"]: board for board in board_information_list}

        return board_dict

    def get_lists_on_board(self, board_id: str) -> dict:
        url = f"https://api.trello.com/1/boards/{board_id}/lists"
        result = self.send_requests(url, None, GET)

        list_dict = {list_on_board["name"]: list_on_board for list_on_board in result}

        return list_dict

    def get_cards(self, list_id):
        url = f"https://api.trello.com/1/lists/{list_id}/cards"
        result = self.send_requests(url, None, GET)

        return result

    def get_all_cards(self, list_ids: dict):
        card_list = []
        for list_id in list_ids.values():
            cards = self.get_cards(list_id["id"])
            card_list.extend(cards)

        return card_list

    def update_card(self, card_id, **kwargs):
        url = f"https://api.trello.com/1/cards/{card_id}"
        result = self.send_requests(url, kwargs, PUT)

        return result

    def update_due_date(self, card_id, due_date: datetime):
        due_date = due_date - timedelta(hours=9)
        url = f"https://api.trello.com/1/cards/{card_id}"
        result = self.send_requests(url, {"due": due_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")}, PUT)

        return result

    def get_check_list(self, check_list_ids: list) -> dict:
        checklist_information_list = []
        for checklist_id in check_list_ids:
            url = f"https://api.trello.com/1/checklists/{checklist_id}"
            result = self.send_requests(url, None, GET)
            checklist_information_list.append(result)

        checklist_information_list.sort(key=lambda x: x["pos"])

        checklist = {checklist_information["name"]: checklist_information for checklist_information in checklist_information_list}

        return checklist