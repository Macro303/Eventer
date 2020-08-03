#!/usr/bin/python3
import copy
import logging
from datetime import datetime
from enum import Enum, auto
from typing import Optional, List, Set

import yaml

from Data import EVENT_DIR, clean_filename
from Data.base_event import Event as BaseEvent

LOGGER = logging.getLogger(__name__)
GAME_TITLE = 'Catan: World Explorers'
GAME_EVENT_DIR = EVENT_DIR.joinpath(clean_filename(GAME_TITLE))
if not GAME_EVENT_DIR.exists():
    GAME_EVENT_DIR.mkdir(parents=True, exist_ok=True)


class EventType(Enum):
    GENERAL_EVENT = auto()

    @classmethod
    def parse_type(cls, type_name: str):
        if type_name in ['General Events']:
            return cls.GENERAL_EVENT
        else:
            LOGGER.error(f"Unknown Event Type: `{type_name}`")
            return None


class Event(BaseEvent):
    def __init__(self, name: str, event_type: EventType, start_time: str, end_time: str,
                 time_zone: Optional[str] = None, details: Optional[List[str]] = None):
        super().__init__(name, event_type, start_time, end_time, time_zone)
        self.details = details or []

    def description(self) -> str:
        fields = []
        if self.details:
            fields.append('\n  - '.join(['<b><u>Details:</u></b>', *self.details]))
        return '\n'.join(fields).strip()

    def __str__(self) -> str:
        fields = []
        for key, value in self.__dict__.items():
            fields.append(f"{key}={value}")
        return f"{type(self).__name__}({', '.join(fields)})"

    def save(self):
        filename = self.start_time().strftime("%Y-%m-%d") + "-" + self.name.replace(" ", "_")
        event_file = GAME_EVENT_DIR.joinpath(filename + ".yaml")
        event_file.touch()
        with open(event_file, 'w', encoding='UTF-8') as yaml_file:
            yaml.safe_dump({
                "Name": self.name,
                "Type": self.event_type.name,
                "Start Time": self.start_time(),
                "End Time": self.end_time(),
                "Timezone": self.time_zone,
                "Details": self.details or []
            }, yaml_file)


def load_events() -> Set[Event]:
    LOGGER.info(f"Loading {GAME_TITLE} events")
    events = set()
    files = [p for p in GAME_EVENT_DIR.iterdir() if p.is_file() and p.name.endswith('.yaml')]
    for file in files:
        with open(file, 'r', encoding='UTF-8') as event_file:
            yaml_event = yaml.safe_load(event_file)
            event = Event(
                name=yaml_event['Name'],
                event_type=EventType[yaml_event['Type']],
                start_time=yaml_event['Start Time'],
                end_time=yaml_event['End Time'],
                time_zone=yaml_event['Timezone']
            )
            days_dif = (datetime.today() - event.end_time()).days
            if days_dif > 14:
                LOGGER.warning(f"Skipping Old Event `{event.start_time().strftime('%Y-%m-%d')}|"
                               f"{event.name}` => {days_dif} days old")
                continue
            if (event.end_time() - event.start_time()).days > 8:
                temp = copy.deepcopy(event)

                temp.start_time_str = temp.start_time_str
                temp.end_time_str = temp.start_time_str
                temp.name = temp.name + ' Begins'
                events.add(temp)

                event.start_time_str = event.end_time_str
                event.end_time_str = event.end_time_str
                event.name = event.name + ' Ends'
                events.add(event)
            else:
                events.add(event)
    return events


EVENTS = load_events()
