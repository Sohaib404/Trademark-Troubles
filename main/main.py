import discord
import speech_recognition as sr
import wave

class botClient(discord.Client):   
    
    vc = None
    
    async def on_ready(self):
        print('Logged on as' + self.user.name)
    
    async def on_message(self,message):
        if(message.content == "!join"):
            self.vc = await message.author.voice.channel.connect()
            self.communicate()
        elif(message.content == "!leave"):
            if(self.vc):
                await self.vc.disconnect()
                
    
    def communicate(self):
        pass

bot = botClient()
bot.run("TOKEN")    
        
    
