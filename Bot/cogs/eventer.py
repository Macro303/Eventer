import logging
from datetime import datetime

from discord import Embed
from discord.ext import commands
from discord.member import Member
from pony.orm import db_session
from pytz import timezone

from Bot import load_colour, insert_calendar_event
from Database import Attendee, EventType, Event

LOGGER = logging.getLogger(__name__)


def generate_embed(event: Event, author: Member) -> Embed:
    embed = Embed(title=event.name, colour=load_colour(event.event_type.colour_code))

    embed.add_field(name='Game', value=event.game)
    embed.add_field(name='Type', value=event.event_type.name)
    if event.all_day:
        if event.start_datetime.date() == event.end_datetime.date():
            embed.add_field(name='Date', value=event.start_datetime.date().strftime('%d %b'))
        else:
            embed.add_field(name='Start Date', value=event.start_datetime.date().strftime('%d %b'))
            embed.add_field(name='End Date', value=event.start_datetime.date().strftime('%d %b'))
    else:
        if event.start_datetime == event.end_datetime:
            embed.add_field(name='Time', value=event.start_datetime.strftime('%d %b %H:%M'))
        else:
            embed.add_field(name='Start Time', value=event.start_datetime.strftime('%d %b %H:%M'))
            embed.add_field(name='End Time', value=event.end_datetime.strftime('%d %b %H:%M'))

    embed.set_footer(text=f"Requested by {author.name}", icon_url=author.avatar_url)
    return embed


class EventerCog(commands.Cog, name='Eventer Commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name='Types',
        aliases=['Type'],
        pass_context=True,
        invoke_without_command=True,
        case_insensitive=True,
        usage='<Username|str>'
    )
    async def type_group(self, ctx, username: str):
        with db_session:
            result = Attendee.get(username=username)
            if result:
                result_str = '\n'.join(sorted(result.event_types, key=lambda x: x.name))
                await ctx.send(f'**{username}\'s Event Types:**\n```{result_str}```')
                await ctx.message.delete()
            else:
                LOGGER.warning(f"Unable to find `{username}`")
                await ctx.message.add_reaction('❎')

    @type_group.command(
        name='Create',
        pass_context=True,
        usage='<Name|str> <Colour Code|str=000000>'
    )
    async def create_type(self, ctx, name: str, colour_code: str = '000000'):
        with db_session:
            event_type = EventType.safe_insert(name, colour_code)
            await ctx.message.add_reaction('✅')

    @type_group.command(
        name='List',
        pass_context=True,
        usage=''
    )
    async def list_types(self, ctx):
        with db_session:
            results = EventType.select()[:]
            if results:
                result_str = '\n'.join(sorted(results, key=lambda x: x.name))
                await ctx.send(f'**Event Types:**\n```{result_str}```')
                await ctx.message.delete()
            else:
                LOGGER.warning('No `EventType`s found')
                await ctx.message.add_reaction('❎')

    @commands.group(
        name='Attendee',
        pass_context=True,
        invoke_without_command=True,
        case_insensitive=True,
        usage=None,
        hidden=True
    )
    async def attendee_group(self, ctx):
        pass

    @attendee_group.command(
        name='Create',
        pass_context=True,
        usage='<Username|str> <Email|str>'
    )
    async def create_attendee(self, ctx, username: str, email: str):
        with db_session:
            attendee = Attendee.safe_insert(username=username, email=email)
            await ctx.message.add_reaction('✅')

    @attendee_group.command(
        name='Edit',
        pass_context=True,
        usage='<Username|str> [<Type|str>]'
    )
    async def edit_attendee(self, ctx, username: str, *type_names: str):
        with db_session:
            attendee = Attendee.get(username=username)
            if attendee:
                for type_name in type_names:
                    event_type = EventType.get(name=type_name)
                    if event_type:
                        if event_type in attendee.event_types:
                            attendee.event_types.remove(event_type)
                        else:
                            attendee.event_types.add(event_type)
                        await ctx.message.add_reaction('✅')
                    else:
                        LOGGER.warning(f"Unable to find: {type_name}")
                        await ctx.message.add_reaction('❎')
            else:
                LOGGER.warning(f"Unable to find: {username}")
                await ctx.message.add_reaction('❎')

    @attendee_group.command(
        name='Remove',
        pass_context=True,
        usage='<Username|str>'
    )
    async def remove_attendee(self, ctx, username: str):
        with db_session:
            attendee = Attendee.get(username=username)
            if attendee:
                attendee.delete()
            await ctx.message.add_reaction('✅')

    @commands.group(
        name='Events',
        aliases=['Event'],
        pass_context=True,
        invoke_without_command=True,
        case_insensitive=True,
        usage='<Username|str>'
    )
    async def event_group(self, ctx, username: str):
        with db_session:
            attendee = Attendee.get(username=username)
            if attendee:
                events = Event.select()[:]
                if events:
                    for event in sorted(events, key=lambda x: (x.start_datetime, x.name)):
                        if event.event_type in attendee.event_types:
                            await ctx.send(embed=generate_embed(event, ctx.author))
                else:
                    LOGGER.warning('No events found')
                    await ctx.message.add_reaction('❎')
            else:
                LOGGER.warning(f"Unable to find: {username}")
                await ctx.message.add_reaction('❎')

    @event_group.command(
        name='List',
        pass_context=True,
        usage='<Type|str>'
    )
    async def list_events(self, ctx, type_name: str):
        with db_session:
            event_type = EventType.get(name=type_name)
            if event_type:
                if event_type.events:
                    for event in sorted(event_type.events, key=lambda x: (x.start_datetime, x.name)):
                        await ctx.send(embed=generate_embed(event, ctx.author))
                else:
                    LOGGER.warning('No events found')
                    await ctx.message.add_reaction('❎')
            else:
                LOGGER.warning(f"Unable to find: {type_name}")
                await ctx.message.add_reaction('❎')

    @event_group.command(
        name='Create',
        pass_context=True,
        usage='<Name|str> <Game|str> <Type|str> <Start Datetime|str> <End Datetime|str> <Is Local Timezone|bool=False> <All Day|bool=False>',
        hidden=True
    )
    async def create_event(self, ctx, name: str, game: str, type_name: str, start_time: str, end_time: str,
                           local_timezone: bool = False, all_day: bool = False):
        with db_session:
            event = Event.get(name=name)
            if event:
                LOGGER.warning(f"{name} already exists")
                await ctx.message.add_reaction('❎')
            else:
                event_type = EventType.get(name=type_name)
                if event_type:
                    try:
                        start_datetime = datetime.strptime(start_time, '%y-%m-%d %H:%M')
                        end_datetime = datetime.strptime(end_time, '%y-%m-%d %H:%M')
                        if not local_timezone:
                            start_datetime = datetime.strptime(
                                timezone('America/Los_Angeles').localize(start_datetime).astimezone(
                                    timezone('Pacific/Auckland')).strftime('%y-%m-%d %H:%M'), '%y-%m-%d %H:%M')
                            end_datetime = datetime.strptime(
                                timezone('America/Los_Angeles').localize(end_datetime).astimezone(
                                    timezone('Pacific/Auckland')).strftime('%y-%m-%d %H:%M'), '%y-%m-%d %H:%M')
                        event = Event.safe_insert(name, start_datetime, end_datetime, event_type, all_day=all_day,
                                                  game=game or None)
                        create_google_event(event)
                        await ctx.send(embed=generate_embed(event, ctx.author))
                        await ctx.message.delete()
                    except ValueError:
                        LOGGER.warning(f"Unable to parse datetimes: {start_time} - {end_time}")
                        await ctx.message.add_reaction('❎')
                else:
                    LOGGER.warning(f"Unable to find: {type_name}")
                    await ctx.message.add_reaction('❎')


