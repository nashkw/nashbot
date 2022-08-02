# debug.py


from os import listdir, path
from emoji import emojize
from random import randint
from discord import Embed, HTTPException
from nashbot import errs, quotes, read, resources, menus, varz
from discord.ext.commands import is_owner, command, MissingRequiredArgument, Cog


class Debug(Cog, name='debug'):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🔬'

    async def test_eset(self, ctx, emoji_set, name):
        egroups = [emoji_set[i:i + 20] for i in range(0, len(emoji_set), 20)]
        for group in egroups:
            embed = Embed(title=name, description='testing testing')
            msg = await read.embed(ctx, embed)
            for e in group:
                try:
                    await msg.add_reaction(emojize(e, language='alias'))
                except HTTPException:
                    await read.quote(ctx, f'warning: the emoji "{e}" is not reaction safe')

    @command(name='emojisets', aliases=['esets', 'eset'], brief='test emoji sets in reactions', hidden=True,
             help='test all emoji sets in reaction form 2 confirm they can b successfully converted to unicode',
             usage=['emojisets', 'eset hearts'])
    @is_owner()
    async def emojisets(self, ctx, eset_n: str = None):
        if eset_n:
            if eset_n in quotes.emoji_sets:
                await self.test_eset(ctx, quotes.emoji_sets[eset_n], eset_n)
            else:
                raise errs.FailedSearch
        else:
            for k, eset in quotes.emoji_sets.items():
                await self.test_eset(ctx, eset, k)

    @command(name='msgtruth', aliases=['mtrue', 'etrue'], brief='test the true form of a message', hidden=True,
             help='read back the contents of the users message, separating it out into a list of characters',
             usage=['msgtruth greetingz 🤡', 'mtrue hello there <@985864214260371476>', 'etrue ❤️🧡💛💚💙💜'])
    @is_owner()
    async def msgtruth(self, ctx, *, m: str):
        await read.quote(ctx, f"```unaltered: {m}\nlist of characters: {list(m)}```")

    @command(name='dlforget', aliases=['dlsforget', 'forgetdl'], brief='remove music download history', hidden=True,
             help='clear the list of previously downloaded music that the downloader uses to dynamically skip songs it '
                  'has already downloaded')
    @is_owner()
    async def dlforget(self, ctx):
        try:
            varz.DOWNLOADS_LOG_PATH.unlink()
            await read.official(ctx, 'downloads log successfully cleared', 'white_check_mark')
        except FileNotFoundError:
            await read.official(ctx, 'downloads log already empty', 'negative_squared_cross_mark')

    @command(name='dlpurge', aliases=['dlspurge', 'purgedl'], brief='remove downloaded music', hidden=True,
             help= 'purge music downloads. u can specify a folder to delete, or tell the bot to remove the most '
                   'recently downloaded folder. if u dont specify anything all contents of the music downloads folder '
                   'will b wiped (meaning any music that hasnt already been moved elsewhere will b permanently deleted '
                   'so use w/ caution !!!)',
             usage=['dlpurge', 'dlspurge all', 'purgedl Daft Punk (Alive 2007)', 'dlpurge newest'])
    @is_owner()
    async def dlpurge(self, ctx, *, target: str = ''):
        downloaded = listdir(varz.DOWNLOADS_PATH)
        if not downloaded:
            target = None
        elif target in quotes.all_contents_names or target == '':
            target = ''
        elif target in quotes.latest_names:
            target = path.basename(max([varz.DOWNLOADS_PATH / item for item in downloaded], key=path.getmtime))
        elif target not in downloaded:
            raise errs.FailedSearch

        folder = target if target else 'downloads'
        if target is not None and resources.empty_folder(varz.DOWNLOADS_PATH / target, delete_after=target):
            await read.official(ctx, f'{folder} folder successfully cleared', 'white_check_mark')
        else:
            await read.official(ctx, f'{folder} folder already empty', 'negative_squared_cross_mark')

    @command(name='quizresult', aliases=['quizres', 'quizzed'], brief='view a result of a nashbot™ quiz', hidden=True,
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
            elif ctx.command == self.bot.get_command('dlpurge'):
                await read.err(ctx, 'uuuh thats not the name of a downloaded folder, srry man. check 4 typos maybe ??')
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
    bot.add_cog(Debug(bot))
