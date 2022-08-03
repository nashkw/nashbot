# resources.py


from random import choice
from pathlib import Path
from nashbot.errs import NoVClient, BadArg, FailedSearch, TooSmall
from nashbot.varz import ALBUMS_PATH, DOWNLOADS_PATH
from nashbot.quotes import get_table, quizzes, everyone_names
from discord.ext.commands import check


# helper functions

def flatten(to_flatten):
    return [item for sublist in to_flatten for item in sublist]


def empty_folder(pth: Path, delete_after=False):
    has_done_work = False
    for item in pth.iterdir():
        has_done_work = True
        if item.is_file():
            item.unlink()
        else:
            empty_folder(item, delete_after=True)
    if delete_after:
        pth.rmdir()
    return has_done_work


def get_member_variations(members):
    return set(flatten([[m, m.name, m.id, m.mention] for m in members]))


def get_commands(bot):
    return flatten([[cmd.name] + cmd.aliases for cmd in bot.commands])


def get_downloaded():
    downloads = sorted([d for d in DOWNLOADS_PATH.iterdir()], key=lambda p: p.lstat().st_mtime, reverse=True)
    return [[i + 1, d.stem, len(list(d.iterdir()))] for i, d in enumerate(downloads) if d.is_dir()]


def get_albums():
    albums = [album for album in ALBUMS_PATH.iterdir() if album.stem != 'Album Art' and album.stem[0] != '.']
    return [[i + 1, album.stem] for i, album in enumerate(albums)]


def get_quizzes(simple=False):
    return [[i+1, k, quizzes[k][0]['type'] if simple else quizzes[k][0]] for i, k in enumerate(sorted(quizzes.keys()))]


def get_quiz_name(quiz, return_list=False):
    if quiz.isdigit():
        indexes = [q[0] for q in get_quizzes()]
        if int(quiz) in indexes:
            quiz = get_quizzes().pop(indexes.index(int(quiz)))[1]
        else:
            raise BadArg(message='quizlist')
    else:
        for attr in ['type', 'name', 'nickname']:
            if quiz in [q[2][attr] for q in get_quizzes()]:
                possible = [q[1] for q in get_quizzes() if q[2][attr] == quiz]
                quiz = possible if return_list else choice(possible)
                break
        else:
            if quiz not in [q[1] for q in get_quizzes()]:
                raise FailedSearch(message=f'quiz named "{quiz}", & thats not a quiz type either')
    return [quiz, ] if return_list and not isinstance(quiz, list) else quiz


def parse_opts(ctx, opts):
    if opts in everyone_names:
        opts = [member.name for member in ctx.channel.members]
    else:
        opts = opts.replace(', ', ',').split(',')
    return opts


def clean_msg(m):
    return m.content.lower().replace('?', '').replace('...', '').replace(' :)', '').strip()


def table_paginate(p_list, n=10, trunc=50, head=None):
    return [get_table(page, trunc=trunc, head=head) for page in [p_list[i:i + n] for i in range(0, len(p_list), n)]]


def get_songs(songs):
    if '_type' not in songs:
        return [songs]
    elif not songs['entries']:
        raise FailedSearch if songs['extractor'] == 'youtube:search' else TooSmall
    return songs['entries']


# custom checks


def is_v_client():
    def predicate(ctx):
        if not ctx.voice_client:
            raise NoVClient
        return True
    return check(predicate)


def is_target_member(target):
    def predicate(m):
        return get_member_variations([m.author]).intersection({target})
    return predicate
