# fun.py


from random import choice, shuffle
from nashbot import errs, quotes, read, vars, resources
from itertools import cycle
from discord.ext.commands import command, Cog


class Fun(Cog, name='fun'):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🎉'
        self.skelly_spam = False

    @command(name='hi', aliases=['hello', 'howdy', 'greetings', 'salutations'], help='greet the bot')
    async def hi(self, ctx):
        await read.quote(ctx, choice(await quotes.get_hi_quotes(ctx)))

    @command(name='highfive', aliases=['hifive', 'high5', 'hi5'], help='ask the bot to give u a high five')
    async def highfive(self, ctx):
        await read.quote(ctx, choice(await quotes.get_highfive_quotes(ctx)))

    @command(name='joke', help='ask the bot to tell u a joke')
    async def joke(self, ctx):
        await read.quote(ctx, choice(await quotes.get_joke_quotes(ctx)))

    @command(name='kkjoke', aliases=['knockknockjoke'], help='ask the bot to tell u a knock knock joke')
    async def kkjoke(self, ctx):
        joke = choice(await quotes.get_kkjoke_quotes(ctx))
        vars.frozen_users.append(ctx.message.author.id)

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.message.author

        async def wait_for_response(expected):
            while True:
                content = resources.clean_msg(await self.bot.wait_for("message", check=check))
                if content.partition(' ')[0] in resources.get_commands(self.bot):
                    await read.quote(ctx, choice(quotes.cmd_midcmd_quotes))
                    await read.official(ctx, 'joke cancelled', 'no_entry_sign')
                    vars.frozen_users.remove(ctx.message.author.id)
                    return False  # cancel joke
                elif content in expected:
                    return True  # successful progression
                elif content in quotes.welcome_activators:
                    await read.quote(ctx, choice(quotes.welcome_quotes))
                    await read.official(ctx, 'joke cancelled', 'no_entry_sign')
                    vars.frozen_users.remove(ctx.message.author.id)
                    return False  # cancel joke
                elif content in quotes.cancel_activators:
                    if choice([True, False]):
                        await read.quote(ctx, choice(quotes.cancel_obedient))
                        await read.official(ctx, 'joke cancelled', 'no_entry_sign')
                        vars.frozen_users.remove(ctx.message.author.id)
                        return False  # cancel joke
                    else:
                        await read.quote(ctx, choice(quotes.cancel_disobedient))
                        await read.quote(ctx, f'{ctx.message.author.name}: {choice(expected)}?')
                        return True  # successful progression
                else:
                    quotes_unexpected = await quotes.get_unexpected_quotes(choice(expected))
                    await read.quote(ctx, choice(quotes_unexpected))

        await read.quote(ctx, 'knock knock')
        if not await wait_for_response(quotes.step_1_expected):
            return  # cancel joke
        await read.quote(ctx, joke[0])
        if not await wait_for_response([joke[0] + ' who', ]):
            return  # cancel joke
        await read.quote(ctx, joke[1:])
        vars.frozen_users.remove(ctx.message.author.id)

    @command(name='skellygif', aliases=['skeleton', 'skelly'], help='ask the bot for a skeleton gif')
    async def skellygif(self, ctx, spam: str = None):
        if self.skelly_spam:
            self.skelly_spam = False
        elif spam in quotes.spam_activators or spam is None:
            self.skelly_spam = spam
            skelly_gifs = [sgif for sgif in vars.SKELLY_PATH.glob('*.gif')]
            shuffle(skelly_gifs)
            for gif in cycle(skelly_gifs):
                await read.file(ctx, gif)
                if not self.skelly_spam:
                    if self.skelly_spam is not None:
                        await read.official(ctx, 'end of skeleton spam', 'skull_crossbones')
                    return
        else:
            raise errs.BadArg

    async def error_handling(self, ctx, error):
        if isinstance(error, errs.BadArg):
            if ctx.command == self.bot.get_command('skellygif'):
                await read.err(ctx, 'uh... whaa? try "skellygif spam" if thats wt u were aiming 4. or just "skellygif"')
            else:
                return False
        else:
            return False
        return True


def setup(bot):
    bot.add_cog(Fun(bot))



