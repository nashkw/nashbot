# reminders.py


from quotes import *
from resources import *


class Reminders(commands.Cog, name='reminders'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='remindme', help='set a reminder for yourself')
    async def remindme(self, ctx):
        await read_quote(ctx, 'placeholder')

    async def error_handling(self, ctx, error):
        return False


def setup(bot):
    bot.add_cog(Reminders(bot))
