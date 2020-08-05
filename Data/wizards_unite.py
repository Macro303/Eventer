#!/usr/bin/python3
import copy
import logging
from datetime import datetime
from enum import Enum, auto
from typing import Optional, List, Set, Dict

import yaml

from Data import EVENT_DIR, clean_filename
from Data.base_event import Event as BaseEvent

LOGGER = logging.getLogger(__name__)
GAME_TITLE = 'Harry Potter: Wizards Unite'
GAME_EVENT_DIR = EVENT_DIR.joinpath(clean_filename(GAME_TITLE))
if not GAME_EVENT_DIR.exists():
    GAME_EVENT_DIR.mkdir(parents=True, exist_ok=True)


class EventType(Enum):
    GENERAL_EVENT = auto()
    COMMUNITY_DAY = auto()
    BRILLIANT_EVENT = auto()
    WIZARDING_WEEKEND = auto()

    @classmethod
    def parse_type(cls, type_name: str):
        if type_name in ['General Events']:
            return cls.GENERAL_EVENT
        elif type_name in ['Community Days']:
            return cls.COMMUNITY_DAY
        elif type_name in ['Brilliant Events']:
            return cls.BRILLIANT_EVENT
        elif type_name in ['Wizarding Weekends']:
            return cls.WIZARDING_WEEKEND
        else:
            LOGGER.error(f"Unknown Event Type: `{type_name}`")
            return None


class Event(BaseEvent):
    def __init__(self, name: str, event_type: EventType, start_time: str, end_time: str,
                 time_zone: Optional[str] = None, all_day: bool = False, family: Optional[str] = None,
                 pages: Optional[List[str]] = None, foundables: Optional[List[str]] = None,
                 event_foundables: Optional[Dict[str, List[str]]] = None, bonuses: Optional[List[str]] = None):
        super().__init__(name, event_type, start_time, end_time, time_zone, all_day)
        self.family = family
        self.pages = pages or []
        self.foundables = foundables or []
        self.event_foundables = event_foundables or {}
        self.bonuses = bonuses or []

    def description(self) -> str:
        fields = []
        if self.family:
            fields.append(f"<b><u>Family:</u></b> {self.family}")
        if self.pages:
            fields.append('\n  - '.join(['<b><u>Pages:</u></b>', *self.pages]))
        if self.foundables:
            fields.append('\n  - '.join(['<b><u>Foundables:</u></b>', *self.foundables]))
        if self.event_foundables:
            output = ["<b><u>Event Foundables:</u></b>"]
            for key, values in self.event_foundables.items():
                output.append('\n    - '.join([f"  <b>{key}:</b>", *values]))
            fields.append('\n'.join(output))
        if self.bonuses:
            fields.append('\n  - '.join(['<b><u>Bonuses:</u></b>', *self.bonuses]))
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
                'Name': self.name,
                'Type': self.event_type.name,
                'Start Time': self.start_time_str,
                'End Time': self.end_time_str,
                'Timezone': self.time_zone,
                'All Day': self.all_day,
                'Family': self.family,
                'Pages': self.pages or [],
                'Foundables': self.foundables or [],
                'Event Foundables': self.event_foundables or {},
                'Bonuses': self.bonuses or []
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
                time_zone=yaml_event['Timezone'],
                all_day=yaml_event['All Day'] if 'All Day' in yaml_event else False,
                family=yaml_event['Family'],
                pages=yaml_event['Pages'],
                foundables=yaml_event['Foundables'],
                event_foundables=yaml_event['Event Foundables'],
                bonuses=yaml_event['Bonuses']
            )
            days_dif = (datetime.today() - event.end_time()).days
            if days_dif > 14:
                LOGGER.warning(f"Skipping Old Event `{event.start_date_str()}|{event.name}` => {days_dif} days old")
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
