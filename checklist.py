#!/usr/bin/env python3
import dataclasses

@dataclasses.dataclass
class CheckList:
    name: str
    items: dict

    def check_items_status(self) -> list:
        check_items_list = [item for item in self.items["checkItems"]]
        check_items_list.sort(key=lambda k: k["pos"])

        return check_items_list
