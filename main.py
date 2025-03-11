import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
from database import setup_database
import traceback

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Setup intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True
intents.presences = True

bot = commands.Bot(command_prefix="!", intents=intents)


# Hapus perintah help bawaan
bot.remove_command("help")
async def on_ready():
    print(f"✅ Bot {bot.user} siap digunakan!")
async def load_cogs():
    print("📂 Loading Cogs...")
    for filename in os.listdir("./cogs"):
        print(f"🔍 Checking file: {filename}")  # Debugging

        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"✅ Loaded {filename}")
            except Exception as e:
                print(f"❌ Gagal memuat {filename}: {e}")
                traceback.print_exc()
print("📂 Cogs loaded!")


async def main():
    setup_database()  # Pastikan database sudah di-setup
    async with bot:
        await load_cogs()
        try:
            await bot.start(TOKEN)
        except KeyboardInterrupt:
            print("Bot dihentikan secara manual.")
        finally:
            await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
