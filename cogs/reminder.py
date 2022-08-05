# reminder.py

from nashbot import read, errs
from database import r_db
from datetime import datetime
from discord.ext import tasks
from dateutil.parser import parse, ParserError
from dpytools.parsers import to_timedelta
from dpytools.errors import InvalidTimeString
from discord.ext.commands import Cog, command


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
             help='TODO',
             usage=['TODO'])
    async def setreminder(self, ctx,  content: str, *, time):
        if len(spaced := time.split(' ')) > 1 and spaced[0] in {'for', 'at', 'in', 'after'}:
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
        await read.official(ctx, f'reminder set for {time}', 'alarm_clock')

    async def error_handling(self, ctx, error):
        return False


def setup(bot):
    bot.add_cog(Reminder(bot))
