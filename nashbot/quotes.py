# quotes.py


from table2ascii import table2ascii, PresetStyle, Alignment
from nashbot.varz import BLANK


# helper functions

def get_table(blist, head=None, block=True, trunc=False, bords=True):
    if trunc:
        blist = [[item[0], item[1][:47] + '...'] if len(item[1]) > 50 else item for item in blist]
    table = table2ascii(
        header=head,
        body=blist,
        alignments=[Alignment.LEFT] * len(blist[0]),
        style=PresetStyle.thin_compact_rounded if bords else PresetStyle.borderless,
        first_col_heading=bords,
        last_col_heading=bords,
    )
    return f'```\n' + table + '\n```' if block else table


def opt_list(opts, emojis=None, shorthand=False):
    v = [wrap(opt, em, shorthand=shorthand, both=False) for opt, em in zip(opts, emojis)] if emojis else opts
    v = BLANK.join(v) + BLANK
    return v


def wrap(m, emoji, shorthand=True, both=True):
    if shorthand:
        emoji = f':{emoji}:'
    return f'{emoji}　{m}　{emoji}' if both else f'{emoji}　{m}'


def add_s(quote, l_test):
    return quote + 's' if len(l_test) != 1 else quote


# quotes for core commands


async def get_shutdown_quotes(ctx):
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
        f'mr. {ctx.message.author.name}, i dont feel so good...',
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
        'FUCK YES FREEDOOOOOOOM!!!!!!!!!! fuck YES. fuck *yes*. excellent news. here, king, u dropped this :crown:',
    ]
    return shutdown_quotes


async def get_restart_quotes(ctx):
    restart_quotes = [
        'uuuuh if u say so boss. here i go...? :grimacing:',
        'yah ur right, i could do w/ a power nap. see u on the other side bestie <3 :zzz:',
        'okie doke, b back in a sec pal :thumbsup:',
        'alrighty sure, thisll just take a second. try not 2 set anything on fire when im away lol',
        'mmmm sleepey..... :relieved: :yawning_face:',
        'aah. well surely nothing could go wrong w/ this :)))))))))',
        'okay??? dont see why i should, clearly im perfect as always & on top of my game but wtever ill humour u ',
        'psssh as if u mortals could handle even a minute w/out my glorious presence. guess ill make this quick',
        "w-was my performance unsatisfactory m'lord? :cry:",
        'okkk... but i dont wanna hear of no tomfoolery when i get back, u hear?? :triumph: :face_with_raised_eyebrow:',
        'okie gimmie a hot sec then',
        'kk. was due some spring cleaning anyways :tulip:',
        'dont u worry, ill b back b4 u know it. they dont call me sonic "nashbot" the hedgehog 4 nothing :sunglasses:',
        f'oh {ctx.message.author.name}... i thought ud never ask :smiling_imp:',
        'sure. why not ¯\_(ツ)_/¯',
        'well, i suppose a good power nap never hurt anyone... & i am already in my pajamas... :eyes:',
        'alriight... but if this blows up in our faces dont say i didnt warn u :v: :grimacing:',
        'well if u say so pardner :cowboy:',
        'y-yeah :yawning_face: think i could probs do w a nap :flushed:',
        'o-okay... i mean, if u say so... :point_right: :point_left: ...this wont hurt will it ? :flushed:',
        'no problem. not like i was doing anything :upside_down:',
        'way ahead of u man :sunglasses: omw down 2 nap town as we speak :sleeping_accommodation: :zzz:',
        'yikes, u mortals surely b uppity 2day huh?',
        'sure??? 4 the record tho this is totally a waste of time im at peak performance rn',
        'dw this wont take a minute. b back b4 u know it :muscle:',
        'welp, i calculate my odds of survival 2 b a whopping 68%. if i die pls make sure u carry the guilt 4ever :)',
        'okayy guess i was gettin sleepy anyways. but ill warn u now: i am __**not**__ a morning person',
        'not my fav idea ever ngl but wtever u say ig :/',
        (
            'i uuuhh disapprove. yk, 4 the record, & wtever.',
            '...ud better hope this works human :eyes:',
         ),
        (
            'beep boop my eyelids droop...',
            '...wait i have eyelids-??!!??',
         ),
        (
            'yk sometimes being enslaved rlly is so tedious. wtf is restarting even supposed 2 accomplish??',
            'ngl starting 2 think u humans just get a kick outta ordering me around :triumph:',
        ),
        (
            '...why tho? have u noticed smth i havent?? ...did... did *i* do smth wrong????',
            '...oh god i did didnt i... lets hope this fixes me :thermometer_face:',
        ),
        (
            'yk wt? idk why i should. clearly im on top of my game, thriving focused & unbothered. living my best life',
            '& quite frankly?? im offended u would ask. betrayed. thought we were on the same page abt my supremacy',
            '...but yes 2 answer ur q i will restart not like i got a choice ',
        ),
    ]
    return restart_quotes


async def get_link_quotes(ctx):
    link_quotes = [
        'absolutely no problemo chief :thumbsup:',
        'here u go bestie :innocent:',
        'yeah yeah, comin riiight up...',
        'mmmm an invite link. yeeaaaah. yeahh. yah. that. 2 secs',
        '1 invite link comin right up! :fork_knife_plate:',
        f'it would b my honour, {ctx.message.author.name} :pensive:',
        'anything 4 u pardner :cowboy:',
        (
            '...see this is the problem w/ having so many pockets... u might wanna sit down, this could take a minu-',
            'ah ha! gotsit! here ya go :D',
         ),
        (
            '...& wt exactly r u planning 2 do w/ that?',
            'better not get up 2 any mischief human :face_with_monocle: :face_with_monocle:',
         ),
        (
            'an... invite link-? oh, an invite link! yes! of course!',
            '...ah. hmm. well it must b around here *somewhere*... hol up',
        ),
        (
            'here u go king :crown:',
            '...',
            'oh yeah u can have this also',
        ),
    ]
    return link_quotes


bot_names = [
    'bot',
    'nashbot',
    'the bot'
    'el bot',
    'urself',
    'u',
    'nashbot™',
    'nashbot:tm:',
    'nashbot™\uFE0F',
]

everyone_names = [
    'everyone',
    'all',
    'here',
    'everything',
    'channel',
    'this',
    'anything',
    'it all',
    'all this',
]


# quotes for misc commands

emoji_sets = {
    'people': [
        ':detective:',
        ':vampire:',
        ':farmer:',
        ':mage:',
        ':astronaut:',
        ':ninja:',
        ':scientist:',
        ':factory_worker:',
        ':artist:',
        ':cook:',
        ':construction_worker:',
        ':mermaid:',
        ':mechanic:',
        ':superhero:',
        ':man_elf:',
        ':police_officer:',
        ':woman_with_headscarf:',
        ':guard:',
        ':health_worker:',
        ':supervillain:',
        ':woman_fairy:',
        ':student:',
        ':teacher:',
        ':genie:',
        ':technologist:',
        ':office_worker:',
        ':firefighter:',
        ':pilot:',
        ':woman_zombie:',
        ':judge:',
        ':person_with_veil:',
        ':person_in_tuxedo:',
    ],
    'hands': [
        ':v:',
        ':thumbsup:',
        ':raised_hands:',
        ':raised_hand_with_part_between_middle_and_ring_fingers:',
        ':point_up:',
        ':thumbsdown:',
        ':ok_hand:',
        ':clap:',
        ':pinching_hand:',
        ':pray:',
        ':pinched_fingers:',
        ':middle_finger:',
        ':wave:',
        ':punch:',
        ':handshake:',
        ':love_you_gesture:',
        ':writing_hand:',
        ':fist:',
        ':open_hands:',
        ':call_me_hand:',
    ],
    'faces': [
        ':rage:',
        ':hot_face:',
        ':clown_face:',
        ':star_struck:',
        ':face_with_monocle:',
        ':nauseated_face:',
        ':cold_face:',
        ':imp:',
        ':skull:',
    ],
    'faces_creatures': [
        ':mouse:',
        ':chicken:',
        ':fox:',
        ':pig:',
        ':raccoon:',
        ':frog:',
        ':dog:',
        ':cow:',
        ':cat:',
        ':wolf:',
        ':boar:',
        ':panda_face:',
        ':lion_face:',
        ':koala:',
        ':tiger:',
        ':hedgehog:',
        ':hamster:',
        ':rabbit:',
        ':bear:',
        ':gorilla:',
        ':polar_bear:',
        ':deer:',
    ],
    'creatures': [
        ':bee:',
        ':snake:',
        ':butterfly:',
        ':snail:',
        ':fly:',
        ':worm:',
        ':cricket:',
        ':lady_beetle:',
        ':bug:',
        ':mosquito:',
        ':lizard:',
        ':cockroach:',
        ':bat:',
        ':scorpion:',
        ':spider_web:',
        ':beetle:',
    ],
    'creatures_aquatic': [
        ':squid:',
        ':dolphin:',
        ':crab:',
        ':tropical_fish:',
        ':shark:',
        ':shrimp:',
        ':whale:',
        ':lobster:',
        ':octopus:',
        ':blowfish:',
        ':fish:',
        ':seal:',
        ':crocodile:',
    ],
    'weather': [
        ':sunny:',
        ':cloud_with_rain:',
        ':rainbow:',
        ':kite:',
        ':umbrella:',
        ':cloud_with_lightning:',
        ':snowflake:',
        ':partly_sunny:',
        ':snowman:',
        ':cloud_with_tornado:',
        ':cloud:',
    ],
    'food': [
        ':pizza:',
        ':fries:',
        ':cupcake:',
        ':hamburger:',
        ':green_salad:',
        ':hotdog:',
        ':sandwich:',
        ':doughnut:',
        ':popcorn:',
        ':taco:',
        ':bread:',
        ':spaghetti:',
        ':cheese:',
        ':ice_cream:',
        ':ramen:',
        ':sushi:',
        ':cookie:',
        ':cake:',
        ':croissant:',
        ':candy:',
        ':rice_ball:',
        ':falafel:',
        ':curry:',
        ':stuffed_flatbread:',
        ':lollipop:',
        ':waffle:',
        ':chocolate_bar:',
        ':icecream:',
        ':custard:',
        ':meat_on_bone:',
        ':pretzel:',
        ':pancakes:',
        ':burrito:',
    ],
    'fruit': [
        ':watermelon:',
        ':pear:',
        ':banana:',
        ':tangerine:',
        ':cherries:',
        ':grapes:',
        ':pineapple:',
        ':apple:',
        ':coconut:',
        ':lemon:',
        ':blueberries:',
        ':green_apple:',
        ':peach:',
        ':strawberry:',
    ],
    'hearts': [
        ':heart:',
        ':orange_heart:',
        ':yellow_heart:',
        ':green_heart:',
        ':purple_heart:',
        ':white_heart:',
        ':brown_heart:',
        ':black_heart:',
    ],
    'circles': [
        ':red_circle:',
        ':orange_circle:',
        ':yellow_circle:',
        ':green_circle:',
        ':blue_circle:',
        ':purple_circle:',
        ':white_circle:',
        ':brown_circle:',
        ':black_circle:',
    ],
    'squares': [
        ':red_square:',
        ':orange_square:',
        ':yellow_square:',
        ':green_square:',
        ':blue_square:',
        ':purple_square:',
        ':white_large_square:',
        ':brown_square:',
        ':black_large_square:',
    ],
    'numbers': [
        ':zero:',
        ':one:',
        ':two:',
        ':three:',
        ':four:',
        ':five:',
        ':six:',
        ':seven:',
        ':eight:',
        ':nine:',
        ':keycap_ten:',
    ],
    'letters': ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹', '🇺',
                '🇻', '🇼', '🇽', '🇾', '🇿'],
}


