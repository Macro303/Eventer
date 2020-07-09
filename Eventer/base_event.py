#!/usr/bin/python3
import logging
from datetime import datetime
from enum import Enum, auto
from typing import Optional, Set

from pytz import timezone

LOGGER = logging.getLogger(__name__)


class EventType(Enum):
    GENERAL_EVENT = auto()


class Event:
    def __init__(self, name: str, event_type: EventType, start_time: str, end_time: str,
                 time_zone: Optional[str] = None):
        self.name = name
        self.event_type = event_type
        self.time_zone = time_zone or 'Pacific/Auckland'
        self.start_time_str = start_time
        self.end_time_str = end_time

    def start_time(self) -> datetime:
        return datetime.strptime(self.start_time_str, '%Y-%m-%dT%H:%M:%S')

    def start_time_localized(self) -> str:
        return timezone(self.time_zone).localize(self.start_time()).astimezone(timezone('Pacific/Auckland')) \
            .isoformat(sep='T')

    def end_time(self) -> datetime:
        return datetime.strptime(self.end_time_str, '%Y-%m-%dT%H:%M:%S')

    def end_time_localized(self) -> str:
        return timezone(self.time_zone).localize(self.end_time()).astimezone(timezone('Pacific/Auckland')) \
            .isoformat(sep='T')

    def description(self) -> str:
        return ''

    def __str__(self) -> str:
        fields = []
        for key, value in self.__dict__.items():
            fields.append(f"{key}={value}")
        return f"{type(self).__name__}({', '.join(fields)})"


class Attendee:
    def __init__(self, name: str, email: str, event_types: Set[EventType]):
        self.name = name
        self.email = email
        self.event_types = event_types

    def to_dict(self):
        return {'displayName': self.name, 'email': self.email, 'optional': True}

    def __str__(self) -> str:
        fields = []
        for key, value in self.__dict__.items():
            fields.append(f"{key}={value}")
        return f"{type(self).__name__}({', '.join(fields)})"
