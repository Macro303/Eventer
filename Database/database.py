import logging
from datetime import datetime

from pony.orm import Database, PrimaryKey, Required, Optional, Set, db_session

LOGGER = logging.getLogger(__name__)
db = Database()


def initialize_enums():
    with db_session:
        PokemonGoEventType.safe_insert('General Event', '27AE60')
        PokemonGoEventType.safe_insert('GO Battle League', '8E44AD')
        PokemonGoEventType.safe_insert('Raid Battle', 'C0392B')
        PokemonGoEventType.safe_insert('Giovanni', '000000')  # TODO Assign a Colour
        PokemonGoEventType.safe_insert('Research Breakthrough', '795548')
        PokemonGoEventType.safe_insert('Community Day', '1660A9')
        PokemonGoEventType.safe_insert('Raid Hour', 'C0392B')
        PokemonGoEventType.safe_insert('Spotlight Hour', 'E58E26')
        PokemonGoEventType.safe_insert('Paid Event', 'DE3E9B')

        WizardsUniteEventType.safe_insert('General Event', '27AE60')

        CatanEventType.safe_insert('General Event', '27AE60')


class PokemonGo(db.Entity):
    username = PrimaryKey(str)
    email = Required(str, unique=True)
    event_types = Set('PokemonGoEventType')

    @classmethod
    def safe_insert(cls, username: str, email: str, event_types=None):
        if event_types is None:
            event_types = []
        return cls.get(username=username) or cls.get(email=email) or cls(username=username, email=email,
                                                                         event_types=event_types)

    def event_dict(self):
        return {'displayName': self.username, 'email': self.email, 'optional': True}


class PokemonGoEventType(db.Entity):
    name = PrimaryKey(str)
    colour_code = Required(str)
    members = Set(PokemonGo)
    events = Set('PokemonGoEvent')

    @classmethod
    def find(cls, name: str):
        for item in cls.select()[:]:
            if item.name.lower() == name.lower():
                return item
        return None

    @classmethod
    def safe_insert(cls, name: str, colour_code: str):
        return cls.get(name=name) or cls(name=name, colour_code=colour_code)


class PokemonGoEvent(db.Entity):
    name = Required(str)
    start_datetime = Required(datetime)
    end_datetime = Required(datetime)
    event_type = Required(PokemonGoEventType)
    all_day = Optional(bool, default=False, sql_default=False)

    PrimaryKey(name, start_datetime)

    @classmethod
    def safe_insert(cls, name: str, start_datetime: datetime, end_datetime: datetime, event_type: PokemonGoEventType,
                    all_day: bool = False):
        return cls.get(name=name, start_datetime=start_datetime) or cls(name=name, start_datetime=start_datetime,
                                                                        end_datetime=end_datetime,
                                                                        event_type=event_type, all_day=all_day)


class WizardsUnite(db.Entity):
    username = PrimaryKey(str)
    email = Required(str, unique=True)
    event_types = Set('WizardsUniteEventType')

    @classmethod
    def safe_insert(cls, username: str, email: str, general_event: bool = False):
        return cls.get(username=username) or cls.get(email=email) or cls(username=username, email=email,
                                                                         general_event=general_event)


class WizardsUniteEventType(db.Entity):
    name = PrimaryKey(str)
    colour_code = Required(str)
    members = Set(WizardsUnite)
    events = Set('WizardsUniteEvent')

    @classmethod
    def find(cls, name: str):
        for item in cls.select()[:]:
            if item.name.lower() == name.lower():
                return item
        return None

    @classmethod
    def safe_insert(cls, name: str, colour_code: str):
        return cls.get(name=name) or cls(name=name, colour_code=colour_code)


class WizardsUniteEvent(db.Entity):
    name = Required(str)
    start_datetime = Required(datetime)
    end_datetime = Required(datetime)
    event_type = Required(WizardsUniteEventType)
    all_day = Optional(bool, default=False, sql_default=False)

    PrimaryKey(name, start_datetime)

    @classmethod
    def safe_insert(cls, name: str, start_datetime: datetime, end_datetime: datetime, event_type: WizardsUniteEventType,
                    all_day: bool = False):
        return cls.get(name=name, start_datetime=start_datetime) or cls(name=name, start_datetime=start_datetime,
                                                                        end_datetime=end_datetime,
                                                                        event_type=event_type, all_day=all_day)


class Catan(db.Entity):
    username = PrimaryKey(str)
    email = Required(str, unique=True)
    event_types = Set('CatanEventType')

    @classmethod
    def safe_insert(cls, username: str, email: str, general_event: bool = False):
        return cls.get(username=username) or cls.get(email=email) or cls(username=username, email=email,
                                                                         general_event=general_event)


class CatanEventType(db.Entity):
    name = PrimaryKey(str)
    colour_code = Required(str)
    members = Set(Catan)
    events = Set('CatanEvent')

    @classmethod
    def find(cls, name: str):
        for item in cls.select()[:]:
            if item.name.lower() == name.lower():
                return item
        return None

    @classmethod
    def safe_insert(cls, name: str, colour_code: str):
        return cls.get(name=name) or cls(name=name, colour_code=colour_code)


class CatanEvent(db.Entity):
    name = Required(str)
    start_datetime = Required(datetime)
    end_datetime = Required(datetime)
    event_type = Required(CatanEventType)
    all_day = Optional(bool, default=False, sql_default=False)

    PrimaryKey(name, start_datetime)

    @classmethod
    def safe_insert(cls, name: str, start_datetime: datetime, end_datetime: datetime, event_type: CatanEventType,
                    all_day: bool = False):
        return cls.get(name=name, start_datetime=start_datetime) or cls(name=name, start_datetime=start_datetime,
                                                                        end_datetime=end_datetime,
                                                                        event_type=event_type, all_day=all_day)
