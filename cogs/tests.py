# tests.py


import emoji
import discord
from discord.ext import commands
from nashbot import errs
from nashbot import vars
from nashbot import read
from nashbot import menus
from nashbot import quotes
from nashbot import resources


class Tests(commands.Cog, name='tests'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='emojisets', aliases=['esets', 'eset'], help='test emoji sets in reactions', hidden=True)
    @resources.is_nash()
    async def emojisets(self, ctx, eset_n: str = None):

        async def test_eset(emoji_set, name):
            egroups = [emoji_set[i:i + 20] for i in range(0, len(emoji_set), 20)]
            for group in egroups:
                embed = discord.Embed(title=name, description='testing testing')
                msg = await read.embed(ctx, embed)
                for e in group:
                    try:
                        await msg.add_reaction(emoji.emojize(e, language='alias'))
                    except discord.HTTPException:
                        await read.quote(ctx, f'warning: the emoji "{e}" is not reaction safe')

        if eset_n:
            if eset_n in quotes.emoji_sets:
                await test_eset(quotes.emoji_sets[eset_n], eset_n)
            else:
                raise errs.FailedSearch
        else:
            for k, eset in quotes.emoji_sets.items():
                await test_eset(eset, k)

    @commands.command(name='emojitruth', aliases=['etruth', 'etrue'], help='test the true form of emojis', hidden=True)
    @resources.is_nash()
    async def emojitruth(self, ctx, *, emojis: str):
        await read.quote(ctx, f"```unaltered: {emojis}\nlist of characters: {list(emojis)}```")

    async def error_handling(self, ctx, error):
        if isinstance(error, errs.FailedSearch):
            if ctx.command == self.bot.get_command('emojisets'):
                await read.err(ctx, 'uuuh thats not the name of an emoji set, srry man. check for typos maybe ?')
            else:
                return False
        elif isinstance(error, commands.MissingRequiredArgument):
            if ctx.command == self.bot.get_command('emojitruth'):
                await read.err(ctx, '2 use this cmd u gotta give some emojis to test my man my jester my fool :)')
            else:
                return False
        else:
            return False
        return True


def setup(bot):
    bot.add_cog(Tests(bot))
