import discord
from discord.ext import commands
import random
import os

class Player():
    def __init__(self):
        self.presentables = []
        self.problem = ""
        self.votes = 0
    
class bizBot():
    #class full of game logic stuff
    problems = []
    
    imageFolder = "imgs\\"
    
    #gamephases none: no game started, starting: submitting ideas, planning: making ideas, presenting, voting
    gamePhase = "none"
    
    currentPresentIndex = 0  
    currentPresent = None
    presentOrder = None
    slideIndex = 0
    
    voted = []
    
    players = {}
    
    admin = None
    
    def __init__(self):
        pass
    


bot = commands.Bot(command_prefix="!")

@bot.command()
async def start(ctx):
    if bizBot.gamePhase == "none":
        bizBot.gamePhase = "starting"
        await ctx.channel.send("**Game started, use !submit <prompt> to submit as many problem promts as you'd like.\nUse !done when you're all done submitting.**")
        bizBot.admin = ctx.message.author
            
        
@bot.event
async def on_ready():
    print("Bot Online")
    #make folder to store images
    if not "imgs" in os.listdir("."):
        os.mkdir("imgs")

@bot.command()
async def wisdom(ctx):
    #depressing wisdom bot easter egg
    wisdoms = [
        "**Only the dead have seen the end of war.**",
        "**Violence is the last refuge of the incompetent.**",
        "**When you have to kill a man, it costs nothing to be polite.**",
        "**The last enemy that shall be destroyed is death.**",
        "**If you expect the worst, you'll never be disappointed.**",
        "**One may as well be optimistic. The road to catastrophe will be rougher if it's paved with dread.**",
        "**Behind every beautiful thing, there's some kind of pain.**",
        "**Appear weak when you are strong, and strong when you are weak.**",
        "**Let your plans be dark and impenetrable as night, and when you move, fall like a thunderbolt.**",
        "**If you know the enemy and know yourself, you need not fear the result of a hundred battles.**"
        
    ]
    await ctx.send(content=f"{random.choice(wisdoms)}", tts=True)
    await ctx.send(file=discord.File("guy.gif"))

@bot.command()
async def submit(ctx, *, problem="None"):
    if bizBot.gamePhase == "starting" and ctx.message.author in bizBot.players:
        await ctx.channel.purge(limit=1)
        bizBot.problems.append(problem)
        await ctx.send("**" + ctx.message.author.name + " submitted a prompt.**")
    print(bizBot.problems)
    
@bot.command()
async def play(ctx):
    if ctx.message.author not in bizBot.players and bizBot.gamePhase == "none":
        bizBot.players[ctx.message.author] = Player()
        await ctx.send("**" + ctx.message.author.name + " joined the game.**")
        await ctx.send("**Use !start to become the game master and start the game.**")
    print(bizBot.players)
    
@bot.command()
async def leave(ctx):
    if ctx.message.author in bizBot.players:
        del bizBot.players[ctx.message.author]
        if bizBot.gamePhase == 'presenting' or bizBot.gamePhase == 'voting':        
            bizBot.presentOrder.remove(ctx.meessage.author)
            
        if bizBot.currentPresent == ctx.message.author:
            bizBot.currentPresent = None
            bizBot.slideIndex = 0
        
        if len(bizBot.players) == 0 or bizBot.admin == ctx.message.author:
            await endGame(ctx)
            
        bizBot.voted.remove(ctx.message.author)
            

async def distributeProblems():
    random.shuffle(bizBot.problems)
    for i,p in enumerate(bizBot.players.items()):
        await p[0].send("**Your problem to solve is: **" + bizBot.problems[i] + "**.**")
        await p[0].send("**Use !text <text> to add a text description\nAttach an image in a message to add a image.\n**")
        bizBot.players[p[0]].problem = bizBot.problems[i]
        
        
@bot.command()
async def text(ctx,*,msg):
    if bizBot.gamePhase == "planning" and ctx.author in bizBot.players:
        bizBot.players[ctx.author].presentables.append(msg)
        print(msg)
        
image_types = ["png", "jpeg", "gif", "jpg"]

@bot.event
async def on_message(message: discord.Message): 
    if bizBot.gamePhase == "planning" and message.author in bizBot.players:
        for attachment in message.attachments:
            if any(attachment.filename.lower().endswith(image) for image in image_types):
                await attachment.save(bizBot.imageFolder + attachment.filename)
                bizBot.players[message.author].presentables.append(discord.File(bizBot.imageFolder + attachment.filename))
                #await message.channel.send(file = bizBot.players[message.author].presentables[-1])
        
    await bot.process_commands(message)

