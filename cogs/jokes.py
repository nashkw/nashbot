# jokes.py


import random
from quotes import *
from resources import *


class Jokes(commands.Cog, name='jokes'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='joke', help='ask the bot to tell u a joke')
    async def joke(self, ctx):
        await read_quote(ctx, random.choice(await get_joke_quotes(ctx)))

    @commands.command(name='kkjoke', aliases=['knockknockjoke'], help='ask the bot to tell u a knock knock joke')
    async def kkjoke(self, ctx):
        quotes = random.choice(await get_kkjoke_quotes(ctx))
        frozen_users.append(ctx.message.author.id)

        def check(m):
            return m.channel == ctx.channel and m.author == ctx.message.author

        async def wait_for_response(expected):
            while True:
                content = clean_msg(await self.bot.wait_for("message", check=check))
                if content.partition(' ')[0] in get_commands(self.bot):
                    await read_quote(ctx, random.choice(cmd_midcmd_quotes))
                    await read_official(ctx, 'joke cancelled', 'no_entry_sign')
                    frozen_users.remove(ctx.message.author.id)
                    return False  # cancel joke
                elif content in expected:
                    return True  # successful progression
                elif content in welcome_activators:
                    await read_quote(ctx, random.choice(welcome_quotes))
                    await read_official(ctx, 'joke cancelled', 'no_entry_sign')
                    frozen_users.remove(ctx.message.author.id)
                    return False  # cancel joke
                elif content in cancel_activators:
                    if random.choice([True, False]):
                        await read_quote(ctx, random.choice(cancel_obedient))
                        await read_official(ctx, 'joke cancelled', 'no_entry_sign')
                        frozen_users.remove(ctx.message.author.id)
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
        frozen_users.remove(ctx.message.author.id)

    async def error_handling(self, ctx, error):
        return False


def setup(bot):
    bot.add_cog(Jokes(bot))



