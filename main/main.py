import discord

class botClient(discord.Client):   
    async def on_ready(self):
        print('Logged on as' + self.user)
        
    
        
    
