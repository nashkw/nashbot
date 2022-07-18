# read.py
import asyncio

from discord import File
from asyncio import sleep
from nashbot.menus import *
from nashbot.quotes import wrap


async def embed(ctx, emb):
    await ctx.trigger_typing()
    return await ctx.send(embed=emb)


async def paginated(ctx, title, pages, headers=None, footer=None):
    await ctx.trigger_typing()
    m = MyMenuPages(PSource(pages, title, headers=headers, footer=footer), clear_reactions_after=True)
    await m.start(ctx)


async def help_paginated(ctx, buttons, title, pages, headers=None, footer=None):
    await ctx.trigger_typing()
    m = HelpPages(buttons, PSource(pages, title, headers=headers, footer=footer), clear_reactions_after=True)
    await m.start(ctx)


async def quote(ctx, quo):
    await ctx.trigger_typing()
    if isinstance(quo, tuple):
        await ctx.send(quo[0])
        for line in quo[1:]:
            await ctx.trigger_typing()
            await sleep(1)
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
    await ctx.send(file=File(filename))
