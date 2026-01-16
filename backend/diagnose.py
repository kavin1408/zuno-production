import os
from dotenv import load_dotenv
load_dotenv()

db_url = os.getenv("DATABASE_URL", "sqlite:///./zuno_v2.db")
print(f"DATABASE_URL: |{db_url}|")

try:
    import yt_dlp
    print("yt-dlp: Installed")
except ImportError:
    print("yt-dlp: NOT INSTALLED")

try:
    from sqlalchemy import create_engine
    engine = create_engine(db_url)
    connection = engine.connect()
    print("Database Connection: SUCCESS")
    connection.close()
except Exception as e:
    print(f"Database Connection: FAILED - {e}")
