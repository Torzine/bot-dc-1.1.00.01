import sqlite3

DATABASE_PATH = "activity.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn


def setup_database():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS activity (
            user_id INTEGER PRIMARY KEY,
            ign TEXT,
            role TEXT,
            voice_time INTEGER DEFAULT 0,
            message_count INTEGER DEFAULT 0,
            online_time INTEGER DEFAULT 0
        )
    """
    )
    conn.commit()
    conn.close()


def get_user_activity(user_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "SELECT user_id, ign, role, voice_time, message_count, online_time FROM activity WHERE user_id = ?",
        (user_id,),
    )
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "user_id": row[0],
            "ign": row[1],
            "role": row[2],
            "voice_time": row[3],
            "message_count": row[4],
            "online_time": row[5],
        }
    return None