@bot.command()
async def next(ctx):
    await ctx.channel.purge(limit=1)
    print(bizBot.players[ctx.author].presentables)
    print(bizBot.players)
    if bizBot.gamePhase == 'presenting' and ctx.author in bizBot.players:
        
        if bizBot.currentPresentIndex < len(bizBot.presentOrder):
                
            if ctx.author == bizBot.currentPresent:
                if bizBot.slideIndex < len(bizBot.players[ctx.author].presentables):
                    presentable = bizBot.players[ctx.author].presentables[bizBot.slideIndex]
                    
                    if isinstance(presentable,str):
                        await ctx.channel.send(presentable)
                    else:
                        await ctx.channel.send(file=presentable)
                    bizBot.slideIndex += 1
                else:
                    bizBot.currentPresentIndex += 1  
                    bizBot.currentPresent = None
                    bizBot.slideIndex = 0
            
            if bizBot.currentPresent == None and bizBot.currentPresentIndex < len(bizBot.presentOrder):
                await ctx.channel.send("**------------------------------------------------------------------**")
                await ctx.channel.send("Next presenter is: " + bizBot.presentOrder[bizBot.currentPresentIndex].name)
                bizBot.currentPresent = bizBot.presentOrder[bizBot.currentPresentIndex]
                await ctx.channel.send("Their problem was: " + bizBot.players[bizBot.currentPresent].problem)
                
                if bizBot.currentPresentIndex >= len(bizBot.presentOrder):
                    await ctx.channel.send("**PRESENTING OVER! Use !done to start voting phase.**")
        else:
            await ctx.channel.send("**PRESENTING OVER! Use !done to start voting phase.**")

async def endGame(ctx):
    
    await ctx.send("**GAME HAS ENDED**")
    
    bizBot.players = {}
    bizBot.presentOrder = None
    bizBot.problems = []


    bizBot.gamePhase = "none"
    
    bizBot.currentPresentIndex = 0  
    bizBot.currentPresent = None
    bizBot.presentOrder = None
    bizBot.slideIndex = 0
    
    bizBot.voted = []
    
    
    bizBot.admin = None
    
    #remove all images once done
    for f in os.listdir(bizBot.imageFolder):
        os.remove(os.path.join(bizBot.imageFolder,f))
        
@bot.command()
async def restart(ctx):
    if bizBot.gamePhase != "none":
        if bizBot.admin == ctx.author:
            await endGame(ctx)
        else:
            await ctx.send("**ONLY THE GAME MASTER CAN RESTART THE GAME:** " + bizBot.admin.name)

@bot.command()
async def vote(ctx,msg):
    await ctx.channel.purge(limit=1)
    if bizBot.gamePhase == 'voting':
        num = int(msg)
    
        if ctx.author not in bizBot.voted:
            bizBot.voted.append(ctx.author)
            bizBot.players[bizBot.presentOrder[num]].votes += 1
    
    if len(bizBot.voted) == len(bizBot.players):
        maxP = [None,0]
        for playerObj,player in bizBot.players.items():
            if player.votes > maxP[1]:
                maxP = [playerObj,player.votes]
        await ctx.send("**:confetti_ball:THE PLAYER WITH THE MOST VOTES IS " + maxP[0].name + "!:confetti_ball:**")
        await endGame(ctx)
    
@bot.command()
async def helptmt(ctx):
    await ctx.send("TradeMark Troubles help:\n!play to join the game!\n!start to become the game master and start the game\n")       
@bot.command()
async def done(ctx):
    if bizBot.admin == ctx.author:
        if bizBot.gamePhase == "starting":
            await ctx.channel.send("**Planning phase begins. Check private DM's. Use !done to end planning phase.**")
            bizBot.gamePhase = "planning"
            await distributeProblems()
        elif bizBot.gamePhase == "planning":
            await ctx.channel.send("**Presenting phase begins. Use !next to move to the next presenter/next slide.**")
            bizBot.presentOrder = list(bizBot.players.keys())
                  
            bizBot.gamePhase = "presenting"
        elif bizBot.gamePhase == "presenting":
            await ctx.channel.send("**Voting phase begins.**")
            for i,player in enumerate(bizBot.presentOrder):
                await ctx.channel.send("!vote " + str(i) + " for " + player.name + " who solved: " + bizBot.players[player].problem)
            bizBot.gamePhase = "voting"
    else :
        await ctx.channel.send("**You must be the game master to use !done.**")
    
bot.run("BOT_TOKEN_HERE")



