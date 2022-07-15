# reminders.py


from discord.ext import commands
from nashbot import errs
from nashbot import vars
from nashbot import read
from nashbot import menus
from nashbot import quotes
from nashbot import resources


class Reminders(commands.Cog, name='reminders'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='remindme', help='set a reminder for yourself')
    async def remindme(self, ctx):
        await read.quote(ctx, 'placeholder')

    async def error_handling(self, ctx, error):
        return False


def setup(bot):
    bot.add_cog(Reminders(bot))
