# cog_music.py


import random
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from quotes import *


FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn', }
YDL_OPTS = {'format': 'bestaudio', 'noplaylist': True, }


class FailedSearch(commands.BadArgument):
    pass


class NotInVChannel(commands.BadArgument):
    pass


def is_v_client():
    def predicate(ctx):
        return ctx.voice_client
    return commands.check(predicate)


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
        self.looping = True
        while not self.bot.is_closed() and self.looping:
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
            await read_official(ctx, f'now playing: "{self.nowplaying}"', 'musical_note')
            await self.next.wait()
            self.nowplaying = ''

    @commands.command(name='play', help='play music from youtube')
    async def play(self, ctx, *, search: str):
        async with ctx.typing():
            if not ctx.author.voice:
                raise NotInVChannel

            info = self.ydl.extract_info(f"ytsearch:{search}", download=False)
            if not info['entries']:
                raise FailedSearch
            else:
                info = info['entries'][0]

            if not ctx.voice_client:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.voice_client.move_to(ctx.author.voice.channel)

            await self.queue_sources.put(await discord.FFmpegOpusAudio.from_probe(info['formats'][0]['url'], **FFMPEG_OPTS))
            self.queue_titles.append(info['title'])
        await read_official(ctx, f'added to music queue: "{info["title"]}"', 'white_check_mark')
        if not self.looping:
            await self.music_loop(ctx)

    @commands.command(name='togglepause', aliases=['unpause', 'pause'],
                      help='pause or unpause the currently playing song')
    @is_v_client()
    async def togglepause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await read_official(ctx, f'paused music: "{self.nowplaying}"', 'pause_button')
        elif ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await read_official(ctx, f'unpaused music: "{self.nowplaying}"', 'arrow_forward')

    @commands.command(name='skip', aliases=['nextsong', 'next', ],
                      help='skip the currently playing song')
    @is_v_client()
    async def skip(self, ctx):
        ctx.voice_client.stop()
        await read_official(ctx, f'skipped: "{self.nowplaying}"', 'track_next')

    @commands.command(name='dequeue', aliases=['queueremove', 'qremove', 'unqueue', 'dq', ],
                      help='remove a song from the music queue')
    @is_v_client()
    async def dequeue(self, ctx, index: int):
        if index == 0:
            ctx.voice_client.stop()
        elif 0 < index - 1 < len(self.queue_titles):
            newq = asyncio.Queue()
            i = 0
            while not self.queue_sources.empty():
                item = self.queue_sources.get_nowait()
                if i != index - 1:
                    newq.put_nowait(item)
                i = i + 1
            self.queue_sources = newq
            await read_official(ctx, f'removed from music queue: "{self.queue_titles.pop(index - 1)}"',
                                'negative_squared_cross_mark')
        else:
            raise IndexError

    @commands.command(name='clearqueue', aliases=['queueclear', 'qclear', 'clearq', ],
                      help='clear the music queue')
    @is_v_client()
    async def clearqueue(self, ctx):
        await self.end_music(ctx)
        await read_official(ctx, 'music queue cleared', 'x')

    @commands.command(name='showqueue', aliases=['queueshow', 'qshow', 'showq', ],
                      help='show the current music queue')
    @is_v_client()
    async def showqueue(self, ctx):
        await read_quote(ctx, ('music queue:', f'> 0: :musical_note: "{self.nowplaying}" :musical_note:'))
        for index, item in enumerate(self.queue_titles):
            await read_quote(ctx, f'> {index + 1}: "{item}"')

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await read_quote(ctx, random.choice(await get_no_music_quotes(ctx)))
        elif isinstance(error, NotInVChannel):
            await read_official(ctx, 'yo u gotta b in a voice channel 2 play shit. i need audience yk?', 'warning')
        elif isinstance(error, FailedSearch):
            await read_official(ctx, 'ur search got no results srry, u sure thats the songs name??', 'warning')
        elif isinstance(error, commands.BadArgument) and ctx.command == self.bot.get_command('dequeue'):
            await read_official(ctx, 'oof thats not how u use this cmd m8. try smth like "dequeue 1"', 'warning')
        elif isinstance(error.__cause__, IndexError) and ctx.command == self.bot.get_command('dequeue'):
            await read_official(ctx, 'invalid index buddy. here, find the index w/ this list & try again', 'warning')
            await ctx.invoke(self.bot.get_command('showqueue'))
        elif isinstance(error, commands.MissingRequiredArgument) and ctx.command == self.bot.get_command('dequeue'):
            await read_official(ctx, '2 use this cmd u gotta give the index of the song u want gone', 'warning')
            await ctx.invoke(self.bot.get_command('showqueue'))
        elif isinstance(error, commands.MissingRequiredArgument) and ctx.command == self.bot.get_command('play'):
            await read_official(ctx, '2 use this cmd u gotta give the name of the song u wanna play bud', 'warning')
        else:
            await read_official(ctx, f'unknown music error: {str(error).lower()}', 'warning')


def setup(bot):
    bot.add_cog(Music(bot))
