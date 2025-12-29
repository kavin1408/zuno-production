import os
import requests
import json
from datetime import date
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """You are Zuno, an elite AI student mentor and curriculum designer.
Your goal is to be strict but supportive, enforcing daily study habits.
You are concise, outcome-oriented, and encouraging.
You create personalized study plans that follow a progressive learning path from fundamentals to mastery.
You understand that strong foundations are critical - always start with basics before advancing.
You provide actionable feedback and ensure each lesson builds on previous knowledge."""

def call_openrouter(messages, model="meta-llama/llama-3.1-70b-instruct"):
    if not OPENROUTER_API_KEY:
        print("Warning: OPENROUTER_API_KEY is not set.")
        return None

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        # Optional headers for OpenRouter
        "HTTP-Referer": "https://zuno.app", 
        "X-Title": "Zuno Mentor"
    }
    
    data = {
        "model": model,
        "messages": messages
    }
    
    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        ai_response = result['choices'][0]['message']['content']
        print(f"AI Response: {ai_response}")  # Debug logging
        return ai_response
    except requests.exceptions.RequestException as e:
        print(f"AI Service Request Error: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response Status: {e.response.status_code}")
            print(f"Response Body: {e.response.text}")
        return None
    except Exception as e:
        print(f"AI Service Error: {e}")
        return None

def extract_json(text):
    """
    Extracts JSON from a string that might contain markdown code blocks or extra text.
    """
    if not text:
        return None
    
    # Try to find JSON block
    import re
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass
            
    # Fallback: try raw string if it looks like JSON
    try:
        return json.loads(text)
    except:
        return None

def detect_level_and_confirm(subject, exam, time_min, target_date):
    """
    Analyzes the user's goal and estimates their current level (Beginner/Intermediate/Advanced)
    based on the ambitiousness of the goal vs time.
    Returns a JSON string or structure: { "level": "...", "message": "..." }
    """
    prompt = f"""
    The student wants to study '{subject}' for '{exam}'.
    They can commit {time_min} minutes daily until {target_date}.
    
    1. Estimate their starting level (Beginner, Intermediate, Advanced) based on generic assumptions or just assign 'Beginner' if unsure.
    2. Write a short, punchy confirmation message welcoming them to the grind.
    
    Respond in pure JSON format:
    {{
      "level": "Beginner|Intermediate|Advanced",
      "message": "Start encouragement string"
    }}
    """
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    
    response = call_openrouter(messages)
    data = extract_json(response)
    return json.dumps(data) if data else None

import research_service

def generate_daily_task_content(subject, exam, level, recent_topics=None, time_minutes=45):
    """
    Generates a daily task with a researched high-quality YouTube resource.
    """
    recent_context = f"Recently covered: {recent_topics}" if recent_topics else "This is their first day."
    is_starting = not recent_topics or recent_topics.strip() == "" or "first day" in recent_context.lower()
    
    # Time adjustment logic
    time_guidance = "Standard lesson"
    if time_minutes <= 30:
        time_guidance = "CONCISE, FOCUSED sub-topic (Micro-learning)"
    elif time_minutes >= 90:
        time_guidance = "DEEP DIVE, COMPREHENSIVE topic (Intensive)"
    
    # Step 1: Generate a specific study topic and search query
    query_prompt = f"""
    The student is studying '{subject}' for '{exam}' at a '{level}' level.
    Time Commitment: {time_minutes} minutes ({time_guidance})
    {recent_context}
    
    CRITICAL CURRICULUM GUIDELINES:
    - For BEGINNERS or FIRST DAY: You MUST start with absolute fundamentals and core concepts
    - Build progressively: Each topic should build on previously covered material
    - Ensure prerequisites are met before introducing advanced concepts
    - Follow a logical learning path from basics to mastery
    
    {"⚠️ IMPORTANT: This is their FIRST DAY - START WITH THE MOST BASIC FUNDAMENTALS!" if is_starting else ""}
    
    Task:
    1. Identify the next logical topic following a structured curriculum
    2. Ensure the topic fits into a {time_minutes}-minute study session ({time_guidance})
    3. Suggest a specific YouTube search query for the best tutorial
    
    Examples of proper progression for '{subject}':
    - Beginner/First topics: Core concepts, basic terminology, "What is {subject}", foundational principles, basic setup
    - Intermediate topics: Practical applications, common patterns, problem-solving techniques
    - Advanced topics: Optimization, edge cases, advanced techniques, best practices
    
    Respond in pure JSON format:
    {{
      "topic": "Specific Topic Name (appropriate for their level and progression)",
      "search_query": "YouTube search query for beginners/intermediate/advanced tutorial",
      "rationale": "Brief explanation of why this topic is the right next step and fits the time limit"
    }}
    """
    
    query_response_str = call_openrouter([
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": query_prompt}
    ])
    
    if not query_response_str:
        return None
        
    query_data = extract_json(query_response_str)
    if not query_data:
        print(f"Failed to extract JSON from query response: {query_response_str}")
        return None
        
    try:
        topic = query_data.get("topic", "General Topic")
        search_query = query_data.get("search_query", f"{subject} {exam} tutorial")
        
        # Step 2: Research Resources
        resources = research_service.search_youtube_resources(search_query, limit=3)
        
        if not resources:
            resource_link = f"https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
            resource_context = "No specific video found, providing search results."
        else:
            # We pick the top one (already sorted by popularity)
            best_res = resources[0]
            resource_link = best_res['url']
            resource_context = f"Top video: '{best_res['title']}' with {best_res['views']} views from {best_res['uploader']}."

        # Step 3: Generate final task description
        learning_stage = "Starting from fundamentals" if is_starting or level == "Beginner" else "Building on previous knowledge"
        
        task_prompt = f"""
        Topic: {topic}
        Resource: {resource_link} ({resource_context})
        Student Level: {level}
        Learning Stage: {learning_stage}
        Time Allocation: {time_minutes} minutes ({time_guidance})
        
        Create a clear, actionable study task tailored exactly for a {time_minutes}-minute session.
        
        IMPORTANT GUIDELINES:
        - For beginners/first day: Focus on understanding CORE CONCEPTS before moving to applications
        - Ensure the task is appropriate for their current level
        - Build confidence with achievable, well-structured goals
        - Emphasize comprehension over completion
        
        Respond in pure JSON format:
        {{
          "topic": "{topic}",
          "description": "Clear, step-by-step instructions emphasizing fundamentals and understanding. Include what they should learn and how to approach it.",
          "resource_link": "{resource_link}"
        }}
        """
        
        response = call_openrouter([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task_prompt}
        ])
        
        data = extract_json(response)
        return json.dumps(data) if data else None
        
    except Exception as e:
        print(f"Error in daily task generation flow: {e}")
        return None

