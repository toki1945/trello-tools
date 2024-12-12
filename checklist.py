#!/usr/bin/env python3

class CheckList:

    def __init__(self, name, items):
        self.name = name
        self.items = items

    def print_check_list(self):
        print(self.name)
        check_items = [item for item in self.items]
        check_items.sort(key=lambda k: k["pos"])

        for check_item in check_items:
            print(check_item["name"], check_item["state"])