# cog_music.py


import random
import asyncio
import discord
import youtube_dl
from discord.ext import commands
from quotes import *
from settings import *


class Music(commands.Cog, name='music'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='playmusic', help='tell the bot play music from a youtube link')
    async def playmusic(self, ctx, url: str):
        if ctx.author.voice is None:
            await read_quote(ctx, 'TODO join a voice channel 1st bro, i need an audience 4 this kinda thing yk ;)')
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

    @commands.command(name='stopmusic', help='tell the bot to stop playing music')
    async def stopmusic(self, ctx):
        if ctx.voice_client is None:
            await read_quote(ctx, random.choice(await get_no_music_quotes(ctx)))
        else:
            await read_quote(ctx, random.choice(await get_endmusic_quotes(ctx)))
            await read_quote(ctx, ':no_entry_sign: music stopped :no_entry_sign:')
            await ctx.voice_client.disconnect()

    @commands.command(name='pausemusic', help='tell the bot to pause or unpause music')
    async def pause(self, ctx):
        if ctx.voice_client is None:
            await read_quote(ctx, random.choice(await get_no_music_quotes(ctx)))
        elif ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await read_quote(ctx, ':pause_button: music paused :pause_button:')
        elif ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await read_quote(ctx, ':arrow_forward: music unpaused :arrow_forward:')


def setup(bot):
    bot.add_cog(Music(bot))
