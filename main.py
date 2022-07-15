# main.py

import os
import sys
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
from nashbot import errs, quotes, read, resources, vars


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class CustomHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        embed = discord.Embed(title=quotes.wrap('nashbot™ commands & curios 4 all ur earthly needs', 'sparkles'))
        for map_cog, map_cmds in mapping.items():
            if not (map_cog and map_cog.qualified_name == 'tests'):
                v = f"```\n{quotes.get_table([[cmd, cmd.help] for cmd in map_cmds if not cmd.hidden])}\n```"
                if map_cog:
                    embed.add_field(name=map_cog.qualified_name, value=v, inline=False)
                else:
                    embed.add_field(name='nashbot™', value=v.lower(), inline=False)
        await read.embed(self.get_destination(), embed)


bot = commands.Bot(
    command_prefix='',
    intents=discord.Intents.default(),
    help_command=CustomHelp()
)

for cog in [path.stem for path in vars.COGS_PATH.glob('*.py')]:
    bot.load_extension(f'cogs.{cog}')


@bot.event
async def on_ready():
    if 'restart' in os.environ:
        print('\nnashbot™ restarted successfully')
        await bot.get_channel(int(os.environ.pop('restart'))).send(quotes.wrap('...powering up...', 'zap'))
    print('nashbot™ has connected to discord')


@bot.event
async def on_disconnect():
    print('nashbot™ has disconnected from discord')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, errs.GlobalCheckFailure):
        return
    elif isinstance(error, commands.errors.CommandNotFound):
        return
    elif isinstance(error, errs.NotNash):
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
@resources.is_nash()
async def shutdown(ctx):
    await read.quote(ctx, random.choice(await quotes.get_shutdown_quotes(ctx)))
    await safe_shutdown(ctx)
    await bot.close()


@bot.command(name='restart', aliases=['reboot', 'refresh'], help='restart the bot')
async def restart(ctx):
    await read.quote(ctx, random.choice(await quotes.get_restart_quotes(ctx)))
    await safe_shutdown(ctx)
    os.environ['restart'] = str(ctx.channel.id)
    os.execv(sys.executable, ['python'] + sys.argv)


bot.run(TOKEN)
