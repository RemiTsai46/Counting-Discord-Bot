import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.message_content = True

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
        await message.channel.send("hello")
    await bot.process_commands(message)

@bot.command()
async def test(ctx, arg1, arg2):
    await ctx.send(arg1 + arg2)

bot.run('MTAwNzU5MDAxMDkyMjQ3NTYxMA.GjcIeu.-hJGc794YB_eACjhg45IzWH16vsBpIxjyCsNqE')
