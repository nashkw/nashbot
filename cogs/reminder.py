# reminder.py


from pymongo import DESCENDING
from discord import TextChannel
from nashbot import read, errs, quotes
from database import r_db
from datetime import datetime
from discord.ext import tasks
from dateutil.parser import parse, ParserError
from dpytools.parsers import to_timedelta
from dpytools.errors import InvalidTimeString
from discord.ext.commands import Cog, command, MissingRequiredArgument, is_owner, ChannelNotFound, BadArgument


class Reminder(Cog, name='reminder'):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '⏰'
        self.db = r_db.reminders
        self.archive = r_db.reminders_archive
        self.reminder_loop.start()

    async def del_entry(self, entry, now):
        await self.db.delete_one({'_id': entry['_id']})
        entry['deleted'] = now
        await self.archive.insert_one(entry)

    @tasks.loop(minutes=1)
    async def reminder_loop(self):
        await self.bot.wait_until_ready()
        async for r in self.db.find({'time': {'$lte': (now := datetime.now())}}):
            channel, user = self.bot.get_channel(r['channel']), await self.bot.fetch_user(r['user'])
            await read.official(channel, f'{user.mention} {r["msg"]}', 'alarm_clock')
            if (time := r['repeat']) is not False:
                await self.db.update_one({'_id': r['_id']}, {'$set': {'time': now + to_timedelta(time)}})
            else:
                await self.del_entry(r, now)

    @command(name='setreminder', aliases=['remindme', 'reminder', 'rset'], brief='set a reminder in this channel',
             help='set a reminder in this channel. 1st ull need 2 give a message - it can b anything including emojis '
                  'or mentions, but remember 2 enclose it in quotation marks if it includes a space cus otherwise itll '
                  'get mixed up w/ the time. the time should b given 2nd, & can either b relative ("15m" will b '
                  'interpreted as 15min from now) or absolute (such as "8:25am 16th august"). the bot will do its best '
                  '2 interpret ur input but try & b as clear as possible 2 avoid miscommunication !! note that '
                  'reminders will only b accurate 2 the minute so specifying seconds tends 2 b irrelevant',
             usage=['setreminder games 1h30m', 'remindme "order tickets" in 2w', 'reminder "call ?" 3pm april 4th 2023',
                    'rset "<@985864214260371476> go to bed :)" at 11pm', 'setreminder "winter solstice" for 21/12/22'])
    async def setreminder(self, ctx,  content: str, *, time):
        if len(spaced := time.split(' ')) > 1 and spaced[0] in {'for', 'at', 'in', 'after', 'on'}:
            time = ''.join(spaced[1:])
        try:
            try:
                time = ctx.message.created_at + to_timedelta(time)
            except InvalidTimeString:
                time = parse(time, dayfirst=True, fuzzy=True)
        except ParserError:
            raise errs.BadArg
        reminder = {'user': ctx.author.id, 'channel': ctx.channel.id, 'time': time, 'msg': content, 'repeat': False}
        await self.db.insert_one(reminder)
        await read.official(ctx, f'reminder set for {time.strftime("%I:%M%p on %d/%m/%Y")}', 'alarm_clock')

    @command(name='delreminder', aliases=['rmreminder', 'rdel', 'delrem'], brief='remove a reminder from this channel',
             help='remove a reminder thats currently set in this channel. ull need 2 specify the index of the reminder '
                  'u want gone (which can b found w/ the reminderlist cmd). careful 2 use a recent version of this '
                  'list when looking up ur index tho cus its indexed by most recently set, meaning new reminders '
                  'getting set will probs change up the previous indexing. remember that u cant delete reminders u '
                  'didnt set (unless ur name is nash lol). deleted reminders will b moved 2 the reminder archive',
             usage=['delreminder 3'])
    async def delreminder(self, ctx, index: int):
        if entries := await self.db.find({'channel': ctx.channel.id}).sort('time').to_list(None):
            if 0 <= index - 1 < len(entries):
                reminder = entries[index - 1]
                if reminder['user'] not in {ctx.author.id}.union(self.bot.owner_ids):
                    raise errs.NotAllowed
                await self.del_entry(reminder, ctx.message.created_at)
                await read.official(ctx, 'successfully deleted & archived reminder', 'recycle')
            else:
                raise errs.BadArg
        else:
            await read.official(ctx, f'no reminders currently set in {ctx.channel.mention}', 'x')

    @command(name='reminderlist', aliases=['rshow', 'rlist', 'reminders'], brief='show all reminders in this channel',
             help='show an indexed list of all reminders currently set in this channel, sorted by most recently set')
    async def reminderlist(self, ctx):
        r_list = await self.db.find({'channel': ctx.channel.id}).sort('time').to_list(None)
        full_quote = ['reminders set up in this here channelator', 'alarm_clock']
        empty_quote = f'no reminders currently set in {ctx.channel.mention}'
        await read.reminder_list(ctx, r_list, full_quote, empty_quote)

    @command(name='archivelist', aliases=['rarchive', 'oldrlist'], brief='show reminders archived from this channel',
             help='show an indexed list of all reminders archived from this channel, sorted by most recently deleted')
    async def archivelist(self, ctx):
        r_list = await self.archive.find({'channel': ctx.channel.id}).sort('deleted', DESCENDING).to_list(None)
        full_quote = ['reminders archived from this here channelator', 'recycle']
        empty_quote = f'no reminders archived from {ctx.channel.mention}'
        await read.reminder_list(ctx, r_list, full_quote, empty_quote, archive=True)

    @command(name='allreminders', aliases=['allrlist', 'allr'], brief='show all reminders in all channels', hidden=True,
             help='show an indexed list of all reminders set across all channels, sorted by most recently set')
    @is_owner()
    async def allreminders(self, ctx):
        r_list = await self.db.find().sort('time').to_list(None)
        full_quote = ['master list of all reminders (!!)', 'alarm_clock']
        empty_quote = 'no reminders currently set in any channel'
        await read.reminder_list(ctx, r_list, full_quote, empty_quote, hide=True)

    @command(name='reminderpurge', aliases=['rpurge', 'rclear'], brief='clear all reminders in a channel', hidden=True,
             help='purge all reminders currently set in a channel. if no channel is specified the bot will assume u '
                  'mean the current channel. any purged reminders will not b added 2 the reminders archive, meaning '
                  'there is no way 2 recover them afterwards (so use w/ caution !!!)',
             usage=['reminderpurge', 'rpurge general', 'rclear 999267695289704549', f'rpurge <#958642449578872905>'])
    @is_owner()
    async def reminderpurge(self, ctx, channel: TextChannel = None):
        channel = ctx.channel if channel is None else channel
        if count := await self.db.count_documents({'channel': channel.id}):
            self.db.delete_many({'channel': channel.id})
            count = f'{count} {quotes.add_s("reminder", count)}'
            await read.official(ctx, f'successfully purged {count} from {channel.mention}', 'white_check_mark')
        else:
            await read.official(ctx, f'no reminders currently set in {channel.mention}', 'negative_squared_cross_mark')

    async def error_handling(self, ctx, error):
        if isinstance(error, ChannelNotFound):
            if ctx.command == self.bot.get_command('reminderpurge'):
                await read.err(ctx, f'uh, u whaa-?? bruh thats not a channel i dont think. u sure u spellin it right??')
            else:
                return False
        elif isinstance(error, errs.BadArg):
            if ctx.command == self.bot.get_command('setreminder'):
                await read.err(ctx, f'uuuh ngl man idk wtf ur meaning by that. try smth like "2h5m" or "11pm feb 22nd"')
            elif ctx.command == self.bot.get_command('delreminder'):
                await read.err(ctx, f'ahh invalid index buddy. here, find the index w/ this list & try again')
                await ctx.invoke(self.bot.get_command('reminderlist'))
            else:
                return False
        elif isinstance(error, errs.NotAllowed):
            if ctx.command == self.bot.get_command('delreminder'):
                await read.err(ctx, f'bro u werent the 1 who set that reminder so im not gonna let u delete it ...srry')
            else:
                return False
        elif isinstance(error, MissingRequiredArgument):
            if ctx.command == self.bot.get_command('setreminder'):
                await read.err(ctx, '2 use this cmd u gotta give a msg & then a time (like "2h5m" or "11pm feb 22nd")')
            elif ctx.command == self.bot.get_command('delreminder'):
                await read.err(ctx, 'yo u gotta give the index of the reminder u want gone (check w/ the rlist cmd)')
            else:
                return False
        elif isinstance(error, BadArgument):
            if ctx.command == self.bot.get_command('delreminder'):
                await read.err(ctx, 'oof thats not how u use this cmd m8. try smth like "delreminder 4" or wtever')
            else:
                return False
        else:
            return False
        return True


def setup(bot):
    bot.add_cog(Reminder(bot))
