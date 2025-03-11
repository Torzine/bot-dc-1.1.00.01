import time
import discord
from discord.ext import commands
from database import get_db_connection

user_voice_start = {}  # Menyimpan waktu join voice channel
user_online_start = {}  # Menyimpan waktu online pengguna


class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return
        if message.content.startswith("!"):
            return  # Abaikan pesan dari bot

        update_message_count(message.author.id)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Mencatat waktu pengguna berada di voice channel"""
        user_id = member.id

        if before.channel is None and after.channel is not None:
            # Pengguna baru masuk voice channel -> Simpan waktu masuk
            user_voice_start[user_id] = time.time()
        elif before.channel is not None and after.channel is None:
            # Pengguna keluar dari voice channel -> Hitung waktu & update ke database
            if user_id in user_voice_start:
                duration = time.time() - user_voice_start[user_id]
                update_voice_time(user_id, duration)
                del user_voice_start[user_id]

    @commands.Cog.listener()
    async def on_presence_update(self, before, after):
        """Mencatat waktu pengguna online"""
        user_id = after.id
        if (
            before.status == discord.Status.offline
            and after.status != discord.Status.offline
        ):
            # Pengguna baru online -> Simpan waktu masuk
            user_online_start[user_id] = time.time()
        elif (
            before.status != discord.Status.offline
            and after.status == discord.Status.offline
        ):
            # Pengguna offline -> Hitung waktu online & update ke database
            if user_id in user_online_start:
                duration = time.time() - user_online_start[user_id]
                update_online_time(user_id, duration)
                del user_online_start[user_id]


def update_message_count(user_id):
    """Update jumlah pesan di database"""
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT message_count FROM activity WHERE user_id = ?", (user_id,))
    row = c.fetchone()

    if row is None:
        c.execute(
            "INSERT INTO activity (user_id, message_count) VALUES (?, ?)", (user_id, 1)
        )
    else:
        c.execute(
            "UPDATE activity SET message_count = message_count + 1 WHERE user_id = ?",
            (user_id,),
        )

    conn.commit()
    conn.close()


def update_voice_time(user_id, duration):
    """Update voice_time di database"""
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT voice_time FROM activity WHERE user_id = ?", (user_id,))
    row = c.fetchone()

    if row is None:
        c.execute(
            "INSERT INTO activity (user_id, voice_time) VALUES (?, ?)",
            (user_id, duration),
        )
    else:
        new_time = row[0] + duration
        c.execute(
            "UPDATE activity SET voice_time = ? WHERE user_id = ?", (new_time, user_id)
        )

    conn.commit()
    conn.close()


def update_online_time(user_id, duration):
    """Update online_time di database"""
    conn = get_db_connection()
    c = conn.cursor()

    c.execute("SELECT online_time FROM activity WHERE user_id = ?", (user_id,))
    row = c.fetchone()

    if row is None:
        c.execute(
            "INSERT INTO activity (user_id, online_time) VALUES (?, ?)",
            (user_id, duration),
        )
    else:
        new_time = row[0] + duration
        c.execute(
            "UPDATE activity SET online_time = ? WHERE user_id = ?", (new_time, user_id)
        )

    conn.commit()
    conn.close()


def compute_xp(activity):
    """
    Menghitung XP berdasarkan data aktivitas.
    - voice_time: waktu dalam detik (1 XP per menit)
    - message_count: jumlah pesan (0.5 XP per pesan)
    - online_time: waktu online dalam detik (0.2 XP per menit)
    """
    voice_time = activity.get("voice_time", 0)
    message_count = activity.get("message_count", 0)
    online_time = activity.get("online_time", 0)

    voice_minutes = voice_time / 60
    online_minutes = online_time / 60

    xp_voice = voice_minutes * 1
    xp_messages = message_count * 0.5
    xp_online = online_minutes * 0.2

    return int(xp_voice + xp_messages + xp_online)


def compute_level(xp):
    """Menghitung level dari total XP, 100 XP per level."""
    return xp // 100


async def setup(bot):
    await bot.add_cog(Activity(bot))
