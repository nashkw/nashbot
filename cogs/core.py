# core.py


from os import environ, execv
from sys import argv, executable
from random import choice
from discord import Embed, NotFound
from nashbot import quotes, read, varz, resources, errs
from discord.ext.commands import Cog, HelpCommand, command, is_owner, BadArgument


class Core(Cog, name='nashbot'):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '🛠'
        self.orig_help = bot.help_command
        bot.help_command = CustomHelp()
        bot.help_command.cog = self

    async def safe_shutdown(self, ctx):
        if varz.skelly_spam:
            varz.skelly_spam = False
        if varz.active_menus:
            await self.deactivate_embeds(ctx)
        if ctx.voice_client is not None:
            await ctx.invoke(self.bot.get_command('clearqueue'))
        await read.official(ctx, '...shutting down...', 'zzz')

    async def deactivate_embeds(self, ctx):
        async with ctx.typing():
            while varz.active_menus:
                varz.active_menus[0].stop()
                try:
                    await varz.active_menus[0].message.remove_reaction(varz.STOP_EMOJI, self.bot.user)
                except NotFound:
                    pass
        await read.official(ctx, 'embeds deactivated', 'x')

    @command(name='shutdown', aliases=['die', 'kys'], brief='shut down the bot', hidden=True,
             help='completely shut down the bot. it wont restart automatically afterwards so use w/ caution !!')
    @is_owner()
    async def shutdown(self, ctx):
        await read.quote(ctx, choice(await quotes.get_shutdown_quotes(ctx)))
        await self.safe_shutdown(ctx)
        print('\n> nashbot™ shutting down...')
        await self.bot.close()

    @command(name='restart', aliases=['reboot', 'refresh'], brief='restart the bot',
             help='restart the bot. this will deactivate all embeds, clear all music queues, etc. use w/ caution !!')
    async def restart(self, ctx):
        await read.quote(ctx, choice(await quotes.get_restart_quotes(ctx)))
        await self.safe_shutdown(ctx)
        print('\n> nashbot™ restarting...')
        environ['restart'] = str(ctx.channel.id)
        execv(executable, ['python'] + argv)

    @command(name='stopembeds', aliases=['embedstop', 'killembeds'], brief='deactivate all embeds', hidden=True,
             help='deactivate all currently active embeds')
    @is_owner()
    async def stopembeds(self, ctx):
        if varz.active_menus:
            await self.deactivate_embeds(ctx)
        else:
            await read.official(ctx, 'no active embeds', 'negative_squared_cross_mark')

    @command(name='botlink', aliases=['botadder', 'invitebot'], brief='get nashbots invite link',
             help='ask the bot to send u its invite to server link. this link can be used 2 add the bot 2 a server '
                  'u have the "manage server" permission for. note that nashbot will need admin privileges')
    async def botlink(self, ctx):
        await read.quote(ctx, choice(await quotes.get_link_quotes(ctx)))
        await read.quote(ctx, varz.BOT_INVITE_LINK)

    @command(name='serverlink', aliases=['getinvite', 'invitelink', 'inviter'], brief='get this servers invite link',
             help='ask the bot for a link u can send 2 other ppl in order 2 let them join this server. the invite '
             'youll get will never expire')
    async def serverlink(self, ctx):
        await read.quote(ctx, choice(await quotes.get_link_quotes(ctx)))
        await read.quote(ctx, await ctx.channel.create_invite())

    @command(name='purge', aliases=['flush', 'clearchannel'], brief='purge messages from the current channel',
             help='delete messages from the current text channel. u can select a user to target & ignore messages '
                  'from other users. u can also specify a number of messages to search through when purging. left '
                  'blank, this cmd will simply delete all messages in the channel', hidden=True,
             usage=['purge', 'flush nashbot™', 'clearchannel nashk 50', 'purge 100', 'flush everything'])
    @is_owner()
    async def purge(self, ctx, target: str = None, extent: int = None):
        if target:
            if target in quotes.bot_names:
                target = self.bot.user
            elif target in quotes.everyone_names:
                target = None
            elif target.isdigit() and extent is None:
                extent = int(target)
                target = None
            if target and target not in resources.get_member_variations(ctx.guild.members):
                raise errs.BadArg(message=target)
            elif target:
                target = resources.is_target_member(target)
        gone = await ctx.channel.purge(limit=extent, check=target)
        await read.official(ctx, f'removed {len(gone)} {quotes.add_s("message", gone)} from {ctx.channel.mention}', 'x')

    async def error_handling(self, ctx, error):
        if isinstance(error, BadArgument):
            if ctx.command == self.bot.get_command('purge'):
                await read.err(ctx, '...thats not how u use that cmd lol. try smth like "purge 8" or "purge [user] 12"')
            else:
                return False
        elif isinstance(error, errs.BadArg):
            if ctx.command == self.bot.get_command('purge'):
                await read.err(ctx, f'uuuuh whomst?? "{error}" isnt anyone in this server i dont think. a typo mayhap?')
            else:
                return False
        else:
            return False
        return True

    def cog_unload(self):
        self.bot.help_command = self.orig_help


