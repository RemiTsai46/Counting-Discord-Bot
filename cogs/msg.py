import discord
from discord.ext import commands
from discord import app_commands

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
 
  	# cog 裡面的 decorator 改成這個
    @commands.Cog.listener()
    async def on_message(self, message): #要把 self 給放進去
       
        # 後面這邊都是一樣的
        
        if message.author.bot:
            return
       
        if "bot" in message.content.lower() and "hi" in message.content.lower():
            await message.channel.send(f"alle {message.author.display_name}!")
    
async def setup(bot):
    await bot.add_cog(OnMessage(bot))

'''
@bot.command()
async def test(ctx, arg1, arg2):
    await ctx.send(arg1 + arg2)
'''