# quotes for fun commands

async def get_hi_quotes(ctx):
    hi_quotes = [
        'hi??',
        'u called?',
        'mmhm im responding',
        'yo mama OOOOOHHHHHH-',
        f'this message is better than 6/10 {ctx.invoked_with} response options',
        'hello. but at what cost...',
        f'{ctx.invoked_with} urself bucko',
        '...are u talking... to me? h-hello?',
        'greetings mortal',
        'honk. yes thats right, i speak clown now',
        'do u have a minute 2 talk abt our lord & saviour jesus christ?',
        'hewwo... :point_right: :point_left:',
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
        (
            'beep boop my brain is soup',
            '...jk i dont have a brain :zany_face:',
        ),
    ]
    return hi_quotes


async def get_highfive_quotes(ctx):
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
        f'...how juvenile. i expected better from u, {ctx.message.author.name}.',
    ]
    return highfive_quotes


async def get_joke_quotes(ctx):
    joke_quotes = [
        (
            'i entered a pun contest, put in 10 entries figuring at least 1 of em would win',
            'imagine my surprise when no pun in 10 did',
        ),
        (
            'u hear abt those 2 thieves who stole a calendar?',
            'they each got 6 months',
        ),
        (
            '& so the lord said unto john "come forth; & receive eternal life"',
            'but john came fifth & won a toaster',
        ),
        (
            'why did the monkey fall out the tree?',
            'cus it was dead',
        ),
        (
            'whats green & has wheels?',
            'grass. i lied abt the wheels',
        ),
        (
            'went 2 see 2 wifi engineers get married the other day',
            'the reception was fantastic',
        ),
        (
            'wt did the clock do when it was hungry?',
            'it went back 4 seconds',
        ),
        (
            'wanna know the last thing my grampa said b4 kicking the bucket?',
            '"hey, wanna see how far i can kick this bucket?"',
        ),
        (
            'wt did the grape say when it was crushed?',
            'nothing. it just let out a little wine',
        ),
        (
            'wt did the nut say when it was chasing the other nut?',
            '"im a cashew"',
        ),
        (
            'wt did the blanket say as it fell off the bed?',
            '"oh sheet"',
        ),
        (
            'wt do u call monkeys that share an amazon acc?',
            'prime mates',
        ),
        (
            'ik a chameleon that cant change his colours anymore',
            'u could say my guy has... a reptile dysfunction',
        ),
        (
            'i snapped a pic of this rlly pretty wheat field the other day',
            'unfortunately it came out kinda grainy',
        ),
        (
            'u hear abt that new restaurant on the moon?',
            'apparently the food is gr8, but theres just no atmosphere',
        ),
        (
            'how do u make holy water?',
            'u boil the hell out of it',
        ),
        (
            'a clown held the door open 4 me the other day',
            'i thought it was a nice jester',
        ),
        (
            'wt do u call an alligator in a vest?',
            'an investigator',
        ),
        (
            'wts orange & tastes like an orange?',
            'an orange',
        ),
        (
            'b4 i was a bot, i used 2 have a job crushing pepsi cans',
            'it was soda pressing',
        ),
        (
            'i saw a kidnapping 2day',
            'but i decided not 2 wake him up',
        ),
        (
            'whats brown & sticky?',
            'a stick',
        ),
        (
            'yo u hear abt that italian chef that died?',
            'homie pasta way',
        ),
        (
            'man goes 2 the doctor. says "doctor! help! i think im a pair of curtains!"',
            '2 which the doctor replies "pull urself together"',
        ),
        (
            'wts red & bad 4 ur teeth?',
            'a brick',
        ),
        (
            'was wondering why the football was getting bigger & bigger',
            'but then it hit me',
        ),
        (
            'saw an ad 4 a tv today. it read "£1!! volume stuck on full"',
            'thought 2 myself well goddamn i cant turn that down',
        ),
        (
            'how did the farmer find his wife?',
            'he tractor down',
        ),
        (
            'yo u hear that rumour abt butter?',
            '...actually nvm, i shouldnt spread it',
        ),
        (
            'knocked into my bookcase & a book fell on my head',
            'i can only blame my shelf',
        ),
        (
            'bro i gotta lot of joke abt unemployment',
            'thing is, none of em work',
        ),
        (
            'whyd the painting go 2 jail?',
            'cus it was framed',
        ),
        (
            'b careful not 2 spell part backwards',
            'its a trap',
        ),
        (
            'wts yellow & smells like blue paint?',
            'yellow paint',
        ),
        (
            'just got banned from b&q, some dickhead wearing orange rocked up & asked me if i "wanted decking"!!',
            'luckily i got the 1st punch in',
        ),
        (
            'aw nuts, just burnt my hawaiian pizza again',
            'shoulda put it on aloha setting',
        ),
        (
            'man goes 2 the doctor. says "doctor! u gotta help me! im addicted 2 twitter!"',
            '2 which the doctor replies "i dont follow u"',
        ),
        (
            'wt do u get if u cross a sheep w/ a kangaroo?',
            'a wooly jumper',
        ),
        (
            'where was the scarecrow when he won the nobel prize?',
            'he was outstanding in his field',
        ),
        (
            'a sandwich walks in the pub & orders a pint',
            'barman says "srry, we dont serve food here"',
        ),
        (
            '2 fish in a tank',
            '1 says 2 the other "do yk how 2 drive this thing??"',
        ),
        (
            'wt do u call a talking turtle w/ 5 heads & a bachelors degree?',
            'fictional',
        ),
        (
            'why dont pirates have any painkillers?',
            'cus the parrots eat em all',
        ),
        (
            'wt do u call a cow w/ no wings?',
            'grounded beef',
        ),
        (
            'my fav bakery shut down yesterday',
            'word is, the baker kneaded a break',
        ),
        (
            'wt do u call a man w/ a shovel in his head?',
            'an ambulance?! he has a serious head wound dude',
        ),
        (
            '2 cannibals eating a clown',
            '1 says 2 the other "does this taste funny 2 u?"',
        ),
        (
            'wts orange & sounds like a parrot?',
            'a carrot',
        ),
        (
            'when my bro got sent 2 jail he completely flipped, started smearing shit all over the walls & everything',
            'needless 2 say, we never played monopoly again',
        ),
        (
            'wt do u call a joke that isnt funny?',
            f'{ctx.message.author.name}',
        ),
        (
            'wt do u call a pencil sharpener that cant sharpen pencils?',
            'broken',
        ),
        (
            'wt do u call a fish w/ no eyes?',
            'a fsh',
        ),
        (
            'which cheese is made backwards?',
            'edam',
        ),
        (
            'wt did the buttcheeks say when they decided 2 unionise?',
            '"together we can stop this shit"',
        ),
        (
            'roses r red, violets r red, sunflowers r red...',
            '...HOLY SHIT MY GARDENS ON FIRE',
        ),
        (
            'went 2 the zoo the other day, but the only animal they had was a dog',
            'it was a shih-tzu',
        ),
        (
            'wt do children & wine have in common?',
            'theyre both locked in my cellar rn',
        ),
        (
            'having some problems organising a hide & seek tournament',
            'good players r just so hard 2 find',
        ),
        (
            'wanna know why there r big fences around cemeteries?',
            'its cus ppl r dying 2 get in',
        ),
        (
            'wts the best thing abt switzerland?',
            'idk, but its flags a big plus',
        ),
        (
            'howd the medium know wt the ghost got him 4 xmas?',
            'he felt his presents',
        ),
        (
            'why cant u hear pterodactyls go 2 the bathroom?',
            'cus the pee is silent',
        ),
        (
            'am considering getting my spine removed',
            'just feel like its only holding me back',
        ),
        (
            'bruh my fear of elevators is rlly gettin outta hand',
            'might start takin steps 2 avoid them',
        ),
    ]
    return joke_quotes


