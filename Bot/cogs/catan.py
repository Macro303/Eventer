import logging
from datetime import datetime

from discord import Embed
from discord.ext import commands
from discord.member import Member
from pony.orm import db_session
from pytz import timezone

from Bot import load_colour, insert_calendar_event
from Database import Catan, CatanEventType, CatanEvent

LOGGER = logging.getLogger(__name__)


def generate_embed(event: CatanEvent, author: Member) -> Embed:
    embed = Embed(title=event.name, colour=load_colour(event.event_type.colour_code))

    embed.add_field(name='Game', value='Catan: World Explorers')
    embed.add_field(name='Type', value=event.event_type.name.replace('_', ' ').title())
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


class CatanCog(commands.Cog, name='Catan: World Explorers Commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name='Catan',
        aliases=['WorldExplorers', 'WE'],
        pass_context=True,
        invoke_without_command=True,
        case_insensitive=True,
        usage='<Username|str>'
    )
    async def catan_group(self, ctx, username: str):
        with db_session:
            result = Catan.get(username=username)
            if result and result.event_types:
                await ctx.send(f"{username} is following: " + ', '.join([x.name for x in result.event_types]))
                await ctx.message.delete()
            elif result:
                await ctx.send(f"{username} is not following any events")
                await ctx.message.delete()
            else:
                await ctx.message.add_reaction('❎')

    @catan_group.command(
        name='Join',
        pass_context=True,
        usage='<Username|str> <Email|str>'
    )
    async def join(self, ctx, username: str, email: str):
        with db_session:
            Catan.safe_insert(username, email)
            await ctx.message.add_reaction('✅')

    @catan_group.command(
        name='Leave',
        pass_context=True,
        usage='<Username|str>'
    )
    async def leave(self, ctx, username: str):
        with db_session:
            result = Catan.get(username=username)
            if result:
                result.delete()
            await ctx.message.add_reaction('✅')

    @catan_group.command(
        name='Edit',
        pass_context=True,
        usage='<Username|str> [<Type|str>]'
    )
    async def edit_types(self, ctx, username: str, *type_names: str):
        with db_session:
            user = Catan.get(username=username)
            if user:
                for type_name in type_names:
                    event_type = CatanEventType.find(name=type_name)
                    if event_type:
                        if event_type in user.event_types:
                            user.event_types.remove(event_type)
                        else:
                            user.event_types.add(event_type)
                        await ctx.message.add_reaction('✅')
                    else:
                        LOGGER.warning(f"Unable to find: {type_name}")
                        await ctx.message.add_reaction('❎')
            else:
                LOGGER.warning(f"Unable to find: {username}")
                await ctx.message.add_reaction('❎')

    @catan_group.group(
        name='Events',
        aliases=['Event'],
        pass_context=True,
        invoke_without_command=True,
        case_insensitive=True,
        usage=''
    )
    async def event_group(self, ctx):
        with db_session:
            results = CatanEvent.select()[:]
            if results:
                for event in results:
                    await ctx.send(embed=generate_embed(event, ctx.author))
                await ctx.message.delete()
            else:
                LOGGER.warning('No events found')
                await ctx.message.add_reaction('❎')

    @event_group.command(
        name='Types',
        pass_context=True,
        usage=''
    )
    async def event_type_list(self, ctx):
        with db_session:
            await ctx.send(', '.join([x.name for x in CatanEventType.select()[:]]))
            await ctx.message.delete()

    @event_group.command(
        name='Create',
        pass_context=True,
        usage='<Name|str> <Start Time|str> <End Date|str> <Type|str> <Is Local Timezone|bool=False> <All Day|bool=False>',
        hidden=True
    )
    async def create_event(self, ctx, name: str, start_time: str, end_time: str, type_name: str,
                           local_timezone: bool = False, all_day: bool = False):
        with db_session:
            event = CatanEvent.get(name=name)
            if event:
                LOGGER.warning(f"{name} already exists")
                await ctx.message.add_reaction('❎')
            else:
                event_type = CatanEventType.find(type_name)
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
                        event = CatanEvent.safe_insert(name, start_datetime, end_datetime, event_type, all_day=all_day)
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
    bot.add_cog(CatanCog(bot))


def create_google_event(event: CatanEvent):
    event_json = {
        'summary': event.name,
        'start': {
            'timeZone': 'Pacific/Auckland'
        },
        'end': {
            'timeZone': 'Pacific/Auckland'
        },
        'attendees': [x.event_dict() for x in CatanEvent.select(lambda x: event.event_type in x.event_types)],
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

    insert_calendar_event('Pokemon Go', event_json)
