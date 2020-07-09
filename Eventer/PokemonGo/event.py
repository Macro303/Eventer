#!/usr/bin/python3
import logging
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum, auto

from pytz import timezone

from Eventer.base_event import Event as BaseEvent

LOGGER = logging.getLogger(__name__)


class EventType(Enum):
    GENERAL_EVENTS = auto()
    GO_BATTLE_LEAGUE = auto()
    RAID_BATTLES = auto()
    GIOVANNI_SPECIAL_RESEARCH = auto()
    RESEARCH_BREAKTHROUGH = auto()
    COMMUNITY_DAY = auto()
    RAID_HOUR = auto()
    POKEMON_SPOTLIGHT_HOUR = auto()


class Event(BaseEvent):
    def __init__(self, name: str, event_type: EventType, start_time: str, end_time: str,
                 time_zone: Optional[str] = None, wild: Optional[List[str]] = None,
                 research: Optional[List[str]] = None, eggs: Optional[Dict[str, List[str]]] = None,
                 raids: Optional[Dict[str, List[str]]] = None, bonuses: Optional[List[str]] = None):
        super().__init__(name, event_type, start_time, end_time, time_zone)
        self.wild = wild or []
        self.research = research or []
        self.eggs = eggs or {}
        self.raids = raids or {}
        self.bonuses = bonuses or []

    def description(self) -> str:
        fields = []
        if self.wild:
            fields.append('\n  - '.join(['<b><u>Wild:</b></u>', *self.wild]))
        if self.research:
            fields.append('\n  - '.join(['<b><u>Research:</b></u>', *self.research]))
        if self.eggs:
            output = ["<b><u>Eggs:</b></u>"]
            for key, values in self.eggs.items():
                output.append('\n    - '.join([f"  <b>{key}:</b>", *values]))
            fields.append('\n'.join(output))
        if self.raids:
            output = ["<b><u>Raids:</b></u>"]
            for key, values in self.raids.items():
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
