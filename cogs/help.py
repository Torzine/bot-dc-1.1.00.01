import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help_command(self, ctx):
        embed = discord.Embed(
            title="🚀 Panduan Perintah Bot",
            description="Berikut adalah daftar perintah yang tersedia:",
            color=0x1ECF75,
        )
        embed.add_field(
            name="💡 `!help`", value="Menampilkan panduan perintah bot.", inline=False
        )
        embed.add_field(
            name="🎮 `!req_member <IGN>`",
            value="Request role **Member** dan ubah nickname.",
            inline=False,
        )
        embed.add_field(
            name="🎮 `!req_alliance <IGN>`",
            value="Request role **Alliance** dan ubah nickname.",
            inline=False,
        )
        embed.add_field(
            name="❌ `!remove_role @User <Role>`",
            value="Menghapus role dari pengguna (Admin Only).",
            inline=False,
        )
        embed.add_field(
            name="📊 `!recap`",
            value="Melihat ringkasan aktivitas pribadi.",
            inline=False,
        )
        embed.add_field(
            name="📊 `!recap @user`",
            value="Melihat ringkasan aktivitas anggota lain.",
            inline=False,
        )
        embed.add_field(
            name="📊 `!recap all member`",
            value="Melihat ringkasan aktivitas member.",
            inline=False,
        )
        embed.add_field(
            name="📊 `!recap all alliance`",
            value="Melihat ringkasan aktivitas alliance.",
            inline=False,
        )
        embed.add_field(name="🏓 `!ping`", value="Mengecek respons bot.", inline=False)
        embed.set_footer(text="✨ Ketik !help <command> untuk info detail perintah.")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
