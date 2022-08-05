# reminder.py


from nashbot import read, errs, resources, quotes
from database import r_db
from datetime import datetime
from humanize import naturaldelta
from discord.ext import tasks
from dateutil.parser import parse, ParserError
from dpytools.parsers import to_timedelta
from dpytools.errors import InvalidTimeString
from discord.ext.commands import Cog, command, MissingRequiredArgument


class Reminder(Cog, name='reminder'):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '⏰'
        self.reminder_loop.start()

    @tasks.loop(minutes=1)
    async def reminder_loop(self):
        await self.bot.wait_until_ready()
        async for r in r_db.reminders.find({'time': {'$lte': (now := datetime.now())}}):
            channel, user = self.bot.get_channel(r['channel']), await self.bot.fetch_user(r['user'])
            await read.official(channel, f'{user.mention} {r["msg"]}', 'alarm_clock')
            if (time := r['repeat']) is not False:
                await r_db.reminders.update_one({'_id': r['_id']}, {'$set': {'time': now + to_timedelta(time)}})
            else:
                await r_db.reminders.delete_one({'_id': r['_id']})

    @command(name='setreminder', aliases=['remindme', 'reminder', 'note2self'], brief='set a reminder in this channel',
             help='set a reminder in this channel. 1st ull need 2 give a message - it can b anything including emojis '
                  'or mentions, but remember 2 enclose it in quotation marks if it includes a space cus otherwise itll '
                  'get mixed up w/ the time. the time should b given 2nd, & can either b relative ("15m" will b '
                  'interpreted as 15min from now) or absolute (such as "8:25am 16th august"). the bot will do its best '
                  '2 interpret ur input but try & b as clear as possible 2 avoid miscommunication !! note that '
                  'reminders will only b accurate 2 the minute so specifying seconds tends 2 b irrelevant',
             usage=['setreminder games 1h30m', 'remindme "order tickets" in 2w', 'reminder "call ?" 3pm april 4th 2023',
                    'note2self "<@985864214260371476> bedtime" at 11pm', 'setreminder "winter solstice" for 21/12/22'])
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
        await r_db.reminders.insert_one({
            'user': ctx.author.id,
            'channel': ctx.channel.id,
            'time': time,
            'msg': content,
            'repeat': False,
        })
        await read.official(ctx, f'reminder set for {time.strftime("%I:%M%p on %d/%m/%Y")}', 'alarm_clock')

    @command(name='reminderlist', aliases=['rshow', 'rlist', 'reminders'], brief='show all reminders in this channel',
             help='show all reminders currently set in this channel')
    async def reminderlist(self, ctx):
        if fill := await r_db.reminders.find({'channel': ctx.channel.id}).sort('time').to_list(None):
            fill = [[i + 1, r['msg'], naturaldelta(r['time'] - ctx.message.created_at)] for i, r in enumerate(fill)]
            fill = resources.table_paginate(fill, trunc=33, head=['', 'message', 'due in'])
            await read.paginated(ctx, quotes.wrap(f'reminders set up in this here channelator', 'alarm_clock'), fill)
        else:
            await read.official(ctx, f'no reminders currently set in <#{ctx.channel.id}>', 'x')

    async def error_handling(self, ctx, error):
        if isinstance(error, errs.BadArg):
            if ctx.command == self.bot.get_command('setreminder'):
                await read.err(ctx, f'uuuh ngl man idk wtf ur meaning by that. try smth like "2h5m" or "11pm feb 22nd"')
            else:
                return False
        elif isinstance(error, MissingRequiredArgument):
            if ctx.command == self.bot.get_command('setreminder'):
                await read.err(ctx, '2 use this cmd u gotta give a msg & then a time (like "2h5m" or "11pm feb 22nd")')
            else:
                return False
        else:
            return False
        return True


def setup(bot):
    bot.add_cog(Reminder(bot))
