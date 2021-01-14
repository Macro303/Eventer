import logging
from enum import Enum, auto

from pony.orm import Database, PrimaryKey, Required, Optional

LOGGER = logging.getLogger(__name__)
db = Database()


class User(db.Entity):
    username = PrimaryKey(str)
    email = Required(str, unique=True)

    # Reverse columns
    pokemon_go = Optional('PokemonGo')
    wizards_unite = Optional('WizardsUnite')
    world_explorers = Optional('WorldExplorers')

    @classmethod
    def safe_insert(cls, username: str, email: str):
        return cls.get(username=username, email=email) or cls(username=username, email=email)


class EventType(Enum):
    GENERAL_EVENT = auto(), 'FF0000'
    GO_BATTLE_LEAGUE = auto(), 'FF0000'
    RAID_BATTLE = auto(), 'FF0000'
    GIOVANNI = auto(), 'FF0000'
    RESEARCH_BREAKTHROUGH = auto(), 'FF0000'
    COMMUNITY_DAY = auto(), 'FF0000'
    RAID_HOUR = auto(), 'FF0000'
    SPOTLIGHT_HOUR = auto(), 'FF0000'
    PAID_EVENT = auto(), 'FF0000'

    @classmethod
    def find(cls, name: str):
        for value, entry in cls.__members__.items():
            if name.lower() == value.lower().replace('_', ' '):
                return entry
        return None

    def __new__(cls, value, colour_code):
        entry = object.__new__(cls)
        entry._value_ = value
        entry.colour_code = colour_code
        return entry


class PokemonGo(db.Entity):
    user = PrimaryKey(User)
    general_event = Required(bool, default=False, sql_default=False)
    go_battle_league = Required(bool, default=False, sql_default=False)
    raid_battle = Required(bool, default=False, sql_default=False)
    giovanni = Required(bool, default=False, sql_default=False)
    research_breakthrough = Required(bool, default=False, sql_default=False)
    community_day = Required(bool, default=False, sql_default=False)
    raid_hour = Required(bool, default=False, sql_default=False)
    spotlight_hour = Required(bool, default=False, sql_default=False)
    paid_event = Required(bool, default=False, sql_default=False)

    @classmethod
    def safe_insert(cls, user: User, general_event: bool = False, go_battle_league: bool = False,
                    raid_battle: bool = False, giovanni: bool = False, research_breakthrough: bool = False,
                    community_day: bool = False, raid_hour: bool = False, spotlight_hour: bool = False,
                    paid_event: bool = False):
        return cls.get(user=user) or cls(user=user, general_event=general_event, go_battle_league=go_battle_league,
                                         raid_battle=raid_battle, giovanni=giovanni,
                                         research_breakthrough=research_breakthrough, community_day=community_day,
                                         raid_hour=raid_hour, spotlight_hour=spotlight_hour, paid_event=paid_event)


class WizardsUnite(db.Entity):
    user = PrimaryKey(User)
    general_event = Required(bool, default=False, sql_default=False)

    @classmethod
    def safe_insert(cls, user: User, general_event: bool = False):
        return cls.get(user=user) or cls(user=user, general_event=general_event)


class WorldExplorers(db.Entity):
    user = PrimaryKey(User)
    general_event = Required(bool, default=False, sql_default=False)

    @classmethod
    def safe_insert(cls, user: User, general_event: bool = False):
        return cls.get(user=user) or cls(user=user, general_event=general_event)