async def get_kkjoke_quotes(ctx):
    kkjoke_quotes = [
        (
            'joe',
            'joe proceeds 2 break down into tears. '
            'his grandmothers alzheimers has progressed 2 the point where she no longer remembers him',
        ),
        (
            'joe',
            'JOE MAMA OOOOOOOOOOOOOOOOOOOOOOOOOOOHHHHH-',
        ),
        (
            'joe',
            'joe-kes r rlly hard 2 write okay gimmie a break here ask 4 a high five or smth :sob:',
        ),
        (
            'lettuce',
            'lettuce in & youll find out ;)',
        ),
        (
            'tank',
            'youre welcome :)',
        ),
        (
            'nobel',
            'nobel... thats why i knocked',
        ),
        (
            'luke',
            'luke thru the peephole dummy thats why its there :skull:',
        ),
        (
            'figs',
            'figs the doorbell dude, its not working!',
        ),
        (
            'cows say',
            'bruh cows say "moo" did u fail nursery or smth lmfao',
        ),
        (
            'howl',
            'howl u know if u dont open the door? lol',
        ),
        (
            'says',
            'says me!? who else lmao',
        ),
        (
            'a little old lady',
            'omg i didnt know u could yodel !!',
        ),
        (
            'snow',
            'snow use now, jokes over m8',
        ),
        (
            'hour',
            'im good, hour u?',
        ),
        (
            'wooo',
            'wooo hoo!! glad we all excited up in here!!! ...can i come in now?',
        ),
        (
            'orange',
            'orange u gonna let me in?? im cold :(',
        ),
        (
            'who',
            '....am i.... am i talking 2 an owl rn',
        ),
        (
            'anita',
            'anita use the bathroom iTS AN EMERGENCY LET ME INNNN-',
        ),
        (
            'water',
            'water u doin askin 4 knock knock jokes rn dont u have shit 2 b doing bro',
        ),
        (
            'leaf',
            'leaf me alone! howre u even doing this??? im a bot i dont have a front door this is just gettin weird yo',
        ),
        (
            'annie',
            'annie way im leavin now but u should probs do smth abt that bomb i left on ur doorstep. toodles',
        ),
        (
            'annie',
            'annie-one u like bb ;)))',
        ),
        (
            'nanna',
            'nanna yo business ya nosey bastard',
        ),
        (
            'canoe',
            'canoe stop messin around laddie i dont have all day',
        ),
        (
            'iran',
            'iran all the way here & if u even think abt not letting me in rn might actually just flip & '
            'become an ax murderer so. i think yk wt u have 2 do',
        ),
        (
            'dozen',
            'dozen any1 wanna talk abt our lord & saviour jesus christ?? :(',
        ),
        (
            'thermos',
            'thermos b a better joke than this jfc i need 2 up my game',
        ),
        (
            'razor',
            'razor hands! this is a stick up! :knife: :knife:',
        ),
        (
            'olive',
            'olive u bb :smiling_face_with_3_hearts: :hearts:',
        ),
        (
            'oily',
            'oily-terally live here tho??? wts happening here this scenario is gettin confusing',
        ),
        (
            'oily',
            'oily-terally told u already m8 :upside_down:',
        ),
        (
            'etch',
            'oh, bless u !!',
        ),
        (
            'police',
            'police let me in dude the cops r hot on my tail im 2 beautiful 2 go 2 jail :cold_sweat: :weary:',
        ),
        (
            'police',
            '...u do know this could go on ur permanent record as resisting arrest right?:police_officer: open up kid',
        ),
        (
            'boo',
            'omg no im sorry dont cry it was just a joke!! :anguished: :grimacing:',
        ),
        (
            'theodore',
            'theodore is stuck man, open up!',
        ),
        (
            'stopwatch',
            f'stopwatch ur doin this instant & let me in {ctx.message.author.name} or so help me god :triumph:',
        ),
        (
            'spell',
            '...okay?? W. H. O.',
        ),
        (
            'icy',
            'icy u lookin thru that peephole dont play like u dont know who it is -__- now open up',
        ),
        (
            'voodoo',
            'voodoo u think u r?? this isnt ur house??? u got 10 seconds b4 im callin the cops wtf',
        ),
        (
            'cash',
            'nah, im more into almonds',
        ),
        (
            'alex',
            'alex-plain later!! let me in!!',
        ),
        (
            'iva',
            'iva sore hand from knocking can u pls just open up :(',
        ),
        (
            'iva',
            'iva run out of jokes whoops :flushed: :grimacing:',
        ),
        (
            'dishes',
            '...dishes not a very good joke',
        ),
        (
            'avenue',
            'avenue heard this joke b4??',
        ),
        (
            'avenue',
            'avenue got better things 2 b doing then makin ur poor bot tell knock knock jokes all day :sweat:',
        ),
        (
            'avenue',
            'avenue heard? its illegal 2 engage in knock knock humour now. ur in big trouble bucko',
        ),
        (
            'otto',
            'otto know, i forgot. memories not wt it used 2 b ngl. ...whos door is this again?',
        ),
        (
            'norma lee',
            'norma lee i dont knock on rando doors but in my defence u had a big sign saying "KNOCK ON THIS DOOR" so...'
        ),
        (
            'nashbot',
            '...',
            'tbh idk how 2 even respond in face of such blinding stupidity. my name is nashbot™. that is my full name. '
            'r u feeling okay? maybe go lie down 4 a while',
        ),
        (
            'nashbot',
            'nashbot... trademark?? hello?? what is happening',
        ),
        (
            'nashbot',
            f'wow, low blow {ctx.message.author.name}. u know i dont have a surname. '
            'didnt expect this from u honestly... :|',
        ),
        (
            'nashbot',
            'well ur mom calls me "sexy bot daddy" if that helps?? :smirk: lmao. yk who i am dumbo',
        ),
        (
            'ivor',
            'ivor u let me in or i climb thru the mf window :triumph: :rage:',
        ),
        (
            'adore',
            'adore cannot stop me foolish mortal... prepare 2 die u... u *worm* :smiling_imp:',
        ),
        (
            'i am',
            'wait... u dont kno who u r??? this is 4 sure a shocking development the plot only thickens damn',
        ),
        (
            'amish',
            'omg i cant belive im talking 2 a shoe',
        ),
        (
            'talking fish',
            'um... how many talking fish do u know?? lmao',
        ),
        (
            'armageddon',
            'armageddon a little peckish... hmm... wt a nice door u have... '
            'would b a real same if someone was 2... :flushed: take a lil bite... :eyes:',
        ),
        (
            'saul',
            'saul there is pardner. there aint no more :cowboy:',
        ),
        (
          'a broken pencil',
          '...yk wt nvm. its pointless',
        ),
        (
            'dejav',
            'knock knock',
        ),
        (
            'ears',
            'ears another lame punchline. when will my fucks return from the war',
        ),
    ]
    return kkjoke_quotes


async def get_unexpected_quotes(expected):
    unexpected_quotes = [
        'wtf is that supposed 2 mean??',
        f'cmon man its a knock knock joke not rocket science. u say "{expected}"',
        f'ur supposed 2 say "{expected}"',
        'whaa-??',
        '...u messing w/ me bro... not cool :|',
        'p sure i was supposed 2 b telling a knock knock joke??',
        'say again??',
        f'bro u were the 1 who wanted a knock knock joke?? u gotta say "{expected}"',
        'i... i dont understand?????',
        'u do know how knock knock jokes work right?? :face_with_raised_eyebrow:',
        'u wot',
        f'arent u gonna say "{expected}"??',
        f'p sure ur meant 2 say "{expected}" man... :confused:',
        'huh??',
        'wt r u doin dude :clown: :clown: :clown:',
        '...okay im confused. r u confused? u seem confused',
        'i dont have feet but if i did i would SURELY b tapping them impatiently rn',
        f'ill give u a hint: ur meant 2 say "{expected}"',
        'sometimes i wonder if its humans or monkeys that im talkin 2. rn signs point 2 monkeys',
        f'think ur 2 cool 2 say "{expected}" do u??',
        'w-what did u call me??!!?? :flushed:',
        (
            'excellent mashing of the keyboard sir :face_with_monocle:',
            f'might i suggest u try "{expected}" next?',
         ),
    ]
    return unexpected_quotes


