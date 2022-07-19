# reminder.py


from nashbot import read
from discord.ext.commands import Cog, command


class Reminder(Cog, name='reminder'):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '⏰'

    @command(name='remindme', brief='set a reminder for yourself',
             help='TODO',
             usage=['TODO'])
    async def remindme(self, ctx):
        await read.quote(ctx, 'TODO')

    async def error_handling(self, ctx, error):
        return False


def setup(bot):
    bot.add_cog(Reminder(bot))
