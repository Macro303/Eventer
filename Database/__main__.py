import logging

from pony.orm import db_session, flush

from Database import EventType, User, PokemonGo, WizardsUnite, WorldExplorers
from Logger import init_logger

LOGGER = logging.getLogger(__name__)


def add_pokemon_event(user: User, type_name: str):
    event_type = EventType.find(type_name)
    if event_type and 'Pokemon Go' in event_type.games:
        entry = PokemonGo.safe_insert(user)
        event_dict = {
            'General Event': entry.general_event,
            'Community Day': entry.community_day
        }
        if event_dict.get(type_name, None):
            event_dict.get(type_name, None) = not event_dict.get(type_name, None)
        if found:
            found = not found
        flush()
    else:
        LOGGER.warning(f"Unable to find: {type_name}")


def add_wizards_event(user: User, type_name: str):
    event_type = EventType.find(type_name)
    if event_type:
        entry = WizardsUnite.safe_insert(user)
        pre = (entry.__dict__.items()[event_type.name.lower()]) is bool
        entry.__dict__.items()[event_type.name.lower()] = not pre


def add_catan_event(user: User, type_name: str):
    event_type = EventType.find(type_name)
    if event_type:
        entry = WorldExplorers.safe_insert(user)
        pre = (entry.__dict__.items()[event_type.name.lower()]) is bool
        entry.__dict__.items()[event_type.name.lower()] = not pre


def main():
    with db_session:
        # region Users
        user = User.safe_insert("Macro303", "Macro303@pm.me")

        flush()
        # endregion

        # region Events
        for event in ['General Event', 'Community Day']:
            add_pokemon_event(user, event)
        # PokemonGo.safe_insert(user, general_event=True, community_day=True)
        # WizardsUnite.safe_insert(user, general_event=True)
        # WorldExplorers.safe_insert(user)

        flush()
        # endregion

        User.select().show(width=175)
        PokemonGo.select().show(width=175)
        WizardsUnite.select().show(width=175)
        WorldExplorers.select().show(width=175)


if __name__ == "__main__":
    init_logger('Eventer-Database')
    main()
