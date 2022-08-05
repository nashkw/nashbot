# reminder.py

from nashbot import read, errs
from database import r_db
from datetime import datetime
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
        reminders = r_db.reminders.find({'next_time': {'$lte': (now := datetime.now())}})
        async for r in reminders:
            channel = self.bot.get_channel(r['channel_id'])
            author = await self.bot.fetch_user(r['user_id'])
            await read.official(channel, f'{author.mention} {r["content"]}', 'alarm_clock')
            if (time := r['recurrent_time']) is not False:
                await r_db.reminders.update_one({'_id': r['_id']}, {'$set': {'next_time': now + to_timedelta(time)}})
            else:
                await r_db.reminders.delete_one({'_id': r['_id']})

    @command(name='setreminder', aliases=['remindme', 'reminder', 'note2self'], brief='set a reminder in this channel',
             help='set a reminder in this channel. 1st ull need 2 give a message - it can b anything including emojis '
                  'or mentions, but remember 2 enclose it in quotation marks if it includes a space cus otherwise itll '
                  'get mixed up w/ the time. the time should b given 2nd, & can either b relative ("15m" will b '
                  'interpreted as 15min from now) or absolute (such as "8:25am 16th august"). the bot will do its best '
                  '2 interpret ur input but try & b as clear as possible 2 avoid miscommunication !!',
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
            'user_id': ctx.author.id,
            'channel_id': ctx.channel.id,
            'next_time': time,
            'content': content,
            'recurrent_time': False,
        })
        await read.official(ctx, f'reminder set for {time.strftime("%I:%M%p on %d/%m/%Y")}', 'alarm_clock')

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
