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

        async def force_continue(quote_bank, expected):
            await read.quote(ctx, choice(quote_bank))
            await read.quote(ctx, f'{ctx.message.author.name}: {choice(expected)}?')
            return True

        async def wait_for_response(expected):
            nonsense_count = 0
            while True:
                content = resources.clean_msg(await self.bot.wait_for("message", check=check))
                if content.partition(' ')[0] in resources.get_commands(self.bot):
                    return await cancel(quotes.cmd_midcmd_quotes)
                elif content in expected:
                    return True
                elif content in quotes.kkjoke_confused or content in quotes.step_1_expected:
                    return await force_continue(quotes.kkjoke_pity_continue, expected)
                elif content in quotes.welcome_activators:
                    return await cancel(quotes.welcome_quotes)
                elif content in quotes.cancel_activators:
                    if choice([True, False]):
                        return await cancel(quotes.cancel_obedient)
                    else:
                        return await force_continue(quotes.cancel_disobedient, expected)
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

    @command(name='skellygif', aliases=['skelly', 'skeleton', 'skellyspam'], brief='ask the bot for a skeleton gif',
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

    @command(name='quiz', aliases=['takequiz', 'doquiz', 'quizme'], brief='take one of the nashbot™ quizzes',
             help='take a nashbot™ quiz! ull get a random quiz if u dont specify anything, but u can pick a quiz by '
                  'either its name or index (found via the quizlist cmd). u can also specify a quiz type to randomly '
                  'select a quiz from (again, check the quizlist cmd to find options)',
             usage=['quiz', 'takequiz 2', 'doquiz uwu', 'quizme uwu vibeomatic', 'quiz meme'])
    async def quiz(self, ctx, *, quiz=None):
        if quiz is None:
            quiz = choice(resources.get_quizzes())[1]
        elif quiz.isdigit():
            indexes = [q[0] for q in resources.get_quizzes()]
            if int(quiz) in indexes:
                quiz = resources.get_quizzes().pop(indexes.index(int(quiz)))[1]
            else:
                raise errs.BadArg
        else:
            for attr in ['type', 'name', 'nickname']:
                if quiz in [q[2][attr] for q in resources.get_quizzes()]:
                    quiz = choice([q[1] for q in resources.get_quizzes() if q[2][attr] == quiz])
                    break
            else:
                if quiz not in [q[1] for q in resources.get_quizzes()]:
                    raise errs.FailedSearch
        await read.quiz(ctx, quiz)

    @command(name='quizlist', aliases=['quizzes', 'showquizzes'], brief='show all available nashbot™ quizzes',
             help='show all available nashbot™ quizzes, their types, & their indexes (4 use in the quiz cmd)')
    async def quizlist(self, ctx):
        fill = resources.table_paginate(resources.get_quizzes(simple=True), 10, head=['index', 'quiz name', 'type'])
        await read.paginated(ctx, quotes.wrap('nashbot™ quizzical questions 4 fun & profit', 'brain'), fill)

    async def error_handling(self, ctx, error):
        if ctx.command == self.bot.get_command('kkjoke') and ctx.message.author.id in varz.frozen_users:
            varz.frozen_users.remove(ctx.message.author.id)
        elif isinstance(error, errs.FailedSearch):
            if ctx.command == self.bot.get_command('quiz'):
                await read.err(ctx, 'theres no quiz w/ that name srry, & thats not a quiz type either. a typo maybe??')
            else:
                return False
        elif isinstance(error, errs.BadArg):
            if ctx.command == self.bot.get_command('skellygif'):
                await read.err(ctx, 'uh... whaa? try "skellygif spam" if thats wt u were aiming 4. or just "skellygif"')
            elif ctx.command == self.bot.get_command('quiz'):
                await read.err(ctx, 'invalid index buddy. here, find the index w/ this list & try again')
                await ctx.invoke(self.bot.get_command('quizlist'))
            else:
                return False
        else:
            return False
        return True


def setup(bot):
    bot.add_cog(Fun(bot))



