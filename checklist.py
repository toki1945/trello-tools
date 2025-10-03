#!/usr/bin/env python3
from dataclasses import dataclass

@dataclass
class CheckItem:
    name: str
    pos: int
    state: str

    def __repr__(self):
        return f"name = {self.name}, state = {self.state}"


@dataclass
class CheckList:
    name: str
    items: dict

    def items_status(self) -> list:
        check_items = [CheckItem(check_item["name"], check_item["pos"], check_item["state"]) for check_item in self.items["checkItems"]]
        return sorted(check_items, key=lambda item: item.pos)

