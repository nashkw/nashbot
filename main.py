# main.py


from os import getenv, environ, execv
from sys import argv, executable
from random import choice
from dotenv import load_dotenv
from discord import Intents
from nashbot import errs, quotes, read, vars
from discord.ext.commands import is_owner, errors, Bot


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


async def safe_shutdown(ctx):
    if vars.active_menus:
        async with ctx.typing():
            while vars.active_menus:
                vars.active_menus[0].stop()
                await vars.active_menus[0].message.remove_reaction('\N{BLACK SQUARE FOR STOP}\ufe0f', bot.user)
        await read.official(ctx, 'embeds deactivated', 'x')
    if ctx.voice_client is not None:
        await ctx.invoke(bot.get_command('clearqueue'))
    await read.official(ctx, '...shutting down...', 'zzz')


@bot.command(name='shutdown', aliases=['die', 'kys'], help='shut down the bot')
@is_owner()
async def shutdown(ctx):
    await read.quote(ctx, choice(await quotes.get_shutdown_quotes(ctx)))
    await safe_shutdown(ctx)
    await bot.close()


@bot.command(name='restart', aliases=['reboot', 'refresh'], help='restart the bot')
async def restart(ctx):
    await read.quote(ctx, choice(await quotes.get_restart_quotes(ctx)))
    await safe_shutdown(ctx)
    environ['restart'] = str(ctx.channel.id)
    execv(executable, ['python'] + argv)


bot.run(TOKEN)
