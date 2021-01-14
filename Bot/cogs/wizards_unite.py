import logging
from typing import Dict, Any

from discord import Embed
from discord.ext import commands
from discord.member import Member
from pony.orm import db_session

from Bot import load_colour
from Database import User, EventType, WizardsUnite

LOGGER = logging.getLogger(__name__)


def generate_embed(event: Dict[str, Any], author: Member) -> Embed:
    embed = Embed(title=event['Name'], colour=load_colour(event['Type']))

    embed.add_field(name='Game', value=event['Game'])
    embed.add_field(name='Type', value=event['Type'])
    embed.add_field(name='Start Date', value=event['Start Date'])
    embed.add_field(name='End Date', value=event['End Date'])

    embed.set_footer(text=f"Requested by {author.name}", icon_url=author.avatar_url)
    return embed


class WizardsUniteCog(commands.Cog, name='Wizard\'s Unite Commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(
        name='WizardsUnite',
        aliases=['WU'],
        pass_context=True,
        invoke_without_command=True,
        case_insensitive=True,
        hidden=True
    )
    async def wizards_group(self, ctx):
        pass

    @wizards_group.command(
        name='Join',
        pass_context=True,
        usage='<Username|str> <Email|str>'
    )
    async def join(self, ctx, username: str, email: str):
        with db_session:
            User.safe_insert(username, email)
            await ctx.message.add_reaction('\N{THUMBS UP SIGN}')

    @wizards_group.command(
        name='Leave',
        pass_context=True,
        usage='<Username|str>'
    )
    async def leave(self, ctx, username: str):
        result = User.get(username=username)
        if result:
            result.delete()
        await ctx.message.add_reaction('\N{THUMBS UP SIGN}')

    @wizards_group.command(
        name='Edit',
        pass_context=True,
        usage='<Username|str> [<Type|str>]'
    )
    async def config_group(self, ctx, username: str, *type_names: str):
        with db_session:
            user = User.get(username=username)
            if user:
                for type_name in type_names:
                    event_type = EventType.find(type_name)
                    if event_type:
                        entry = WizardsUnite.safe_insert(user)
                        pre = (entry.__dict__.items()[event_type.name.lower()]) is bool
                        entry.__dict__.items()[event_type.name.lower()] = not pre
                    else:
                        LOGGER.warning(f"Unable to find: {type_name}")
            else:
                await ctx.message.add_reaction('\N{THUMBS DOWN SIGN}')


def setup(bot):
    bot.add_cog(WizardsUniteCog(bot))
