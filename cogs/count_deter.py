import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os

intents = discord.Intents.all()
intents.message_content = True

class OnNumber(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        msgDelta = False # ?
        num = [0, 0] # curr, prev
        name = ["", ""] # curr, prev
        messages = [[message.content,message.author] async for message in message.channel.history(limit=1000)]

        m = 0
        for msg in messages:
            if msg[1].bot == False:
                try:
                    numDelta = int(msg[0])
                    nameDelta = msg[1]
                except ValueError:
                    if m == 0:
                        break
                    else:
                        continue
                else:
                    if msgDelta == True:
                        num[1] = numDelta
                        name[1] = nameDelta
                        if num[0] != num[1] + 1:
                            await message.channel.send(f"Hey! You counted wrong! The next number is: {num[1] + 1}", delete_after = 5, reference = message)
                            await message.delete()
                            msgDelta = False
                            messages = None
                        elif name[0] == name[1]:
                            await message.channel.send(f"Hey! You can't count twice! The next number is: {num[1] + 1}", delete_after = 5, reference = message)
                            await message.delete()
                        num = [0, 0]
                        name = ["", ""]
                        break
                    else:
                        num[0] = numDelta
                        name[0] = nameDelta
                        msgDelta = True
            else:
                continue
            m += 1
    
async def setup(bot):
    await bot.add_cog(OnNumber(bot))