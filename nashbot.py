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
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to discord')


@bot.event
async def on_disconnect():
    print(f'{bot.user.name} has disconnected from discord')


async def read_quote(ctx, quote) :
    if isinstance(quote, tuple):
        for line in quote:
            await ctx.send(line)
            await asyncio.sleep(1)
    else:
        await ctx.send(quote)


@bot.command(name='hi', help='greet the bot')
async def hi(ctx):
    quotes = await get_hi_quotes(ctx)
    await read_quote(ctx, random.choice(quotes))


@bot.command(name='highfive', help='ask the bot to give u a high five')
async def highfive(ctx):
    quotes = await get_highfive_quotes(ctx)
    await read_quote(ctx, random.choice(quotes))


@bot.command(name='shutdown', help='shut down the bot')
async def shutdown(ctx):
    quotes = await get_shutdown_quotes(ctx)
    await read_quote(ctx, (random.choice(quotes), ':zzz: ...shutting down... :zzz:'))
    await bot.close()


@bot.command(name='joke', help='ask the bot to tell u a joke')
async def joke(ctx):
    quotes = await get_joke_quotes(ctx)
    await read_quote(ctx, random.choice(quotes))


@bot.command(name='kkjoke', help='ask the bot to tell u a knock knock joke')
async def kkjoke(ctx):
    quotes = await get_kkjoke_quotes(ctx)
    quotes = random.choice(quotes)

    def check(m):
        return m.channel == ctx.channel and m.author == ctx.message.author

    await read_quote(ctx, 'knock knock')
    while True:
        m = await bot.wait_for("message", check=check)
        content = m.content.lower().strip().replace('?', '')
        if content in step_1_expected:
            break
        elif content in cancel_responses:
            await read_quote(ctx, random.choice(cancel_quotes))
            break
        else:
            await read_quote(ctx, random.choice(await get_unexpected_quotes('whos there')))

    await read_quote(ctx, quotes[0])
    while True:
        m = await bot.wait_for("message", check=check)
        content = m.content.lower().strip().replace('?', '')
        expected = quotes[0] + ' who'
        if content == expected:
            break
        elif content in cancel_responses:
            await read_quote(ctx, random.choice(cancel_quotes))
            break
        else:
            await read_quote(ctx, random.choice(await get_unexpected_quotes(expected)))

    await read_quote(ctx, quotes[1:])


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        f.write(f'Unhandled error: {args[0]}\n\n')

bot.run(TOKEN)