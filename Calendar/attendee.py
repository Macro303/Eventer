#!/usr/bin/python3
import logging
from typing import Set

from Calendar.Events.base_event import EventType

LOGGER = logging.getLogger(__name__)


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
