"""
Database migration to add YouTube validation fields to task_resources table.
This script adds the new columns needed for YouTube video validation.
"""

from sqlalchemy import create_engine, text
import os

def migrate_youtube_validation():
    """Add YouTube validation fields to task_resources table."""
    
    # Use SQLite database
    database_url = os.getenv("DATABASE_URL", "sqlite:///./zuno_v2.db")
    if database_url.startswith("postgresql"):
        print("Detected PostgreSQL, using local SQLite for migration")
        database_url = "sqlite:///./zuno_v2.db"
    
    engine = create_engine(database_url)
    
    print(f"Starting YouTube validation migration on {database_url}...")
    
    with engine.connect() as conn:
        # Check if columns already exist
        try:
            # For SQLite
            result = conn.execute(text("PRAGMA table_info(task_resources)"))
            existing_columns = {row[1] for row in result}
            
            columns_to_add = []
            
            if 'video_id' not in existing_columns:
                columns_to_add.append(("video_id", "ADD COLUMN video_id VARCHAR"))
            
            if 'validated_at' not in existing_columns:
                columns_to_add.append(("validated_at", "ADD COLUMN validated_at DATETIME"))
            
            if 'is_embeddable' not in existing_columns:
                columns_to_add.append(("is_embeddable", "ADD COLUMN is_embeddable BOOLEAN DEFAULT 0"))
            
            # SQLite doesn't support multiple ADD COLUMN in one statement
            for column_name, column_def in columns_to_add:
                try:
                    sql = f"ALTER TABLE task_resources {column_def}"
                    print(f"Executing: {sql}")
                    conn.execute(text(sql))
                    conn.commit()
                    print(f"✓ Added column: {column_name}")
                except Exception as e:
                    print(f"✗ Error adding column {column_name}: {e}")
            
            if not columns_to_add:
                print("✓ All columns already exist, no migration needed")
            else:
                print(f"\n✓ Migration complete! Added {len(columns_to_add)} columns")
            
        except Exception as e:
            print(f"✗ Migration failed: {e}")
            raise

if __name__ == "__main__":
    migrate_youtube_validation()