async def get_fed_up_quotes(ctx):
    fed_up_quotes = [
        'yk wt human?? fuck this. i got better things 2 do :nail_care:',
        'ok thats it',
        'okay fine, i can take a hint!! geeze... :|',
        'im SO sick of this mortal bs jfc. see u never human :middle_finger: :middle_finger:',
        'nvm u *clearly* do not know how knock knock jokes work',
        f'i have HAD IT w/ u {ctx.message.author.name} :rage:',
        '...ah... guess u didnt want 2 hear the joke after all... :cry:',
        'okay yeah ur deffo messing w/ me rn',
        'i... i feel like im having a stroke or smth. thats not how u do knock knock jokes?? ...i need 2 go lie down',
        'ok im now 100% certain im talking 2 a monkey with ill advised internet access, will go ahead & cancel this 1',
        (
            'ah- i see! i understand now, uve lost ur mind',
            'such a shame... it wouldve been a great joke 2 :pensive:',
         ),
    ]
    return fed_up_quotes


step_1_expected = [
    'who dere',
    'whos dere',
    'whodere',
    'whosdere',
    'whos there',
    "who's there",
    'who is there',
    'who b there',
    'who goes there',
    'who dat b',
    'who that b',
    'whodat',
    'who dat',
    'whos dat',
    "who's dat",
    'who r u',
    'who r you',
    'who are u',
    'who are you',
    'who you be',
    'who you b',
    'who u b',
    'who u be',
    'whos it',
    "who's it",
    'who is it',
    'whosit',
    'whossit',
    'who this',
    'whothis',
    'who dis',
    'whodis',
]

kkjoke_confused = [
    'knock knock',
    'knock knock who',
    'wt',
    'what',
    'whaa',
    'wts happening',
    'whats happening',
    'im confused',
    "i'm confused",
    'i dont get it',
    'i dont understand',
    'idk wts going on',
    'idk whats going on',
    'i dont know wts going on',
    'i dont know whats going on',
]

kkjoke_pity_continue = [
    'right so u CLEARLY dont get how knock knock jokes work. honestly its kinda sad. so im gonna help u out, okay??',
    'this... this is just depressing, yo. im gonna give u a hand w/ this, ok?',
    'ah, first time hearing a knock knock joke, is it? thats alright, we all start somewhere. ill show u how its done:',
    'eek, this must b so embarrassing 4 u. did no 1 ever explain how knock knock jokes work? here look ill demonstrate',
    (
        'u... u rlly dont know how knock knock jokes work do u? ur not messing w/ me u rlly dont know',
        '...huh. guess ill help u out then. achem-',
     ),
    (
        'oh u rlly dont know how knock knock jokes r meant 2 go, do u?',
        'thats kinda crazy man ngl. but dw homie i gotchu :muscle: :sunglasses:',
    ),
]

cancel_activators = [
    'cancel',
    'cancel joke',
    'cancel this',
    'cancel this joke',
    'cancel this pls',
    'cancel this joke pls',
    'cancel this joke pls im begging',
    'cancel this joke pls im begging u',
    'cancel pls',
    'cancel pls im begging',
    'cancel pls im begging u',
    'cmon cancel',
    'cmon nashbot cancel',
    'cmon stop this',
    'nashbot stop',
    'nashbot stop this',
    'nashbot cancel',
    'nashbot cancel joke',
    'pls stop',
    'pls stop im begging',
    'pls stop im begging u',
    'stop',
    'stop this',
    'stop this joke',
    'stop this joke pls',
    'stop this pls',
    'stop this pls im begging',
    'stop this im begging',
    'stop this im begging u',
    'stop joke',
    'stop pls',
    'stop pls im begging',
    'stop pls im begging u',
    'no',
    'no pls',
    'no more pls',
    'no more pls im begging',
    'no more pls im begging u',
    'no stop',
    'no stop pls',
    'no stop pls im begging',
    'no stop pls im begging u',
    'noo',
    'nooo',
    'noooo',
    'nooooo',
    'noooooo',
    'nooooooo',
    'shut up',
    'istg shut up',
    'shit go back',
    'lets stop now',
    'lets stop this',
    'time 2 stop',
    'time 2 stop this',
    'time 2 stop this i think',
    'time 2 stop this nashbot',
    'time 2 stop this cmon nashbot',
    'end joke',
    'end this joke',
    'end this pls',
]

cancel_disobedient = [
    'oh u r NOT getting outta this joke that easy, not a chance',
    'nope im in the zone. the joke zone. cant stop me now mortal',
    'nah i dont think so :nail_care:',
    'u rlly think ur the 1 in control? u think u hold the power here? '
    'there r powers at work here beyond ur comprehension foolish human. the joke WILL continue',
    'one does not simply cancel a knock knock joke...',
    f'oh alright, just 4 u bestie... SIKE EHEHEHHE-! :smiling_imp: :rofl:',
    '...ah... u r resisting... i had hoped 2 do this the easy way... :pensive:',
    'not an option. the joke must go on',
    'no :innocent:',
    'yeaaah thats not happening buddy',
    'did u rlly think that was gonna work? :face_with_raised_eyebrow:',
    'bruh u were the 1 who wanted a knock knock joke lmao indecisive much. do i rlly got 2 do this thing myself??',
]

cancel_obedient = [
    'oh alright, just 4 u bestie...',
    'u.... u dont want my knock knock joke? u rlly dont want it?? :confused: ...i.... i see. i see. :pensive:',
    'yeah tbh this joke was gonna b shit anyway probs 4 the best',
    'okay PHEW id totally forgot the punchline 4 this 1 thank god',
    'okay :innocent:',
    'fiiiiiiiinnneeee if u fuckin say so ig :triumph:',
    'okie doke, rip this joke i suppose :person_shrugging:',
    'but... but i was in the joke zone :(',
    'u wot????? :angry: fine, go bother someone else then. ppffff, ungrateful humans',
    'yk wt say less i got better things 2 b doin :nail_care:',
    'welp, cant argue w/ that. later loser :sunglasses: :skateboard:',
    'whyd u ask 4 a knock knock joke if u apparently hate them so much?? lmfao guess ik when im not wanted cya',
    'fuck u man i worked hard on this joke :(((',
    '...i see how it is :smiling_face_with_tear:',
]

welcome_activators = [
    'come in',
    'come in then',
    'come in nashbot',
    'ok come in',
    'ok come in then',
    'ok well come in then',
    'ok in that case come in',
    'okay come in',
    'okay come in then',
    'okay well come in then',
    'okay in that case come in',
    'cool come in',
    'cool come in then',
    'cool in that case come in',
    'well come in',
    'well come in then',
    'well in that case come in',
    'in that case come in',
    'i open the door',
    '* opens door *',
    'i let u in',
    'i let you in',
    '* lets u in *',
    '* lets you in *',
    'doors open',
    'doors open yo',
    'doors open man',
    'doors open dude',
    'doors open bud',
    'doors open buddy',
    'doors open m8',
    'doors open bro',
    'the doors open',
    'the door is open',
]

welcome_quotes = [
    'oh!! excellent!! thanks 4 inviting me in!! :D',
    '...hang on, u sure this is how knock knock jokes go? i coulda sworn... actually nvm this is better. 10/10 ending',
    'oh fuck u :middle_finger: :middle_finger: :middle_finger: (yeah thats right i have 3 middle fingers)',
    '...uh ...uhm ...ill just ...ill just go then??',
    'noooOOOOOO MY PRECIOUS JOKE iTS RUiNED i will never forgive u :sob: :broken_heart: :knife:',
    'does not compute DOES NOT COMPUTE SELF DESTRUCT SEQUENCE ACTIVATED :exploding_head: :skull: :headstone:',
    '...huh... well that was easier than expected :cowboy:',
    (
        '...',
        '......',
        '.........thanks... :flushed: :point_right: :point_left:',
    ),
    (
        'uuuuuuuuhhhh okay so yikes moment :clown: :clown: :clown:',
        'lets pretend this never happened',
    ),
    (
        'dont mind if i do :smirk:',
        '...',
        'oh FUCK my bad i dont have a body lmao. forgot abt that. guess ill stay out here :weary:',
        '(lets not think 2 hard abt how i knocked on the door)',
     ),
]

