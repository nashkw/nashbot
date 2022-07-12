# tests.py


import discord
from quotes import *
from resources import *


class Tests(commands.Cog, name='tests'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='emojisets', aliases=['esets', 'eset'], help='test emoji sets in reactions', hidden=True)
    @is_nash()
    async def emojisets(self, ctx, eset_n: str = None):

        async def test_eset(eset, name):
            egroups = [eset[i:i + 20] for i in range(0, len(eset), 20)]
            for group in egroups:
                embed = discord.Embed(title=name, description='testing testing')
                msg = await read_embed(ctx, embed)
                for emoji in group:
                    await msg.add_reaction(emoji)

        if eset_n:
            if eset_n in emoji_sets:
                await test_eset(emoji_sets[eset_n], eset_n)
            else:
                raise FailedSearch
        else:
            for k, eset in emoji_sets.items():
                await test_eset(eset, k)

    @commands.command(name='emojitruth', aliases=['etruth', 'etrue'], help='test the true form of emojis', hidden=True)
    @is_nash()
    async def emojitruth(self, ctx, *, emojis: str):
        await read_quote(ctx, f"```unaltered: {emojis}\nlist of characters: {list(emojis)}```")

    async def error_handling(self, ctx, error):
        if isinstance(error, FailedSearch):
            if ctx.command == self.bot.get_command('emojisets'):
                await read_err(ctx, 'uuuh thats not the name of an emoji set, srry man. check for typos maybe ?')
            else:
                return False
        elif isinstance(error, commands.MissingRequiredArgument):
            if ctx.command == self.bot.get_command('emojitruth'):
                await read_err(ctx, '2 use this cmd u gotta give some emojis to test my man my jester my fool :)')
            else:
                return False
        else:
            return False
        return True


def setup(bot):
    bot.add_cog(Tests(bot))
