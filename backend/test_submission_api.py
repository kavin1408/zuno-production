import requests
import json

# Replace with a real token if needed, but the backend is currently using a mock user ID for Depends(get_current_user_id) 
# Wait, no, auth.py actually verifies the token.
# I'll use a dummy token and see if auth fails or if I can bypass it for testing.
# Actually, I should probably use the same logic as the frontend but in Python.

BACKEND_URL = "http://127.0.0.1:8000"

def test_submission():
    # This won't work without a real Supabase token unless I bypass auth.
    # For now, I'll just check if the endpoint is reachable.
    try:
        data = {
            "task_id": 11,
            "submission_text": "Independent test submission"
        }
        # Trying without auth to see the 401
        res = requests.post(f"{BACKEND_URL}/submit-task", json=data, timeout=5)
        print(f"Status: {res.status_code}")
        print(f"Response: {res.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_submission()