def setup(bot):
    bot.add_cog(Core(bot))


class CustomHelp(HelpCommand):

    def __init__(self):
        self.COG_HELP_FOOTER = '(for more information on a command try typing "help [commandname]")'
        cmd_attrs = {
            'brief': 'show this menu',
            'help': 'show a help menu with all the cmd categories, or a more specific help message if u requested smth',
            'aliases': ['helpme', 'sendhelp'],
            'extras': {'examples': ['help', 'sendhelp music', 'helpme vote']},
        }
        super().__init__(command_attrs=cmd_attrs)

    def page_tables(self, cmds):
        p_tables = ''
        for cmdset in [[c for c in cmds if not c.hidden], [c for c in cmds if c.hidden]]:
            if cmdset:
                p_tables += quotes.get_table([[c, c.brief.lower()] for c in cmdset])
        return p_tables

    def num_cmds(self, cmds):
        n_cmds, cmds = [], [[c for c in cmds if not c.hidden], [c for c in cmds if c.hidden]]
        if cmds[0]:
            n_cmds.append(quotes.add_s(f'{len(cmds[0])} command', cmds[0]))
        if cmds[1]:
            n_cmds.append(quotes.add_s(f'{len(cmds[1])} nash-only command', cmds[1]))
        return f'({", ".join(n_cmds)})'

    async def send_bot_help(self, mapping):
        title = quotes.wrap('nashbot™ commands & curios 4 all ur earthly needs', 'sparkles')
        buttons, pages, headers, footers = ['⏏️'], [varz.BLANK], ['command categories:'], [False]
        for cog, cmds in mapping.items():
            if cmds and cog:
                buttons.append(cog.emoji)
                pages.append(self.page_tables(cmds))
                headers.append(f'{cog.emoji}　**{cog.qualified_name}**　{self.num_cmds(cmds)}')
                footers.append(self.COG_HELP_FOOTER)
        pages[0] += quotes.opt_list(headers[1:])
        await read.help_paginated(self.context, buttons, title, pages, heads=headers, foots=footers)

    async def send_cog_help(self, cog):
        e = Embed(title=quotes.wrap(f'{cog.qualified_name} commands', cog.emoji, shorthand=False))
        e.add_field(name=self.num_cmds(cog.get_commands()), value=self.page_tables(cog.get_commands()) + '\n')
        e.set_footer(text=self.COG_HELP_FOOTER)
        await read.embed(self.get_destination(), e)

    async def send_command_help(self, cmd):
        explanation = varz.BLANK + cmd.help + varz.BLANK
        e = Embed(title=quotes.wrap(f'the {cmd} command', cmd.cog.emoji, shorthand=False), description=explanation)
        if cmd.aliases:
            e.add_field(name='other names for this command:', value='> ' + '\n> '.join(cmd.aliases) + varz.BLANK)
        if cmd.usage:
            examples = '\n'.join([f'> " {example} "' for example in cmd.usage]) + varz.BLANK
            e.add_field(name='examples of how to use this command: ', value=examples)
        if cmd.hidden:
            e.set_footer(text='(warning: this is a nash-only command, unusable by everyone else)')
        await read.embed(self.get_destination(), e)

    async def send_error_message(self, error):
        await read.err(self.context, 'umm ' + error.lower() + '.. srry man :|')

