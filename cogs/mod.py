import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="nuke", description=r"Delete {count} messages")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.describe(count="message count")
    async def nuke(self, interaction: discord.Interaction, count: int):
        if count < 1:
           await interaction.response.send_message("Amount must be greater than 0", ephemeral=True)
           return
 
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=count)
        await interaction.followup.send(f"Deleted {len(deleted)} message(s)", ephemeral=True)


    @app_commands.command(name="mute", description="Mute someone")
    @app_commands.checks.has_permissions(moderate_members=True)
    @app_commands.describe(minutes="minutes", reason="reason")
    async def mute(self, interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = None):
        if member == interaction.user:
            return await interaction.response.send_message("Can't mute yourself you dum dum >_>", ephemeral=True)
 
        if member.top_role >= interaction.guild.me.top_role:
            return await interaction.response.send_message("Insufficient role hierarchy.", ephemeral=True)
 
        if minutes > 40320: # 28 days
            return await interaction.response.send_message("You can't mute people for more than 28 days.", ephemeral=True)
 
        try:
            duration = timedelta(minutes=minutes)
            await member.timeout(duration, reason=reason)
            await interaction.response.send_message(
                f"⏳ {member.mention} has been muted for {minutes} minute(s).\n**Reason:** {reason or '原因不明（？）'}", 
                ephemeral=True
            )
        except discord.Forbidden:
            await interaction.response.send_message("No permission.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)
 
async def setup(bot):
    await bot.add_cog(Moderation(bot))