import sqlite3
import os

def migrate():
    db_path = "zuno_v2.db"
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check and add columns for 'goals'
    cursor.execute("PRAGMA table_info(goals)")
    cols = [c[1] for c in cursor.fetchall()]
    if "target_goal" not in cols:
        print("Adding 'target_goal' to goals")
        cursor.execute("ALTER TABLE goals ADD COLUMN target_goal TEXT")
    if "learning_style" not in cols:
        print("Adding 'learning_style' to goals")
        cursor.execute("ALTER TABLE goals ADD COLUMN learning_style TEXT")

    # Check and add columns for 'daily_tasks'
    cursor.execute("PRAGMA table_info(daily_tasks)")
    cols = [c[1] for c in cursor.fetchall()]
    if "roadmap_task_id" not in cols:
        print("Adding 'roadmap_task_id' to daily_tasks")
        cursor.execute("ALTER TABLE daily_tasks ADD COLUMN roadmap_task_id INTEGER")

    # Create roadmaps and roadmap_tasks if they don't exist
    # (Though Base.metadata.create_all should handle new tables, let's be sure)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roadmaps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        goal_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        is_active BOOLEAN DEFAULT 1,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(goal_id) REFERENCES goals(id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS roadmap_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        roadmap_id INTEGER NOT NULL,
        phase TEXT NOT NULL,
        module TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        estimated_time_minutes INTEGER NOT NULL,
        resource_links TEXT,
        output_deliverable TEXT,
        order_index INTEGER NOT NULL,
        status TEXT DEFAULT 'pending',
        completed_at DATETIME,
        scheduled_date DATE,
        FOREIGN KEY(roadmap_id) REFERENCES roadmaps(id)
    )
    """)

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
