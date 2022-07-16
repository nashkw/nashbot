# errs.py


from discord.ext import commands


class FailedSearch(commands.CommandError):
    pass


class NotInVChannel(commands.CommandError):
    pass


class NoVClient(commands.CommandError):
    pass


class QueuelessShuffle(commands.CommandError):
    pass


class BadArg(commands.CommandError):
    pass


class GlobalCheckFailure(commands.CommandError):
    pass
