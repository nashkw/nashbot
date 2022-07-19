# resources.py


from nashbot.errs import *
from nashbot.varz import ALBUMS_PATH
from nashbot.quotes import get_table
from discord.ext.commands import check


# helper functions

def get_commands(bot):
    return [cmd for cmdlist in [[cmd.name] + cmd.aliases for cmd in bot.commands] for cmd in cmdlist]


def get_albums():
    albums = [album for album in ALBUMS_PATH.iterdir() if album.stem != 'Album Art' and album.stem[0] != '.']
    return [[i + 1, album.stem] for i, album in enumerate(albums)]


def clean_msg(m):
    return m.content.lower().replace('?', '').replace('...', '').replace(' :)', '').strip()


def table_paginate(p_list, n):
    return [get_table(page, trunc=True) for page in [p_list[i:i + n] for i in range(0, len(p_list), n)]]


# custom checks


def is_v_client():
    def predicate(ctx):
        if not ctx.voice_client:
            raise NoVClient
        return True
    return check(predicate)