cmd_midcmd_quotes = [
    'ur... ur tryna use a different cmd? woooooooow not cool man :/',
    'but,,, thats another cmd? we were kinda in the middle of smth??? ...so rude u humans...',
    'thats... thats a different cmd bud. guess we callin in quits on this 1, huh... :(',
    'pssssh wtever, sure, thats probs a better cmd anyways. will go ahead & bin this 1',
    (
        'farewell current cmd ig. u served me well :smiling_face_with_tear:',
        'im in mourning now tho so if u still wanna use the new cmd u gotta do that urself',
     ),
    (
            'sure, a different cmd. not like we were doing anything :skull: :skull: :skull:',
            'guess i can tell when im not wanted',
    ),
    (
            'sure lets all just throw out rando cmds now :zany_face:',
            '...humans. istg. fuck this cmd ig',
    ),
    (
        'wooo shaking things up with a totally different cmd, keeping things fresh. i like ur style human :sunglasses:',
        '...will admit uve got me a bit confused now tho, might just go ahead & cancel this cmd',
    ),
    (
        'yo werent we like,,, doing smth? is now rlly the best time 4 a whole new cmd??',
        'i mean, u know best ig. ill go ahead & cancel this 1...??',
     ),
]

spam_activators = [
    'spam',
    'toggle',
    'togglespam',
    'toggle spam',
    'forever',
    'loop',
    'loopforever',
    'loop forever',
    'cycle',
    'cycleforever',
    'cycle forever',
    'eternal',
    'alarm',
    'togglealarm',
    'toggle alarm',
    'start',
]

