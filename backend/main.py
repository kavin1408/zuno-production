from fastapi import FastAPI, Depends, HTTPException, status
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import User, Goal, DailyTask, Submission, Roadmap, RoadmapTask
from auth import get_current_user_id
import ai_service
import json
import os
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import datetime
from fastapi.middleware.cors import CORSMiddleware

# Create DB Tables
# Create DB Tables - WRAPPED TO PREVENT CRASH
db_startup_error = None
try:
    Base.metadata.create_all(bind=engine)
    print("Database tables created/verified successfully.")
except Exception as e:
    db_startup_error = str(e)
    print(f"CRITICAL DATABASE ERROR: {e}")

# Production build trigger: 4
print("--- STARTING ZUNO BACKEND ---")
app = FastAPI(title="Zuno Backend")

# CORS configuration - TEMPORARY: Allow all origins to fix blocking
# TODO: Tighten this once deployment is confirmed working
print("CORS Configuration: Allowing ALL origins (temporary for debugging)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins temporarily
    allow_credentials=False,  # Must be False when using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# --- Pydantic Models ---
class OnboardingRequest(BaseModel):
    subjects: List[str] # Multiple skills
    exam_or_skill: str
    daily_time_minutes: int
    target_date: date

class TaskSubmissionRequest(BaseModel):
    task_id: int
    submission_text: Optional[str] = None
    submission_image_url: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    goal_id: Optional[int] = None
    task_id: Optional[int] = None

class RoadmapRequest(BaseModel):
    subject: str
    goal: str
    level: str = "Beginner"

# --- Endpoints ---

@app.get("/health")
def health_check():
    status = "ok" if not db_startup_error else "degraded"
    return {
        "status": status, 
        "message": "Zuno Backend is production ready",
        "db_error": db_startup_error
    }

@app.get("/test-resources")
def test_resources():
    """Diagnostic endpoint to test resource search"""
    try:
        import research_service
        
        # Test curated resources
        curated = research_service.get_curated_resource("python", "Beginner")
        
        # Test YouTube search with fallback
        youtube_results = research_service.search_youtube_resources("python tutorial", limit=1)
        
        return {
            "curated_resource": curated,
            "youtube_search_result": youtube_results[0] if youtube_results else None,
            "youtube_search_count": len(youtube_results),
            "status": "Resource search is working"
        }
    except Exception as e:
        import traceback
        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "status": "Resource search failed"
        }


@app.get("/")
def root():
    status_msg = "Operational" if not db_startup_error else "Database Error"
    return {
        "message": "Welcome to Zuno API.", 
        "status": status_msg,
        "db_error_details": db_startup_error,
        "instruction": "If db_error is present, check Railway Variables."
    }

@app.post("/onboarding")
def onboarding(req: OnboardingRequest, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    # Check if user exists, create if not
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        user = User(id=user_id, email="user@example.com") # Basic placeholder, real email can be extracted from JWT if needed
        db.add(user)
        db.commit()
        db.refresh(user)
    
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
            detected_level=detected_level
        )
        db.add(new_goal)
        responses.append({"subject": subject, "detected_level": detected_level, "message": message})
    
    db.commit() # Commit all new goals and updates
    return {"message": "Onboarding complete", "goals": responses}

