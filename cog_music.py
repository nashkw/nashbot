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
        self.queue = asyncio.Queue()
        self.next = asyncio.Event()
        self.nowplaying = ''
        self.looping = False

    async def music_loop(self, ctx):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.looping = True
            self.next.clear()
            try:
                mitem = self.queue.get_nowait()
            except asyncio.QueueEmpty:
                break

            ctx.voice_client.play(mitem[1], after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.nowplaying = mitem[0]
            await read_quote(ctx, f':musical_note:  now playing: "{self.nowplaying}" :musical_note:')
            await self.next.wait()
            self.nowplaying = ''
        await ctx.invoke(self.bot.get_command('stopmusic'))
        self.looping = False

    @commands.command(name='playmusic', help='tell the bot play music from youtube')
    async def playmusic(self, ctx,  *, search: str):
        await ctx.trigger_typing()

        if ctx.author.voice is None:
            await read_quote(ctx, 'TODO join a voice channel 1st bro, i need an audience 4 this kinda thing yk ;)')
            return

        if ctx.voice_client is None:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.voice_client.move_to(ctx.author.voice.channel)

        info = self.ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
        mitem = (info['title'], await discord.FFmpegOpusAudio.from_probe(info['formats'][0]['url'], **FFMPEG_OPTS))
        await self.queue.put(mitem)
        await read_quote(ctx, f':white_check_mark: added to music queue: "{mitem[0]}" :white_check_mark: ')

        if not self.looping:
            await self.music_loop(ctx)

    @commands.command(name='stopmusic', help='tell the bot to stop playing music')
    async def stopmusic(self, ctx):
        if ctx.voice_client is None:
            await read_quote(ctx, random.choice(await get_no_music_quotes(ctx)))
        else:
            self.queue = asyncio.Queue()
            self.next = asyncio.Event()
            self.nowplaying = ''
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

    @commands.command(name='showqueue', help='ask the bot to read out the current music queue')
    async def showqueue(self, ctx):
        if self.queue:
            await read_quote(ctx, 'music queue:')
            for item in self.queue:
                await read_quote(ctx, f'> {item}')
        else:
            await read_quote(ctx, 'TODO queue empty')

def setup(bot):
    bot.add_cog(Music(bot))
