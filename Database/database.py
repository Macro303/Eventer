import logging
from datetime import datetime
from typing import Optional as Opt

from pony.orm import Database, PrimaryKey, Required, Optional, Set, db_session

LOGGER = logging.getLogger(__name__)
db = Database()


def initialize_enums():
    with db_session:
        EventType.safe_insert('General Event', '27AE60')


class Attendee(db.Entity):
    username = PrimaryKey(str)
    email = Required(str, unique=True)
    event_types = Set('EventType')

    @classmethod
    def safe_insert(cls, username: str, email: str, event_types=None):
        if event_types is None:
            event_types = []
        return cls.get(username=username) or cls.get(email=email) or cls(username=username, email=email,
                                                                         event_types=event_types)

    def event_dict(self):
        return {'displayName': self.username, 'email': self.email, 'optional': True}


class EventType(db.Entity):
    name = PrimaryKey(str)
    colour_code = Required(str)
    attendees = Set(Attendee)
    events = Set('Event')

    @classmethod
    def find(cls, name: str):
        for item in cls.select()[:]:
            if item.name.lower() == name.lower():
                return item
        return None

    @classmethod
    def safe_insert(cls, name: str, colour_code: str):
        return cls.get(name=name) or cls(name=name, colour_code=colour_code)


class Event(db.Entity):
    name = Required(str)
    start_datetime = Required(datetime)
    end_datetime = Required(datetime)
    event_type = Required(EventType)
    all_day = Optional(bool, default=False, sql_default=False)
    game = Optional(str, nullable=True)

    PrimaryKey(name, start_datetime)

    @classmethod
    def safe_insert(cls, name: str, start_datetime: datetime, end_datetime: datetime, event_type: EventType,
                    all_day: bool = False, game: Opt[str] = None):
        return cls.get(name=name, start_datetime=start_datetime) or cls(name=name, start_datetime=start_datetime,
                                                                        end_datetime=end_datetime,
                                                                        event_type=event_type, all_day=all_day,
                                                                        game=game)