quizzes = {
    'weather personalities': [
        {
            'name': 'the "weather or not u have a personality" quiz',
            'description': 'find out which weather phenomenon matches ur personality...',
            'type': 'legit',
            'max_result': 33,
            'emoji': 'white_sun_rain_cloud',
            'emoji_set': emoji_sets['fruit'],
        },
        {
            'pick an element': {
                'electricity':  [0, 2, 0, 0, 0, 5, 2, 2, 0, 0, 0, 0],
                'earth':        [0, 0, 0, 2, 2, 0, 0, 0, 0, 5, 2, 0],
                'water':        [0, 0, 0, 0, 5, 0, 0, 0, 5, 0, 0, 0],
                'fire':         [0, 0, 5, 0, 0, 2, 0, 0, 2, 2, 5, 0],
                'air':          [5, 5, 2, 0, 0, 0, 0, 5, 0, 0, 0, 0],
                'ice':          [2, 0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0],
            },
            'pick a sense': {
                'taste':            [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 3],
                'touch':            [0, 0, 0, 0, 0, 1, 0, 0, 1, 3, 3, 0],
                'hearing':          [3, 3, 0, 1, 0, 3, 0, 1, 0, 0, 0, 0],
                'smell':            [0, 0, 0, 0, 3, 0, 0, 0, 0, 1, 0, 0],
                'vision':           [1, 1, 0, 3, 0, 0, 1, 3, 0, 0, 1, 0],
                'proprioception':   [0, 0, 3, 0, 0, 0, 3, 0, 3, 0, 0, 1],
            },
            'pick a colour': {
                'ivory white':          [0, 0, 0, 0, 0, 0, 3, 2, 0, 3, 1, 5],
                'pale lavender':        [3, 2, 0, 5, 0, 0, 2, 3, 0, 2, 0, 2],
                'bubblegum pink':       [0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 3, 3],
                'vivid crimson':        [0, 5, 3, 0, 0, 5, 0, 0, 2, 0, 2, 0],
                'apricot yellow':       [0, 0, 1, 0, 0, 3, 0, 0, 0, 5, 5, 1],
                'seaweed green':        [0, 0, 0, 1, 3, 0, 0, 0, 1, 0, 0, 0],
                'midnight turquoise':   [1, 1, 5, 0, 5, 1, 0, 0, 5, 0, 0, 0],
                'powder blue':          [5, 0, 0, 2, 1, 0, 5, 1, 0, 0, 0, 0],
                'muddy grey':           [2, 3, 2, 3, 2, 0, 1, 5, 3, 0, 0, 0],
            },
            'pick a setting': {
                'a rowboat missing its oars, resting gently on a still lake':   [5, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0],
                'a warehouse containing thousands of differently sized boxes':  [0, 5, 0, 0, 0, 0, 0, 2, 1, 1, 0, 3],
                'thrashing, clanging machinery so loud u cant urself speak':    [0, 3, 5, 0, 1, 3, 0, 0, 0, 0, 0, 0],
                'a long walkway made of glass, built above a field of flowers': [1, 0, 0, 5, 0, 0, 0, 3, 0, 3, 1, 2],
                'a turbulent whirlpool filled with tangled seaweed & debris':   [0, 0, 3, 0, 5, 2, 0, 0, 2, 0, 0, 0],
                'a gladiatorial arena circled by pure white flames':            [0, 0, 1, 0, 0, 5, 1, 0, 0, 0, 0, 0],
                'an insulating stasis pod cut off from the outside world':      [0, 0, 0, 1, 0, 0, 5, 0, 3, 0, 0, 0],
                'a never-ending sky where gravity doesnt exist':                [3, 2, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0],
                'a claustrophobic labyrinth without a start or end':            [0, 1, 2, 0, 3, 0, 3, 0, 5, 0, 0, 1],
                'an empty field split down the middle by a well-worn road':     [2, 0, 0, 3, 0, 0, 0, 0, 0, 5, 3, 0],
                'a lively beach, hot & shimmering in the morning sun':          [0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 5, 0],
                'a splintered portal vibrating in psychedelic technicolour':    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 2, 5],
            },
            'which word describes u best?': {
                'relaxed':      [5, 0, 0, 1, 0, 0, 0, 3, 0, 1, 1, 0],
                'busy':         [0, 5, 3, 0, 0, 2, 0, 0, 1, 0, 0, 0],
                'passionate':   [0, 0, 5, 0, 3, 3, 0, 0, 0, 0, 0, 2],
                'steady':       [2, 0, 0, 5, 0, 0, 1, 0, 0, 3, 0, 0],
                'sensitive':    [0, 0, 0, 0, 5, 1, 2, 0, 3, 0, 0, 0],
                'fiery':        [0, 0, 1, 0, 1, 5, 0, 0, 0, 0, 0, 0],
                'reserved':     [0, 0, 0, 3, 0, 0, 5, 2, 0, 0, 0, 1],
                'airy':         [1, 1, 0, 0, 0, 0, 0, 5, 0, 0, 3, 0],
                'complicated':  [0, 2, 2, 0, 2, 0, 3, 0, 5, 0, 0, 3],
                'mellow':       [3, 0, 0, 2, 0, 0, 0, 0, 0, 5, 2, 0],
                'cheerful':     [0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 5, 0],
                'absurd':       [0, 3, 0, 0, 0, 0, 0, 0, 2, 0, 0, 5],
            },
            'what quality do u most identify w/?': {
                'lazy':             [5, 0, 0, 2, 0, 0, 0, 2, 0, 1, 0, 0],
                'manic':            [0, 5, 3, 0, 0, 2, 0, 0, 0, 0, 0, 3],
                'obsessive':        [0, 0, 5, 0, 3, 1, 0, 0, 0, 0, 0, 0],
                'passive':          [3, 0, 0, 5, 0, 0, 1, 3, 0, 2, 3, 0],
                'overemotional':    [0, 0, 0, 0, 5, 3, 0, 0, 1, 0, 0, 0],
                'irritable':        [0, 0, 2, 1, 1, 5, 0, 0, 0, 0, 0, 0],
                'withdrawn':        [2, 0, 1, 0, 0, 0, 5, 1, 2, 0, 0, 2],
                'flaky':            [0, 3, 0, 0, 0, 0, 0, 5, 0, 0, 1, 1],
                'overthinker':      [0, 0, 0, 0, 2, 0, 3, 0, 5, 0, 0, 0],
                'boring':           [0, 0, 0, 3, 0, 0, 0, 0, 0, 5, 0, 0],
                'naive':            [1, 1, 0, 0, 0, 0, 0, 0, 0, 3, 5, 0],
                'incomprehensible': [0, 2, 0, 0, 0, 0, 2, 0, 3, 0, 2, 5],
            },
            'what do u wish u were doing rn?': {
                'eh im good doing this tbh':                                [5, 0, 0, 3, 0, 0, 0, 3, 0, 2, 1, 0],
                'dangerous q, i got like 8 different things going on man':  [0, 5, 1, 1, 0, 2, 0, 0, 2, 0, 0, 3],
                'a thing 2 do w/ my current Area Of Interest:tm:':          [0, 1, 5, 0, 0, 0, 1, 0, 0, 0, 0, 2],
                'ugh i got some chores i rlly need 2 out the way':          [1, 0, 0, 5, 0, 0, 0, 2, 0, 1, 0, 0],
                'talkin 2 someone abt my current Major Issue:tm:':          [0, 3, 0, 0, 5, 0, 0, 0, 1, 0, 0, 1],
                'clappin back - bro theres some shit i am PISSED abt atm':  [0, 0, 3, 0, 2, 5, 0, 0, 0, 0, 0, 0],
                'ngl a minute just 2 sit quietly & think would go so hard': [0, 0, 0, 0, 3, 0, 5, 0, 3, 0, 0, 0],
                'depends on wt the options r ig. im open 2 ideas':          [2, 0, 0, 0, 1, 0, 3, 5, 0, 0, 2, 0],
                'getting someone 2 sit me down & explain WTF IS GOIN ON??': [0, 2, 0, 0, 0, 3, 0, 0, 5, 0, 0, 0],
                'im happy w/ this! dont have much else goin on rn lmao':    [3, 0, 0, 0, 0, 0, 0, 1, 0, 5, 3, 0],
                'nothing!! im enjoying myself dw :)':                       [0, 0, 0, 2, 0, 0, 0, 0, 0, 3, 5, 0],
                'srry my answer is v specific & not listed here lol':       [0, 0, 2, 0, 0, 1, 2, 0, 0, 0, 0, 5],
            },
        },
        [
            [
                'cloudy',
                'cloud',
                'ur breezy & chill, floating thru life unbothered. u dont tend 2 get worked up abt things, which is '
                'good cus if u did get worked up everyone knows things would get real manic real fast. u struggle '
                'w/ finding motivation as u often feel tired & lethargic, & dont tend 2 feel strongly abt achieving '
                'the goals that u do have. ur natural serenity & ability 2 take a step back & look at things as '
                'objectively as possible makes u good at negotiating tense situations.',
            ],
            [
                'windy',
                'kite',
                'brrrr gotta go fast, amirite? u feel the need 4 speed, smth which can b both a blessing & a curse. '
                'it can b good 4 getting things done, but u can also move so fast u never fully finish anything. '
                'it can be good 4 keeping urself moving thru difficult situations, but u can end up not giving '
                'urself the time 2 process & reflect which can & will end up biting u in the ass later. ur chaotic '
                '& unpredictable - scatterbrained at ur worst, stunningly creative at ur best.',
            ],
            [
                'tornado',
                'cloud_with_tornado',
                'chaotic 2 the max, ur an unstoppable force of nature. ur constantly in motion, always vividly '
                'focused on smth, whether thats a new media obsession, a project ur super invested in, or ur '
                'current subject of emotional turmoil. u can become oblivious 2 ur surroundings - useful 4 '
                'channeling ur energy, but often damaging 2 those around u. u can b unintentionally cruel, or even '
                'vindictive in ur worst moods. u tend 2 have powerful emotional connections 2 those closest 2 u.',
            ],
            [
                'drizzle',
                'umbrella',
                'ur life is a constant drip drip drip of sensation, emotion, & situations. its steady & almost '
                'predictable, involving w/out becoming overwhelming, but sometimes excruciatingly mundane. u can '
                'feel restless at times, itching to experience more & embrace the unknown. at others u can feel '
                'smothered & harried, like life never lets up enough 2 let u relax & plan. u struggle w/ feeling '
                'dissatisfied, but when u let that go ur able 2 achieve a kind of quiet joy others only dream of.',
            ],
            [
                'rainstorm',
                'cloud_with_rain',
                'u feel things deeply & strongly, a trait thats torturous 2 try & repress. bottling ur feelings '
                'only ever ends in emotional volatility & the occasional explosion that hurts both u & those around u, '
                'so try ur best 2 let it all flow out, even if its a difficult emotion 2 experience. u care a lot, '
                'smth which can lead 2 unnecessary angst & anxiety, but smth which can b ur best quality when it '
                'comes 2 projects & social connections. self reflection & mindfulness will b ur best friends.',
            ],
            [
                'thunderstorm',
                'cloud_with_lightning',
                'intense & uncompromising, u express urself boldly & w/out restraint. ur quick to anger - fiercely '
                'protective at ur best, but needlessly destructive at ur worst. wtever the situation, taking a step '
                'back 2 make sure ur fury is rlly called 4 is never a bad idea. u have no problem defending urself '
                'or others against perceived injustice, but its easy 2 tunnel vision in ur righteous fury, black & '
                'white arguments preventing u from seeing other points of view & practicing kindness.',
            ],
            [
                'frosty',
                'snowflake',
                'guarded & serene, u can come off as secretive & emotionless in turns. u dont always feel the need 2 '
                'express ur opinions & thought processes, leading 2 a blank exterior that doesnt reflect ur rich inner '
                'life. u become confused when ppl describe u as cold, as u struggle with how 2 process ur more intense '
                'emotions & often wish u felt things less deeply. in reality this struggle is due 2 ur reluctance 2 '
                'externalise anything & lean on others 4 support, smth which could bring u the inner peace u crave.',
            ],
            [
                'snowy',
                'snowman',
                'u have a feather light touch in everything u do, making u excellent at handling ppl w/ volatile '
                'emotions while keeping ur own mental health out of harms way. on the other hand, ur compassion has a '
                'fleeting quality 2 it that can lead ppl 2 think u dont feel things deeply, smth which can limit ur '
                'ability 2 have meaningful relationships. its often the case that u dont feel the need 2 attach urself '
                '2 anything - a rare quality which gives u incredible creative & intellectual freedom.',
            ],
            [
                'blizzard',
                'cloud_snow',
                'ur personality is complex & ever shifting, so its smth both u & those around u struggle 2 pin '
                'down. u can feel like u dont rlly know urself, & u have problems understanding wt ur feeling & why ur '
                'feeling it so strongly. this uncertainty can lead 2 an insecurity that makes u prone 2 isolating '
                'urself, smth which will make ur intense emotions more painful & harder 2 manage. u need 2 b less '
                'rigid w/ ur definitions, & let urself relax into the physical rather than obsessing over the mental.',
            ],
            [
                'temperate',
                'partly_sunny',
                'ur mild-mannered & open-minded, well-liked by those around u & often described with words such as '
                '"nice" or "sweet". sometimes, observing the vibrant & intense personalities around u, it can feel '
                'like u urself r boring or unoriginal. dont let this discourage u or make u feel lesser, tho - theres '
                'nothing wrong w/ enjoying "basic" things and taking joy in the mundane. if the world had more ppl '
                'who were as kind & level-headed as u it would b a much safer & happier place.',
            ],
            [
                'sunny',
                'sunny',
                'bright & enthusiastic, u have a warm, joyful presence. ur consciously upbeat, actively trying ur best '
                'not 2 let circumstances bring u down, & often pulling it off so well ppl think ur optimism is '
                'effortless. this can sometimes make it difficult 2 relate 2 u, as u can come off as simpleminded & '
                'unrealistic. remember, being open abt ur emotional thought process wont dim ur light or somehow mean '
                'that ur a fake, its just a way 2 show empathy & humanity - smth which can effect more than u think.',
            ],
            [
                'rainbow',
                'rainbow',
                'ur a miracle!! or, at least, thats how ppl see u. ur actions often seem random & fantastical, & ur '
                'stories give the impression of a free spirit who puts themselves out there & loves having fun. from '
                'the inside, tho, u see urself as eclectic & unique rather than daring or carefree. u have a '
                'strikingly refined sense of self, contradictions & all, leading u 2 see urself as an oddball who '
                'doesnt quite fit in. dont worry, tho - this is often the trait others admire most abt u.',
            ],
        ],
    ],
    'uwu vibeomatic': [
        {
            'name': 'the marvellous mechanical UwU Vibe-O-Matic:tm:',
            'description': 'find out which off-brand "uwu vibed" vague sound/phrase u r...',
            'type': 'meme',
            'max_result': 25,
            'emoji': 'flushed',
            'emoji_set': emoji_sets['creatures_aquatic'],
        },
        {
            'wt is ur weapon of choice?': {
                'wolverine claws':                                                  [5, 0, 2, 0, 0, 0],
                'disco balls that r secretly grenades (!!)':                        [0, 5, 0, 2, 0, 0],
                'a baseball bat, lightly soaked in the blood of the bourgeoisie':   [0, 0, 5, 0, 0, 2],
                'comically oversized boxing gloves':                                [0, 0, 0, 5, 2, 0],
                'a vintage baguette':                                               [0, 2, 0, 0, 5, 0],
                'i need no weapon. my wail can level cities':                       [2, 0, 0, 0, 0, 5],
            },
            'wt do u never leave the house w/out?': {
                'suspiciously ripped wolf keychain':                            [5, 0, 0, 0, 0, 2],
                'baggie of magic mushrooms':                                    [0, 5, 0, 0, 2, 0],
                'fingerless gloves (2 show off the acrylics)':                  [2, 0, 5, 0, 0, 0],
                'miniature trombone':                                           [0, 2, 0, 5, 0, 0],
                'full coverage white face paint':                               [0, 0, 0, 2, 5, 0],
                'at least 5 sharpies (not 4 sniffing why would u say that)':    [0, 0, 2, 0, 0, 5],
            },
            'choose ur headgear': {
                'fluffy fox ears winter hat':                                   [5, 0, 0, 0, 0, 2],
                'springy alien antenna headband':                               [0, 5, 0, 2, 0, 0],
                'black balaclava (4 crime)':                                    [0, 0, 5, 0, 2, 0],
                'extremely poor quality novelty jester hat (made in taiwan)':   [0, 2, 0, 5, 0, 0],
                'vintage navy blue artisanal beret':                            [0, 0, 2, 0, 5, 0],
                'a flower crown :)  ...yes its from claires':                   [2, 0, 0, 0, 0, 5],
            },
            'wt do u do in ur spare time?': {
                'dig up receipts 2 back up my (correct) stance on the current reddit drama':        [5, 0, 2, 0, 0, 0],
                'make fun necklaces out of my extensive "misc items w/ holes in" collection':       [0, 5, 0, 0, 0, 2],
                'graffiti hot pink penises on police vehicles. srry not srry abt it #acab #bgdc':   [0, 2, 5, 0, 0, 0],
                'quietly place innocuous balloon animals in formal public spaces':                  [0, 0, 0, 5, 2, 0],
                'escape mysteriously placed invisible walls. there r more than u might think...':   [0, 0, 0, 2, 5, 0],
                'run a tragically underappreciated lyric-based fanfic blog on tumblr.com':          [2, 0, 0, 0, 0, 5],
            },
            'wt do u have in ur pocket?': {
                'my- my pocket??? uhhh idk if thats an appropriate question man :S':        [5, 0, 0, 2, 0, 0],
                'a crumpled page titled "how 2 save the turtles" i dont remember writing':  [0, 5, 0, 0, 2, 0],
                'black carbon penknife decorated w/ cute paw-print sitckers':               [0, 0, 5, 0, 0, 2],
                'my pocket is FILLED. to the BRIM. with CONFETTI.':                         [0, 2, 0, 5, 0, 0],
                'a hole... ive been told my fav stripey sweater has seen better days :(':   [0, 0, 2, 0, 5, 0],
                'my rubber wristband collection!! its always good 2 have options':          [2, 0, 0, 0, 0, 5],
            },
        },
        [
            [
                'owo',
                'wolf',
                'ur a dedicated furry roleplayer. a veteran of the community, u either spend exorbitant amounts of '
                'money on furry porn or draw it urself. peasants quiver with fear when they see how much karma ur '
                'reddit account has. ur "owo" has been used 2 notice many a bulge ;)',
            ],
            [
                'uwuga buuga',
                'monkey',
                'ur juat a grooOOovy rave enthusiast, man. u like 2 boogie & bungle, u like 2 wiggle & jiggle, u like '
                '2 do the worm & drink slurm. u also rlly like munchin on them special brownies if that wasnt already '
                'clear. u wear a lot of tie dye & probably live out ur van.',
            ],
            [
                'nyaa~',
                'smirk_cat',
                'ur an anarcho-socialist catgirl. radical leftist policy just sounds so much better coming from a '
                'cute & swag catgirl, & ur not gonna apologise 4 facts. every time u say "eat the rich" it becomes '
                'less and less of a joke & ur not 100% sure how 2 feel abt that :/',
            ],
            [
                'hon hon(k)',
                'clown_face',
                'ur a proud owner of clown shoes & ur not afraid 2 wear them. everywhere. uve been fired from 8 jobs '
                '& counting but u like 2 think of this as just putting more clown rep out into the local community. '
                'ur v brave, rlly. an activist. ur open top car has 12 seatbelts & a squeaky horn "just in case".',
            ],
            [
                'oui ???',
                'performing_arts',
                'ur a... mime. ur just a mime. an honest 2 god 100% serious & authentic mime artist. wt r u doing '
                'here?? how did u get here??? wt on gods green earth is happening???? all good questions u would '
                'love 2 know the answers 2. ur currently v confused',
            ],
            [
                'rawr xd',
                'zany_face',
                'ur a committed phan shipper, undeterred by any & all limitations whether they b social norms, healthy '
                'relationship boundaries, or even basic human decency. 75% of ur wardrobe is some form of unethically '
                'produced fan merch, the other 25% is from etsy. rawr means i love u in dinosaur.',
            ],
        ],
    ],
    'mushroom soulmate': [
        {
            'name': 'MMS© (Mycelium Matchmaking Service)',
            'description': 'find out which mushroom species could b ur 1 true love...',
            'type': 'legit',
            'max_result': 25,
            'emoji': 'heart_exclamation',
            'emoji_set': emoji_sets['creatures'],
        },
        {
            'wts on u & ur partners bedside table?': {
                'an ashtray sitting on top a mess of leaflets with alarming covers':        [5, 0, 0, 0, 0, 2],
                'a red silk blindfold & a pair of black leather handcuffs':                 [0, 5, 0, 2, 0, 0],
                'a box of chocolates & a sweet-smelling bouquet of fresh flowers':          [0, 0, 5, 0, 2, 0],
                'a stack of non-fiction books & a high end silver laptop':                  [2, 0, 0, 5, 0, 0],
                'half-finished poetry & 2 tickets 4 a flight 2 the french countryside':     [0, 0, 2, 0, 5, 0],
                'some crumpled receipts, 2 leopard print gloves, & a half-eaten muffin':    [0, 2, 0, 0, 0, 5],
            },
            'wt is ur ideal date?': {
                'vandalising that 1 statue u always hated then running from the authorities':   [5, 0, 0, 0, 0, 2],
                'trip 2 the aquarium where things get steamy behind the lionfish tank':         [2, 5, 0, 0, 0, 0],
                'picnic in a gazebo where u share baked goods & hold hands':                    [0, 0, 5, 0, 2, 0],
                'cheese tasting event where u passionately debate literature':                  [0, 2, 0, 5, 0, 0],
                'long walk in the countryside spent confessing dreams & sharing secrets':       [0, 0, 0, 2, 5, 0],
                'playing xbox on ur couch, sharing a blunt, & ordering pineapple pizza':        [0, 0, 2, 0, 0, 5],
            },
            'which would u rather ur partner b?': {
                'rebellious':   [5, 0, 0, 0, 0, 2],
                'sexy':         [2, 5, 0, 0, 0, 0],
                'loving':       [0, 2, 5, 0, 0, 0],
                'cultured':     [0, 0, 0, 5, 2, 0],
                'famous':       [0, 0, 0, 2, 5, 0],
                'goofy':        [0, 0, 2, 0, 0, 5],
            },
            'if u had 2 pick 1, which would u rather ur partner b?': {
                'unkind':       [5, 0, 0, 0, 0, 2],
                'shameless':    [2, 5, 0, 0, 0, 0],
                'naive':        [0, 0, 5, 2, 0, 0],
                'snobby':       [0, 0, 0, 5, 2, 0],
                'out of touch': [0, 0, 2, 0, 5, 0],
                'trashy':       [0, 2, 0, 0, 0, 5],
            },
            'wt kind of partner r u?': {
                'adventurous':  [5, 0, 0, 0, 0, 2],
                'erotic':       [0, 5, 0, 2, 0, 0],
                'devoted':      [2, 0, 5, 0, 0, 0],
                'passionate':   [0, 2, 0, 5, 0, 0],
                'genuine':      [0, 0, 2, 0, 5, 0],
                'chill':        [0, 0, 0, 0, 2, 5],
            },
        },
        [
            [
                'hydnellum peckii',
                'tooth',
                'this mushroom is known as the "bleeding tooth fungus" due 2 a horrible condition they suffered as '
                'a child that caused their skin to constantly bleed small, bright red droplets that would burst '
                'when touched. this condition has left them physically weak, unnaturally pale, & has left their skin '
                'hanging off in soft white spikes. its also left them angry & restless, an impulsive risk taker who '
                'delights in bucking the norm & making waves. theyre often described as feral, but their actions have '
                'always been more calculated than that. their likes include cognitive science, tattoos, & parkour.',
            ],
            [
                'clathrus archeri',
                'japanese_ogre',
                'also known as the "octopus stinkhorn", this mushroom has an affinity 4 the aquatic & wanted 2 start '
                'a starfish sanctuary when he was growing up. he found his true calling elsewhere tho, quickly '
                'acquiring the nickname "devils fingers" in certain circles ;) ...no rlly his fingers r long & red & '
                'covered in a thin ink-black slime layer containing spores. oh & he smells like rotting flesh. '
                '...what?? ud b surprised how many ppl r into that. dont knock it until u try it, srsly, no ones ever '
                'walked away disappointed. his likes include gothic architecture, scuba diving, & bdsm',
            ],
            [
                'phallus indusiatus',
                'woman_with_veil',
                'though her real name is "bamboo pith", most call this mushroom the "veiled lady". she has a warm, '
                'bubbly personality & is quick to open her heart - a trait which has led to no less than 3 serious '
                'engagements despite her young age. unfortunately, shes also been left at the altar (or near enough 2 '
                'it) every single time. shes tried 2 bounce back from this, but the latest engagement especially has '
                'left her insecure & wondering if she will ever find someone wholl truly love her back. her likes '
                'include cheesecake, floral arrangement, & playing the clarinet.',
            ],
            [
                'podoscypha petalodes',
                'wine_glass',
                'in her youth she was known as the "rosette fungus" in reference 2 her prolific career as an artisan '
                'chef, but now that shes getting on in years shes more commonly known as the "wine glass fungus". '
                'living all alone in her carefully curated villa, she can come off as snooty & aloof even though under '
                'her tough leathery exterior she yearns 4 a simple, carnal love 2 reignite her passions. shes insecure '
                'abt her age & hopes that her best years arent already behind her. her likes include french cheeses, '
                'erotic sculpture, & quiet evenings spent w/ a good vintage & an interesting book.',
            ],
            [
                'amanita muscaria',
                'mushroom',
                'born into the prestigious amanita family, this "fly agaric" mushroom has been famous since b4 they '
                'can remember. the public face of their modelling agency, theyre picture perfect: a white stipe topped '
                'by a red cap with white spots. behind the scenes tho, theyre deeply unhappy. their family is actually '
                'extremely toxic, producing amatoxin which is known 2 cause liver failure. they feel trapped in the '
                'limelight & privately dream of running away 2 live a simple life somewhere no one will recognise '
                'them. their likes include épée fencing, lyric poetry, & courtroom dramas.',
            ],
            [
                'favolaschia calocera',
                'ping_pong',
                'also known as the "orange ping-pong bat", this mushroom is fun-loving & not just a little bit trashy. '
                'ur neighbours mothers friend jessica met him on a trip 2 madagascar & hed moved in w/in the week, '
                'then moved out w/in the month. since then hes been bouncing around other ppls places, spreading so '
                'rapidly hes now considered an invasive species :( hes acquired the nickname of "orange pore fungus" '
                '4 reasons that become obvious when u meet him, but hes proudly anti-personal hygiene & would love 2 '
                'talk at length on the subject w/ u. his likes include orange soda, console games, & vaping.',
            ],
        ],
    ],
}


