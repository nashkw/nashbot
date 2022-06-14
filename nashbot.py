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
        'yo mama OOOOOHHHHHH-',
        'this message is better than 6/10 hi response options',
        'howdus :sunflower:',
        'hello. but at what cost...',
        'hi urself bucko',
        '...are u talking... to me? h-hello?',
        'greetings mortal',
        'honk. yes thats right, i speak clown now',
        'do u have a minute 2 talk abt our lord & saviour jesus christ?',
        'hewwo... :point_right: :point_left:',
        'beep boop my brain is soup. jk i dont have a brain',
        'this is an extra super rare response!!!!! or maybe its the most common one. youll never know',
        'salutations, etc.',
        'd-did you hear that? a-! ah-!! a g-g-g-ghost!!??!!',
        'congratulations!! you win!! enter your card details and national insurance no. to continue :)',
        'why hello there my strangely fleshy companion what can i do for u on this fine day',
        'error 404 hi response not found. suggestion: give the bot a raise',
        'greetings... fRoM tHe wOrLd oF tOmOrRoW!!!! (spooky)',
        'my, what a phenomenal greeting. however will i top that',
    ]

    if message.content == 'hi':
        response = random.choice(hi_quotes)
        await message.channel.send(response)
    elif message.content == 'high five':
        await message.channel.send('u gots it pardner :hand_splayed: :cowboy:')
    elif message.content == 'pingus':
        await message.channel.send('pongus. or possibly chongus. only time will tell...')
    elif message.content == 'nashbot':
        await message.channel.send('SILENCE!! do not speak that word in vain, mortal. didnt you see the trademark??')


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n\n')
        else:
            raise

client.run(TOKEN)