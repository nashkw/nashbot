# core.py


from os import environ, execv
from sys import argv, executable
from random import choice
from nashbot import quotes, read, vars
from discord.ext.commands import Cog, HelpCommand, command, is_owner


class CustomHelp(HelpCommand):
    async def send_bot_help(self, mapping):
        title = quotes.wrap('nashbot™ commands & curios 4 all ur earthly needs', 'sparkles')
        buttons, pages, headers = ['⏏️'], [[]], ['command categories:']
        for i, (cog, cmds) in enumerate(mapping.items()):
            if cmds and cog:
                cmds = [[c for c in cmds if not c.hidden], [c for c in cmds if c.hidden]]
                if cmds[0]:
                    p = f"```\n{quotes.get_table([[c, c.help.lower()] for c in cmds[0]])}\n"
                    n_cmds = f'{len(cmds[0])} commands' if len(cmds[0]) > 1 else f'{len(cmds[0])} command'
                else:
                    p = '```\n'
                    n_cmds = ''
                if cmds[1]:
                    p += f"{quotes.get_table([[c, c.help.lower()] for c in cmds[1]])}\n```"
                    n_only = f' nash-only commands' if len(cmds[1]) > 1 else f' nash-only command'
                    n_cmds += f', {len(cmds[1])}{n_only}' if n_cmds else f'{len(cmds[1])}{n_only}'
                else:
                    p += '```'

                buttons.append(cog.emoji)
                pages.append(p)
                headers.append(f'{cog.emoji}　**{cog.qualified_name}**　({n_cmds})')
        pages[0] = '\n\u200b\n' + quotes.opt_list(headers[1:])
        await read.help_paginated(self.context, buttons, title, pages, headers=headers)


class Core(Cog, name='nashbot™'):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🛠'
        self.orig_help = bot.help_command
        bot.help_command = CustomHelp()
        bot.help_command.cog = self

    async def safe_shutdown(self, ctx):
        if vars.active_menus:
            async with ctx.typing():
                while vars.active_menus:
                    vars.active_menus[0].stop()
                    await vars.active_menus[0].message.remove_reaction('\N{BLACK SQUARE FOR STOP}\ufe0f', self.bot.user)
            await read.official(ctx, 'embeds deactivated', 'x')
        if ctx.voice_client is not None:
            await ctx.invoke(self.bot.get_command('clearqueue'))
        await read.official(ctx, '...shutting down...', 'zzz')

    @command(name='shutdown', aliases=['die', 'kys'], help='shut down the bot')
    @is_owner()
    async def shutdown(self, ctx):
        await read.quote(ctx, choice(await quotes.get_shutdown_quotes(ctx)))
        await self.safe_shutdown(ctx)
        await self.bot.close()

    @command(name='restart', aliases=['reboot', 'refresh'], help='restart the bot')
    async def restart(self, ctx):
        await read.quote(ctx, choice(await quotes.get_restart_quotes(ctx)))
        await self.safe_shutdown(ctx)
        environ['restart'] = str(ctx.channel.id)
        execv(executable, ['python'] + argv)

    async def error_handling(self, ctx, error):
        return False

    def cog_unload(self):
        self.bot.help_command = self.orig_help


def setup(bot):
    bot.add_cog(Core(bot))

