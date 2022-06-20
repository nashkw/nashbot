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

cogs = [cog_music]
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


@bot.command(name='joke', help='ask the bot to tell u a joke')
async def joke(ctx):
    await read_quote(ctx, random.choice(await get_joke_quotes(ctx)))


@bot.command(name='kkjoke', help='ask the bot to tell u a knock knock joke')
async def kkjoke(ctx):
    quotes = random.choice(await get_kkjoke_quotes(ctx))

    def check(m):
        return m.channel == ctx.channel and m.author == ctx.message.author

    def clean_msg(m):
        return m.content.lower().replace('?', '').replace('...', '').replace(' :)', '').strip()

    async def wait_for_response(expected):
        while True:
            content = clean_msg(await bot.wait_for("message", check=check))
            if content in expected:
                return True  # successful progression
            elif content in welcome_responses:
                await read_quote(ctx, random.choice(welcome_quotes))
                await read_quote(ctx, ':no_entry_sign: joke cancelled :no_entry_sign:')
                return False  # cancel joke
            elif content in cancel_responses:
                if random.choice([True, False]):
                    await read_quote(ctx, random.choice(cancel_obedient))
                    await read_quote(ctx, ':no_entry_sign: joke cancelled :no_entry_sign:')
                    return False  # cancel joke
                else:
                    await read_quote(ctx, random.choice(cancel_disobedient))
                    await read_quote(ctx, f'{ctx.message.author.name}: {random.choice(expected)}?')
                    return True  # successful progression
            else:
                quotes_unexpected = await get_unexpected_quotes(random.choice(expected))
                await read_quote(ctx, random.choice(quotes_unexpected))

    await read_quote(ctx, 'knock knock')
    if not await wait_for_response(step_1_expected):
        return  # cancel joke
    await read_quote(ctx, quotes[0])
    if not await wait_for_response([quotes[0] + ' who', ]):
        return  # cancel joke
    await read_quote(ctx, quotes[1:])


bot.run(TOKEN)