#!/usr/bin/env python3
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging


@dataclass
class Card:
    id: str
    name: str
    information: dict

    def checklist_ids(self):
        return self.information.get("idChecklists")


    def get_due_date(self):
        try:
            due = self.information.get("due", None)
            if not due:
                return None

            due_date = datetime.strptime(due, "%Y-%m-%dT%H:%M:%S.000Z")
            return due_date + timedelta(hours=9)
        except ValueError as e:
            logging.error(f"Invalid date format: {str(e)}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error in get_due_date: {str(e)}")
            return None


    def update_due_date_for_habit_card(self):
        try:
            day = datetime.now()
            today = datetime(day.year, day.month, day.day, hour=22, minute=0)

            due_date = self.get_due_date()
            if due_date is None:
                return None


            return today if day.hour < 22 else today + timedelta(hours=15)
        except Exception as e:
            logging.error(f"Failed to update due date: {str(e)}")
            return None