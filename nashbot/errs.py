# errs.py


from discord.ext.commands import CommandError


class FailedSearch(CommandError):
    pass


class NotInVChannel(CommandError):
    pass


class NoVClient(CommandError):
    pass


class QueuelessShuffle(CommandError):
    pass


class BadArg(CommandError):
    pass


class GlobalCheckFailure(CommandError):
    pass
