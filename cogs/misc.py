# misc.py


import random
from quotes import *
from resources import *


class Misc(commands.Cog, name='misc'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hi', aliases=['hello', 'howdy', 'greetings', 'salutations'], help='greet the bot')
    async def hi(self, ctx):
        await read_quote(ctx, random.choice(await get_hi_quotes(ctx)))

    @commands.command(name='highfive', aliases=['hifive', 'high5', 'hi5'], help='ask the bot to give u a high five')
    async def highfive(self, ctx):
        await read_quote(ctx, random.choice(await get_highfive_quotes(ctx)))

    async def error_handling(self, ctx, error):
        return False


def setup(bot):
    bot.add_cog(Misc(bot))