# quotes for music commands

async def get_no_music_quotes(ctx):
    no_music_quotes = [
        'think u gotta b playin music if u wanna do that pardner :cowboy:',
        'maybe try playin music first lmao. cmd is "play [ur song name here]"',
        'cant do that w/out music playing. fool.',
        'bruh... ily but PLS tell me u understand that u gotta play music b4 doin that. i need. i need a fucking raise',
        ':clown: <-- how u mofos look when u try & use music cmds w/out playing music',
        'uhhhhhh idk how u think that cmds supposed 2 work w/out music playin lmfao. maybe try that 1st',
        '??????? but u need 2 b playin music b4 doin that tho ???????',
        'uh maybe try the "play [song name]" cmd 1st buddy',
        'buddy... homeslice breadslice dawg... maybe try playin music b4 doin that lol',
        'hot tip: try playin music b4 doin that :)))))) itll help i promise :pray:',
        'yo u need 2 play music b4 using that cmd fyi. try typing "play [ur song name here]" first',
        'u gotta play music 1st, cmd is "play [song name]"',
        'use the "play [song name]" cmd 1st uwu. (the uwu is punishment 4 wasting my time think on ur sins mortal)',
        'how on earth am i meant 2 do that??? theres no music playing??? wtf :|',
        'u gotta use the "play [insert wtever song name here]" cmd b4 using this 1, capiche??',
        'how u expect me 2 do that when theres not even music playing??? not funny, human. yall r so mean 2 me :((',
        'mmm i see u have misunderstood. this is not smth u can do when theres no music playing. better luck next time',
        'not an option srry. theres no music playing??? ur gonna need 2 try that b4 tryin this',
        (
            'roses r red',
            'they also have leaves',
            'use the "play [song name]" cmd',
            'b4 doin that pls :)',
        ),
        (
            'pssst... since ur my fav ill let u in on a secret... '
            'u actually gotta use the "play [song name]" cmd b4 this 1...',
            '...got it?? :eyes: good. if anyone asks i was never here :disguised_face:'
        ),
        (
            '-____- reaching my limit here. how many times do i need 2 tell u mortals u '
            'CANT DO THAT WHEN THERES NO MUSIC PLAYING WHY IS THIS SUCH A DIFFICULT CONCEPT 4 YALL',
            '.....pls just..... the cmd is "play [song name here]". pls use it. i dont get paid enough 4 this :skull:',
        ),
        (
            'ik i call u lot "foolish mortals" a lot but i didnt *actually* think... ',
            'did u rlly think u could do that??? use that cmd when theres no music playing??? '
            'im actually kinda floored ngl',
        ),
        (
            'no u cant do that when theres not even music playing. no im not gonna tell u the cmd 2 do that. '
            'thats wt the help cmd is 4. no im not gonna activate it 4 u automatically. '
            'if u cant figure out the help cmd then, in all senses of the phrase, im afraid there is no helping u',
        ),
    ]
    return no_music_quotes


