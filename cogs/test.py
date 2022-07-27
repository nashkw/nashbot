# test.py


from emoji import emojize
from random import randint
from discord import Embed, HTTPException
from nashbot import errs, quotes, read, resources, menus
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

    @command(name='quizresult', aliases=['quizres', 'quizzed'], brief='test a result of a nashbot™ quiz', hidden=True,
             help='generate the result to a given quiz (quiz can b specified in all the same ways as it can b in the '
                  'quiz cmd - namely by name, index, or type. if ur specification is more than 1 word remember 2 '
                  'enclose it in quotes otherwise itll get confused w/ ur target result). if u dont specify which '
                  'result u want all percentages will b randomly generated, but u can specify a target result by '
                  'either index or name (u can check these via the quizresults cmd)',
             usage=['quizresult weather', 'quizres meme', 'quizzed "mushroom soulmate" 3', 'quizresult uwu rawr xd'])
    @is_owner()
    async def quizresult(self, ctx, quiz: str, *, result=None):
        quiz = resources.get_quiz_name(quiz)
        menu = menus.QuizPages(quiz, clear_reactions_after=True)
        menu.ctx = ctx
        tally = [[randint(0, menu.info['max_result'] - 1), res] for res in menu.results]
        if result is not None:
            if result.isdigit():
                result = int(result) - 1
            elif result in [res[0] for res in menu.results]:
                result = [res[0] for res in menu.results].index(result)
            else:
                raise errs.FailedSearch(message=f'result named "{result}" in the {quiz} quiz')
            if 0 <= result < len(menu.results):
                tally[result] = [menu.info['max_result'], tally[result][1]]
            else:
                raise errs.BadArg(message='quizresults')
        await read.embed(ctx, menu.get_result(tally))

    @command(name='quizresults', aliases=['quizreslist'], brief='list all possible results of a quiz', hidden=True,
             help='show a list of all possible results 4 the specified nashbot™ quiz. u can specify a quiz the same '
                  'way u would 4 the quiz cmd, namely by giving its name or index (check the quizlist cmd 2 find '
                  'these). if u specify by type all quizzes of that type will b selected. if u dont specify anything '
                  'u will see lists of results for all avaliable nashbot™ quizzes',
             usage=['quizresults', 'quizreslist mushroom soulmate', 'quizresults meme'])
    @is_owner()
    async def quizresults(self, ctx, *, quiz: str = None):
        if quiz is None:
            quiz_list = [q[1] for q in resources.get_quizzes()]
        else:
            quiz_list = resources.get_quiz_name(quiz, return_list=True)
        pages = [quotes.get_table([[i + 1, r[0]] for i, r in enumerate(quotes.quizzes[q][2])]) for q in quiz_list]
        quiz_list = [quotes.wrap(q, quotes.quizzes[q][0]['emoji'], both=False) for q in quiz_list]
        await read.paginated(ctx, quotes.wrap('possible nashbot™ quiz results', 'brain'), pages, heads=quiz_list)

    async def error_handling(self, ctx, error):
        if isinstance(error, errs.FailedSearch):
            if ctx.command == self.bot.get_command('emojisets'):
                await read.err(ctx, 'uuuh thats not the name of an emoji set, srry man. check 4 typos maybe ??')
            elif ctx.command in {self.bot.get_command('quizresult'), self.bot.get_command('quizresults')}:
                await read.err(ctx, f'soooo theres no {error}. srry man idk wt 2 say. check 4 typos maybe ??')
            else:
                return False
        elif isinstance(error, errs.BadArg):
            if ctx.command in {self.bot.get_command('quizresult'), self.bot.get_command('quizresults')}:
                await read.err(ctx, f'yikes, invalid index buddy. maybe check it against the {error} cmd first ??')
            else:
                return False
        elif isinstance(error, MissingRequiredArgument):
            if ctx.command == self.bot.get_command('msgtruth'):
                await read.err(ctx, '2 use this cmd u gotta give some input 2 test my man my jester my fool :)')
            elif ctx.command == self.bot.get_command('quizresult'):
                await read.err(ctx, '2 use this cmd u gotta give the name (or index or type or wtever) of the quiz!!')
            else:
                return False
        else:
            return False
        return True


def setup(bot):
    bot.add_cog(Test(bot))
