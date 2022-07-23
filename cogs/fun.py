# fun.py


from random import choice, shuffle
from nashbot import errs, quotes, read, varz, resources
from itertools import cycle
from discord.ext.commands import command, Cog


class Fun(Cog, name='fun'):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🎉'
        self.skelly_spam = False

    @command(name='hi', aliases=['hello', 'howdy', 'greetings', 'salutations', 'hewwo', 'helno'], brief='greet the bot',
             help='greet the bot! hopefully itll greet u back? wt a nice lil ping pong cmd :)')
    async def hi(self, ctx):
        await read.quote(ctx, choice(await quotes.get_hi_quotes(ctx)))

    @command(name='highfive', aliases=['hifive', 'high5', 'hi5'], brief='ask the bot to give u a high five',
             help='ask the bot 4 a high five! hopefully it wont leave u hangin? wt a nice lil ping pong cmd :)')
    async def highfive(self, ctx):
        await read.quote(ctx, choice(await quotes.get_highfive_quotes(ctx)))

    @command(name='joke', aliases=['telljoke', 'bfunny', 'befunny'], brief='ask the bot to tell u a joke',
             help='ask the bot 2 tell u a joke! warning: those with bad joke allergies should proceed with caution')
    async def joke(self, ctx):
        await read.quote(ctx, choice(await quotes.get_joke_quotes(ctx)))

    @command(name='kkjoke', aliases=['knockknockjoke'], brief='ask the bot to tell u a knock knock joke',
             help='ask the bot 2 tell u a knock knock joke! remember youll have to participate tho, takes 2 2 tango :)')
    async def kkjoke(self, ctx):
        joke = choice(await quotes.get_kkjoke_quotes(ctx))
        varz.frozen_users.append(ctx.message.author.id)

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.message.author

        async def cancel(quote_bank):
            await read.quote(ctx, choice(quote_bank))
            await read.official(ctx, 'joke cancelled', 'no_entry_sign')
            varz.frozen_users.remove(ctx.message.author.id)
            return False

        async def wait_for_response(expected):
            nonsense_count = 0
            while True:
                content = resources.clean_msg(await self.bot.wait_for("message", check=check))
                if content.partition(' ')[0] in resources.get_commands(self.bot):
                    return await cancel(quotes.cmd_midcmd_quotes)
                elif content in expected:
                    return True
                elif content in quotes.welcome_activators:
                    return await cancel(quotes.welcome_quotes)
                elif content in quotes.cancel_activators:
                    if choice([True, False]):
                        return await cancel(quotes.cancel_obedient)
                    else:
                        await read.quote(ctx, choice(quotes.cancel_disobedient))
                        await read.quote(ctx, f'{ctx.message.author.name}: {choice(expected)}?')
                        return True
                else:
                    nonsense_count += 1
                    if nonsense_count >= 5:
                        return await cancel(await quotes.get_fed_up_quotes(ctx))
                    else:
                        await read.quote(ctx, choice(await quotes.get_unexpected_quotes(choice(expected))))

        await read.quote(ctx, 'knock knock')
        if not await wait_for_response(quotes.step_1_expected):
            return  # cancel joke
        await read.quote(ctx, joke[0])
        if not await wait_for_response([joke[0] + ' who', ]):
            return  # cancel joke
        await read.quote(ctx, joke[1:])
        varz.frozen_users.remove(ctx.message.author.id)

    @command(name='skellygif', aliases=['skelly', 'skeleton'], brief='ask the bot for a skeleton gif',
             help='ask 4 a skeleton gif. & if u activate the spam theyll just keep comin until u use this cmd again!',
             usage=['skellygif', 'skelly spam', 'skeleton toggle'])
    async def skellygif(self, ctx, spam: str = None):
        if self.skelly_spam:
            self.skelly_spam = False
        elif spam in quotes.spam_activators or spam is None:
            self.skelly_spam = spam
            skelly_gifs = [sgif for sgif in varz.SKELLY_PATH.glob('*.gif')]
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
        if ctx.command == self.bot.get_command('kkjoke') and ctx.message.author.id in varz.frozen_users:
            varz.frozen_users.remove(ctx.message.author.id)
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



