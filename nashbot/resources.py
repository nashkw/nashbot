# resources.py


from nashbot.errs import *
from nashbot.vars import ALBUMS_PATH


# helper functions

def get_commands(bot):
    return [cmd for cmdlist in [[cmd.name] + cmd.aliases for cmd in bot.commands] for cmd in cmdlist]


def get_albums():
    albums = [album for album in ALBUMS_PATH.iterdir() if album.stem != 'Album Art' and album.stem[0] != '.']
    return [[i + 1, album.stem] for i, album in enumerate(albums)]


def clean_msg(m):
    return m.content.lower().replace('?', '').replace('...', '').replace(' :)', '').strip()


# custom checks

def is_nash():
    def predicate(ctx):
        if ctx.message.author.id not in [386921492601896961, 727183720628486306]:
            raise NotNash
        return True
    return commands.check(predicate)


def is_v_client():
    def predicate(ctx):
        if not ctx.voice_client:
            raise NoVClient
        return True
    return commands.check(predicate)
