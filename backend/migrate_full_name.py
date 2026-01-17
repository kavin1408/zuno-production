import sqlite3
import os

DB_FILE = "zuno_v2.db"

def migrate():
    if not os.path.exists(DB_FILE):
        print(f"Database file {DB_FILE} not found. Nothing to migrate.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        print("Checking if 'full_name' column exists in 'users' table...")
        cursor.execute("PRAGMA table_info(users)")
        columns = [info[1] for info in cursor.fetchall()]

        if "full_name" in columns:
            print("Column 'full_name' already exists.")
        else:
            print("Adding 'full_name' column to 'users' table...")
            cursor.execute("ALTER TABLE users ADD COLUMN full_name VARCHAR")
            conn.commit()
            print("Migration successful: Added 'full_name' column.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
