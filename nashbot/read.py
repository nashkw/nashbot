# read.py


import asyncio
from nashbot.menus import *
from nashbot.quotes import wrap


async def embed(channel, emb):
    await channel.trigger_typing()
    return await channel.send(embed=emb)


async def paginated(ctx, title, pages, header=None, footer=None):
    await ctx.trigger_typing()
    m = MyMenuPages(ctx.bot.user.id, MySource(pages, title, header=header, footer=footer), clear_reactions_after=True)
    await m.start(ctx)


async def quote(ctx, quo):
    await ctx.trigger_typing()
    if isinstance(quo, tuple):
        await ctx.send(quo[0])
        for line in quo[1:]:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send(line)
    else:
        await ctx.send(quo)


async def official(ctx, quo, emoji):
    await ctx.trigger_typing()
    await ctx.send(wrap(quo, emoji))


async def err(ctx, quo):
    await official(ctx, quo, 'warning')


async def file(ctx, filename):
    await ctx.trigger_typing()
    await ctx.send(file=discord.File(filename))