#!/usr/bin/env python3
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

class CardInformation:

    def __init__(self, card_id, name):
        self.card_id = card_id
        self.name = name


class CardInformationWithDate(CardInformation):

    def __init__(self, card_id, name, start, due):
        super().__init__(card_id, name)
        self.start = start
        self.due = due

    def print_card_info(self):
        start = self.convert_date(self.start).strftime("%Y-%m-%d %H:%M")
        due = self.convert_date(self.due).strftime("%Y-%m-%d %H:%M")

        print(f"タスク名： {self.name}")
        [print(f"開始日: {start}") if start else print("start dose not exists")]
        [print(f"開始日: {due}") if due else print("due dose not exists")]

    def convert_date(self, date):
        if not date:
            return

        convert_date = datetime.fromisoformat(date) +timedelta(hours=9)

        return convert_date

    def analyze_start_date(self):
        if not self.start:
            return
        start = self.convert_date(self.start)
        today = datetime.now(ZoneInfo("Asia/Tokyo"))

        if start.day == today.day:
            return 2
        elif start <= today + timedelta(days=2):
            return 1
        else:
            return 0


class CardInfoWithCheckList(CardInformation):

    def __init__(self, card_id, name, checklist):
        super().__init__(card_id, name)
        self.checklist = checklist

    def print_check_list(self):
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print(f"タスク名： {self.name}")
        for check_items in self.checklist:
            print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
            print("チェックリスト名：" + check_items["name"])
            comp_task_list = []
            in_comp_task_list = []
            for items_detail in check_items["checkItems"]:
                items = {"pos": items_detail["pos"], "name": items_detail["name"], "state": items_detail["state"]}
                comp_task_list.append(items) if items_detail["state"] == "complete" else in_comp_task_list.append(items)

            comp_task_list.sort(key=lambda k :k["pos"])
            in_comp_task_list.sort(key=lambda k :k["pos"])

            print("・完了済みタスク")
            [print(f'{comp_task["name"]}, 進捗：{comp_task["state"]}') for comp_task in comp_task_list]
            print("\n")
            print("・未着手タスク")
            [print(f'{in_comp_task["name"]}, 進捗：{in_comp_task["state"]}') for in_comp_task in in_comp_task_list]

            print("\n")

        print("\n")
