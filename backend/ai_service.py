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
        response = requests.post(OPENROUTER_URL, headers=headers, json=data, timeout=30)
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
    
def generate_curated_resources(subject, topic, level="Beginner", goal="General Mastery", limit=3):
    """
    Uses AI reasoning combined with real YouTube search to generate high-quality resources.
    """
    import youtube_service
    
    # Step 1: Search for real YouTube videos
    search_query = f"{subject} {topic} tutorial {level}"
    youtube_results = youtube_service.search_and_validate_videos(search_query, limit=2)
    
    resources = []
    
    # Add validated YouTube videos
    for video in youtube_results:
        resources.append({
            "title": video['title'],
            "url": video['url'],
            "platform": "YouTube",
            "resource_type": "video",
            "rationale": f"Popular tutorial with {video['views']:,} views. Verified embeddable.",
            "video_confidence": "high",
            "video_id": video['video_id'],
            "is_embeddable": video['is_embeddable'],
            "validated_at": video['validated_at']
        })
    
    # If no embeddable videos found, add fallback search link
    if len(resources) == 0:
        fallback_url = youtube_service.youtube_service.get_fallback_search_url(search_query)
        resources.append({
            "title": f"YouTube Tutorials: {topic}",
            "url": fallback_url,
            "platform": "YouTube",
            "resource_type": "video",
            "rationale": "Curated search results updated live from YouTube.",
            "video_confidence": "fallback",
            "video_id": None,
            "is_embeddable": False,
            "validated_at": None
        })
    
    # Step 2: Ask AI for additional non-YouTube resources
    if len(resources) < limit:
        remaining = limit - len(resources)
        prompt = f"""
        You are an expert educational researcher. Find {remaining} high-quality, free NON-YOUTUBE resources for a student.
        
        Student Profile:
        - Subject: {subject}
        - Topic: {topic}
        - Level: {level}
        - Overall Goal: {goal}
        
        Task: Provide {remaining} resources from trusted platforms (MDN, GitHub, Dev.to, Official Docs, freeCodeCamp, etc.).
        
        Requirements:
        1. NO YOUTUBE LINKS - we already have those
        2. Only suggest top-tier educators or official sources
        3. Realistic URLs that follow standard formats (e.g., developer.mozilla.org, github.com)
        4. Format: Respond ONLY in pure JSON array
        
        JSON Structure:
        [
          {{
            "title": "Resource Title",
            "url": "https://...",
            "platform": "MDN / GitHub / Blog / Official Docs",
            "resource_type": "article / docs / interactive",
            "rationale": "Why this is perfect for a {level} student on this topic (1 line)."
          }}
        ]
        """
        
        response = call_openrouter([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ])
        
        ai_resources = extract_json(response)
        if isinstance(ai_resources, list):
            resources.extend(ai_resources[:remaining])
    
    return resources

def generate_daily_task_content(subject, exam, level, topic, time_minutes, is_starting=False):
    """
    Generates a daily task with multiple curated resources.
    Returns JSON string with 'topic', 'description', and 'resources' list.
    """
    try:
        # Step 1: Research Resources using AI Curiosity/Reasoning
        resources = generate_curated_resources(subject, topic, level, exam)
        
        # Select best resource for context
        best_res_text = "Free web resources"
        if resources:
            best_res_text = f"Curated resources from {resources[0]['platform']}"

        time_guidance = "Focus on basics" if time_minutes < 45 else "Include a small exercise"
        
        task_prompt = f"""
        Topic: {topic}
        Subject: {subject}
        Resources: {json.dumps(resources)}
        Student Level: {level}
        Time: {time_minutes} minutes
        
        Create a clear, actionable study task for this student. 
        Focus on: {time_guidance}.
        
        Respond in pure JSON:
        {{
          "topic": "{topic}",
          "description": "Step-by-step guide...",
          "resources": {json.dumps(resources)}
        }}
        """
        
        response = call_openrouter([
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": task_prompt}
        ])
        
        data = extract_json(response)
        if data:
            if "resources" not in data:
                data["resources"] = resources
            return json.dumps(data)
        return None
        
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

def generate_full_roadmap(subject, level, goal, daily_time_min, target_date, style):
    """
    Generates a comprehensive multi-phase roadmap for a specific subject and goal.
    Returns a JSON structure: { "title": "...", "phases": [ { "name": "...", "modules": [ { "name": "...", "tasks": [...] } ] } ] }
    """
    prompt = f"""
    Create a detailed, professional learning roadmap for a student.
    
    Student Profile:
    - Subject: {subject}
    - Current Level: {level}
    - Target Goal: {goal} (e.g., job-ready, exam prep)
    - Daily Commitment: {daily_time_min} minutes
    - Target Date: {target_date}
    - Learning Style Preference: {style} (videos, articles, projects, mixed)
    
    Roadmap Requirements:
    1. Structure: Phases (e.g. Fundamentals) -> Modules (e.g. Basics of Syntax) -> Tasks (specific lessons).
    2. Logic: Sequence tasks from absolute basics to advanced topics.
    3. Content: Each task must have a title, description, estimated time, and a suggested 'deliverable' (what to build/write).
    4. Duration: The total time of all tasks should roughly align with the number of days until {target_date} at {daily_time_min} mins/day.
    5. Personalization: Adjust the curriculum depth for {level} level and {goal} goal.
    
    RESPOND ONLY IN PURE JSON:
    {{
      "title": "Your Personalized {subject} Roadmap",
      "phases": [
        {{
          "name": "Phase Name",
          "modules": [
            {{
              "name": "Module Name",
              "tasks": [
                {{
                  "title": "Task Title",
                  "description": "Specific learning objectives",
                  "estimated_time": 45,
                  "output_deliverable": "What the student should finish",
                  "resource_type": "{style}"
                }}
              ]
            }}
          ]
        }}
      ]
    }}
    """
    
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    
    response = call_openrouter(messages)
    data = extract_json(response)
    return data

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
