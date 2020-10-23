#!/usr/bin/python3
import logging
from argparse import ArgumentParser, Namespace
from typing import Set

from googleapiclient import errors
from googleapiclient.discovery import build

from Calendar import get_creds, CONFIG, list_events, load_attendees
from Calendar.attendee import Attendee
from Calendar.Events import pokemon_go, wizards_unite, catan_explorer
from Calendar.Events.base_event import Event
from Logger import init_logger

LOGGER = logging.getLogger(__name__)


def get_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true',
                        help='Stops Events from being created in Google Calendar')
    parser.add_argument('-c', '--catan', action='store_true',
                        help='Reads and Creates the events for the Catan: World Explorers Game')
    parser.add_argument('-p', '--pokemon', action='store_true',
                        help='Reads and Creates the events for the Pokemon Go Game')
    parser.add_argument('-w', '--wizards', action='store_true',
                        help='Reads and Creates the events for the Harry Potter: Wizards Unite Game')
    return parser.parse_args()


def main(run_pokemon: bool = False, run_wizards: bool = False, run_catan: bool = False, run_tests: bool = True):
    games = set()
    if run_pokemon:
        games.add(pokemon_go)
    if run_wizards:
        games.add(wizards_unite)
    if run_catan:
        games.add(catan_explorer)

    LOGGER.info(f"Creating Events for: {[x.__name__ for x in games]}")

    attendees = {}
    all_events = {}
    for game in games:
        # Attendees
        temp = load_attendees(game=game)
        if not temp:
            LOGGER.info(f"No {game.GAME_TITLE} attendees.")
        attendees[game.GAME_TITLE] = temp

        # Events
        temp = game.load_events()
        if not temp:
            LOGGER.info(f"No {game.GAME_TITLE} events.")
        all_events[game.GAME_TITLE] = temp

    service = build('calendar', 'v3', credentials=get_creds(), cache_discovery=False)
    for game_title, file_events in all_events.items():
        if not CONFIG[game_title]['Google Calendar ID']:
            continue

        calendar_events = list_events(service=service, game_title=game_title)

        for file_event in file_events:
            filtered_attendees = set([x for x in attendees[game_title] if file_event.event_type in x.event_types])
            filtered = filter(lambda x: x['summary'] == file_event.name and (
                x['start']['dateTime'] == file_event.start_time_localized() if 'dateTime' in x['start'] else
                x['start']['date'] == file_event.start_date_str()), calendar_events)
            exists = next(filtered, None)
            if exists:
                update_event(service=service, file_event=file_event, calendar_event=exists,
                             attendees=filtered_attendees, calendar_id=CONFIG[game_title]['Google Calendar ID'],
                             testing=run_tests)
            else:
                create_event(service, file_event, attendees=filtered_attendees,
                             calendar_id=CONFIG[game_title]['Google Calendar ID'], testing=run_tests)

    LOGGER.info('Finished creating events')


def update_event(service, file_event: Event, calendar_event, attendees: Set[Attendee], calendar_id: str,
                 testing: bool = True):
    update_required = False
    if file_event.description() != calendar_event.get('description', ''):
        old = calendar_event.get('description', '')
        calendar_event['description'] = file_event.description()
        LOGGER.debug(f"Updated from:\n`{old}`\n=>\n`{calendar_event['description']}`")
        update_required = True
    missing = [x for x in attendees if x.email not in set([x['email'] for x in calendar_event.get('attendees', [])])]
    if missing:
        calendar_event['attendees'] = [x.to_dict() for x in attendees]
        update_required = True
    if update_required:
        if not testing:
            service.events().patch(calendarId=calendar_id, eventId=calendar_event['id'], body=calendar_event).execute()
        LOGGER.info(f"{file_event.start_date_str()}|{file_event.name} Event updated")


def create_event(service, file_event: Event, attendees: Set[Attendee], calendar_id: str, testing: bool = True):
    event_json = {
        'summary': file_event.name,
        'description': file_event.description(),
        'start': {
            'timeZone': file_event.time_zone
        },
        'end': {
            'timeZone': file_event.time_zone
        },
        'attendees': [x.to_dict() for x in attendees],
        'reminders': {
            'useDefault': False,
            'overrides': []
        },
        'guestsCanSeeOtherGuests': False,
        'guestsCanModify': False,
        'transparency': 'transparent'
    }
    if file_event.all_day:
        event_json['start']['date'] = file_event.start_date_str()
        event_json['end']['date'] = file_event.end_date_str()
        event_json['reminders']['overrides'].append({'method': 'popup', 'minutes': 3 * 60})
        event_json['reminders']['overrides'].append({'method': 'popup', 'minutes': 15 * 60})
    else:
        event_json['start']['dateTime'] = file_event.start_time_str
        event_json['end']['dateTime'] = file_event.end_time_str
        event_json['reminders']['overrides'].append({'method': 'popup', 'minutes': 2 * 60})
        event_json['reminders']['overrides'].append({'method': 'popup', 'minutes': 24 * 60})

    try:
        if not testing:
            calendar_event = service.events().insert(calendarId=calendar_id, body=event_json).execute()
        LOGGER.info(f"{file_event.start_date_str()}|{file_event.name} created")
    except errors.HttpError as err:
        LOGGER.error(err)


if __name__ == '__main__':
    init_logger('Calendar')
    args = get_arguments()
    try:
        main(args.pokemon, args.wizards, args.catan, args.test)
    except:
        LOGGER.fatal('Unable to connect to Google')
