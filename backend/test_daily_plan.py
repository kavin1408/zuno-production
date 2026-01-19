from main import get_daily_plan
from database import SessionLocal
import traceback

def test_daily_plan():
    db = SessionLocal()
    # Use the same user ID as test_onboarding.py
    user_id = "test_user_123"
    
    print(f"Testing get_daily_plan for user: {user_id}")
    try:
        # Mock dependency injection by passing db explicitly
        # user_id is passed as str directly because Depends is handled by FastAPI
        results = get_daily_plan(user_id=user_id, db=db)
        print("SUCCESS! Results found:", len(results))
        for task in results:
            print(f"- Task: {task.get('topic')}")
    except Exception as e:
        print("FAILED!")
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_daily_plan()