def setup(bot):
    bot.add_cog(EventerCog(bot))


def create_google_event(event: Event):
    event_json = {
        'summary': event.name,
        'start': {
            'timeZone': 'Pacific/Auckland'
        },
        'end': {
            'timeZone': 'Pacific/Auckland'
        },
        'attendees': [x.event_dict() for x in Attendee.select(lambda x: event.event_type in x.event_types)],
        'reminders': {
            'useDefault': False,
            'overrides': []
        },
        'guestsCanSeeOtherGuests': False,
        'guestsCanModify': False,
        'transparency': 'transparent'
    }
    if event.all_day:
        event_json['start']['date'] = event.start_datetime.date().strftime('%Y-%m-%d')
        event_json['end']['date'] = event.end_datetime.date().strftime('%Y-%m-%d')
        event_json['reminders']['overrides'].append({'method': 'popup', 'minutes': 3 * 60})
        event_json['reminders']['overrides'].append({'method': 'popup', 'minutes': 15 * 60})
    else:
        event_json['start']['dateTime'] = event.start_datetime.strftime('%Y-%m-%dT%H:%M:%S')
        event_json['end']['dateTime'] = event.end_datetime.strftime('%Y-%m-%dT%H:%M:%S')
        event_json['reminders']['overrides'].append({'method': 'popup', 'minutes': 2 * 60})
        event_json['reminders']['overrides'].append({'method': 'popup', 'minutes': 24 * 60})

    insert_calendar_event(event_json)
