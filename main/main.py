import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
import random

class Player():
    name = ""
    presentables = []
class bizBot():
        
    problems = []
    
    #gamephases none: no game started, starting: submitting ideas, planning: making ideas, presenting, voting
    gamePhase = "none"
    
    submittingTime = 0
    planningTime = 0
    presentableTime = 0
    maxPresentables = 0
    
    
    players = {}
    
    admin = None
    
    def __init__(self):
        pass
    


bot = commands.Bot(command_prefix="!")

@bot.command()
async def start(ctx,*,values="a"):
    if bizBot.gamePhase == "none":
        timers = values.split(" ")
        timers = [int(x) for x in timers]
        if len(timers) != 4:
            await ctx.send("wrong amount of values.\n usage is !start !start <submitting time> <planning time> <presentable time> <max presentables>")
        else:
            bizBot.submittingTime = timers[0]
            bizBot.planningTime = timers[1]
            bizBot.presentableTime = timers[2]
            bizBot.maxPresentables = timers[3]
            bizBot.gamePhase = "starting"
            bizBot.admin = ctx.message.author
            print(timers)
            
        
@bot.event
async def on_ready():
    print("Bot Online")

@bot.command()
async def wisdom(ctx):
    wisdoms = [
        "Only the dead have seen the end of war.",
        "It is forbidden to kill; therefore all murderers are punished unless they kill in large numbers and to the sound of trumpets.",
        "Violence is the last refuge of the incompetent.",
        "When you have to kill a man, it costs nothing to be polite.",
        "Death, in its silent sure march is fast gathering those whom I have longest loved, so that when he shall knock at my door, I will more willingly follow.",
        "The last enemy that shall be destroyed is death.",
        "If you expect the worst, you'll never be disappointed.",
        "To die will be an awfully big adventure.",
        "One may as well be optimistic. The road to catastrophe will be rougher if it's paved with dread.",
        "Behind every beautiful thing, there's some kind of pain.",
        "At the point of death, the pain is over. Yeah, I guess it is a friend.",
        "Each night, when I go to sleep, I die."
    ]
    await ctx.send(content=f"{random.choice(wisdoms)}", tts=True)

@bot.command()
async def submit(ctx, *, problem="None"):
    if bizBot.gamePhase == "starting":
        await ctx.channel.purge(limit=1)
        bizBot.problems.append(problem)
    print(bizBot.problems)
    
@bot.command()
async def play(ctx):
    if ctx.message.author not in bizBot.players and bizBot.gamePhase == "none":
        bizBot.players.append((ctx.message.author,Player()))
    print(bizBot.players)
    
@bot.command()
async def leave(ctx):
    if ctx.message.author in bizBot.players:
        bizBot.players.remove(ctx.message.author)
        
@bot.command()
async def done(ctx):
    if bizBot.gamePhase == "starting":
        bizBot.gamePhase = "planning"
    elif bizBot.gamePhase == "planning":
        bizBot.gamePhase = "presenting"
    elif bizBot.gamePhase == "presenting":
        bizBot.gamePhase = "voting"


bot.run("ODAwMDg2Mjg1MTY3MzYyMDQ5.YANAaw.Nxln1b6nGLpkKBY5gWL-L86R_jY")
