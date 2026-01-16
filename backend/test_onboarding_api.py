import requests
import json

# Since we don't have a real token, we might need to bypass auth or use a dummy one if the backend allows it.
# Actually, the backend auth.py uses Supabase JWT.
# Let's see if we can find a token in the environment or if there's a bypass.

url = "http://localhost:8000/onboarding"
payload = {
    "subjects": ["Python", "SQL"],
    "full_name": "Test User",
    "exam_or_skill": "General Mastery",
    "daily_time_minutes": 60,
    "target_date": "2026-04-01",
    "target_goal": "job-ready",
    "learning_style": "mixed"
}

# Try without token first to see if it gives 401
try:
    print("Testing /onboarding without token...")
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
