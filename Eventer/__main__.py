#!/usr/bin/python3
import logging
from argparse import ArgumentParser, Namespace
from typing import Set

from googleapiclient import errors
from googleapiclient.discovery import build

from Eventer import CatanExplorer, PokemonGo, WizardsUnite, get_creds, CONFIG, list_events
from Eventer.base_event import Event, Attendee
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


args = get_arguments()


def main():
    games = set()
    if args.catan:
        games.add(CatanExplorer)
    if args.pokemon:
        games.add(PokemonGo)
    if args.wizards:
        games.add(WizardsUnite)

    attendees = {}
    all_events = {}
    for game in games:
        # Attendees
        temp = game.load_attendees()
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
        LOGGER.info(f"Game Title: {game_title}")
        LOGGER.info(f"Attendees: {attendees}")
        if not CONFIG[game_title]['Google Calendar ID']:
            continue

        calendar_events = list_events(service=service, game_title=game_title)

        for file_event in file_events:
            filtered_attendees = [x for x in attendees[game_title] if file_event.event_type in x.event_types]
            filtered = filter(lambda x: x['summary'] == file_event.name and x['start'][
                'dateTime'] == file_event.start_time_localized(), calendar_events)
            exists = next(filtered, None)
            if exists:
                update_event(service=service, file_event=file_event, calendar_event=exists,
                             attendees=filtered_attendees, calendar_id=CONFIG[game_title]['Google Calendar ID'])
            else:
                create_event(service, file_event, attendees=filtered_attendees,
                             calendar_id=CONFIG[game_title]['Google Calendar ID'])


def update_event(service, file_event: Event, calendar_event, attendees: Set[Attendee], calendar_id: str):
    update_required = False
    if file_event.description() != calendar_event.get('description', ''):
        calendar_event['description'] = file_event.description()
        update_required = True
    missing = [x for x in attendees if x.email not in set([x['email'] for x in calendar_event.get('attendees', [])])]
    if missing:
        calendar_event['attendees'] = [x.to_dict() for x in attendees]
        update_required = True
    if update_required:
        if not args.test:
            service.events().patch(calendarId=calendar_id, eventId=calendar_event['id'], body=calendar_event).execute()
        LOGGER.info(f"{file_event.start_time().strftime('%Y-%m-%d')}|{file_event.name} Event updated")


def create_event(service, file_event: Event, attendees: Set[Attendee], calendar_id: str):
    event_json = {
        'summary': file_event.name,
        'description': file_event.description(),
        'start': {
            'dateTime': file_event.start_time_str,
            'timeZone': file_event.time_zone
        },
        'end': {
            'dateTime': file_event.end_time_str,
            'timeZone': file_event.time_zone
        },
        'attendees': [x.to_dict() for x in attendees],
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 2 * 60},
                {'method': 'popup', 'minutes': 24 * 60}
            ]
        },
        'guestsCanSeeOtherGuests': False,
        'guestsCanModify': False,
        'transparency': 'transparent'
    }

    try:
        if not args.test:
            calendar_event = service.events().insert(calendarId=calendar_id, body=event_json).execute()
        LOGGER.info(f"{file_event.start_time().strftime('%Y-%m-%d')}|{file_event.name} created")
    except errors.HttpError as err:
        LOGGER.error(err)


if __name__ == '__main__':
    init_logger('Eventer')
    main()
