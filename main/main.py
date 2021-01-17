import discord
from discord.ext import commands
import random

bot = commands.Bot(command_prefix = "!")

@bot.event
async def on_ready():
    print("Logged in")

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
async def clear(ctx, amount=1000):
    await ctx.channel.purge(limit=amount)

bot.run("ODAwMDg2Mjg1MTY3MzYyMDQ5.YANAaw.Nxln1b6nGLpkKBY5gWL-L86R_jY")
