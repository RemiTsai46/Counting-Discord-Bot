import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')
intents = discord.Intents.all()
intents.message_content = True

#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="k!",intents=intents)

@bot.event
async def on_ready():
    print("Bot is up!")


@bot.event
async def on_message(message):

    if message.author == bot.user:
        return
  
    '''if message.content == "hello":
        await message.reply("hello") '''

    msgDelta = False # ?
    num = [0, 0] # curr, prev
    name = ["", ""] # curr, prev
    messages = [[message.content,message.author] async for message in message.channel.history(limit=1000)]

    for msg in messages:
        if msg[1].bot == False:
            try:
                numDelta = int(msg[0])
                nameDelta = msg[1]
            except ValueError:
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
    
    await bot.process_commands(message)

@bot.command()
async def test(ctx, arg1, arg2):
    await ctx.send(arg1 + arg2)

bot.run(token)