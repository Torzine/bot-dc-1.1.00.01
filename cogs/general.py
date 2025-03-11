import discord
from discord.ext import commands
from database import get_user_activity
from cogs.activity import compute_xp, compute_level


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="profile")
    async def profile(self, ctx, member: discord.Member = None):
        member = (
            member or ctx.author
        )  # Jika tidak ada yang di-tag, gunakan pengirim command
        user_id = member.id
        activity = get_user_activity(user_id)

        if activity is None:
            if member == ctx.author:
                await ctx.send(
                    "⚠️ Data tidak ditemukan. Silakan gunakan `!req_member` untuk mendaftar."
                )
            else:
                await ctx.send(f"⚠️ Data tidak ditemukan untuk {member.mention}.")

        xp = compute_xp(activity)
        level = compute_level(xp)

        embed = discord.Embed(title=f"Profil {member.name}", color=discord.Color.blue())
        embed.set_thumbnail(
            url=member.avatar.url if member.avatar else member.default_avatar.url
        )
        embed.add_field(
            name="IGN", value=activity.get("ign", "Tidak tersedia"), inline=False
        )
        embed.add_field(
            name="Role", value=activity.get("role", "Tidak tersedia"), inline=False
        )
        embed.add_field(name="XP", value=f"{xp} XP", inline=True)
        embed.add_field(name="Level", value=f"Level {level}", inline=True)

        await ctx.send(embed=embed)

        return

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f"🏓 Pong! Latency: {round(self.bot.latency * 1000)}ms")


async def setup(bot):
    await bot.add_cog(General(bot))
