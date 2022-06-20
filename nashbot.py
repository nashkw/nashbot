# nashbot.py


import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
import cog_jokes
import cog_music
from quotes import *


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='', intents=discord.Intents.default())

cogs = [cog_jokes, cog_music]
for cog in cogs:
    cog.setup(bot)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to discord')


@bot.event
async def on_disconnect():
    print(f'{bot.user.name} has disconnected from discord')


@bot.event
async def on_error(event, *args, **kwargs):
    print(f'logging error: {args[0]}\n')
    with open('err.log', 'a') as f:
        f.write(f'Unhandled error: {args[0]}\n\n')


@bot.command(name='hi', help='greet the bot')
async def hi(ctx):
    await read_quote(ctx, random.choice(await get_hi_quotes(ctx)))


@bot.command(name='highfive', help='ask the bot to give u a high five')
async def highfive(ctx):
    await read_quote(ctx, random.choice(await get_highfive_quotes(ctx)))


@bot.command(name='shutdown', help='shut down the bot')
async def shutdown(ctx):
    await read_quote(ctx, random.choice(await get_shutdown_quotes(ctx)))
    await read_quote(ctx, ':zzz: ...shutting down... :zzz:')
    await bot.close()


bot.run(TOKEN)