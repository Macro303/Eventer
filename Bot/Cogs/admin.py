#!/usr/bin/env python3
import logging
from datetime import datetime

from discord import Embed
from discord.ext import commands

from Bot import CONFIG
from Calendar import __main__ as calendar
from Data import pokemon_go, wizards_unite, catan_explorer, clean_filename
from Data.base_event import Event

LOGGER = logging.getLogger(__name__)


def event_embed(item: Event, author_name: str, author_icon_url: str, game_name: str) -> Embed:
    description = item.description() \
        .replace("<b>", "**").replace("</b>", "**").replace("<u>", "__").replace("</u>", "__")
    embed = Embed(
        title=item.name,
        description=f"```{description}```" if description else None
    )

    folder_name = clean_filename(game_name).replace(' ', '%20')
    embed.set_author(name=game_name,
                     icon_url=f"https://raw.githubusercontent.com/Macro303/Eventer/main/Events/{folder_name}/logo.jpg")

    embed.add_field(name="Type", value=item.event_type.name)
    embed.add_field(name="Start Date", value=item.start_time_str)
    embed.add_field(name="End Date", value=item.end_time_str)
    embed.add_field(name="Timezone", value=item.time_zone)

    embed.set_footer(text=f"Requested by {author_name}", icon_url=author_icon_url)
    return embed


class AdminCog(commands.Cog, name='Other Commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_role('Admin')
    @commands.command(
        name='Create',
        description='Creates the events in the appropriate Calendars',
        usage='(Create Pokemon Go|False) (Create Harry Potter: Wizards Unite|False) (Create Catan: Wizards Unite|False)'
    )
    async def create_events(self, ctx, pokemon: bool = False, wizards: bool = False, catan: bool = False):
        LOGGER.info('Create events request received')
        calendar.main(pokemon, wizards, catan, True)
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')
        LOGGER.info('Create events request fulfilled')

    @commands.command(
        name='Current',
        description='Lists all current events',
        usage=''
    )
    async def current_events(self, ctx):
        LOGGER.info('Current events request received')
        for game in [pokemon_go, wizards_unite, catan_explorer]:
            count = 0
            for event in sorted(game.EVENTS, key=lambda x: x.start_time()):
                start_dif = (event.start_time() - datetime.today()).days
                end_dif = (datetime.today() - event.end_time()).days
                if start_dif <= 0 and end_dif <= 0:
                    count += 1
                    await ctx.send(embed=event_embed(
                        item=event,
                        author_name=ctx.author.name,
                        author_icon_url=ctx.author.avatar_url,
                        game_name=game.GAME_TITLE
                    ))
            if count == 0:
                await ctx.send(f"No **{game.GAME_TITLE}** events currently active")
        await ctx.message.delete()
        LOGGER.info('Current events request fulfilled')

    @commands.command(
        name='Upcoming',
        description='Lists all upcoming events (Upcoming = next 7 days)',
        usage=''
    )
    async def upcoming_events(self, ctx):
        LOGGER.info('Upcoming events request received')
        for game in [pokemon_go, wizards_unite, catan_explorer]:
            count = 0
            for event in sorted(game.EVENTS, key=lambda x: x.start_time()):
                start_dif = (event.start_time() - datetime.today()).days
                if 7 >= start_dif >= 0:
                    count += 1
                    await ctx.send(embed=event_embed(
                        item=event,
                        author_name=ctx.author.name,
                        author_icon_url=ctx.author.avatar_url,
                        game_name=game.GAME_TITLE
                    ))
            if count == 0:
                await ctx.send(f"No **{game.GAME_TITLE}** events upcoming")
        await ctx.message.delete()
        LOGGER.info('Upcoming events request fulfilled')

    @commands.command(
        name='Help',
        description='The help command',
        usage=''
    )
    async def help_command(self, ctx):
        embed = Embed(title='Eventer Commands')
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        cogs = [c for c in self.bot.cogs.keys()]
        for cog in cogs:
            cog_commands = self.bot.get_cog(cog).get_commands()
            commands_list = []
            for comm in cog_commands:
                usage = f"{CONFIG['Prefix']}{comm.name} {comm.usage}".strip()
                commands_list.append(f"**{comm.name}** - `{usage}`\n*{comm.description}*")

            embed.add_field(name=cog, value='\n'.join(commands_list), inline=False)

        embed.set_footer(
            text=f"Requested by {ctx.message.author.name}",
            icon_url=ctx.message.author.avatar_url
        )
        await ctx.send(embed=embed)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(AdminCog(bot))
