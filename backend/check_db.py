import sqlite3

def check_db():
    try:
        conn = sqlite3.connect('zuno.db')
        cursor = conn.cursor()
        
        print("--- Users ---")
        cursor.execute("SELECT * FROM users")
        print(cursor.fetchall())
        
        print("\n--- Goals ---")
        cursor.execute("SELECT * FROM goals")
        print(cursor.fetchall())
        
        print("\n--- Daily Tasks ---")
        cursor.execute("SELECT * FROM daily_tasks")
        print(cursor.fetchall())
        
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_db()
