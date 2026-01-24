from fastapi import FastAPI, Depends, HTTPException, status
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import User, Goal, DailyTask, Submission, Roadmap, RoadmapTask, TaskResource
from auth import get_current_user_id, get_current_user_claims
import ai_service
import json
from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
import re

# Create DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Zuno Backend")

import os

# CORS Configuration
# Explicitly allowing both variants to prevent any matching edge cases
origins = [
    "http://localhost:5173", 
    "http://localhost:3000", 
    "https://zuno-v2.vercel.app", 
    "https://zuno-v2.vercel.app/",
    "https://zuno-production.vercel.app",
]

# Add origins from environment variable
env_origins = os.getenv("ALLOWED_ORIGINS", "")
if env_origins:
    origins.extend([o.strip() for o in env_origins.split(",") if o.strip()])

print(f"DEBUG: CORS Allowed Origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    # Regex to support all deployment previews and subdomains
    allow_origin_regex=r"https://.*\.vercel\.app", 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept", "Origin"],
)

# --- Pydantic Models ---
class OnboardingRequest(BaseModel):
    subjects: List[str] # Multiple skills
    full_name: Optional[str] = None
    exam_or_skill: str
    daily_time_minutes: int
    target_date: date
    target_goal: Optional[str] = "General Mastery"
    learning_style: Optional[str] = "Mixed"

class TaskSubmissionRequest(BaseModel):
    task_id: int
    submission_text: Optional[str] = None
    submission_image_url: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    goal_id: Optional[int] = None
    task_id: Optional[int] = None

class UserProfileUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    daily_time_minutes: Optional[int] = None
    learning_style: Optional[str] = None
    target_goal: Optional[str] = None

# --- Endpoints ---

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Zuno Backend is running"}

@app.get("/debug-cors")
def debug_cors():
    return {
        "allowed_origins": origins,
        "env_origins": os.getenv("ALLOWED_ORIGINS"),
        "ver": "1.0.1"
    }

