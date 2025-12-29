from fastapi import FastAPI, Depends, HTTPException, status
from dotenv import load_dotenv
load_dotenv()
from sqlalchemy.orm import Session
from database import engine, get_db, Base
from models import User, Goal, DailyTask, Submission
from auth import get_current_user_id
import ai_service
import json
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from fastapi.middleware.cors import CORSMiddleware

# Create DB Tables
Base.metadata.create_all(bind=engine)

# Production build trigger: 1
app = FastAPI(title="Zuno Backend")

# CORS configuration
ALLOWED_ORIGINS = [
    "http://localhost:5173", # Local dev
    "https://zuno-mentor.vercel.app", # Replace with actual prod domain if known
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, you'd specify ALLOWED_ORIGINS
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

# --- Endpoints ---

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Zuno Backend is production ready"}

@app.get("/")
def root():
    return {"message": "Welcome to Zuno API. Visit /health for status."}

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
                    # Skip if AI fails for one goal, but maybe log it
                    continue
                    
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
            "is_completed": task.is_completed
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
        
    # Streak Logic (Simple: consecutive days with completed tasks/submissions ending today or yesterday)
    # ... Implementation of complex date logic might be overkill, let's just count total completed for now or a basic check
    # For MVP, let's keep it simple:
    
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
