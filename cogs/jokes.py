# jokes.py


from random import choice
from nashbot import quotes, read, resources, vars
from discord.ext import commands


class Jokes(commands.Cog, name='jokes'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='joke', help='ask the bot to tell u a joke')
    async def joke(self, ctx):
        await read.quote(ctx, choice(await quotes.get_joke_quotes(ctx)))

    @commands.command(name='kkjoke', aliases=['knockknockjoke'], help='ask the bot to tell u a knock knock joke')
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

    async def error_handling(self, ctx, error):
        return False


def setup(bot):
    bot.add_cog(Jokes(bot))



