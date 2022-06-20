# nashbot.py


import os
import random
import asyncio
import discord
import youtube_dl
from dotenv import load_dotenv
from discord.ext import commands
from quotes import *
from settings import *


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='', intents=discord.Intents.default())


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


async def read_quote(ctx, quote) :
    if isinstance(quote, tuple):
        for line in quote:
            await ctx.send(line)
            await asyncio.sleep(1)
    else:
        await ctx.send(quote)


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


@bot.command(name='playmusic', help='tell the bot play music from a youtube link')
async def playmusic(ctx, url: str):
    if ctx.author.voice is None:
        await read_quote(ctx, 'join a voice channel 1st bro, i need an audience 4 this kinda thing yk ;)')
        return

    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()
    else:
        await ctx.voice_client.move_to(ctx.author.voice.channel)

    with youtube_dl.YoutubeDL(YDL_OPTS) as ydl:
        info = ydl.extract_info(url, download=False)
        source = await discord.FFmpegOpusAudio.from_probe(info['formats'][0]['url'], **FFMPEG_OPTS)
        ctx.voice_client.play(source)
        await read_quote(ctx, f':musical_note:  now playing: "{info["title"]}" :musical_note:')


@bot.command(name='stopmusic', help='tell the bot to stop playing music')
async def stopmusic(ctx):
    if ctx.voice_client is None:
        await read_quote(ctx, random.choice(await get_no_music_quotes(ctx)))
    else:
        await read_quote(ctx, random.choice(await get_endmusic_quotes(ctx)))
        await read_quote(ctx, ':no_entry_sign: music stopped :no_entry_sign:')
        await ctx.voice_client.disconnect()


@bot.command(name='pausemusic', help='tell the bot to pause or unpause music')
async def pause(ctx):
    if ctx.voice_client is None:
        await read_quote(ctx, random.choice(await get_no_music_quotes(ctx)))
    elif ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await read_quote(ctx, ':pause_button: music paused :pause_button:')
    elif ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await read_quote(ctx, ':arrow_forward: music unpaused :arrow_forward:')

bot.run(TOKEN)