# nashbot.py


import os
import random
import discord
from dotenv import load_dotenv
from discord.ext import commands
import cog_jokes
import cog_music
from quotes import *


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class CustomHelp(commands.HelpCommand):
    async def send_bot_help(self, mapping):
        channel = self.get_destination()
        embed = discord.Embed(title=':sparkles: nashbot™ commands & curios 4 all ur earthly needs :sparkles:')
        for map_cog, map_cmds in mapping.items():
            v = get_table([[cmd, cmd.help] for cmd in map_cmds if not cmd.hidden])
            v = f"```\n{v}\n```"
            if map_cog:
                embed.add_field(name=map_cog.qualified_name, value=v, inline=False)
            else:
                embed.add_field(name='misc', value=v, inline=False)
        await read_embed(channel, embed)


bot = commands.Bot(
    command_prefix='',
    intents=discord.Intents.default(),
    help_command=CustomHelp()
)

cogs = [cog_jokes, cog_music]
for cog in cogs:
    cog.setup(bot)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to discord')


@bot.event
async def on_disconnect():
    print(f'{bot.user.name} has disconnected from discord')


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        f.write(f'unhandled error: {args[0]}\n\n')
    print(f'error logged to err.log: {args[0]}\n')


@bot.command(name='hi', aliases=['hello', 'howdy', 'greetings', 'salutations'], help='greet the bot')
async def hi(ctx):
    await read_quote(ctx, random.choice(await get_hi_quotes(ctx)))


@bot.command(name='highfive', aliases=['hifive', 'high5', 'hi5'], help='ask the bot to give u a high five')
async def highfive(ctx):
    await read_quote(ctx, random.choice(await get_highfive_quotes(ctx)))


@bot.command(name='shutdown', aliases=['die', 'kys'], help='shut down the bot')
async def shutdown(ctx):
    await read_quote(ctx, random.choice(await get_shutdown_quotes(ctx)))
    if ctx.voice_client is not None:
        await ctx.invoke(bot.get_command('clearqueue'))
    await read_official(ctx, '...shutting down...', 'zzz')
    await bot.close()


bot.run(TOKEN)