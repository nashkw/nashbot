# errs.py


from discord.ext.commands import CommandError


class FailedSearch(CommandError):
    def __init__(self, message='search unsuccessful with given parameter', *args):
        super().__init__(message, *args)


class NotInVChannel(CommandError):
    def __init__(self, message='the target user is not currently in a voice channel', *args):
        super().__init__(message, *args)


class NoVClient(CommandError):
    def __init__(self, message='the bot is not currently playing music', *args):
        super().__init__(message, *args)


class TooSmall(CommandError):
    def __init__(self, message='the target is too small to carry out that operation', *args):
        super().__init__(message, *args)


class BadArg(CommandError):
    def __init__(self, message='the given argument is invalid for use in this operation', *args):
        super().__init__(message, *args)


class GlobalCheckFailure(CommandError):
    def __init__(self, message='failed to pass the global command check', *args):
        super().__init__(message, *args)
