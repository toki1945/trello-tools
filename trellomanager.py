#!/usr/bin/env python3
import requests

from commonlogger import Commonlogger

GET = "GET"
PUT = "PUT"
POST = "POST"

class TrelloManager:
    def __init__(self, api, token):
        self.api_key = api
        self.token = token
        logger = Commonlogger("trello-manager").setup()
        self.logger = logger

    def send_requests(self, url, data, method):
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

        return response.json()

    def get_user_id(self, trello_id):
        url = f"https://api.trello.com/1/members/{trello_id}"
        result = self.send_requests(url, None, GET)

        return result["id"]

    def get_board_id(self, trello_id):
        url = f"https://api.trello.com/1/members/{trello_id}"
        result = self.send_requests(url, None, GET)

        return result["idBoards"]

    def get_board_name(self, board_id):
        url = f"https://api.trello.com/1/boards/{board_id}"
        result = self.send_requests(url, None, GET)

        return result["name"]

    def get_lists_on_board(self, board_id):
        url = f"https://api.trello.com/1/boards/{board_id}/lists"
        result = self.send_requests(url, None, GET)

        return result

    def get_cards(self, list_id):
        url = f"https://api.trello.com/1/lists/{list_id}/cards"
        result = self.send_requests(url, None, GET)

        return result

    def get_check_list(self, check_list_id):
        url = f"https://api.trello.com/1/checklists/{check_list_id}"
        result = self.send_requests(url, None, GET)

        return result