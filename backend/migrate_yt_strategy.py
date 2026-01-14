import sqlite3
import os

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), "zuno_v2.db")

def migrate():
    print(f"Connecting to database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        print("Adding video_confidence column...")
        cursor.execute("ALTER TABLE task_resources ADD COLUMN video_confidence TEXT")
    except sqlite3.OperationalError:
        print("video_confidence column already exists.")

    try:
        print("Adding validated column...")
        cursor.execute("ALTER TABLE task_resources ADD COLUMN validated BOOLEAN DEFAULT 0")
    except sqlite3.OperationalError:
        print("validated column already exists.")

    try:
        print("Adding fallback_used column...")
        cursor.execute("ALTER TABLE task_resources ADD COLUMN fallback_used BOOLEAN DEFAULT 0")
    except sqlite3.OperationalError:
        print("fallback_used column already exists.")

    conn.commit()
    conn.close()
    print("Migration completed.")

if __name__ == "__main__":
    migrate()
