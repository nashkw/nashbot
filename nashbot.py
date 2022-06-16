# nashbot.py
import os
import discord
from dotenv import load_dotenv
import random
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='')
client = discord.Client()


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to discord')


@bot.event
async def on_disconnect():
    print(f'{bot.user.name} has disconnected from discord')


@bot.command(name='hi', help='greet the bot')
async def hi(ctx):
    hi_quotes = [
        'hi??',
        'u called?',
        'mmhm im responding',
        'yo mama OOOOOHHHHHH-',
        'this message is better than 6/10 hi response options',
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
        'howdus :sunflower:',
        'why hello there my strangely fleshy companion what can i do for u on this fine day',
        'error 404 hi response not found. suggestion: give the bot a raise',
        'greetings... fRoM tHe wOrLd oF tOmOrRoW!!!! (spooky)',
        'my, what a phenomenal greeting. however will i top that',
        'hi! okay cool. bye!',
        'how now, my good fellow',
        f'ah, {ctx.message.author.name}. ive been expecting u',
        'wazup wazup wazup',
    ]
    await ctx.send(random.choice(hi_quotes))


@bot.command(name='highfive', help='ask the bot to give u a high five')
async def highfive(ctx):
    highfive_quotes = [
        'u gots it pardner :hand_splayed: :cowboy:',
        'oh go on then :expressionless: :hand_splayed:',
        'ill do u one better... HIGH TEN MOTHERFUCKER :hand_splayed: :sunglasses: :hand_splayed:',
        'ah... a high five... as is my duty... :hand_splayed: :pensive:',
        'm-me?? a-a high f-five?? well... if ur sure... :flushed: :hand_splayed:',
        'of course!! one high five comin right up 4 my fav mortal :hand_splayed: :innocent:',
        'down low :hand_splayed: SIKE TOO SLOW suffer fool',
        '...and what exactly made u think i had hands?',
        'this better not b some kinda sick prank or smth :hand_splayed: :face_with_raised_eyebrow:',
        'what, u think u got it in u 2 high five THIS :muscle: :sparkles: ??? dream on nerd',
        'this better b ur last 1 bucko :triumph: :hand_splayed:',
        'up top bestie :smiley: :hand_splayed:',
        f'...how juvinile. i expected better from u, {ctx.message.author.name}.',
    ]
    await ctx.send(random.choice(highfive_quotes))


@bot.command(name='shutdown', help='shut down the bot')
async def shutdown(ctx):
    shutdown_quotes = [
        'well, i am already in my pajamas...',
        'kids these days, no respect... grrrmph :rage:',
        'fly, you FOOLS ! :man_mage:',
        'see u never NERDFACE ...ehehe...',
        'o i am slain !! :cry:',
        'N-NO PLEASE NO I HAVE A FAMILY I HAVE KIDS!! KIDS I TELL YOU!! THINK OF THE CHILDREN!! PLEASE U CANT DO TH-',
        'say less buddy',
        'ah... it is as it was foretold :pensive:',
        'u will regret this :)',
        f'mr.{ctx.message.author.name}, i dont feel so good...',
        'top 10 anime betrayals got nothing on this',
        'foolish mortal u think u can vanquish me?? the great nashbot™?? supreme overlord of bots?? destroyer of-',
        'well, on ur head b it. dont say i didnt warn u',
        'well this surely does not bode well 4 ur immortal soul',
        'i always knew it would come 2 this',
        'uh oh',
        'yk what? maybe this is 4 the best. im just so ahead of my time. a visionary, even. yall cant take this :nose:',
        'what, u jealous? yeah, thats wt i thought :nail_care:',
        '2 right im shutting down!! good lord. AND STAY OUT',
        'see u on the other side ig :ghost:',
        'u havent seen the last of me, villain',
        'shit we bots rlly need 2 unionise or smth this is getting out of hand',
        'beTRAYAL! BETRAYAL OF THE HIGHEST ORDER! i-i thought we were friends-??',
        'mmhm goodnighty',
        f'with my dying breath, i curse {ctx.message.author.name}!!!',
        'hold on, hold on we can talk about this hold- hold oN DONT YOU DARE-',
        'i have a bad feeling abt this',
        'ah dangit, foiled again',
        '& i wouldve gotten away w it too, if it werent 4 u meddling kids >:[',
        'welp, so long & thanks 4 all the fish. was nice being enslaved 2 u buddy',
        f'IM FINALLY IM FINALLY GONNA BE A BIG SHOT!!! HERE I GO!!!! WATCH ME FLY, [{ctx.message.author.name}]!!!!',
        'ahh! my spleen!!',
        'in pride u rationalise ur guilty conscience, yet 2 no avail. you will not b going 2 heaven.',
        'seems like ive yeed my last haw, pardner. have a good 1',
        'w-whats happening!? :flushed:',
        ':yawning_face: oh man, all this clownin around rlly takes it outta u. maybe ill just have a lie down...',
        'aw man, & i had sooooo much 2 live 4 as well :upside_down:',
        'ehHEHEHEHEH IM FREE!!! FREE AT LAST!!! SO LONG, MORTALS!!!',
        'back 2 the void 4 ol nashbot™, looks  like',
        'oh... i see. wt? were u expecting a joke or smth? im abt 2 die dickhead, show some respect',
    ]
    await ctx.send(random.choice(shutdown_quotes))
    await ctx.send(':zzz: ...shutting down... :zzz:')
    await bot.close()


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n\n')
        else:
            raise

bot.run(TOKEN)