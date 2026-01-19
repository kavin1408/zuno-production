from main import onboarding, OnboardingRequest
from database import SessionLocal
from datetime import date

def test_onboarding():
    db = SessionLocal()
    user_id = "test_user_123"
    
    req = OnboardingRequest(
        subjects=["Python"],
        exam_or_skill="General Mastery",
        daily_time_minutes=60,
        target_date=date(2025, 5, 1),
        target_goal="job-ready",
        learning_style="mixed"
    )
    
    try:
        # We need to mock get_current_user_id since it's a dependency
        # But here we just call the function directly
        result = onboarding(req, claims={"sub": user_id, "email": "test@example.com"}, db=db)
        print("SUCCESS:", result)
    except Exception as e:
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_onboarding()
