# test.py


from emoji import emojize
from discord import Embed, HTTPException
from nashbot import errs, quotes, read
from discord.ext.commands import is_owner, command, MissingRequiredArgument, Cog


class Test(Cog, name='test'):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🔬'

    @command(name='emojisets', aliases=['esets', 'eset'], brief='test emoji sets in reactions', hidden=True,
             help='test all emoji sets in reaction form to confirm they can be successfully converted to unicode',
             usage=['emojisets', 'eset hearts'])
    @is_owner()
    async def emojisets(self, ctx, eset_n: str = None):

        async def test_eset(emoji_set, name):
            egroups = [emoji_set[i:i + 20] for i in range(0, len(emoji_set), 20)]
            for group in egroups:
                embed = Embed(title=name, description='testing testing')
                msg = await read.embed(ctx, embed)
                for e in group:
                    try:
                        await msg.add_reaction(emojize(e, language='alias'))
                    except HTTPException:
                        await read.quote(ctx, f'warning: the emoji "{e}" is not reaction safe')

        if eset_n:
            if eset_n in quotes.emoji_sets:
                await test_eset(quotes.emoji_sets[eset_n], eset_n)
            else:
                raise errs.FailedSearch
        else:
            for k, eset in quotes.emoji_sets.items():
                await test_eset(eset, k)

    @command(name='msgtruth', aliases=['mtrue', 'etrue'], brief='test the true form of a message', hidden=True,
             help='read back the contents of the users message, separating it out into a list of characters',
             usage=['msgtruth greetingz 🤡', 'mtrue hello there <@985864214260371476>', 'etrue ❤️🧡💛💚💙💜'])
    @is_owner()
    async def msgtruth(self, ctx, *, m: str):
        await read.quote(ctx, f"```unaltered: {m}\nlist of characters: {list(m)}```")

    async def error_handling(self, ctx, error):
        if isinstance(error, errs.FailedSearch):
            if ctx.command == self.bot.get_command('emojisets'):
                await read.err(ctx, 'uuuh thats not the name of an emoji set, srry man. check for typos maybe ?')
            else:
                return False
        elif isinstance(error, MissingRequiredArgument):
            if ctx.command == self.bot.get_command('emojitruth'):
                await read.err(ctx, '2 use this cmd u gotta give some emojis to test my man my jester my fool :)')
            else:
                return False
        else:
            return False
        return True


def setup(bot):
    bot.add_cog(Test(bot))
