# resouces.py


from discord.ext import commands


frozen_users = []


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


class BadIndex(commands.CommandError):
    pass


class GlobalCheckFailure(commands.CommandError):
    pass


# custom checks

def is_nash():
    def predicate(ctx):
        if not ctx.message.author.id in [386921492601896961, 727183720628486306]:
            raise NotNash
        return True
    return commands.check(predicate)


def is_v_client():
    def predicate(ctx):
        if not ctx.voice_client:
            raise NoVClient
        return True
    return commands.check(predicate)