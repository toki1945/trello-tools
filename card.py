#!/usr/bin/env python3
from dataclasses import dataclass


@dataclass
class Card:
    id: str
    name: str
    information: dict


    def checklist_ids(self):
        return self.information.get("idChecklists")


    def get_due_date(self):
        return self.information.get("due", None)
