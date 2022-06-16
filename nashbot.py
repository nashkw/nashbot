# nashbot.py
import asyncio
import os
import discord
from dotenv import load_dotenv
import random
from discord.ext import commands
from quotes import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='')
client = discord.Client()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to discord')


@bot.event
async def on_disconnect():
    print(f'{bot.user.name} has disconnected from discord')


@bot.command(name='hi', help='greet the bot')
async def hi(ctx):
    quotes = await get_hi_quotes(ctx)
    await ctx.send(random.choice(quotes))


@bot.command(name='highfive', help='ask the bot to give u a high five')
async def highfive(ctx):
    quotes = await get_highfive_quotes(ctx)
    await ctx.send(random.choice(quotes))


@bot.command(name='shutdown', help='shut down the bot')
async def shutdown(ctx):
    quotes = await get_shutdown_quotes(ctx)
    await ctx.send(random.choice(quotes))
    await asyncio.sleep(1)
    await ctx.send(':zzz: ...shutting down... :zzz:')
    await bot.close()


@bot.command(name='joke', help='ask the bot to tell u a joke')
async def joke(ctx):
    quotes = await get_joke_quotes(ctx)
    response = random.choice(quotes)
    await ctx.send(response[0])
    await asyncio.sleep(1)
    await ctx.send(response[1])


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n\n')
        else:
            raise

bot.run(TOKEN)