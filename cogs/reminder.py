# reminder.py


from nashbot import read
from database import r_db
from datetime import datetime
from discord.ext import tasks
from dpytools.parsers import to_timedelta
from discord.ext.commands import Cog, command


class Reminder(Cog, name='reminder'):

    def __init__(self, bot):
        self.bot = bot
        self.emoji = '⏰'
        self.reminder_loop.start()

    @tasks.loop(minutes=1)
    async def reminder_loop(self):
        await self.bot.wait_until_ready()
        reminders = r_db.reminders.find({'done': False, 'next_time': {'$lte': (now := datetime.now())}})
        async for reminder in reminders:
            channel = self.bot.get_channel(reminder['channel_id'])
            author = await self.bot.fetch_user(reminder['user_id'])
            await read.official(channel, f'{author.mention} {reminder["content"]}', 'alarm_clock')
            if (time := reminder['recurrent_time']) is not False:
                reminder['next_time'] = now + to_timedelta(time)
            else:
                reminder['done'] = True
            await r_db.reminders.replace_one({'_id': reminder['_id']}, reminder)

    @command(name='reminder', aliases=['remindme', 'remind', 'note2self'], brief='set a reminder in this channel',
             help='TODO',
             usage=['TODO'])
    async def reminder(self, ctx, time: to_timedelta, *, content):
        await r_db.reminders.insert_one({
            'user_id': ctx.author.id,
            'channel_id': ctx.channel.id,
            'next_time': ctx.message.created_at + time,
            'content': content,
            'recurrent_time': False,
            'done': False,
        })
        await read.official(ctx, f'reminder set for {time}', 'alarm_clock')

    async def error_handling(self, ctx, error):
        return False


def setup(bot):
    bot.add_cog(Reminder(bot))
