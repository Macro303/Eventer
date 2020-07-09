#!/usr/bin/python3
import logging
from enum import Enum, auto
from typing import Optional, List

from Eventer.base_event import Event as BaseEvent

LOGGER = logging.getLogger(__name__)


class EventType(Enum):
    GENERAL_EVENT = auto()


class Event(BaseEvent):
    def __init__(self, name: str, event_type: EventType, start_time: str, end_time: str,
                 time_zone: Optional[str] = None, details: Optional[List[str]] = None):
        super().__init__(name, event_type, start_time, end_time, time_zone)
        self.details = details or []

    def description(self) -> str:
        fields = []
        if self.details:
            fields.append('\n  - '.join(['<b><u>Details:</b></u>', *self.details]))
        return '\n'.join(fields).strip()

    def __str__(self) -> str:
        fields = []
        for key, value in self.__dict__.items():
            fields.append(f"{key}={value}")
        return f"{type(self).__name__}({', '.join(fields)})"
