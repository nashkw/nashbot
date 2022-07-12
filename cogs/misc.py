# misc.py


import os
import emoji
import random
import discord
from itertools import cycle
from quotes import *
from resources import *


class Misc(commands.Cog, name='misc'):

    def __init__(self, bot):
        self.bot = bot
        self.skelly_spam = False

    @commands.command(name='hi', aliases=['hello', 'howdy', 'greetings', 'salutations'], help='greet the bot')
    async def hi(self, ctx):
        await read_quote(ctx, random.choice(await get_hi_quotes(ctx)))

    @commands.command(name='highfive', aliases=['hifive', 'high5', 'hi5'], help='ask the bot to give u a high five')
    async def highfive(self, ctx):
        await read_quote(ctx, random.choice(await get_highfive_quotes(ctx)))

    @commands.command(name='random', aliases=['dice', 'rolldice'], help='ask the bot to pick a random number')
    async def random(self, ctx, *, arg: str):
        if arg.isdigit():
            result = [f'randomly selecting in range 1-{arg}', random.randint(1, int(arg))]
        elif len(arg.split('-')) == 2 and arg.split('-')[0].isdigit() and arg.split('-')[1].isdigit():
            params = [int(s) for s in arg.split('-')]
            result = [f'randomly selecting in range {arg}', random.randint(params[0], params[1])]
        elif arg.replace('1 d', 'd').replace('d', '').isdigit():
            arg = arg.replace('1 d', 'd')
            result = [f'rolling a {arg}', random.randint(1, int(arg.replace('d', '')))]
        elif arg.split(' d')[0].isdigit() and arg.split(' d')[1].isdigit():
            params = [int(arg.split(' d')[0]), int(arg.split(' d')[1])]
            result = [f'rolling {arg}', ', '.join([str(random.randint(1, params[1])) for i in range(params[0])])]
        else:
            raise BadArg
        await read_official(ctx, f'{result[0]} to get...   **{result[1]}**', 'game_die')

    @commands.command(name='vote', aliases=['poll'], help='set up a vote with a list of possible choices')
    async def vote(self, ctx, subject: str, *, opts: str):
        opts = opts.replace(', ', ',').split(',')
        valid_sets = [eset for eset in emoji_sets.values() if len(eset) >= len(opts)]
        if valid_sets and len(opts) <= 20:
            emojis = random.choice(valid_sets)
            v = [f'{e} : {opt}' for opt, e in zip(opts, emojis)]
            embed = discord.Embed(title=subject, description='react with the matching emoji to vote :)')
            embed.add_field(name='\u200b', value='\n\u200b\n'.join(v) + '\n\u200b')
            msg = await read_embed(ctx, embed)
            for i in range(len(v)):
                try:
                    await msg.add_reaction(emoji.emojize(emojis[i], language='alias'))
                except discord.HTTPException:
                    await read_err(ctx, f'warning: the emoji "{emojis[i]}" is not reaction safe')
        else:
            raise BadArg

    @commands.command(name='skellygif', aliases=['skeleton', 'skelly'], help='ask the bot for a skeleton gif')
    async def skellygif(self, ctx, spam: str = None):
        if self.skelly_spam:
            self.skelly_spam = False
        elif spam in spam_activators or spam is None:
            self.skelly_spam = spam
            skelly_gifs = [SKELLY_PATH + file for file in os.listdir(SKELLY_PATH) if file.endswith('.gif')]
            random.shuffle(skelly_gifs)
            for gif in cycle(skelly_gifs):
                await read_file(ctx, gif)
                if not self.skelly_spam:
                    if self.skelly_spam is not None:
                        await read_official(ctx, 'end of skeleton spam', 'skull_crossbones')
                    return
        else:
            raise BadArg

    async def error_handling(self, ctx, error):
        if isinstance(error, BadArg):
            if ctx.command == self.bot.get_command('random'):
                await read_err(ctx, '2 use this cmd u gotta give the range 2 choose from. like "random 2-8" or smth')
            elif ctx.command == self.bot.get_command('vote'):
                await read_err(ctx, 'yo thats 2 many options my guy my fella, max number is 20 :|')
            elif ctx.command == self.bot.get_command('skellygif'):
                await read_err(ctx, 'uh... whaa? try "skellygif spam" if thats wt u were aiming 4. or just "skellygif"')
            else:
                return False
        elif isinstance(error, commands.MissingRequiredArgument):
            if ctx.command == self.bot.get_command('random'):
                await read_err(ctx, '2 use this cmd u gotta give the range 2 choose from or the type of dice or smth')
            elif ctx.command == self.bot.get_command('vote'):
                await read_err(ctx, '2 use this cmd u gotta give the subject & then a comma seperated list of options')
            else:
                return False
        else:
            return False
        return True


def setup(bot):
    bot.add_cog(Misc(bot))