@app.post("/onboarding")
def onboarding(req: OnboardingRequest, claims: dict = Depends(get_current_user_claims), db: Session = Depends(get_db)):
    user_id = claims.get("sub")
    email = claims.get("email", "")
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token: missing sub")

    # Check if user exists, create if not
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id, email=email, full_name=req.full_name)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        if req.full_name:
            user.full_name = req.full_name
            db.add(user)
    
    # We'll replace existing goals for simplicity in MVP, or just add. 
    # Let's add new ones and avoid duplicates.
    existing_goals = db.query(Goal).filter(Goal.user_id == user_id).all()
    existing_subjects = {g.subject for g in existing_goals}
    
    responses = []
    for subject in req.subjects:
        if subject in existing_subjects:
            # If a goal for this subject already exists, we might update it or skip.
            # For now, let's skip to avoid re-generating AI level for existing subjects.
            # A more robust solution would update if other parameters (exam_or_skill, time, target_date) changed.
            existing_goal = next((g for g in existing_goals if g.subject == subject), None)
            if existing_goal:
                responses.append({"subject": subject, "detected_level": existing_goal.detected_level, "message": "Goal already exists and updated."})
                # Optionally update other fields if they changed
                existing_goal.exam_or_skill = req.exam_or_skill
                existing_goal.daily_time_minutes = req.daily_time_minutes
                existing_goal.target_date = req.target_date
                db.add(existing_goal) # Mark for update
                continue
            
        ai_response_str = ai_service.detect_level_and_confirm(
            subject, req.exam_or_skill, req.daily_time_minutes, req.target_date
        )
        
        detected_level = "Beginner"
        message = "Welcome to Zuno."
        
        if ai_response_str:
            try:
                ai_data = json.loads(ai_response_str)
                detected_level = ai_data.get("level", "Beginner")
                message = ai_data.get("message", message)
            except json.JSONDecodeError as e:
                print(f"JSON Decode Error: {e}")
                print(f"Raw AI Response: {ai_response_str}")
                pass # Fallback to defaults

        new_goal = Goal(
            user_id=user_id,
            subject=subject,
            exam_or_skill=req.exam_or_skill,
            daily_time_minutes=req.daily_time_minutes,
            target_date=req.target_date,
            detected_level=detected_level,
            target_goal=req.target_goal,
            learning_style=req.learning_style
        )
        db.add(new_goal)
        db.flush() # Get goal ID

        # --- Generate Roadmap via AI ---
        print(f"DEBUG: Generating roadmap for {subject}...")
        try:
            roadmap_data = ai_service.generate_full_roadmap(
                subject, detected_level, req.target_goal, req.daily_time_minutes, req.target_date, req.learning_style
            )
        except Exception as e:
            print(f"ERROR: AI Roadmap generation failed: {e}")
            roadmap_data = None


        if not roadmap_data:
            print("WARNING: AI Roadmap generation failed or returned None. Using fallback roadmap.")
            roadmap_data = {
                "title": f"{subject} Fundamentals (Fallback)",
                "phases": [
                    {
                        "name": "Getting Started",
                        "modules": [
                            {
                                "name": "Introduction",
                                "tasks": [
                                    {
                                        "title": f"Introduction to {subject}",
                                        "description": f"Start your journey by exploring the core concepts of {subject}. Research the basics and set up your learning environment.",
                                        "estimated_time": 30,
                                        "output_deliverable": "A brief summary of what you learned and your setup.",
                                        "resource_type": "research"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }

        if roadmap_data:
            print(f"DEBUG: Roadmap generated successfully. Title: {roadmap_data.get('title')}")
            new_roadmap = Roadmap(
                user_id=user_id,
                goal_id=new_goal.id,
                title=roadmap_data.get("title", f"{subject} Roadmap")
            )
            db.add(new_roadmap)
            db.flush()

            order = 0
            for phase in roadmap_data.get("phases", []):
                for module in phase.get("modules", []):
                    for task in module.get("tasks", []):
                        new_rt = RoadmapTask(
                            roadmap_id=new_roadmap.id,
                            phase=phase.get("name", "Basics"),
                            module=module.get("name", "Module"),
                            title=task.get("title", "Lesson"),
                            description=task.get("description", ""),
                            estimated_time_minutes=task.get("estimated_time", 30),
                            output_deliverable=task.get("output_deliverable", ""),
                            order_index=order
                        )
                        if order == 0:
                            new_rt.status = "active"
                            new_rt.scheduled_date = date.today()
                        
                        db.add(new_rt)
                        order += 1
            print(f"DEBUG: Saved {order} roadmap tasks.")
        else:
            print("WARNING: No roadmap data returned from AI service. User will have a goal but no roadmap.")
        
        responses.append({"subject": subject, "detected_level": detected_level, "message": message})
    
    db.commit() # Commit all new goals, roadmaps, and tasks
    return {"message": "Onboarding complete", "goals": responses}

@app.get("/roadmap")
def get_roadmap(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    roadmap = db.query(Roadmap).filter(Roadmap.user_id == user_id, Roadmap.is_active == True).first()
    if not roadmap:
        return {"roadmap": None}
    
    tasks = db.query(RoadmapTask).filter(RoadmapTask.roadmap_id == roadmap.id).order_by(RoadmapTask.order_index).all()
    
    # Structure into phases/modules for frontend
    phases = {}
    for t in tasks:
        if t.phase not in phases:
            phases[t.phase] = {"name": t.phase, "modules": {}}
        if t.module not in phases[t.phase]["modules"]:
            phases[t.phase]["modules"][t.module] = {"name": t.module, "tasks": []}
            
        phases[t.phase]["modules"][t.module]["tasks"].append({
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status,
            "estimated_time": t.estimated_time_minutes,
            "output": t.output_deliverable
        })
    
    # Convert to list of phases
    result_phases = []
    for p_name, p_data in phases.items():
        modules = []
        for m_name, m_data in p_data["modules"].items():
            modules.append(m_data)
        result_phases.append({"name": p_name, "modules": modules})

    return {
        "id": roadmap.id,
        "title": roadmap.title,
        "phases": result_phases
    }

@app.patch("/roadmap/task/{task_id}/complete")
def complete_roadmap_task(task_id: int, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    task = db.query(RoadmapTask).join(Roadmap).filter(RoadmapTask.id == task_id, Roadmap.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = "completed"
    task.completed_at = datetime.utcnow()
    
    # Unlock next task
    next_task = db.query(RoadmapTask).filter(
        RoadmapTask.roadmap_id == task.roadmap_id, 
        RoadmapTask.order_index == task.order_index + 1
    ).first()
    if next_task:
        next_task.status = "active"
        next_task.scheduled_date = date.today() # Bring forward to today
        
    db.commit()
    return {"message": "Task completed"}

@app.get("/daily-plan")
def get_daily_plan(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    print(f"DEBUG: get_daily_plan called for user {user_id}")
    today = date.today()
    results = []
    
    try:
        # Check for active roadmap tasks first
        active_roadmap_task = db.query(RoadmapTask).join(Roadmap).filter(
            Roadmap.user_id == user_id,
            RoadmapTask.status == "active"
        ).first()
        print(f"DEBUG: active_roadmap_task: {active_roadmap_task}")
    except Exception as e:
        print(f"ERROR in get_daily_plan query: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    if active_roadmap_task:
        # Check if already converted to daily task for today
        task = db.query(DailyTask).filter(
            DailyTask.user_id == user_id,
            DailyTask.roadmap_task_id == active_roadmap_task.id,
            DailyTask.date == today
        ).first()

        if not task:
            # Generate enriched content via AI
            if not active_roadmap_task.roadmap or not active_roadmap_task.roadmap.goal:
                print(f"ERROR: Roadmap or Goal missing for task {active_roadmap_task.id}")
                return [] # Or handle gracefully

            subject = active_roadmap_task.roadmap.goal.subject
            exam = active_roadmap_task.roadmap.goal.exam_or_skill
            level = active_roadmap_task.roadmap.goal.detected_level or "Beginner"
            minutes = active_roadmap_task.roadmap.goal.daily_time_minutes

            print(f"DEBUG: Generating enriched content for task: {active_roadmap_task.title}")
            ai_data_str = ai_service.generate_daily_task_content(
                subject, exam, level, active_roadmap_task.title, minutes
            )

            resources_data = []
            task_description = active_roadmap_task.description

            if ai_data_str:
                try:
                    ai_data = json.loads(ai_data_str)
                    resources_data = ai_data.get("resources", [])
                    task_description = ai_data.get("description", task_description)
                except Exception as e:
                    print(f"Error parsing AI task data: {e}")

            task = DailyTask(
                user_id=user_id,
                goal_id=active_roadmap_task.roadmap.goal_id,
                roadmap_task_id=active_roadmap_task.id,
                topic=active_roadmap_task.title,
                description=task_description,
                date=today
            )
            db.add(task)
            db.commit()
            db.refresh(task)

            # Save resources
            for res in resources_data:
                url = res.get("url", "")
                confidence = res.get("video_confidence", "fallback")
                
                new_res = TaskResource(
                    daily_task_id=task.id,
                    title=res.get("title"),
                    url=url,
                    platform=res.get("platform"),
                    resource_type=res.get("resource_type"),
                    rationale=res.get("rationale"),
                    video_confidence=confidence,
                    validated=res.get("is_embeddable", False),
                    fallback_used=(confidence == "fallback"),
                    video_id=res.get("video_id"),
                    validated_at=datetime.fromisoformat(res["validated_at"]) if res.get("validated_at") else None,
                    is_embeddable=res.get("is_embeddable", False)
                )
                db.add(new_res)
            db.commit()
            db.refresh(task)

        return [{
            "id": task.id,
            "goal_id": task.goal_id,
            "subject": active_roadmap_task.roadmap.goal.subject,
            "level": active_roadmap_task.roadmap.goal.detected_level,
            "goal_description": active_roadmap_task.roadmap.goal.exam_or_skill,
            "topic": task.topic,
            "description": task.description,
            "resources": [{
                "id": r.id,
                "title": r.title,
                "url": r.url,
                "platform": r.platform,
                "type": r.resource_type,
                "rationale": r.rationale
            } for r in task.resources],
            "date": task.date,
            "is_completed": task.is_completed,
            "roadmap_task_id": active_roadmap_task.id
        }]

    return results

@app.get("/task/{task_id}")
def get_task(task_id: int, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    task = db.query(DailyTask).filter(DailyTask.id == task_id, DailyTask.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Enrich with subject/level from goal if available
    subject = "Learning"
    level = "Beginner"
    if task.goal:
        subject = task.goal.subject
        level = task.goal.detected_level
    elif task.roadmap_task and task.roadmap_task.roadmap and task.roadmap_task.roadmap.goal:
        subject = task.roadmap_task.roadmap.goal.subject
        level = task.roadmap_task.roadmap.goal.detected_level

    return {
        "id": task.id,
        "goal_id": task.goal_id,
        "subject": subject,
        "level": level,
        "topic": task.topic,
        "resource_link": task.resource_link,
        "task_description": task.description,
        "resources": [{
            "id": r.id,
            "title": r.title,
            "url": r.url,
            "platform": r.platform,
            "type": r.resource_type,
            "rationale": r.rationale
        } for r in task.resources],
        "date": task.date,
        "is_completed": task.is_completed,
        "roadmap_task_id": task.roadmap_task_id
    }

@app.post("/submit-task")
def submit_task(req: TaskSubmissionRequest, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    task = db.query(DailyTask).filter(DailyTask.id == req.task_id, DailyTask.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    # Check if already submitted
    existing_sub = db.query(Submission).filter(Submission.task_id == req.task_id).first()
    if existing_sub:
         return {"message": "Task already submitted", "score": existing_sub.score, "ai_feedback": existing_sub.ai_feedback}

    # Get the goal to determine level
    level = "Beginner"
    if task.goal:
        level = task.goal.detected_level or "Beginner"

    # Evaluate with AI
    ai_response_str = ai_service.evaluate_submission_content(task.description, req.submission_text or "Image submitted", level)
    
    print(f"DEBUG: AI Score evaluation response: {ai_response_str}")
    
    score = 0
    ai_feedback = "Submission received."
    
    if ai_response_str:
        try:
            eval_data = json.loads(ai_response_str)
            score = eval_data.get("score", 0)
            ai_feedback = eval_data.get("feedback", ai_feedback)
        except Exception as e:
            print(f"ERROR: Failed to parse AI feedback JSON: {e}")
            pass

    submission = Submission( # Renamed from new_submission
        task_id=req.task_id,
        text=req.submission_text,
        image_url=req.submission_image_url,
        ai_feedback=ai_feedback,
        score=score
    )
    db.add(submission) # Changed from db.add(new_submission)
    task.is_completed = True

    # --- Sync with Roadmap ---
    if task.roadmap_task_id:
        roadmap_task = db.query(RoadmapTask).filter(RoadmapTask.id == task.roadmap_task_id).first()
        if roadmap_task:
            roadmap_task.status = "completed"
            roadmap_task.completed_at = datetime.utcnow()
            
            # Unlock next roadmap task
            next_rt = db.query(RoadmapTask).filter(
                RoadmapTask.roadmap_id == roadmap_task.roadmap_id,
                RoadmapTask.order_index == roadmap_task.order_index + 1
            ).first()
            if next_rt:
                next_rt.status = "active"
                next_rt.scheduled_date = date.today()

    db.commit()
    print(f"DEBUG: Submission committed for task {req.task_id}. Score: {score}")
    return {"message": "Success", "score": score, "ai_feedback": ai_feedback}

@app.get("/progress")
def get_progress(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    tasks = db.query(DailyTask).filter(DailyTask.user_id == user_id).order_by(DailyTask.date.desc()).all()
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t.is_completed)
    
    # Calculate Average Score
    submissions = db.query(Submission).join(DailyTask).filter(DailyTask.user_id == user_id).all()
    avg_score = 0
    if submissions:
        total_score = sum([s.score for s in submissions if s.score is not None])
        avg_score = total_score / len(submissions)
        
    # Streak Logic: Count consecutive days of completions starting from today or yesterday
    streak = 0
    if tasks:
        today = date.today()
        yesterday = today - timedelta(days=1)
        
        # Group tasks by date
        tasks_by_date = {}
        for t in tasks:
            if t.date not in tasks_by_date:
                tasks_by_date[t.date] = []
            tasks_by_date[t.date].append(t)
        
        # Check if they did anything today or yesterday to keep streak alive
        current_check = today
        if not any(t.is_completed for t in tasks_by_date.get(today, [])):
            current_check = yesterday
            
        while True:
            day_tasks = tasks_by_date.get(current_check, [])
            if day_tasks and any(t.is_completed for t in day_tasks):
                streak += 1
                current_check -= timedelta(days=1)
            else:
                break
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_percentage": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        "average_score": round(avg_score, 1),
        "current_streak": streak
    }

@app.get("/weekly-summary")
def get_weekly_summary(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    # Simple logic: Get stats and ask AI
    # In a real app, query last 7 days.
    
    completed_count = db.query(DailyTask).filter(DailyTask.user_id == user_id, DailyTask.is_completed == True).count()
    
    # Get average score again
    submissions = db.query(Submission).join(DailyTask).filter(DailyTask.user_id == user_id).all()
    avg_score = 0
    if submissions:
        total_score = sum([s.score for s in submissions if s.score is not None])
        avg_score = total_score / len(submissions)
        
    # Get recent topics and level
    recent_tasks = db.query(DailyTask).filter(DailyTask.user_id == user_id).order_by(DailyTask.date.desc()).limit(5).all()
    topics_list = [t.topic for t in recent_tasks]
    topics_str = ", ".join(topics_list)
    
    goal = db.query(Goal).filter(Goal.user_id == user_id).first()
    level = goal.detected_level if goal else "Beginner"

    summary_text = ai_service.generate_week_summary(completed_count, round(avg_score, 1), 7, level, topics_str)
    
    return {"mentor_summary_text": summary_text}

@app.post("/chat")
def chat(req: ChatRequest, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    goal_context = ""
    task_context = ""
    target_task = None

    if req.goal_id:
        goal = db.query(Goal).filter(Goal.id == req.goal_id, Goal.user_id == user_id).first()
        if goal:
            goal_context = f"Subject: {goal.subject}, Goal: {goal.exam_or_skill}"
    
    if req.task_id:
        target_task = db.query(DailyTask).filter(DailyTask.id == req.task_id, DailyTask.user_id == user_id).first()
        if target_task:
            task_context = f"Task: {target_task.topic}, Description: {target_task.description}, Current Resource: {target_task.resource_link}"

    ai_data = ai_service.answer_question(req.message, goal_context, task_context)
    
    if not ai_data:
        return {"response": "I'm sorry, I'm having trouble thinking right now."}

    # Process Action
    action = ai_data.get("action")
    if action and action.get("type") == "update_resource" and target_task:
        new_link = action.get("new_link")
        if new_link:
            target_task.resource_link = new_link
            db.commit()
            db.refresh(target_task)

    return {
        "response": ai_data.get("answer", "No response from mentor."),
        "action_taken": action.get("type") if action else None,
        "task_updated": target_task.id if (action and target_task) else None
    }

@app.get("/user/profile")
def get_user_profile(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        # Do NOT create user automatically. 
        # User is created only during onboarding when they set goals.
        return {
            "id": user_id,
            "email": "",
            "full_name": "",
            "daily_time_minutes": 60,
            "learning_style": "mixed",
            "target_goal": "General Mastery",
            "has_onboarded": False
        }
    
    # Get user's primary goal to extract preferences
    goal = db.query(Goal).filter(Goal.user_id == user_id).first()
    
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "daily_time_minutes": goal.daily_time_minutes if goal else 60,
        "learning_style": goal.learning_style if goal else "mixed",
        "target_goal": goal.target_goal if goal else "General Mastery",
        "has_onboarded": goal is not None
    }

@app.put("/user/settings")
def update_user_settings(req: UserProfileUpdate, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if req.email:
        user.email = req.email
    if req.full_name:
        user.full_name = req.full_name
        
    # Update preferences in Goal table if exists
    goal = db.query(Goal).filter(Goal.user_id == user_id).first()
    if goal:
        if req.daily_time_minutes:
            goal.daily_time_minutes = req.daily_time_minutes
        if req.learning_style:
            goal.learning_style = req.learning_style
        if req.target_goal:
            goal.target_goal = req.target_goal
            
    db.commit()
    return {"message": "Settings updated successfully"}

@app.post("/task/{task_id}/regenerate-resources")
def regenerate_task_resources(task_id: int, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    task = db.query(DailyTask).filter(DailyTask.id == task_id, DailyTask.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Get goal for AI context
    subject = "Learning"
    exam = "General"
    level = "Beginner"
    minutes = 60
    
    if task.goal:
        subject = task.goal.subject
        exam = task.goal.exam_or_skill
        level = task.goal.detected_level or "Beginner"
        minutes = task.goal.daily_time_minutes
    
    # Generate new resources
    ai_data_str = ai_service.generate_daily_task_content(
        subject, exam, level, task.topic, minutes
    )
    
    if not ai_data_str:
        raise HTTPException(status_code=500, detail="Failed to generate new resources")
        
    try:
        ai_data = json.loads(ai_data_str)
        resources_data = ai_data.get("resources", [])
    except:
        resources_data = []

    # Clear old resources
    db.query(TaskResource).filter(TaskResource.daily_task_id == task.id).delete()
    
    # Save new resources
    for res in resources_data:
        url = res.get("url", "")
        confidence = res.get("video_confidence", "fallback")

        new_res = TaskResource(
            daily_task_id=task.id,
            title=res.get("title"),
            url=url,
            platform=res.get("platform"),
            resource_type=res.get("resource_type"),
            rationale=res.get("rationale"),
            video_confidence=confidence,
            validated=res.get("is_embeddable", False),
            fallback_used=(confidence == "fallback"),
            video_id=res.get("video_id"),
            validated_at=datetime.fromisoformat(res["validated_at"]) if res.get("validated_at") else None,
            is_embeddable=res.get("is_embeddable", False)
        )
        db.add(new_res)
    
    db.commit()
    db.refresh(task)
    
    return {
        "message": "Resources regenerated",
        "resources": [{
            "id": r.id,
            "title": r.title,
            "url": r.url,
            "platform": r.platform,
            "type": r.resource_type,
            "rationale": r.rationale
        } for r in task.resources]
    }

# Server configuration for direct execution
if __name__ == "__main__":
    import uvicorn
    import os
    
    # Get port from environment variable (Railway compatibility)
    # Get port from environment variable (Railway compatibility)
    try:
        env_port = os.getenv("PORT")
        print(f"DEBUG: Starting up... Environment PORT variable is: {env_port}")
        port = int(env_port or 8000)
    except (ValueError, TypeError):
        print(f"DEBUG: Failed to parse PORT '{os.getenv('PORT')}'. Defaulting to 8000.")
        port = 8000
    
    print(f"DEBUG: Uvicorn launching on 0.0.0.0:{port}")
    
    # Run server on 0.0.0.0 for container compatibility
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=False  # Set to True for development
    )
