import discord
from discord.ext import commands

class MemberChecker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def send_status(self):
        """Mengirim pesan embed ke channel saat bot online."""
        channel_id = 1348716614521983037  # Ganti dengan ID channel tujuan
        try:
            channel = await self.bot.fetch_channel(channel_id)  # Fetch lebih akurat
        except discord.NotFound:
            print(f"❌ Channel dengan ID {channel_id} tidak ditemukan!")
            return
        except discord.Forbidden:
            print(f"❌ Bot tidak memiliki izin untuk melihat channel {channel_id}!")
            return

        embed = discord.Embed(
            title="✅ Bot Online!",
            description=f"{self.bot.user.mention} siap melayani 🚀",
            color=discord.Color.green()
        )
        try:
            await channel.send(embed=embed)
            print("✅ Embed status bot berhasil dikirim!")
        except discord.HTTPException as e:
            print(f"❌ Gagal mengirim embed status bot: {e}")

    @commands.Cog.listener()
    async def on_ready(self):
        """Event saat bot online."""
        print(f"🔥 [DEBUG] on_ready() dipanggil untuk {self.__class__.__name__}")
        await self.send_status()  # Panggil embed status bot

async def setup(bot):
    await bot.add_cog(MemberChecker(bot))