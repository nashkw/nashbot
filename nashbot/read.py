# read.py

from discord import File
from asyncio import sleep
from humanize import naturaldelta, naturaltime
from nashbot.menus import Paginated, PSource, HelpPages, QuizPages
from nashbot.quotes import wrap
from nashbot.resources import table_paginate


async def embed(channel, emb):
    await channel.trigger_typing()
    return await channel.send(embed=emb)


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


async def quote(channel, quo):
    await channel.trigger_typing()
    if isinstance(quo, tuple):
        await channel.send(quo[0])
        for line in quo[1:]:
            await channel.trigger_typing()
            await sleep(1)
            await channel.send(line)
    else:
        await channel.send(quo)


async def official(channel, quo, emoji):
    await channel.trigger_typing()
    await channel.send(wrap(quo, emoji))


async def err(channel, quo):
    await official(channel, quo, 'warning')


async def file(channel, filename):
    await channel.trigger_typing()
    await channel.send(file=File(filename))


async def reminder_list(ctx, r_list, full_quote, empty_quote, archive=False, hide=False):
    if r_list:
        now = ctx.message.created_at
        for i, r in enumerate(r_list):
            r_list[i] = [i + 1, r['msg'], naturaltime(r['deleted']) if archive else naturaldelta(r['time'] - now)]
        r_list = table_paginate(r_list, trunc=33, head=['', 'message', 'archived' if archive else 'due in'])
        await paginated(ctx, wrap(full_quote[0], full_quote[1]), r_list, hide=hide)
    else:
        await official(ctx, empty_quote, 'x')
