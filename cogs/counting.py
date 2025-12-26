import discord
from discord.ext import commands
from discord import app_commands
from cogs.internal.count_channel_store import CountChannelStore
import asyncio
import os

intents = discord.Intents.all()
intents.message_content = True

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.data = load_channels()  # load ONCE
        self.func = CountChannelStore()  # create instance

    async def cog_load(self):
        # called when cog is loaded
        await self.func.connect()

    # ----- COUNT CHANNEL LINK -----

    # link
    @app_commands.command(name="link", description="Set the desired channel as a counting channel.")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def link(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_id = interaction.guild.id
        channel_id = channel.id
        channels = await self.func.get(guild_id)

        if channel_id in channels:
            return await interaction.response.send_message("This channel is already linked.")

        await self.func.add(guild_id,channel_id)
        await interaction.response.send_message(f"Linked {channel.mention}")

    # unlink
    @app_commands.command(name="unlink", description="Remove the desired channel from the counting channel list.")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def unlink(self, interaction: discord.Interaction, channel: discord.TextChannel):
        guild_id = interaction.guild.id
        channel_id = channel.id
        channels = await self.func.get(guild_id)

        if channel_id not in channels:
            return await interaction.response.send_message("This channel is not linked.")

        await self.func.remove(guild_id,channel_id)
        await interaction.response.send_message(f"Unlinked {channel.mention}")

    # linked
    @app_commands.command(name="linked", description="Show all linked counting channels")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def linked(self, interaction: discord.Interaction):
        guild_id = interaction.guild.id
        channels = await self.func.get(guild_id)

        if not channels:
            return await interaction.response.send_message("No linked channels.")

        mentions = [f"<#{cid}>" for cid in channels]
        await interaction.response.send_message("Linked channels:\n" + "\n".join(mentions))

    # ----- COUNT DETER -----
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return
        
        guild_id = message.guild.id

        allowed = await self.func.get(guild_id)

        if message.channel.id not in allowed:
            return  # ignore message

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
    await bot.add_cog(Counting(bot))