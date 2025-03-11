import discord
from discord.ext import commands
from database import get_db_connection


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Menghentikan bot dengan aman dan mengirim pesan ke channel tertentu"""
        """Menghentikan bot dengan aman"""
        embed = discord.Embed(
            title="🔴 Bot Shutdown",
            description=(
                f"Bot akan Dimatikan\n**Hubungi {ctx.author.mention} untuk Info Mengenai Bot**"
            ),
            color=discord.Color.red(),
        )
        embed.set_footer(
            text=f"Bot Telah Dimatikan Oleh {ctx.author}",
            icon_url=ctx.author.avatar.url,
        )  # Ganti dengan ID channel yang diinginkan
        channel = self.bot.get_channel(1347819803028754504)

        if channel:
            await channel.send(embed=embed)
        await self.bot.close()

    @commands.command(name="remove_role")
    @commands.has_permissions(administrator=True)
    async def remove_role(self, ctx, member: discord.Member, role_name: str):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role is None:
            embed = discord.Embed(
                title="🚫 Role Tidak Ditemukan",
                description=f"Role **{role_name}** tidak ditemukan.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        if role not in member.roles:
            embed = discord.Embed(
                title="🚫 Role Tidak Dimiliki",
                description=f"{member.display_name} tidak memiliki role **{role_name}**.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        try:
            await member.remove_roles(role)
        except Exception as e:
            embed = discord.Embed(
                title="⚠️ Gagal Menghapus Role",
                description="Silakan hubungi admin atau developer.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            print(e)
            return
        try:
            await member.edit(nick=None)
        except Exception as e:
            embed = discord.Embed(
                title="⚠️ Gagal Mereset Nickname",
                description="Silakan hubungi admin atau developer.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)

        conn = get_db_connection()
        c = conn.cursor()
        try:
            c.execute(
                "UPDATE activity SET ign = NULL, role = NULL WHERE user_id = ?",
                (member.id,),
            )
            conn.commit()

            embed = discord.Embed(
                title=f"✅ Role Dihapus",
                description=f"Role **{role_name}** berhasil dihapus dari {member.display_name}.",
                color=discord.Color.green(),  # Warna hijau untuk sukses
            )

            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="⚠️ Kesalahan Database",
                description="Terjadi kesalahan saat memperbarui database.",
                color=discord.Color.red(),  # Warna merah untuk error
            )
            await ctx.send(embed=embed)
            print(e)
        finally:
            conn.close()

    @commands.command(name="add_role")
    @commands.has_permissions(administrator=True)  # Hanya admin yang bisa pakai
    async def add_role(self, ctx, member: discord.Member, role_type: str, ign: str):
        role_type = role_type.lower()
        if role_type not in ["member", "alliance"]:
            embed = discord.Embed(
                title="🚫 Role Tidak Valid",
                description="Role yang tersedia hanya `member` atau `alliance`.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        role_name = "Member" if role_type == "member" else "Alliance"
        role = discord.utils.get(ctx.guild.roles, name=role_name)

        if role is None:
            embed = discord.Embed(
                title="🚫 Role Tidak Ditemukan",
                description=f"Role **{role_name}** tidak ditemukan. Pastikan role ada di server!",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        # Berikan role ke member
        try:
            await member.add_roles(role)
        except discord.Forbidden:
            embed = discord.Embed(
                title="⚠️ Izin Tidak Cukup",
                description="Bot tidak memiliki izin untuk memberikan role.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        # Ubah nickname
        try:
            await member.edit(nick=ign)
        except discord.Forbidden:
            embed = discord.Embed(
                title="⚠️ Izin Tidak Cukup",
                description="Bot tidak memiliki izin untuk mengubah nickname.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            return

        # Simpan ke database
        conn = get_db_connection()
        c = conn.cursor()
        try:
            # Gunakan INSERT OR REPLACE agar data bisa diperbarui
            c.execute(
                """
                INSERT OR REPLACE INTO activity (user_id, ign, role) 
                VALUES (?, ?, ?)
            """,
                (member.id, ign, role_name),
            )

            conn.commit()

            embed = discord.Embed(
                title="✅ Role Ditambahkan",
                description=f"{member.mention} telah diberikan role **{role_name}** dengan IGN **{ign}**.",
                color=discord.Color.green(),
            )
            embed.set_footer(
                text=f"Ditambahkan oleh {ctx.author}", icon_url=ctx.author.avatar.url
            )
            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="⚠️ Kesalahan Database",
                description="Terjadi kesalahan saat menyimpan ke database.",
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
            print(e)

        finally:
            conn.close()


async def setup(bot):
    await bot.add_cog(Admin(bot))
