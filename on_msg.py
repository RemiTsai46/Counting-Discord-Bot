import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')
intents = discord.Intents.all()
intents.message_content = True
intents.guild_messages = True

#client = discord.Client(intents)
bot = commands.Bot(command_prefix="k!",intents=intents)


@bot.event
async def on_ready():
    print("Bot is up!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content == 'hello':
        mau = message.author
        print(mau.bot)
        await message.channel.send(f"hello, {message.author}")
    await bot.process_commands(message)

@bot.command()
async def test(ctx, arg1, arg2):
    await ctx.send(arg1 + arg2)

bot.run(token)
