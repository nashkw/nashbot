# cog_jokes.py


import random
from discord.ext import commands
from quotes import *


class Jokes(commands.Cog, name='jokes'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='joke', help='ask the bot to tell u a joke')
    async def joke(self, ctx):
        await read_quote(ctx, random.choice(await get_joke_quotes(ctx)))

    @commands.command(name='kkjoke', help='ask the bot to tell u a knock knock joke')
    async def kkjoke(self, ctx):
        quotes = random.choice(await get_kkjoke_quotes(ctx))

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.message.author

        def clean_msg(m):
            return m.content.lower().replace('?', '').replace('...', '').replace(' :)', '').strip()

        async def wait_for_response(expected):
            while True:
                content = clean_msg(await bot.wait_for("message", check=check))
                if content in expected:
                    return True  # successful progression
                elif content in welcome_responses:
                    await read_quote(ctx, random.choice(welcome_quotes))
                    await read_quote(ctx, ':no_entry_sign: joke cancelled :no_entry_sign:')
                    return False  # cancel joke
                elif content in cancel_responses:
                    if random.choice([True, False]):
                        await read_quote(ctx, random.choice(cancel_obedient))
                        await read_quote(ctx, ':no_entry_sign: joke cancelled :no_entry_sign:')
                        return False  # cancel joke
                    else:
                        await read_quote(ctx, random.choice(cancel_disobedient))
                        await read_quote(ctx, f'{ctx.message.author.name}: {random.choice(expected)}?')
                        return True  # successful progression
                else:
                    quotes_unexpected = await get_unexpected_quotes(random.choice(expected))
                    await read_quote(ctx, random.choice(quotes_unexpected))

        await read_quote(ctx, 'knock knock')
        if not await wait_for_response(step_1_expected):
            return  # cancel joke
        await read_quote(ctx, quotes[0])
        if not await wait_for_response([quotes[0] + ' who', ]):
            return  # cancel joke
        await read_quote(ctx, quotes[1:])


def setup(bot):
    bot.add_cog(Jokes(bot))



