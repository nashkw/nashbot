# misc.py


from emoji import emojize
from random import choice, randint
from nashbot import errs, quotes, read, varz
from discord import Embed, HTTPException
from discord.ext.commands import command, Cog, MissingRequiredArgument


class Misc(Cog, name='misc'):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '📜'

    @command(name='random', aliases=['rand', 'dice', 'rolldice'], brief='ask the bot to pick a random number',
             help='ask the bot 4 a random number, either by picking from a range or by simulating dice rolls',
             usage=['random 8', 'rand 3-27', 'dice d6', 'rolldice 4 d8'])
    async def random(self, ctx, *, arg: str):
        if arg.isdigit():
            result = [f'randomly selecting in range 1-{arg}', randint(1, int(arg))]
        elif len(arg.split('-')) == 2 and arg.split('-')[0].isdigit() and arg.split('-')[1].isdigit():
            params = [int(s) for s in arg.split('-')]
            result = [f'randomly selecting in range {arg}', randint(params[0], params[1])]
        elif arg.replace('1 d', 'd').replace('d', '').isdigit():
            arg = arg.replace('1 d', 'd')
            result = [f'rolling a {arg}', randint(1, int(arg.replace('d', '')))]
        elif arg.split(' d')[0].isdigit() and arg.split(' d')[1].isdigit():
            params = [int(arg.split(' d')[0]), int(arg.split(' d')[1])]
            result = [f'rolling {arg}', ', '.join([str(randint(1, params[1])) for i in range(params[0])])]
        else:
            raise errs.BadArg
        await read.official(ctx, f'{result[0]} to get...　**{result[1]}**', 'game_die')

    @command(name='vote', aliases=['poll', 'survey', 'callvote'], brief='set up a vote with a list of possible choices',
             help='set up a vote on a subject of ur choice, listing all the possible options to vote on. b careful 2 '
                  'enclose the subject in quotes if its more than 1 word otheriwse itll get confused w/ the options '
                  'list. b careful 2 separate the options list with commas otherwise it wont b recognised',
             usage=['vote proceed? yes, no', "poll 'when yall free?' wed,thurs,fri", 'survey "wt game??" dst, mc, l4d'])
    async def vote(self, ctx, subject: str, *, opts: str):
        opts = opts.replace(', ', ',').split(',')
        valid_sets = [eset for eset in quotes.emoji_sets.values() if len(eset) >= len(opts)]
        if valid_sets and len(opts) <= 20:
            emojis = choice(valid_sets)
            e = Embed(title=quotes.wrap(subject, 'grey_question'))
            e.add_field(name=varz.BLANK, value=quotes.opt_list(opts, emojis=emojis))
            e.set_footer(text='(click the matching emoji to vote)')
            msg = await read.embed(ctx, e)
            for i in range(len(opts)):
                try:
                    await msg.add_reaction(emojize(emojis[i], language='alias'))
                except HTTPException:
                    await read.err(ctx, f'warning: the emoji "{emojis[i]}" is not reaction safe')
        else:
            raise errs.BadArg

    async def error_handling(self, ctx, error):
        if isinstance(error, errs.BadArg):
            if ctx.command == self.bot.get_command('random'):
                await read.err(ctx, '2 use this cmd u gotta give the range 2 choose from. like "random 2-8" or smth')
            elif ctx.command == self.bot.get_command('vote'):
                await read.err(ctx, 'yo thats 2 many options my guy my fella, max number is 20 :|')
            else:
                return False
        elif isinstance(error, MissingRequiredArgument):
            if ctx.command == self.bot.get_command('random'):
                await read.err(ctx, '2 use this cmd u gotta give the range 2 choose from or the type of dice or smth')
            elif ctx.command == self.bot.get_command('vote'):
                await read.err(ctx, '2 use this cmd u gotta give the subject & then a comma seperated list of options')
            else:
                return False
        else:
            return False
        return True


def setup(bot):
    bot.add_cog(Misc(bot))
