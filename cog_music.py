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
        self.q_sources = asyncio.Queue()
        self.q_titles = []
        self.repeating = None
        self.next = asyncio.Event()
        self.nowplaying = ''
        self.looping = False

    async def end_music(self, ctx):
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        self.q_sources = asyncio.Queue()
        self.q_titles = []
        self.repeating = None
        self.next = asyncio.Event()
        self.nowplaying = ''
        self.looping = False

    async def music_loop(self, ctx):
        await self.bot.wait_until_ready()
        self.looping = True
        while not self.bot.is_closed() and self.looping:
            self.next.clear()
            
            if self.repeating is None:
                try:
                    pre_source = self.q_sources.get_nowait()
                    self.nowplaying = self.q_titles.pop(0)
                    await read_official(ctx, f'now playing: "{self.nowplaying}"', 'musical_note')
                except asyncio.QueueEmpty:
                    self.looping = False
                    await self.end_music(ctx)
                    await read_quote(ctx, ':x: end of music queue :x:')
                    return
            else:
                pre_source = self.repeating

            source = await discord.FFmpegOpusAudio.from_probe(pre_source, **FFMPEG_OPTS)
            ctx.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            await self.next.wait()
            if self.repeating is not None:
                self.repeating = pre_source

    @commands.command(name='play', help='play music from youtube')
    async def play(self, ctx, *, search: str):
        async with ctx.typing():
            if not ctx.author.voice:
                raise NotInVChannel

            info = YoutubeDL(YDL_OPTS).extract_info(f"ytsearch:{search}", download=False)
            if not info['entries']:
                raise FailedSearch
            else:
                info = info['entries'][0]

            if not ctx.voice_client:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.voice_client.move_to(ctx.author.voice.channel)

            await self.q_sources.put(info['formats'][0]['url'])
            self.q_titles.append(info['title'])
        await read_official(ctx, f'added to music queue: "{info["title"]}"', 'white_check_mark')
        if not self.looping:
            await self.music_loop(ctx)

    @commands.command(name='pause', aliases=['unpause'], help='pause or unpause the currently playing song')
    @is_v_client()
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await read_official(ctx, f'paused music: "{self.nowplaying}"', 'pause_button')
        elif ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await read_official(ctx, f'unpaused music: "{self.nowplaying}"', 'arrow_forward')

    @commands.command(name='loop', aliases=['unloop'], help='set the currently playing song to loop')
    @is_v_client()
    async def loop(self, ctx):
        if self.repeating is not None:
            self.repeating = None
            await read_official(ctx, f'stopped looping: "{self.nowplaying}"', 'musical_note')
        else:
            self.repeating = True
            await read_official(ctx, f'now looping: "{self.nowplaying}"', 'repeat')

    @commands.command(name='skip', help='skip the currently playing song')
    @is_v_client()
    async def skip(self, ctx):
        ctx.voice_client.stop()
        await read_official(ctx, f'skipped: "{self.nowplaying}"', 'track_next')

    @commands.command(name='dequeue', aliases=['dq', 'qremove'], help='remove a song from the music queue')
    @is_v_client()
    async def dequeue(self, ctx, index: int):
        if index == 0:
            ctx.voice_client.stop()
        elif 0 < index - 1 < len(self.q_titles):
            newq = asyncio.Queue()
            i = 0
            while not self.q_sources.empty():
                item = self.q_sources.get_nowait()
                if i != index - 1:
                    newq.put_nowait(item)
                i = i + 1
            self.q_sources = newq
            await read_official(ctx, f'removed from music queue: "{self.q_titles.pop(index - 1)}"',
                                'negative_squared_cross_mark')
        else:
            raise IndexError

    @commands.command(name='clearqueue', aliases=['clearq', 'qclear'], help='clear the music queue')
    @is_v_client()
    async def clearqueue(self, ctx):
        await self.end_music(ctx)
        await read_official(ctx, 'music queue cleared', 'x')

    @commands.command(name='showqueue', aliases=['showq', 'qshow'], help='show the current music queue')
    @is_v_client()
    async def showqueue(self, ctx):
        embed = discord.Embed(title='music queue')
        v = '\n'.join([f'> {index + 1}: "{item}"' for index, item in enumerate(self.q_titles)])
        emoji = 'repeat' if self.repeating is not None else 'musical_note'
        embed.add_field(name=f':{emoji}: 0: "{self.nowplaying}" :{emoji}:', value=v, inline=False)
        await read_embed(ctx.channel, embed)

    """async def cog_command_error(self, ctx, error):
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
            await read_official(ctx, f'unknown music error: {str(error).lower()}', 'warning')"""


def setup(bot):
    bot.add_cog(Music(bot))
