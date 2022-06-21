# cog_music.py


import random
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from quotes import *


FFMPEG_OPTS = { 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn', }
YDL_OPTS = {'format': 'bestaudio', }


class Music(commands.Cog, name='music'):

    def __init__(self, bot):
        self.bot = bot
        self.ydl = YoutubeDL(YDL_OPTS)
        self.queue_sources = asyncio.Queue()
        self.queue_titles = []
        self.next = asyncio.Event()
        self.nowplaying = ''
        self.looping = False

    async def end_music(self, ctx):
        ctx.voice_client.stop()
        self.queue_sources = asyncio.Queue()
        self.queue_titles = []
        self.next = asyncio.Event()
        self.nowplaying = ''
        self.looping = False
        await ctx.voice_client.disconnect()

    async def music_loop(self, ctx):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.looping = True
            self.next.clear()
            try:
                source = self.queue_sources.get_nowait()
            except asyncio.QueueEmpty:
                self.looping = False
                await self.end_music(ctx)
                await read_quote(ctx, ':x: end of music queue :x:')
                break
            ctx.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.nowplaying = self.queue_titles.pop(0)
            await read_quote(ctx, f':musical_note:  now playing: "{self.nowplaying}" :musical_note:')
            await self.next.wait()
            self.nowplaying = ''

    @commands.command(name='play', help='tell the bot play music from youtube')
    async def play(self, ctx,  *, search: str):
        await ctx.trigger_typing()
        if not ctx.author.voice:
            await read_quote(ctx, 'TODO join a voice channel 1st bro, i need an audience 4 this kinda thing yk ;)')
            return
        elif not ctx.voice_client:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.voice_client.move_to(ctx.author.voice.channel)
        info = self.ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
        await self.queue_sources.put(await discord.FFmpegOpusAudio.from_probe(info['formats'][0]['url'], **FFMPEG_OPTS))
        self.queue_titles.append(info['title'])
        await read_quote(ctx, f':white_check_mark: added to music queue: "{info["title"]}" :white_check_mark: ')
        if not self.looping:
            await self.music_loop(ctx)

    @commands.command(name='clearmusic', help='tell the bot to clear the music queue')
    async def clearmusic(self, ctx):
        if not ctx.voice_client:
            await read_quote(ctx, random.choice(await get_no_music_quotes(ctx)))
        else:
            await self.end_music(ctx)
            await read_quote(ctx, ':x: music queue cleared :x:')

    @commands.command(name='pause', help='tell the bot to pause or unpause music')
    async def pause(self, ctx):
        if not ctx.voice_client:
            await read_quote(ctx, random.choice(await get_no_music_quotes(ctx)))
        elif ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await read_quote(ctx, f':pause_button: paused music: "{self.nowplaying}" :pause_button:')
        elif ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await read_quote(ctx, f':arrow_forward: unpaused music: "{self.nowplaying}" :arrow_forward:')

    @commands.command(name='skip', help='tell the bot to skip the current song')
    async def skip(self, ctx):
        if not ctx.voice_client:
            await read_quote(ctx, random.choice(await get_no_music_quotes(ctx)))
        else:
            ctx.voice_client.stop()
            await read_quote(ctx, f':track_next: skipped: "{self.nowplaying}" :track_next: ')

    @commands.command(name='showmusic', help='ask the bot to read out the current music queue')
    async def showmusic(self, ctx):
        if self.nowplaying:
            await read_quote(ctx, ('music queue:', f'> :musical_note: "{self.nowplaying}" :musical_note:'))
            for item in self.queue_titles:
                await read_quote(ctx, f'> "{item}"')
        else:
            await read_quote(ctx, 'TODO queue empty')

def setup(bot):
    bot.add_cog(Music(bot))
