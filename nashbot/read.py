# read.py

from discord import File
from asyncio import sleep
from nashbot.menus import *
from nashbot.quotes import wrap


async def embed(ctx, emb):
    await ctx.trigger_typing()
    return await ctx.send(embed=emb)


async def paginated(ctx, name, pages, heads=None, foots=None, hide=False):
    await ctx.trigger_typing()
    m = Paginated(PSource(pages, name, heads=heads, foots=foots), clear_reactions_after=True, delete_message_after=hide)
    await m.start(ctx)


async def help_paginated(ctx, buttons, name, pages, heads=None, foots=None):
    await ctx.trigger_typing()
    if isinstance(foots, list):
        foots = [foot if foot else '(use the reaction emojis to navigate)' for foot in foots]
    m = HelpPages(buttons, PSource(pages, name, heads=heads, foots=foots), clear_reactions_after=True)
    await m.start(ctx)


async def quiz(ctx, quiz_name):
    await ctx.trigger_typing()
    m = QuizPages(quiz_name, clear_reactions_after=True)
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
