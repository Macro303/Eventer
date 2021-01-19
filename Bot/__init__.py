import logging
import pickle
from pathlib import Path
from typing import Dict, Any

import yaml
from discord import Colour
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

TOP_DIR = Path(__file__).resolve().parent.parent
LOGGER = logging.getLogger(__name__)

config_file = TOP_DIR.joinpath('config.yaml')
if config_file.exists():
    with open(config_file, 'r', encoding='UTF-8') as yaml_file:
        CONFIG = yaml.safe_load(yaml_file) or {
            'Prefix': '?',
            'Token': None,
            'Calendar ID': None
        }
else:
    config_file.touch()
    CONFIG = {
        'Prefix': '?',
        'Token': None,
        'Calendar ID': None
    }
with open(config_file, 'w', encoding='UTF-8') as yaml_file:
    yaml.safe_dump(CONFIG, yaml_file)


def load_colour(colour: str) -> Colour:
    return Colour(int(colour, 16))


SCOPES = ['https://www.googleapis.com/auth/calendar.events.owned']


def get_creds():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if TOP_DIR.joinpath('token.pickle').exists():
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def insert_calendar_event(event_body: Dict[str, Any]):
    try:
        event = SERVICE.events().insert(calendarId=CONFIG['Calendar ID'], body=event_body).execute()
        if 'date' in event_body['start']:
            LOGGER.info(f"{event_body['start']['date']}|{event_body['summary']} was created")
        else:
            LOGGER.info(f"{event_body['start']['dateTime'].split('T')[0]}|{event_body['summary']} was created")
    except HttpError as err:
        LOGGER.error(err)


SERVICE = build('calendar', 'v3', credentials=get_creds(), cache_discovery=False)