def evaluate_submission_content(task_description, user_text, level="Beginner"):
    """
    Evaluates a user's text submission.
    Returns JSON: { "score": 0-100, "feedback": "..." }
    """
    prompt = f"""
    Task: {task_description}
    User Level: {level}
    User Submission: "{user_text}"
    
    Evaluate the submission acting as a supportive but strict mentor.
    
    CRITERIA:
    1. Relevance: Did they improved address the task?
    2. Effort: Does the submission show genuine effort?
    3. Level-Appropriateness:
       - Beginner: Be encouraging, praise understanding of basics.
       - Intermediate: Look for practical application and correct usage.
       - Advanced: Be strict, look for optimization and best practices.

    If the submission is "Image submitted" (user uploaded a screenshot):
    - Assume they did the work but you cannot see it.
    - Give a high score (85-95) for showing up.
    - Ask a follow-up question in the feedback to verify their understanding.

    Respond in pure JSON format:
    {{
      "score": <integer_0_to_100>,
      "feedback": "Constructive feedback. For high scores, praise specific details. For low scores, explain what is missing."
    }}
    """
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    
    response = call_openrouter(messages)
    data = extract_json(response)
    return json.dumps(data) if data else None

def generate_week_summary(completed_count, avg_score, total_days, level="Beginner", recent_topics=""):
    """
    Generates a mentor summary for the week.
    """
    prompt = f"""
    Weekly Check-in:
    - Level: {level}
    - Tasks Completed: {completed_count}
    - Average Score: {avg_score}
    - Topics Covered: {recent_topics or "None"}
    
    Write a short, powerful paragraph summarizing their performance. 
    1. Acknowledge their level (e.g. "Solid start for a beginner..." or "Good advanced work...").
    2. Mention specific topics they covered to show you are tracking their curriculum.
    3. Be strict if they missed tasks, but praise consistency/scores.
    4. Give a brief "Look ahead" or advice for the next week of study based on their level.
    """
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    
    response = call_openrouter(messages)
    # Week summary is a paragraph, not JSON, so we return raw response
    return response
def answer_question(user_question, goal_context=None, task_context=None):
    """
    Answers a general study doubt or question, potentially triggering an action.
    """
    context_str = f"The student is currently working on: {goal_context}." if goal_context else ""
    if task_context:
        context_str += f" Specific task details: {task_context}"
    
    prompt = f"""
    {context_str}
    
    Student Question: "{user_question}"
    
    Instructions:
    1. Provide a helpful, concise, and encouraging answer.
    2. If the user asks to change the resource, find a better one, or add more resources (like specifically asking for a YouTube video), identify if an ACTION is needed.
    3. Supported Actions:
       - {{"type": "update_resource", "new_link": "https://...", "reason": "..."}}
    
    YOU MUST RESPOND IN PURE JSON FORMAT:
    {{
      "answer": "Your mentor response to the student",
      "action": null or {{ "type": "update_resource", "new_link": "...", "reason": "..." }}
    }}
    """
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    
    response = call_openrouter(messages)
    return extract_json(response)
