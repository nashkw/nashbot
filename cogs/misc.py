# misc.py


import random
import discord
from quotes import *
from resources import *


class Misc(commands.Cog, name='misc'):

    def __init__(self, bot):
        self.bot = bot

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

    @commands.command(name='vote', aliases=['poll'], help='set up a vote from a list of options')
    async def vote(self, ctx, subject: str, *, opts: str):
        embed = discord.Embed(title=subject, description='react with the matching emoji to vote :)')
        emojis = random.choice(list(emoji_sets.values()))
        v = [f'{emoji} : {opt}' for opt, emoji in zip(opts.split(', '), emojis)]
        embed.add_field(name='\u200b', value='\n\u200b\n'.join(v))
        msg = await read_embed(ctx, embed)
        for i in range(len(v)):
            await msg.add_reaction(emojis[i])

    async def error_handling(self, ctx, error):
        if isinstance(error, BadArg):
            if ctx.command == self.bot.get_command('random'):
                await read_error(ctx, '2 use this cmd u gotta give the range 2 choose from. like "random 2-8" or smth')
            else:
                return False
        elif isinstance(error, commands.MissingRequiredArgument):
            if ctx.command == self.bot.get_command('random'):
                await read_error(ctx, '2 use this cmd u gotta give the range 2 choose from or the type of dice or smth')
            else:
                return False
        else:
            return False
        return True


def setup(bot):
    bot.add_cog(Misc(bot))
