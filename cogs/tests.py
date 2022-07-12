# tests.py
import discord

from quotes import *
from resources import *


class Tests(commands.Cog, name='tests'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='emojisets', help='test emoji sets in reactions', hidden=True)
    @is_nash()
    async def emojisets(self, ctx):
        for k, eset in emoji_sets.items():
            egroups = [eset[i:i + 20] for i in range(0, len(eset), 20)]
            for group in egroups:
                embed = discord.Embed(title=k, description='testing testing')
                msg = await read_embed(ctx, embed)
                for emoji in group:
                    await msg.add_reaction(emoji)

    async def error_handling(self, ctx, error):
        return False


def setup(bot):
    bot.add_cog(Tests(bot))
