#!/usr/bin/env python3
import logging
from typing import Optional

from discord import Embed, Member
from discord.ext import commands

import Calendar
from Data import clean_filename
from Data.wizards_unite import Event, EventType, GAME_TITLE

LOGGER = logging.getLogger(__name__)


def event_embed(item: Event, author_name: str, author_icon_url: str) -> Embed:
    description = item.description() \
        .replace("<b>", "**").replace("</b>", "**").replace("<u>", "__").replace("</u>", "__")
    embed = Embed(
        title=item.name + " Created",
        description=f"```{description}```" if description else None
    )

    folder_name = clean_filename(GAME_TITLE).replace(' ', '%20')
    embed.set_author(name=GAME_TITLE,
                     icon_url=f"https://raw.githubusercontent.com/Macro303/Eventer/main/Events/{folder_name}/logo.jpg")

    embed.add_field(name="Type", value=item.event_type.name)
    if item.all_day:
        embed.add_field(name="Start Date", value=item.start_date_str())
        embed.add_field(name="End Date", value=item.end_date_str())
    else:
        embed.add_field(name="Start Date", value=item.start_time_str)
        embed.add_field(name="End Date", value=item.end_time_str)
    embed.add_field(name="Timezone", value=item.time_zone)

    embed.set_footer(text=f"Requested by {author_name}", icon_url=author_icon_url)
    return embed


class WizardsCog(commands.Cog, name=f"{GAME_TITLE} Eventer"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Wizards-Create',
        description='Creates Events',
        usage='[Name] [Type] [Start Time] [End Time] [Pages _Split by ","_] [Foundables _Split by ","_] '
              '[Event Foundables _Not Implemented_] [Bonuses _Split by ","_] (Family|None) (Uses Local Time|False) '
              '(All Day Event|False)'
    )
    async def create_event(self, ctx, name: str, type_str: str, start_time: str, end_time: str, pages: str,
                           foundables: str, event_foundables: str, bonuses: str, family: Optional[str] = None,
                           local_time: bool = False, all_day: bool = False):
        LOGGER.info(f"Creating {GAME_TITLE} event request received")

        event = Event(
            name=name,
            event_type=EventType[type_str.upper()],
            start_time=start_time,
            end_time=end_time,
            time_zone=None if local_time else 'America/Los_Angeles',
            all_day=all_day,
            family=family,
            pages=list(filter(None, [x.strip() for x in pages.split(",")])),
            foundables=list(filter(None, [x.strip() for x in foundables.split(",")])),
            event_foundables=None,
            bonuses=list(filter(None, [x.strip() for x in bonuses.split(",")]))
        )
        event.save()

        await ctx.send(embed=event_embed(
            item=event,
            author_name=ctx.message.author.name,
            author_icon_url=ctx.message.author.avatar_url
        ))
        await ctx.message.delete()
        LOGGER.info(f"Creating {GAME_TITLE} event request fulfilled")

    @commands.command(
        name='Wizards-Error',
        description='Logs error message with Event',
        usage='[Name] [Error Description]'
    )
    async def event_error(self, ctx, name: str, description: str):
        LOGGER.info(f"{GAME_TITLE} error request received")
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
        LOGGER.info(f"{GAME_TITLE} error request fulfilled")

    @commands.command(
        name='Wizards-Types',
        description='Lists Event Types',
        usage=''
    )
    async def list_types(self, ctx):
        LOGGER.info(f"{GAME_TITLE} type list request received")
        event_str = '\n'.join([x for x in EventType.__members__.keys()])

        await ctx.send(f"**{GAME_TITLE}** Event Types:```\n{event_str}```")
        await ctx.message.delete()
        LOGGER.info(f"{GAME_TITLE} type list request fulfilled")

    @commands.command(
        name='Wizards-Leave',
        description='Marks user on event exception list',
        usage='(Member|None)'
    )
    async def leave_event(self, ctx, member: Member = None):
        LOGGER.info(f"{GAME_TITLE} ignore request received")
        member = member or ctx.author
        Calendar.CONFIG[GAME_TITLE]['Ignored'] = list({member.name, *Calendar.CONFIG[GAME_TITLE]['Ignored']})
        Calendar.save_config()
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
        LOGGER.info(f"{GAME_TITLE} ignore request fulfilled")


def setup(bot):
    bot.add_cog(WizardsCog(bot))
