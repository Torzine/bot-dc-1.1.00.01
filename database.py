import os
import mysql.connector

# Debugging: Cek apakah ENV Variabel sudah terbaca dengan benar
print("🔍 MYSQL_HOST:", os.getenv("MYSQL_HOST"))
print("🔍 MYSQL_USER:", os.getenv("MYSQL_USER"))
print("🔍 MYSQL_DATABASE:", os.getenv("MYSQL_DATABASE"))

# Fungsi untuk koneksi ke database MySQL
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )

# Fungsi untuk setup database (jika tabel belum ada)
def setup_database():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS activity (
            user_id BIGINT PRIMARY KEY,
            ign VARCHAR(255),
            role VARCHAR(255),
            voice_time INT DEFAULT 0,
            message_count INT DEFAULT 0,
            online_time INT DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()
    print("✅ Database siap digunakan!")

# Fungsi untuk mengambil aktivitas user berdasarkan user_id
def get_user_activity(user_id):
    conn = get_db_connection()
    c = conn.cursor(dictionary=True)  # Mengembalikan hasil sebagai dictionary
    c.execute(
        "SELECT user_id, ign, role, voice_time, message_count, online_time FROM activity WHERE user_id = %s",
        (user_id,)
    )
    row = c.fetchone()
    conn.close()
    return row  # Mengembalikan dictionary jika data ditemukan, atau None jika tidak ada
