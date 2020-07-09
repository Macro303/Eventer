#!/usr/bin/python3
import logging
import pickle
from pathlib import Path
from datetime import datetime

import yaml
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

TOP_DIR = Path(__file__).resolve().parent.parent
EVENT_DIR = TOP_DIR.joinpath('Events')

LOGGER = logging.getLogger(__name__)

# If changing these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/spreadsheets.readonly']

config_file = TOP_DIR.joinpath('config.yaml')
if config_file.exists():
    with open(config_file, 'r', encoding='UTF-8') as yaml_file:
        CONFIG = yaml.safe_load(yaml_file) or {
            'Google Sheets ID': None,
            'Catan: World Explorers': {
                'Google Calendar ID': None,
                'Ignored': []
            },
            'Harry Potter: Wizards Unite': {
                'Google Calendar ID': None,
                'Ignored': []
            },
            'Pokemon Go': {
                'Google Calendar ID': None,
                'Ignored': []
            }
        }
else:
    config_file.touch()
    CONFIG = {
        'Google Sheets ID': None,
        'Catan: World Explorers': {
            'Google Calendar ID': None,
            'Ignored': []
        },
        'Harry Potter: Wizards Unite': {
            'Google Calendar ID': None,
            'Ignored': []
        },
        'Pokemon Go': {
            'Google Calendar ID': None,
            'Ignored': []
        }
    }
with open(config_file, 'w', encoding='UTF-8') as yaml_file:
    yaml.safe_dump(CONFIG, yaml_file)


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


def list_sheets(service, game_title: str):
    results = service.spreadsheets().values().get(spreadsheetId=CONFIG['Google Sheets ID'], range=game_title).execute()
    return results.get('values', [])

def list_events(service, game_title: str):
    today = datetime.today()
    month = today.month - 2
    year = today.year if month < today.month else today.year - 1
    start = datetime.today().replace(year=year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)
    LOGGER.info(f"Getting all the {game_title} Events after {start.strftime('%Y-%m-%d')}")

    # Call the Calendar API
    events_result = service.events().list(calendarId=CONFIG[game_title]['Google Calendar ID'], timeMin=start.isoformat() + 'Z', singleEvents=True, orderBy='startTime').execute()
    return events_result.get('items', [])

def clean_filename(filename: str) -> str:
    return filename.replace(':', '')
