# quotes.py


import asyncio


async def read_quote(ctx, quote):
    await ctx.trigger_typing()
    if isinstance(quote, tuple):
        await ctx.send(quote[0])
        for line in quote[1:]:
            await ctx.trigger_typing()
            await asyncio.sleep(1)
            await ctx.send(line)
    else:
        await ctx.send(quote)


async def read_official(ctx, quote, emoji):
    await ctx.trigger_typing()
    await ctx.send(f':{emoji}:  {quote}  :{emoji}:')


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
        f'...how juvinile. i expected better from u, {ctx.message.author.name}.',
    ]
    return highfive_quotes


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


# knock knock jokes

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
        f'excellent mashing of the keyboard sir :face_with_monocle: might i suggest u try "{expected}" next?',
        f'think ur 2 cool 2 say "{expected}" do u??',
        'w-what did u call me??!!?? :flushed:',
    ]
    return unexpected_quotes

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

cancel_responses = [
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

welcome_responses = [
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


# music

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
