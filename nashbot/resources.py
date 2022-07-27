# resources.py


from random import choice
from nashbot.errs import NoVClient, BadArg, FailedSearch
from nashbot.varz import ALBUMS_PATH
from nashbot.quotes import get_table, quizzes
from discord.ext.commands import check


# helper functions

def flatten(to_flatten):
    return [item for sublist in to_flatten for item in sublist]


def get_member_variations(members):
    return set(flatten([[m, m.name, m.id, m.mention] for m in members]))


def get_commands(bot):
    return flatten([[cmd.name] + cmd.aliases for cmd in bot.commands])


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


def clean_msg(m):
    return m.content.lower().replace('?', '').replace('...', '').replace(' :)', '').strip()


def table_paginate(p_list, n, head=None):
    return [get_table(page, trunc=True, head=head) for page in [p_list[i:i + n] for i in range(0, len(p_list), n)]]


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
