#!/usr/bin/env python3
from trelloclient import TrelloClient


def get_user_information(client: TrelloClient, name):
    _user_information = client.get_user_information(name)

    return _user_information


def get_board_information(client: TrelloClient, board_id: str) -> dict:
    _board_information = client.get_board_information(board_id)

    return _board_information


def get_lists_on_board(client: TrelloClient, board_id: str) -> dict:
    _lists_on_board = client.get_lists_on_board(board_id)

    return _lists_on_board


def get_cards_on_board(client: TrelloClient, list_id: str) -> list:
    _card_list :list = client.get_cards(list_id)

    return _card_list