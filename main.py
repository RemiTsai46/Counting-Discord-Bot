import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

load_dotenv()
token = os.getenv('TOKEN')
intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="k!",intents=intents)

async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

# @bot.command()
async def fixsync(ctx):
    msg = await ctx.send("修理完畢")
 
    bot.tree.clear_commands(guild=None)
    await bot.tree.sync()
 
    await load_extensions()
 
    bot.tree.copy_global_to(guild=ctx.guild)
    await bot.tree.sync(guild=ctx.guild)
 
    await msg.edit(content="ok")

@bot.event
async def on_ready():

    for guild in bot.guilds:
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
    print("Bot is up!")

    bot.tree.clear_commands(guild=None)
    await bot.tree.sync()
 
    await load_extensions()

# 放結尾
app = Flask('')
 
@app.route('/')
def home():
    return "上線了"
 
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
 
async def main():
   
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

    async with bot:
        await load_extensions()
        await bot.start(token)
 
if __name__ == '__main__':
    asyncio.run(main())