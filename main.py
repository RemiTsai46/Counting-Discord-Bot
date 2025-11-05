import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
intents.message_content = True
token = 'MTAwNzU5MDAxMDkyMjQ3NTYxMA.Gcwtov.HW4OTL9ZDDM4bc_4hLBs7spYyllvzgJEIln_Qc'

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

    msgDelta = False
    numCurr = 0
    numPrev = 0
    messages = [[message.content,message.author.bot] async for message in message.channel.history(limit=1000)]

    for msg in messages:
        if msg[1] == False:
            try:
                numDelta = int(msg[0])
            except ValueError:
                continue
            else:
                if msgDelta == True:
                    numPrev = numDelta
                    if numCurr != numPrev + 1:
                        await message.channel.send(f"Hey! You counted wrong! The next number is: {numPrev + 1}", delete_after = 5, reference = message)
                        await message.delete()
                        numCurr = 0
                        numPrev = 0
                        msgDelta = False
                        messages = None
                        break
                    else:
                        numCurr = 0
                        numPrev = 0
                        await message.channel.send("success", delete_after = 5)
                        break
                else:
                    numCurr = numDelta
                    msgDelta = True
        else:
            continue 
    
    await bot.process_commands(message)

@bot.command()
async def test(ctx, arg1, arg2):
    await ctx.send(arg1 + arg2)

bot.run(token)