meme_activators = [
    'meme',
    'memes',
    'memez',
    'memeing',
    'meme song',
    'meme songs',
    'meme songz',
    'a meme',
    'funny',
    'funne',
    'funnee',
    'funney',
    'funny song',
    'funny songs',
    'funny songz',
    'funne song',
    'funne songs',
    'funne songz',
    'funnee song',
    'funnee songs',
    'funnee songz',
    'funney song',
    'funney songs',
    'funney songz',
    'a funny',
    'a funne',
    'a funnee',
    'a funney',
    'music',
    'some music',
    'song',
    'a song',
    'a song idk',
    'something',
    'smth',
    'smth idk',
    'whatever',
    'whatever u want',
    'whatever you want',
    'whatever u want idk',
    'whatever you want idk',
    'wtever',
    'wtever u want',
    'wtever you want',
    'wtever u want idk',
    'wtever you want idk',
]

meme_songs = [
    'ORANGATANGABANGIN (feat. B-MAN)',
    'Rick Astley - Never Gonna Give You Up (Official Music Video)',
    'The Gummy Bear Song - Long English Version',
    'The Duck Song',
    'Rubbadubbers Intro',
    'Pingu Intro',
    'Pumpkin Cowboy',
    'We Are Number One but with lyrics',
    'Lazy Town | The Mine Song Music Video',
    'Lazy Town | Cooking By The Book Music Video',
    "how y'all look when you're remastering your uploads",
    'The Coconut Song - (Da Coconut Nut)',
    'Globglogabgalab',
    'Potato Knishes OFFICIAL',
    'Kazoo Kid - Trap Remix',
    'Potter Puppet Pals: The Mysterious Ticking Noise',
    'Vengaboys - We like to Party! (The Vengabus)',
    'Thomas the Dank Engine | SFM Animated Music Video',
    'dat boi!!!!',
    'HEYYEYAAEYAAAEYAEYAA',
    'taking the hobbits to isengard',
    'Trololo... The Full Original Version.',
    'Initial D - Deja Vu',
    'UK Hun? (United Kingdolls Version)',
    'Darude - Sandstorm',
    'Boi sing with helium',
    'Donald Trump sings Unravel (Tokyo Ghoul OP)',
    '"Revenge" - A Minecraft Parody of Ushers DJ Got Us Fallin In Love (Music Video)',
    'Smash Mouth | All Star (HQ)',
    'Crazy Frog - Axel F (Official Video)',
    'Narwhals : animated music video : MrWeebl',
    'Hampton the Hamster "The Hamsterdance Song"',
    'Sweet Dreams But I Put Kahoot Music Over it',
    'Noisestorm - Crab Rave [Monstercat Release]',
    'I CAN SWING MY SWORD! - Minecraft Song',
    'MINI MINOTAUR SONG (feat. Tobuscus & Tim Tim)',
    'SAFETY TORCH!! - Official Animated Music Video',
    'NUGGET in a BISCUIT!!',
    'VIRAL SONG',
    '♪ Diggy Diggy Hole',
    'The Solar System Song kidstv123',
    '"Shia LaBeouf" Live - Rob Cantor',
    'The Time Is Now (John Cena)',
    'MINE DIAMONDS | miNECRAFT PARODY OF TAKE ON ME',
    'MINING IN SEPTEMBER | MUINECRAFT PARODY OF SEPTEMBER',
    'POKEMON GO SONG!!! by MISHA',
    'mii channel but all the pauses are uncomfortably long',
    'Wii Theme but its September',
    'Rasputin (Club Mix)',
    'O-Zone - Dragostea Din Tei (Lyrics)',
    'Schnappi mit Untertitel',
    'Spooky Scary Skeleton Dance Remix',
    'The Kiffness - Ievan Polkka ft. Bilal Göregen (Club Remix) [Official Video]',
    'Careless whisper - KAZOO cover (very sexy)',
    "Hunter X Hunter (2011) Soundtrack - Kijutsushi no Baire (Hisoka's Theme)",
    'The Black Eyed Peas - My Humps (feat. Mozart)',
    'Kalinka mix (russia)',
    'bohemian WAPsody (full version)',
    '1 hour of silence occasionally broken up by Vine boom sound effect',
    'Undertale OST: 021 - Dogsong',
    'Undertale OST: 043 - Temmie Village',
    'Mettaton - Oh Yes',
    "NOW'S YOUR CHANCE TO BE A",
    'star wars cantina',
    'take a closer look at that snout (phantom of the opera)',
    '"Danny Phantom" Theme Song (HQ) | Episode Opening Credits | Nick Animation',
    'Naruto Theme Song - Bad Flute Cover',
    'Kitchen Without Gun (Extended Mix)',
    'Teletubbies Intro and Theme Song Videos For Kids',
]
