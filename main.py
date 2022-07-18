# main.py


from os import getenv, environ
from dotenv import load_dotenv
from discord import Intents
from nashbot import errs, quotes, read, vars
from discord.ext.commands import errors, Bot


load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')


bot = Bot(
    command_prefix='',
    intents=Intents.default(),
    owner_ids={386921492601896961, 727183720628486306, 757917569058603066},
)

for cog in [path.stem for path in vars.COGS_PATH.glob('*.py')]:
    bot.load_extension(f'cogs.{cog}')


@bot.event
async def on_ready():
    if 'restart' in environ:
        print('\nnashbot™ restarted successfully')
        await bot.get_channel(int(environ.pop('restart'))).send(quotes.wrap('...powering up...', 'zap'))
    print('nashbot™ has connected to discord')


@bot.event
async def on_disconnect():
    print('nashbot™ has disconnected from discord')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, errs.GlobalCheckFailure):
        return
    elif isinstance(error, errors.CommandNotFound):
        return
    elif isinstance(error, errors.NotOwner):
        await read.err(ctx, 'afraid this is a nash only cmd buddy. ur only hope is identity theft')
        return
    elif ctx.cog:
        if await ctx.cog.error_handling(ctx, error):
            return
    await read.err(ctx, f'unhandled error: {str(error)}')
    print(f'\n\n#####　UNHANDLED ERROR:　{str(error)}　#####\n\n')
    raise error


@bot.check
def check_commands(ctx):
    if ctx.message.author.id in vars.frozen_users:
        raise errs.GlobalCheckFailure
    return True


bot.run(TOKEN)
