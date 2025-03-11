import discord
from discord.ext import commands
from database import get_db_connection

# Tidak perlu impor compute_xp di sini kecuali dipakai


class Request(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["req-member"])
    async def req_member(self, ctx, ign: str = None):
        if ign is None:
            await ctx.send(
                "❌ | Silakan sertakan IGN kamu. Contoh: !req_member NamaKarakter"
            )
            return

        user_id = ctx.author.id
        role_name = "Member"
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role is None:
            await ctx.send(
                f"⚠️ | Role **{role_name}** tidak ditemukan. Hubungi admin untuk memperbaikinya!"
            )
            return

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT ign, role FROM activity WHERE user_id = ?", (user_id,))
        existing = c.fetchone()

        if existing and existing[0]:
            await ctx.send(
                "❌ | Oops! Sepertinya kamu sudah terdaftar. Jika ingin mengubah data, hubungi admin!"
            )
            conn.close()
            return

        try:
            await ctx.author.add_roles(role)
        except Exception as e:
            await ctx.send(
                "⚠️ | Gagal menambahkan role. Pastikan bot memiliki permission Manage Roles."
            )
            print(e)
            conn.close()
            return

        if existing is None:
            c.execute(
                "INSERT INTO activity (user_id, ign, role) VALUES (?, ?, ?)",
                (user_id, ign, role_name),
            )
        else:
            c.execute(
                "UPDATE activity SET ign = ?, role = ? WHERE user_id = ?",
                (ign, role_name, user_id),
            )
        conn.commit()
        conn.close()

        try:
            await ctx.author.edit(nick=ign)
        except Exception as e:
            await ctx.send(
                "⚠️ | Gagal mengubah nickname. Pastikan bot memiliki izin Manage Nicknames."
            )
            print(e)

        embed = discord.Embed(title="Member Request Accepted", color=0x00FF00)
        embed.add_field(name="Discord", value=ctx.author.mention, inline=True)
        embed.add_field(name="IGN", value=ign, inline=True)
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_footer(text="Request berhasil dikirim!")
        await ctx.send(embed=embed)

    @commands.command(aliases=["req-alliance", "req-Alliance"])
    async def req_alliance(self, ctx, ign: str = None):
        if ign is None:
            await ctx.send(
                "❌ | Silakan sertakan IGN kamu. Contoh: !req_alliance NamaKarakter"
            )
            return

        user_id = ctx.author.id
        role_name = "Alliance"
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role is None:
            await ctx.send(
                f"⚠️ | Role **{role_name}** tidak ditemukan. Hubungi admin untuk memperbaikinya!"
            )
            return

        conn = get_db_connection()
        c = conn.cursor()
        c.execute("SELECT ign, role FROM activity WHERE user_id = ?", (user_id,))
        existing = c.fetchone()

        if existing and existing[0]:
            await ctx.send(
                "❌ | Oops! Sepertinya kamu sudah terdaftar. Jika ingin mengubah data, hubungi admin!"
            )
            conn.close()
            return

        try:
            await ctx.author.add_roles(role)
        except Exception as e:
            await ctx.send(
                "⚠️ | Gagal menambahkan role. Pastikan bot memiliki permission Manage Roles."
            )
            print(e)
            conn.close()
            return

        if existing is None:
            c.execute(
                "INSERT INTO activity (user_id, ign, role) VALUES (?, ?, ?)",
                (user_id, ign, role_name),
            )
        else:
            c.execute(
                "UPDATE activity SET ign = ?, role = ? WHERE user_id = ?",
                (ign, role_name, user_id),
            )
        conn.commit()
        conn.close()

        try:
            await ctx.author.edit(nick=ign)
        except Exception as e:
            await ctx.send(
                "⚠️ | Gagal mengubah nickname. Pastikan bot memiliki izin Manage Nicknames."
            )
            print(e)

        embed = discord.Embed(title="Alliance Request Accepted", color=0x00FF00)
        embed.add_field(name="Discord", value=ctx.author.mention, inline=True)
        embed.add_field(name="IGN", value=ign, inline=True)
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_footer(text="Request berhasil dikirim!")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Request(bot))
