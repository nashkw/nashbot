# nashbot.py
import os

import discord
from dotenv import load_dotenv

import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    hi_quotes = [
        'hi??',
        'u called?',
        'mmm im responding',
        'joe mama OOOOOHHHHHH-',
        'this message is better than 6/10 hi response options',
        'howdus :sunflower:',
        'hello. but at what cost...',
        'hi urself bucko',
        '...are u talking... to me? h-hello?',
        'greetings mortal',
    ]

    if message.content == 'hi':
        response = random.choice(hi_quotes)
        await message.channel.send(response)


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n\n')
        else:
            raise

client.run(TOKEN)