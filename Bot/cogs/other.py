import logging

from discord import Embed
from discord.ext import commands
from discord.ext.commands.core import Group

from Bot import CONFIG

LOGGER = logging.getLogger(__name__)


def get_comm_list(comm_list, public_list, private_list, prefix=CONFIG['Prefix']):
    for comm in sorted(comm_list, key=lambda x: x.name):
        names = [comm.name]
        if comm.alias:
            names.extend(comm.alias)
        for name in names:
            if comm.usage is not None:
                usage = f"{prefix}{name} {comm.usage}".strip()
                if comm.hidden:
                    private_list.append(f" - `{usage}`")
                else:
                    public_list.append(f" - `{usage}`")
            if isinstance(comm, Group):
                public_list, private_list = get_comm_list(comm.commands, public_list, private_list, f"{prefix}{name} ")
    return public_list, private_list


class OtherCog(commands.Cog, name='Other Commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='Help',
        description='The help command',
        usage=''
    )
    async def help_command(self, ctx):
        embed = Embed(
            title='Eventer Commands'
        )
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        public_list = []
        private_list = []
        other_list = []
        cogs = [c for c in self.bot.cogs.keys()]
        for cog in cogs:
            if cog == 'Other Commands':
                for comm in sorted(self.bot.get_cog(cog).get_commands(), key=lambda x: x.name):
                    names = [comm.name]
                    if comm.alias:
                        names.extend(comm.alias)
                    for name in names:
                        if comm.usage is not None:
                            usage = f"{CONFIG['Prefix']}{name} {comm.usage}".strip()
                            other_list.append(f" - `{usage}`")
            else:
                public_temp, private_temp = get_comm_list(self.bot.get_cog(cog).get_commands(), [], [])
                for item in public_temp:
                    public_list.append(item)
                for item in private_temp:
                    private_list.append(item)

        if public_list:
            embed.add_field(name='Public Commands', value='\n'.join(public_list), inline=False)
        if private_list and 'Moderator' in [x.name for x in ctx.author.roles]:
            embed.add_field(name='Private Commands', value='\n'.join(private_list), inline=False)
        if other_list:
            embed.add_field(name='Other Commands', value='\n'.join(other_list), inline=False)

        embed.set_footer(
            text=f"Requested by {ctx.author.name}",
            icon_url=ctx.author.avatar_url
        )
        await ctx.send(embed=embed)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(OtherCog(bot))
