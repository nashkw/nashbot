# resources.py


from discord.ext import commands


frozen_users = []


# constants

FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn', }
YDL_OPTS = {'format': 'bestaudio', 'noplaylist': True, }

MUSIC_PATH = 'E:/BACKUPS/Music Backup/Music'
COGS_PATH = './cogs'
MEDIA_PATH = './media/'
SKELLY_PATH = MEDIA_PATH + 'skeleton_gifs/'


# helper functions

def get_commands(bot):
    return [cmd for cmdlist in [[cmd.name] + cmd.aliases for cmd in bot.commands] for cmd in cmdlist]


def clean_msg(m):
    return m.content.lower().replace('?', '').replace('...', '').replace(' :)', '').strip()


# custom errors

class FailedSearch(commands.CommandError):
    pass


class NotInVChannel(commands.CommandError):
    pass


class NotNash(commands.CommandError):
    pass


class NoVClient(commands.CommandError):
    pass


class QueuelessShuffle(commands.CommandError):
    pass


class BadArg(commands.CommandError):
    pass


class GlobalCheckFailure(commands.CommandError):
    pass


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