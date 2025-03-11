import discord
from discord.ext import commands
from database import get_user_activity
from cogs.activity import (
    compute_xp,
    compute_level,
)  # Impor dari modul activity di folder utama


class Recap(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def recap(self, ctx, *, target: str = None):
        if target is None:
            activity = get_user_activity(ctx.author.id)
            if activity:
                xp = compute_xp(activity)
                lvl = compute_level(xp)
                await ctx.send(
                    f"📊 **Recap {ctx.author.display_name}:**\n"
                    f"🗣️ Voice: {activity['voice_time'] // 60}m | "
                    f"📩 {activity['message_count']} msg | "
                    f"🕒 {activity['online_time'] // 60}m\n"
                    f"⭐ XP: {xp} | Level: {lvl}"
                )
            else:
                await ctx.send("❌ Tidak ada data aktivitas untukmu.")
            return

        if target.lower() in ["all member", "all alliance"]:
            role_name = "Member" if target.lower() == "all member" else "Alliance"
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if not role:
                await ctx.send(f"⛔ Role **{role_name}** tidak ditemukan.")
                return

            members = [m for m in ctx.guild.members if role in m.roles]
            if not members:
                await ctx.send(f"⛔ Tidak ada anggota dengan role **{role_name}**.")
                return

            message = f"📢 **Recap Semua {role_name}:**\n"
            for m in members:
                activity = get_user_activity(m.id)
                if activity:
                    xp = compute_xp(activity)
                    lvl = compute_level(xp)
                    message += (
                        f"👤 {m.display_name} - "
                        f"🗣️ {activity['voice_time'] // 60}m | "
                        f"📩 {activity['message_count']} msg | "
                        f"🕒 {activity['online_time'] // 60}m | "
                        f"⭐ XP: {xp} | Level: {lvl}\n"
                    )
            await ctx.send(message)
        else:
            member = discord.utils.get(ctx.guild.members, name=target)
            if member is None:
                await ctx.send("🚫 Pengguna tidak ditemukan.")
                return
            activity = get_user_activity(member.id)
            if activity:
                xp = compute_xp(activity)
                lvl = compute_level(xp)
                await ctx.send(
                    f"📊 **Recap {member.display_name}:**\n"
                    f"🗣️ Voice: {activity['voice_time'] // 60}m | "
                    f"📩 {activity['message_count']} msg | "
                    f"🕒 {activity['online_time'] // 60}m\n"
                    f"⭐ XP: {xp} | Level: {lvl}"
                )
            else:
                await ctx.send("🚫 Tidak ada data aktivitas untuk pengguna tersebut.")


async def setup(bot):
    await bot.add_cog(Recap(bot))
