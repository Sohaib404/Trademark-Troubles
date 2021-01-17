import discord
from discord.ext import commands
import random

class Player():
    def __init__(self):
        self.presentables = []
        self.problem = ""
        self.votes = 0
    
class bizBot():
        
    problems = []
    
    #gamephases none: no game started, starting: submitting ideas, planning: making ideas, presenting, voting
    gamePhase = "none"
    
    currentPresentIndex = 0  
    currentPresent = None
    presentOrder = None
    slideIndex = 0
    
    
    players = {}
    
    admin = None
    
    def __init__(self):
        pass
    


bot = commands.Bot(command_prefix="!")

@bot.command()
async def start(ctx):
    if bizBot.gamePhase == "none":
        bizBot.gamePhase = "starting"
        bizBot.admin = ctx.message.author
            
        
@bot.event
async def on_ready():
    print("Bot Online")

@bot.command()
async def wisdom(ctx):
    #depressing wisdom bot
    wisdoms = [
        "Only the dead have seen the end of war.",
        "Violence is the last refuge of the incompetent.",
        "When you have to kill a man, it costs nothing to be polite.",
        "Death, in its silent sure march is fast gathering those whom I have longest loved, so that when he shall knock at my door, I will more willingly follow.",
        "The last enemy that shall be destroyed is death.",
        "If you expect the worst, you'll never be disappointed.",
        "To die will be an awfully big adventure.",
        "One may as well be optimistic. The road to catastrophe will be rougher if it's paved with dread.",
        "Behind every beautiful thing, there's some kind of pain.",
        "Each night, when I go to sleep, I die."
        
    ]
    await ctx.send(content=f"{random.choice(wisdoms)}", tts=True)
    await ctx.send(file=discord.File("guy.gif"))

@bot.command()
async def submit(ctx, *, problem="None"):
    if bizBot.gamePhase == "starting" and ctx.message.author in bizBot.players:
        await ctx.channel.purge(limit=1)
        bizBot.problems.append(problem)
    print(bizBot.problems)
    
@bot.command()
async def play(ctx):
    if ctx.message.author not in bizBot.players and bizBot.gamePhase == "none":
        bizBot.players[ctx.message.author] = Player()
    print(bizBot.players)
    
@bot.command()
async def leave(ctx):
    if ctx.message.author in bizBot.players:
        bizBot.players.remove(ctx.message.author)
 
async def distributeProblems():
    random.shuffle(bizBot.problems)
    for i,p in enumerate(bizBot.players.items()):
        await p[0].send(bizBot.problems[i])
        await p[0].send("Use !text <text> to add a text description\nAttach an image in a message to add a image\nUse !delete to remove your last added presentable")
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
                await attachment.save(attachment.filename)
                bizBot.players[message.author].presentables.append(discord.File(attachment.filename))
                #await message.channel.send(file = bizBot.players[message.author].presentables[-1])
        
    await bot.process_commands(message)



@bot.command()
async def next(ctx):
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
                await ctx.channel.send("Next presenter is: " + bizBot.presentOrder[bizBot.currentPresentIndex].name)
                bizBot.currentPresent = bizBot.presentOrder[bizBot.currentPresentIndex]
                await ctx.channel.send("Their problem was: " + bizBot.players[bizBot.currentPresent].problem)
                
                if bizBot.currentPresentIndex >= len(bizBot.presentOrder):
                    await ctx.channel.send("PRESENTING OVER!")
        else:
            await ctx.channel.send("PRESENTING OVER!")
    await ctx.channel.purge(limit=1)
            
@bot.command()
async def done(ctx):
    if bizBot.gamePhase == "starting":
        await ctx.channel.send("Planning phase begins. Check private DM's")
        bizBot.gamePhase = "planning"
        await distributeProblems()
    elif bizBot.gamePhase == "planning":
        await ctx.channel.send("Presenting phase begins. Use !next to move to the first presenter and to move to the next slide.")
        bizBot.presentOrder = list(bizBot.players.keys())
        
        bizBot.gamePhase = "presenting"
    elif bizBot.gamePhase == "presenting":
        await ctx.channel.send("Voting phase begins.")
        bizBot.gamePhase = "voting"


bot.run("ODAwMDg2Mjg1MTY3MzYyMDQ5.YANAaw.wf7PoDS1dFxfDjKwDlpixYgY0b4")
