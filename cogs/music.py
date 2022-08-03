# music.py


from eyed3 import load, id3
from random import choice, shuffle
from pathlib import Path
from asyncio import Queue, Event, QueueEmpty
from discord import FFmpegPCMAudio, FFmpegOpusAudio
from nashbot import errs, quotes, read, resources, varz
from youtube_dl import YoutubeDL, DownloadError
from _collections import deque
from urllib.error import HTTPError
from discord.ext.commands import is_owner, Cog, command, MissingRequiredArgument, BadArgument


class Music(Cog, name='music'):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🎧'
        self.q_sources = Queue()
        self.q_titles = []
        self.repeating = None
        self.next = Event()
        self.nowplaying = ''
        self.looping = False

    async def end_music(self, ctx):
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
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

    async def download(self, ctx, ydl, song, title, artist, folder, img):
        ydl.download([song['webpage_url']])
        metadata = load(varz.DOWNLOADS_PATH / folder / f'{Path(ydl.prepare_filename(song)).stem}.mp3').tag
        metadata.album = folder
        metadata.artist = song['uploader'] if artist is None else artist
        metadata.track_num = song['playlist_index']
        if img:
            metadata.images.set(3, await img.read(), img.content_type)
        metadata.save(version=id3.ID3_V2_3)
        await read.official(ctx, f'successfully downloaded: "{title}"', 'white_check_mark')

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
                source = await FFmpegOpusAudio.from_probe(pre_source, **varz.FFMPEG_OPTS)
            ctx.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            await self.next.wait()
            if self.repeating:
                self.repeating = pre_source

    async def music_play(self, ctx, arg, from_yt=True):
        async with ctx.typing():
            if not ctx.author.voice:
                raise errs.NotInVChannel

            if from_yt:
                songs = resources.get_songs(YoutubeDL(varz.YDL_STREAM_OPTS).extract_info(arg, download=False))
                added = f'playlist "{songs[0]["playlist"]}"' if 1 < len(songs) else songs[0]['title']
                for song in songs:
                    await self.q_sources.put(song['formats'][0]['url'])
                    self.q_titles.append(song['title'])
            else:
                songs = sorted(list((varz.ALBUMS_PATH / arg).glob('*.mp3')), key=lambda s: load(s).tag.track_num)
                if not songs:
                    raise errs.FailedSearch
                else:
                    for song in songs:
                        await self.q_sources.put(song)
                        if load(song).tag.title:
                            self.q_titles.append(load(song).tag.title)
                        else:
                            self.q_titles.append(song.stem)
                    added = f'local album "{arg}"'

            if not ctx.voice_client:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.voice_client.move_to(ctx.author.voice.channel)

        await read.official(ctx, f'added to music queue: {added}', 'white_check_mark')

        if not self.looping:
            await self.music_loop(ctx)

    @command(name='play', aliases=['playsong', 'ytplay', 'playlist', 'playsongs'], brief='play music from youtube',
             help='add music from youtube 2 the current music queue & begin playing the queue if its not already '
                  'playing. u can specify the music by a youtube url (either 4 a single song or 4 a playlist), or u '
                  'can specify search terms & the bot will choose the first search result. remember 2 make sure ur in '
                  'a voice channel b4 u try & play music tho',
             usage=['play organgatangabangin b-man', 'playsong https://youtu.be/O3OGqd6snSE', 'ytplay meme',
                    'playlist https://youtube.com/playlist?list=PLSdoVPM5WnndV_AXWGXpzUsIw6fN1RQVN'])
    async def play(self, ctx, *, search: str):
        if search.lower().replace(',', '').strip() in quotes.meme_activators:
            search = choice(quotes.meme_songs)
        await self.music_play(ctx, search)

    @command(name='nashplay', aliases=['nplay', 'localplay'], brief='add a local album to the music queue', hidden=True,
             help='play an album from local music files. specify the album by either its name or index (use the nshow '
                  'cmd 2 find this). remember 2 make sure ur in a voice channel b4 u try & play music tho',
             usage=['nashplay radiohead', 'nplay 83'])
    @is_owner()
    async def nashplay(self, ctx, *, album):
        if album.isdigit():
            indexes = [al[0] for al in resources.get_albums()]
            if int(album) in indexes:
                album = resources.get_albums().pop(indexes.index(int(album)))[1]
            else:
                raise errs.BadArg
        await self.music_play(ctx, album, from_yt=False)

    @command(name='nashsave', aliases=['nsave', 'ndownload'], brief='download a playlist to local files', hidden=True,
             help='download all songs from a youtube playlist to the local file system. ull need 2 specify the name '
                  'of the album, then the name of the artist, then the url of a youtube playlist w/ at least 1 song. '
                  'if u specify the url of a song instead of a playlist it will still download but it wont have any '
                  'value 4 its track number metadata value. remember that any argument containing spaces will need 2 '
                  'b enclosed w/in quotes in order 2 avoid getting mixed up w/ other arguments. if u attach an image '
                  'in either jpeg or png format 2 the msg it will b set as the album art for all songs.',
             usage=['nashsave Kratos VIXX https://youtube.com/playlist?list=PL7nMVfgRrpSllb65Squ4cvfouUQFRjySp',
                    'nsave "Kid A" Radiohead https://youtube.com/playlist?list=PLtP8IJbMRbLwJwxyaCUaUWtBo1KK2K7RG',
                    'ndownload "Alive 2007" "Daft Punk" https://www.youtube.com/watch?v=NFxyYYRqobw'])
    @is_owner()
    async def nashsave(self, ctx, album: str, artist: str, url: str):
        async with ctx.typing():
            opts = varz.YDL_DOWNLOAD_OPTS.copy()

            try:
                songs = resources.get_songs(YoutubeDL(opts).extract_info(url, download=False))
            except DownloadError:
                raise errs.FailedSearch
            playlist = songs[0]['playlist'] if 1 < len(songs) else False
            if playlist:
                await read.official(ctx, f'**initiating playlist download: "{playlist}"**', 'arrow_down')

            if album in quotes.default_names:
                album = playlist if playlist else songs[0]['title']
            if artist in quotes.default_names:
                artist = None
                folder = album
            else:
                folder = f'{artist} ({album})'
            opts['outtmpl'] = opts['outtmpl'].replace('INSERT_TITLE', folder)

            if ctx.message.attachments and ctx.message.attachments[0].content_type in ['image/png', 'image/jpeg']:
                img = ctx.message.attachments[0]
            else:
                img = None

            with YoutubeDL(opts) as ydl:
                for song in songs:
                    title = song["title"]
                    await read.official(ctx, f'now downloading: "{title}"', 'arrow_down')
                    try:
                        await self.download(ctx, ydl, song, title, artist, folder, img)
                    except DownloadError as error:
                        await read.err(ctx, str(error))
                        if error.exc_info[0] is HTTPError and error.exc_info[1].code == 403:
                            try:
                                await read.official(ctx, f'retrying download: "{title}"', 'leftwards_arrow_with_hook')
                                ydl.cache.remove()
                                await self.download(ctx, ydl, song, title, artist, folder, img)
                                continue
                            except DownloadError as e:
                                await read.err(ctx, str(e))
                        await read.official(ctx, f'aborting & skipping download: "{title}"', 'x')
        if playlist:
            await read.official(ctx, f'**completed playlist download: "{playlist}"**', 'white_check_mark')

    @command(name='pause', aliases=['unpause', 'togglepause'], brief='pause or unpause the currently playing song',
             help='toggle the paused effect for the current music queue. keep in mind youll need 2 b playin music b4 '
                  'tryin this')
    @resources.is_v_client()
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await read.official(ctx, f'paused music: "{self.nowplaying}"', 'pause_button')
        elif ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await read.official(ctx, f'unpaused music: "{self.nowplaying}"', 'arrow_forward')

    @command(name='skip', aliases=['next', 'nextsong', 'skipsong'], brief='skip the currently playing song',
             help='skip the currently playing song, even if its looping. keep in mind youll need 2 b playin music b4 '
                  'tryin this')
    @resources.is_v_client()
    async def skip(self, ctx):
        if self.repeating is not None:
            self.repeating = False
        ctx.voice_client.stop()
        await read.official(ctx, f'skipped: "{self.nowplaying}"', 'track_next')

    @command(name='loop', aliases=['unloop', 'toggleloop'], brief='set the currently playing song to loop',
             help='toggle the loop effect for the currently playing song. if u skip a looping song the next song will '
                  'start looping instead. keep in mind youll need 2 b playin music b4 tryin this')
    @resources.is_v_client()
    async def loop(self, ctx):
        if self.repeating:
            self.repeating = None
            await read.official(ctx, f'stopped looping: "{self.nowplaying}"', self.np_emoji())
        else:
            self.repeating = True
            await read.official(ctx, self.np_msg(), self.np_emoji())

    @command(name='shuffle', aliases=['reshuffle', 'qmix', 'mixq'], brief='shuffle the current music queue',
             help='shuffle the current music queue into a different order. wont shuffle the currently playing song. '
                  'keep in mind youll need 2 have at least 2 songs in the queue b4 tryin this')
    @resources.is_v_client()
    async def shuffle(self, ctx):
        if len(self.q_titles) > 1:
            shuffling = list(zip(self.q_titles, self.q_sources._queue))
            shuffle(shuffling)
            qtemp1, qtemp2 = zip(*shuffling)
            self.q_titles, self.q_sources._queue = list(qtemp1), deque(qtemp2)
            await read.official(ctx, 'shuffled music queue', 'twisted_rightwards_arrows')
            await ctx.invoke(self.bot.get_command('showqueue'))
        else:
            raise errs.TooSmall

    @command(name='showqueue', aliases=['showq', 'qshow', 'q'], brief='show the current music queue',
             help='show all currently queued songs & their index in the current music queue. keep in mind youll need '
                  '2 b playing music b4 tryin this')
    @resources.is_v_client()
    async def showqueue(self, ctx):
        np = quotes.wrap(f'**now playing: "{self.nowplaying}"**', self.np_emoji())
        fill = [[i+1, item] for i, item in enumerate(self.q_titles)]
        foot = None if fill else '(there are no songs queued after this one, use the "play [songname]" cmd to add more)'
        fill = resources.table_paginate(fill, n=10) if fill else [varz.BLANK]
        await read.paginated(ctx, quotes.wrap('music queue', 'musical_note'), fill, heads=np, foots=foot)

    @command(name='shownash', aliases=['nshow'], brief='show the available local music albums', hidden=True,
             help='show all available local music albums & their indexes 4 use in the nplay cmd')
    @is_owner()
    async def shownash(self, ctx):
        fill = resources.table_paginate(resources.get_albums(), n=10)
        await read.paginated(ctx, quotes.wrap('forbidden & secret local albums', 'eyes'), fill, hide=True)

    @command(name='dequeue', aliases=['dq', 'qremove'], brief='remove a song from the music queue',
             help='remove the song at the specified index from the music queue. index 0 is always the currently '
                  'playing song. keep in mind youll need 2 b playin music b4 tryin this',
             usage=['dequeue 4', 'dq 0'])
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

    @command(name='clearqueue', aliases=['clearq', 'qclear'], brief='clear the music queue',
             help='clear all songs including the currently playing song from the current music queue. keep in mind '
                  'youll need 2 b playin music b4 tryin this')
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
            if ctx.command in {self.bot.get_command('play'), self.bot.get_command('nashplay')}:
                await read.err(ctx, 'ur search got no results srry, u sure thats the right name??')
            elif ctx.command == self.bot.get_command('nashsave'):
                await read.err(ctx, 'uhhh, u whaa-?? theres no playlist or song w/ that url i dont think :|')
            else:
                return False
        elif isinstance(error, errs.TooSmall):
            if ctx.command == self.bot.get_command('shuffle'):
                await read.err(ctx, 'but,, wheres the queue?? beef up the queue a bit b4 tryin that lmao')
            elif ctx.command in {self.bot.get_command('play'), self.bot.get_command('nashsave')}:
                await read.err(ctx, 'but,, wheres the playlist?? itll need 2 contain at least 1 song b4 u can try that')
            else:
                return False
        elif isinstance(error, errs.BadArg):
            await read.err(ctx, 'invalid index buddy. here, find the index w/ this list & try again')
            if ctx.command == self.bot.get_command('dequeue'):
                await ctx.invoke(self.bot.get_command('showqueue'))
            elif ctx.command == self.bot.get_command('nashplay'):
                await ctx.invoke(self.bot.get_command('shownash'))
            else:
                return False
        elif isinstance(error, MissingRequiredArgument):
            if ctx.command == self.bot.get_command('nashplay'):
                await read.err(ctx, '2 use this cmd u gotta give the albums name or index or, idk, at least *smth*')
            elif ctx.command == self.bot.get_command('play'):
                await read.err(ctx, '2 use this cmd u gotta give the name of the song u wanna play bud')
            elif ctx.command == self.bot.get_command('nashsave'):
                await read.err(ctx, '2 use this cmd u gotta give the album name, the artists name, & the playlist url')
            elif ctx.command == self.bot.get_command('dequeue'):
                await read.err(ctx, '2 use this cmd u gotta give the index of the song u want gone')
                await ctx.invoke(self.bot.get_command('showqueue'))
            else:
                return False
        elif isinstance(error, BadArgument):
            if ctx.command == self.bot.get_command('dequeue'):
                await read.err(ctx, 'oof thats not how u use this cmd m8. try smth like "dequeue 1"')
            else:
                return False
        else:
            return False
        return True


def setup(bot):
    bot.add_cog(Music(bot))
