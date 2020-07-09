#!/usr/bin/python3
import copy
import logging
from datetime import datetime
from typing import Set

import yaml
from googleapiclient.discovery import build

from Eventer import EVENT_DIR, get_creds, CONFIG, list_sheets, clean_filename
from Eventer.PokemonGo.event import Event, EventType
from Eventer.base_event import Attendee

LOGGER = logging.getLogger(__name__)
GAME_TITLE = 'Pokemon Go'
GAME_EVENT_DIR = EVENT_DIR.joinpath(clean_filename(GAME_TITLE))
if not GAME_EVENT_DIR.exists():
    GAME_EVENT_DIR.mkdir(parents=True, exist_ok=True)


def load_attendees() -> Set[Attendee]:
    if not CONFIG[GAME_TITLE]['Google Calendar ID']:
        return set()

    attendees = set()
    service = build('sheets', 'v4', credentials=get_creds(), cache_discovery=False)
    current_sheets = list_sheets(service=service, game_title=GAME_TITLE)

    for entry in current_sheets[1:]:
        if entry[1].strip() in CONFIG[GAME_TITLE]['Ignored']:
            continue
        LOGGER.debug(f"Entry: {entry}")
        event_types = set()
        for temp in entry[3].split(','):
            temp = temp.strip()
            if temp in ['General Events', 'Events']:
                event_types.add(EventType.GENERAL_EVENTS)
            elif temp in ['GO Battle League']:
                event_types.add(EventType.GO_BATTLE_LEAGUE)
            elif temp in ['Raid Battles', 'Raid Day', 'Raid Boss']:
                event_types.add(EventType.RAID_BATTLES)
            elif temp in ['Giovanni Special Research']:
                event_types.add(EventType.GIOVANNI_SPECIAL_RESEARCH)
            elif temp in ['Research Breakthrough']:
                event_types.add(EventType.RESEARCH_BREAKTHROUGH)
            elif temp in ['Community Day']:
                event_types.add(EventType.COMMUNITY_DAY)
            elif temp in ['Raid Hour']:
                event_types.add(EventType.RAID_HOUR)
            elif temp in ['Pokemon Spotlight Hour', 'Mystery Bonus Hour']:
                event_types.add(EventType.POKEMON_SPOTLIGHT_HOUR)
            else:
                LOGGER.error(f"Unknown Event Type: `{temp}`")
        attendees.add(Attendee(
            email=entry[2].strip(),
            name=entry[1].strip(),
            event_types=event_types
        ))
    return attendees


def load_events() -> Set[Event]:
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
                wild=yaml_event['Wild'],
                research=yaml_event['Research'],
                eggs=yaml_event['Eggs'],
                raids=yaml_event['Raids'],
                bonuses=yaml_event['Bonus']
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
