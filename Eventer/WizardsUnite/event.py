#!/usr/bin/python3
import logging
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum, auto

from pytz import timezone

from Eventer.base_event import Event as BaseEvent

LOGGER = logging.getLogger(__name__)


class EventType(Enum):
    GENERAL_EVENT = auto()
    COMMUNITY_DAY = auto()
    BRILLIANT_EVENT = auto()
    WIZARDING_WEEKEND = auto()


class Event(BaseEvent):
    def __init__(self, name: str, event_type: EventType, start_time: str, end_time: str, time_zone: Optional[str] = None, family: Optional[str] = None, pages: Optional[List[str]] = None, foundables: Optional[List[str]] = None, event_foundables: Optional[Dict[str, List[str]]] = None, bonuses: Optional[List[str]] = None):
        super().__init__(name, event_type, start_time, end_time, time_zone)
        self.family = family
        self.pages = pages or []
        self.foundables = foundables or []
        self.event_foundables = event_foundables or []
        self.bonuses = bonuses or []

    def description(self) -> str:
        fields = []
        if self.family:
            fields.append(f"<b><u>Family:</b></u> {self.family}")
        if self.pages:
            fields.append('\n  - '.join(['<b><u>Pages:</b></u>', *self.pages]))
        if self.foundables:
            fields.append('\n  - '.join(['<b><u>Foundables:</b></u>', *self.foundables]))
        if self.event_foundables:
            output = ["<b><u>Event Foundables:</b></u>"]
            for key, values in self.event_foundables.items():
                output.append('\n    - '.join([f"  <b>{key}:</b>", *values]))
            fields.append('\n'.join(output))
        if self.bonuses:
            fields.append('\n  - '.join(['<b><u>Bonuses:</b></u>', *self.bonuses]))
        return '\n'.join(fields).strip()

    def __str__(self) -> str:
        fields = []
        for key, value in self.__dict__.items():
            fields.append(f"{key}={value}")
        return f"{type(self).__name__}({', '.join(fields)})"
