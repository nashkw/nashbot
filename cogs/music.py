# music.py


from eyed3 import load
from random import choice, shuffle
from pathlib import Path
from asyncio import Queue, Event, QueueEmpty
from discord import FFmpegPCMAudio, FFmpegOpusAudio
from nashbot import errs, quotes, read, resources, vars
from youtube_dl import YoutubeDL
from discord.ext import commands
from _collections import deque


class Music(commands.Cog, name='music'):

    def __init__(self, bot):
        self.bot = bot
        self.q_sources = Queue()
        self.q_titles = []
        self.repeating = None
        self.next = Event()
        self.nowplaying = ''
        self.looping = False

    def np_emoji(self):
        return 'repeat' if self.repeating is not None else 'notes'

    def np_msg(self):
        return f'now {"looping" if self.repeating is not None else "playing"}: "{self.nowplaying}"'

    async def end_music(self, ctx):
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
        self.q_sources = Queue()
        self.q_titles = []
        self.repeating = None
        self.next = Event()
        self.nowplaying = ''
        self.looping = False

    async def music_loop(self, ctx):
        await self.bot.wait_until_ready()
        self.looping = True
        while not self.bot.is_closed() and self.looping:
            self.next.clear()
            
            if not self.repeating:
                if self.repeating is not None:
                    self.repeating = True  # loop on new song if skip cmd was called while loop is toggled
                try:
                    pre_source = self.q_sources.get_nowait()
                    self.nowplaying = self.q_titles.pop(0)
                    await read.official(ctx, self.np_msg(), self.np_emoji())
                except QueueEmpty:
                    self.looping = False
                    await self.end_music(ctx)
                    await read.quote(ctx, ':x:　end of music queue　:x:')
                    return
            else:
                pre_source = self.repeating

            if isinstance(pre_source, Path):
                source = FFmpegPCMAudio(source=pre_source)
            else:
                source = await FFmpegOpusAudio.from_probe(pre_source, **vars.FFMPEG_OPTS)
            ctx.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            await self.next.wait()
            if self.repeating:
                self.repeating = pre_source

    async def music_play(self, ctx, arg, is_search=True):
        async with ctx.typing():
            if not ctx.author.voice:
                raise errs.NotInVChannel

            if is_search:
                info = YoutubeDL(vars.YDL_OPTS).extract_info(f"ytsearch:{arg}", download=False)
                if not info['entries']:
                    raise errs.FailedSearch
                else:
                    info = info['entries'][0]
                    await self.q_sources.put(info['formats'][0]['url'])
                    self.q_titles.append(info['title'])
            else:
                songs = sorted(list((vars.ALBUMS_PATH / arg).glob('*.mp3')), key=lambda s: load(s).tag.track_num)
                if not songs:
                    raise errs.FailedSearch
                else:
                    for song in songs:
                        await self.q_sources.put(song)
                        if load(song).tag.title:
                            self.q_titles.append(load(song).tag.title)
                        else:
                            self.q_titles.append(song.stem)

            if not ctx.voice_client:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.voice_client.move_to(ctx.author.voice.channel)

        added = f'"{info["title"]}"' if is_search else f'local album "{arg}"'
        await read.official(ctx, f'added to music queue: {added}', 'white_check_mark')

        if not self.looping:
            await self.music_loop(ctx)

    @commands.command(name='play', help='play a song from youtube')
    async def play(self, ctx, *, search: str):
        if search.lower().replace(',', '').strip() in quotes.meme_activators:
            search = choice(quotes.meme_songs)
        await self.music_play(ctx, search)

    @commands.command(name='nashplay', aliases=['nplay'], help='add a local album to the music queue', hidden=True)
    @resources.is_nash()
    async def nashplay(self, ctx, *, album):
        if album.isdigit():
            indexes = [al[0] for al in resources.get_albums()]
            if int(album) in indexes:
                album = resources.get_albums().pop(indexes.index(int(album)))[1]
            else:
                raise errs.BadArg
        await self.music_play(ctx, album, is_search=False)

    @commands.command(name='pause', aliases=['unpause'], help='pause or unpause the currently playing song')
    @resources.is_v_client()
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await read.official(ctx, f'paused music: "{self.nowplaying}"', 'pause_button')
        elif ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await read.official(ctx, f'unpaused music: "{self.nowplaying}"', 'arrow_forward')

    @commands.command(name='skip', help='skip the currently playing song')
    @resources.is_v_client()
    async def skip(self, ctx):
        if self.repeating is not None:
            self.repeating = False
        ctx.voice_client.stop()
        await read.official(ctx, f'skipped: "{self.nowplaying}"', 'track_next')

    @commands.command(name='loop', aliases=['unloop'], help='set the currently playing song to loop')
    @resources.is_v_client()
    async def loop(self, ctx):
        if self.repeating:
            self.repeating = None
            await read.official(ctx, f'stopped looping: "{self.nowplaying}"', self.np_emoji())
        else:
            self.repeating = True
            await read.official(ctx, self.np_msg(), self.np_emoji())

    @commands.command(name='shuffle', aliases=['reshuffle', 'qmix', 'mixq'], help='shuffle the current music queue')
    @resources.is_v_client()
    async def shuffle(self, ctx):
        if self.q_titles:
            shuffling = list(zip(self.q_titles, self.q_sources._queue))
            shuffle(shuffling)
            qtemp1, qtemp2 = zip(*shuffling)
            self.q_titles, self.q_sources._queue = list(qtemp1), deque(qtemp2)
            await read.official(ctx, 'shuffled music queue', 'twisted_rightwards_arrows')
            await ctx.invoke(self.bot.get_command('showqueue'))
        else:
            raise errs.QueuelessShuffle

    @commands.command(name='showqueue', aliases=['showq', 'qshow', 'q'], help='show the current music queue')
    @resources.is_v_client()
    async def showqueue(self, ctx):
        np = quotes.wrap(f'**now playing: "{self.nowplaying}"**', self.np_emoji())
        v = [[i+1, item] for i, item in enumerate(self.q_titles)]
        v = [f'```{quotes.get_table(item)}```' for item in [v[i:i + 10] for i in range(0, len(v), 10)]]
        await read.paginated(ctx, quotes.wrap('music queue', 'musical_note'), v, header=np)

    @commands.command(name='shownash', aliases=['nshow'], help='show the available local music albums', hidden=True)
    @resources.is_nash()
    async def shownash(self, ctx):
        v = resources.get_albums()
        v = [f'```{quotes.get_table(albums)}```' for albums in [v[i:i + 10] for i in range(0, len(v), 10)]]
        await read.paginated(ctx, quotes.wrap('forbidden & secret local albums', 'eyes'), v)

    @commands.command(name='dequeue', aliases=['dq', 'qremove'], help='remove a song from the music queue')
    @resources.is_v_client()
    async def dequeue(self, ctx, index: int):
        if index == 0:
            await ctx.invoke(self.bot.get_command('skip'))
        elif 0 <= index - 1 < len(self.q_titles):
            new_q = Queue()
            i = 0
            while not self.q_sources.empty():
                item = self.q_sources.get_nowait()
                if i != index - 1:
                    new_q.put_nowait(item)
                i = i + 1
            self.q_sources = new_q
            removed = self.q_titles.pop(index - 1)
            await read.official(ctx, f'removed from music queue: "{removed}"', 'negative_squared_cross_mark')
        else:
            raise errs.BadArg

    @commands.command(name='clearqueue', aliases=['clearq', 'qclear'], help='clear the music queue')
    @resources.is_v_client()
    async def clearqueue(self, ctx):
        await self.end_music(ctx)
        await read.official(ctx, 'music queue cleared', 'x')

    async def error_handling(self, ctx, error):
        if isinstance(error, errs.NoVClient):
            await read.quote(ctx, choice(await quotes.get_no_music_quotes(ctx)))
        elif isinstance(error, errs.NotInVChannel):
            await read.err(ctx, 'yo u gotta b in a voice channel 2 play shit. i need audience yk?')
        elif isinstance(error, errs.FailedSearch):
            await read.err(ctx, 'ur search got no results srry, u sure thats the right name??')
        elif isinstance(error, errs.QueuelessShuffle):
            await read.err(ctx, 'but,, wheres the queue?? beef up the queue a bit b4 tryin that lmao')
        elif isinstance(error, errs.BadArg):
            await read.err(ctx, 'invalid index buddy. here, find the index w/ this list & try again')
            if ctx.command == self.bot.get_command('dequeue'):
                await ctx.invoke(self.bot.get_command('showqueue'))
            elif ctx.command == self.bot.get_command('nashplay'):
                await ctx.invoke(self.bot.get_command('shownash'))
            else:
                return False
        elif isinstance(error, commands.MissingRequiredArgument):
            if ctx.command == self.bot.get_command('nashplay'):
                await read.err(ctx, '2 use this cmd u gotta give the albums name or index or, idk, at least *smth*')
            elif ctx.command == self.bot.get_command('play'):
                await read.err(ctx, '2 use this cmd u gotta give the name of the song u wanna play bud')
            elif ctx.command == self.bot.get_command('dequeue'):
                await read.err(ctx, '2 use this cmd u gotta give the index of the song u want gone')
                await ctx.invoke(self.bot.get_command('showqueue'))
            else:
                return False
        elif isinstance(error, commands.BadArgument):
            if ctx.command == self.bot.get_command('dequeue'):
                await read.err(ctx, 'oof thats not how u use this cmd m8. try smth like "dequeue 1"')
            else:
                return False
        else:
            return False
        return True


def setup(bot):
    bot.add_cog(Music(bot))
