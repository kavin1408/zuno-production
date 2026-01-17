from ai_service import generate_daily_task_content
import json

def test_daily_plan_generation():
    subject = "React"
    exam = "Web Development"
    level = "Beginner"
    recent_topics = None
    
    print(f"Generating daily plan for {subject}...")
    ai_response_str = generate_daily_task_content(subject, exam, level, recent_topics, 60)
    
    if ai_response_str:
        print("AI Response Received:")
        try:
            data = json.loads(ai_response_str)
            print(json.dumps(data, indent=2))
        except:
            print(ai_response_str)
    else:
        print("Failed to get AI response")

if __name__ == "__main__":
    test_daily_plan_generation()