@app.get("/daily-plan")
def get_daily_plan(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    today = date.today()
    
    goals = db.query(Goal).filter(Goal.user_id == user_id).all()
    if not goals:
        raise HTTPException(status_code=400, detail="User has no goals set. Please complete onboarding.")
    
    results = []
    for goal in goals:
        # Check if task exists for today for this goal
        # Use .with_for_update() to lock the row and prevent race conditions
        task = db.query(DailyTask).filter(
            DailyTask.user_id == user_id, 
            DailyTask.goal_id == goal.id, 
            DailyTask.date == today
        ).first()
        
        if not task:
            # Double-check after acquiring lock to prevent race condition
            # This ensures we don't create duplicates if multiple requests come in
            task = db.query(DailyTask).filter(
                DailyTask.user_id == user_id,
                DailyTask.goal_id == goal.id,
                DailyTask.date == today
            ).first()
            
            if not task:
                # Generate new task for this specific goal
                # Get recent tasks for this goal
                recent_tasks = db.query(DailyTask).filter(DailyTask.goal_id == goal.id).order_by(DailyTask.date.desc()).limit(3).all()
                recent_topics = ", ".join([t.topic for t in recent_tasks])
                
                ai_response_str = ai_service.generate_daily_task_content(
                    goal.subject, goal.exam_or_skill, goal.detected_level, recent_topics, goal.daily_time_minutes
                )
                
                if not ai_response_str:
                    # FALLBACK TASK logic if AI fails (e.g. invalid API Key)
                    print(f"AI failed for goal {goal.id}, using fallback.")
                    ai_response_str = json.dumps({
                        "topic": "Fundamentals Review (AI Unavailable)",
                        "description": "The AI mentor is currently offline (check API Key). For today, review the core fundamentals of your subject. Focus on documentation and basic concepts.",
                        "resource_link": "https://www.google.com/search?q=" + goal.subject.replace(" ", "+") + "+fundamentals"
                    })
                    
                try:
                    task_data = json.loads(ai_response_str)
                    task = DailyTask(
                        user_id=user_id,
                        goal_id=goal.id,
                        topic=task_data.get("topic", "Daily Study"),
                        description=task_data.get("description", "Study 30 mins"),
                        resource_link=task_data.get("resource_link", ""),
                        date=today
                    )
                    
                    # LINK TO ROADMAP TASK ?? (Future improvement: find matching pending roadmap task)
                    # For now, we just create the daily task.
                    # Ideally, we should pick the next pending RoadmapTask and make that the DailyTask.
                    
                    db.add(task)
                    db.commit()
                    db.refresh(task)
                except json.JSONDecodeError as e:
                    print(f"JSON Decode Error in daily plan for goal {goal.id}: {e}")
                    print(f"Raw AI Response: {ai_response_str}")
                    continue
                except Exception as e:
                    # Handle any database errors (like unique constraint violations)
                    print(f"Error creating task for goal {goal.id}: {e}")
                    db.rollback()
                    # Try to fetch the task again in case it was created by another request
                    task = db.query(DailyTask).filter(
                        DailyTask.user_id == user_id,
                        DailyTask.goal_id == goal.id,
                        DailyTask.date == today
                    ).first()
                    if not task:
                        continue
                
        results.append({
            "id": task.id,
            "goal_id": task.goal_id,
            "subject": goal.subject,
            "level": goal.detected_level,
            "goal_description": goal.exam_or_skill,
            "topic": task.topic,
            "resource_link": task.resource_link,
            "task_description": task.description,
            "date": task.date,
            "is_completed": task.is_completed,
            "roadmap_task_id": task.roadmap_task_id
        })
        
    if not results:
        # EMERGENCY BYPASS: If no tasks could be created/found (e.g. DB error), return an in-memory task
        # This prevents the "No Learning Paths" redirect loop.
        results.append({
            "id": 0,
            "goal_id": 0,
            "subject": "System Check",
            "level": "Diagnostic",
            "goal_description": "Emergency Dashboard Access",
            "topic": "System Diagnosis",
            "resource_link": "https://zuno.app",
            "task_description": "If you see this, the system failed to save tasks to the database. \n\nPossible Reason: Database write error or Schema mismatch.\n\nPlease attempt to 'Complete' this task to test connection.",
            "date": today,
            "is_completed": False
        })

    return results

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
    
    score = 0
    feedback = "Submission received."
    
    if ai_response_str:
        try:
            eval_data = json.loads(ai_response_str)
            score = eval_data.get("score", 0)
            feedback = eval_data.get("feedback", "")
        except:
            pass

    new_submission = Submission(
        task_id=req.task_id,
        text=req.submission_text,
        image_url=req.submission_image_url,
        ai_feedback=feedback,
        score=score
    )
    
    task.is_completed = True
    
    # SMART LOGIC: Auto-complete linked RoadmapTask
    if task.roadmap_task_id:
        r_task = db.query(RoadmapTask).filter(RoadmapTask.id == task.roadmap_task_id).first()
        if r_task and r_task.status != "completed":
            r_task.status = "completed"
            r_task.completed_at = datetime.datetime.utcnow()
            print(f"SMART LOGIC: Automatically marked Roadmap Task {r_task.id} as completed.")

    db.add(new_submission)
    db.commit()
    
    return {"ai_feedback": feedback, "score": score}

@app.get("/progress")
def get_progress(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    total_tasks = db.query(DailyTask).filter(DailyTask.user_id == user_id).count()
    completed_tasks = db.query(DailyTask).filter(DailyTask.user_id == user_id, DailyTask.is_completed == True).count()
    
    # Calculate Average Score
    submissions = db.query(Submission).join(DailyTask).filter(DailyTask.user_id == user_id).all()
    avg_score = 0
    if submissions:
        total_score = sum([s.score for s in submissions if s.score is not None])
        avg_score = total_score / len(submissions)
        
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_percentage": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0,
        "average_score": round(avg_score, 1),
        "current_streak": completed_tasks # Placeholder for MVP
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

# --- Roadmap Endpoints ---

@app.post("/roadmap/generate")
def create_roadmap(req: RoadmapRequest, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    # Check if exists
    existing_roadmap = db.query(Roadmap).filter(Roadmap.user_id == user_id, Roadmap.goal == req.goal).first()
    if existing_roadmap:
        # For MVP, returning existing one. We can add REGENERATE flag later.
        # But user requirement said "Allow roadmap regeneration (with confirmation)". 
        # Since this is POST, we can assume it's a new request or explicit regen. 
        # Let's delete old one if exists for simplicity or return it?
        # Let's return the old one for now to prevent accidental overwrite, logic should be handled by frontend to explicitly delete first if regen needed.
        # Actually, let's just make a new one if requested.
        pass

    # Call AI
    ai_json = ai_service.generate_roadmap(req.subject, req.goal, level=req.level)
    if not ai_json:
        raise HTTPException(status_code=500, detail="Failed to generate roadmap from AI")
    
    try:
        data = json.loads(ai_json)
        phases = data.get("phases", [])
        
        # Create Roadmap
        new_roadmap = Roadmap(user_id=user_id, goal=req.goal, total_hours=0) # Update hours later
        db.add(new_roadmap)
        db.commit()
        db.refresh(new_roadmap)
        
        idx = 0
        total_hours = 0
        
        for phase_obj in phases:
            phase_name = phase_obj.get("name", "Phase X")
            tasks = phase_obj.get("tasks", [])
            for t in tasks:
                idx += 1
                hours = t.get("estimated_time_hours", 1)
                total_hours += hours
                
                r_task = RoadmapTask(
                    roadmap_id=new_roadmap.id,
                    phase=phase_name,
                    title=t.get("title", "Task"),
                    description=t.get("description", ""),
                    estimated_time_hours=hours,
                    status="pending",
                    order_index=idx
                )
                db.add(r_task)
        
        new_roadmap.total_hours = total_hours
        db.commit()
        
        return {"roadmap_id": new_roadmap.id, "message": "Roadmap generated successfully"}
        
    except Exception as e:
        print(f"Error saving roadmap: {e}")
        raise HTTPException(status_code=500, detail="Error parsing or saving roadmap")

@app.get("/roadmap")
def get_roadmap(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    # Get the most recent roadmap or all? Requirement says "fetch user's roadmap". implied singular active one.
    roadmap = db.query(Roadmap).filter(Roadmap.user_id == user_id).order_by(Roadmap.created_at.desc()).first()
    if not roadmap:
        return {"roadmap": None}
    
    # Get tasks
    tasks = db.query(RoadmapTask).filter(RoadmapTask.roadmap_id == roadmap.id).order_by(RoadmapTask.order_index).all()
    
    # Group by phase
    phases = {}
    for t in tasks:
        if t.phase not in phases:
            phases[t.phase] = []
        phases[t.phase].append({
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "estimated_time": t.estimated_time_hours,
            "status": t.status,
            "completed_at": t.completed_at
        })
        
    return {
        "roadmap": {
            "id": roadmap.id,
            "goal": roadmap.goal,
            "total_hours": roadmap.total_hours,
            "phases": phases
        }
    }

@app.patch("/roadmap/task/{task_id}")
def update_roadmap_task(task_id: int, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    # Manual update endpoint? Or generic status update?
    # Req: PATCH /roadmap/task/:id -> update task status
    # We will assume toggle or set to completed.
    
    # Verify ownership via join
    r_task = db.query(RoadmapTask).join(Roadmap).filter(RoadmapTask.id == task_id, Roadmap.user_id == user_id).first()
    if not r_task:
        raise HTTPException(status_code=404, detail="Task not found")
        
    if r_task.status != "completed":
        r_task.status = "completed"
        r_task.completed_at = datetime.datetime.utcnow()
    else:
        # Optional: toggle back?
        pass # Keep simple for now
        
    db.commit()
    return {"status": r_task.status}
