#!/usr/bin/env python3
from dataclasses import dataclass
from datetime import datetime, timedelta

from checklist import CheckList
from trelloclient import TrelloClient

@dataclass
class CardInformation:
    name: str
    information: dict

    def get_check_list_items(self, client: TrelloClient, checklist_ids: list):
        check_items_list = []
        for check_list_id in checklist_ids:
            check_items = client.get_check_list(check_list_id)
            check_items_list.append(CheckList(check_items["name"], check_items["checkItems"]))

        return check_items_list

    def get_due_date(self):
        due = self.information.get("due", None)
        if not due:
            return

        due_date = datetime.strptime(due, "%Y-%m-%dT%H:%M:%S.000Z")

        return due_date + timedelta(hours=9)

    def update_due_date_for_habit_card(self):
        day = datetime.now()
        today = datetime(day.year, day.month, day.day, hour=22, minute=0)

        due_date = self.get_due_date()
        due_date = today if day.hour < 22 else today + timedelta(hours=15)

        return due_date