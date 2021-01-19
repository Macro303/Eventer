import logging

import discord
from aiohttp.client_exceptions import ClientConnectorError
from discord.ext import commands

from Bot import CONFIG
from Database import initialize_enums
from Logger import init_logger

LOGGER = logging.getLogger(__name__)
COGS = ['Bot.cogs.pokemon_go', 'Bot.cogs.wizards_unite', 'Bot.cogs.catan', 'Bot.cogs.other']
bot = commands.Bot(command_prefix=CONFIG['Prefix'], case_insensitive=True)


@bot.event
async def on_ready():
    LOGGER.info(f"Logged in as: {bot.user}")
    bot.remove_command('Help')
    for cog in COGS:
        bot.load_extension(cog)
    await bot.change_presence(activity=discord.Game(name='with the Calendar'))
    initialize_enums()


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)


if __name__ == "__main__":
    init_logger('Eventer-Bot')
    try:
        if CONFIG['Token']:
            bot.run(CONFIG['Token'], bot=True, reconnect=True)
        else:
            LOGGER.critical('Missing your Discord `Token`, update the config.yaml to continue')
    except ClientConnectorError:
        LOGGER.critical('Unable to access Discord')
