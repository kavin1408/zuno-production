from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)  # Supabase UUID
    email = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    goals = relationship("Goal", back_populates="user")
    tasks = relationship("DailyTask", back_populates="user")
    roadmaps = relationship("Roadmap", back_populates="user")

class Goal(Base):
    __tablename__ = "goals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    subject = Column(String, nullable=False)
    exam_or_skill = Column(String, nullable=False)
    daily_time_minutes = Column(Integer, nullable=False)
    target_date = Column(Date, nullable=False)
    detected_level = Column(String, nullable=True)
    
    # New fields for Smart Roadmap
    target_goal = Column(String, nullable=True) # e.g., "job-ready", "certification"
    learning_style = Column(String, nullable=True) # e.g., "videos", "mixed"

    user = relationship("User", back_populates="goals")
    tasks = relationship("DailyTask", back_populates="goal")
    roadmap = relationship("Roadmap", back_populates="goal", uselist=False)

class Roadmap(Base):
    __tablename__ = "roadmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    user = relationship("User", back_populates="roadmaps")
    goal = relationship("Goal", back_populates="roadmap")
    roadmap_tasks = relationship("RoadmapTask", back_populates="roadmap", cascade="all, delete-orphan")

class RoadmapTask(Base):
    __tablename__ = "roadmap_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=False)
    phase = Column(String, nullable=False) # e.g., "Fundamentals", "Advanced"
    module = Column(String, nullable=False) # e.g., "Intro to Python", "Data Types"
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    estimated_time_minutes = Column(Integer, nullable=False)
    resource_links = Column(Text, nullable=True) # JSON string of links
    output_deliverable = Column(Text, nullable=True)
    order_index = Column(Integer, nullable=False)
    
    status = Column(String, default="pending") # pending, active, completed, skipped
    completed_at = Column(DateTime, nullable=True)
    scheduled_date = Column(Date, nullable=True)
    
    roadmap = relationship("Roadmap", back_populates="roadmap_tasks")
    daily_tasks = relationship("DailyTask", back_populates="roadmap_task")
    resources = relationship("TaskResource", back_populates="roadmap_task", cascade="all, delete-orphan")

class DailyTask(Base):
    __tablename__ = "daily_tasks"
    __table_args__ = (
        {'sqlite_autoincrement': True}
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=True)
    roadmap_task_id = Column(Integer, ForeignKey("roadmap_tasks.id"), nullable=True) # Link to roadmap
    topic = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    resource_link = Column(String, nullable=True)
    date = Column(Date, default=datetime.date.today, nullable=False)
    is_completed = Column(Boolean, default=False)

    user = relationship("User", back_populates="tasks")
    goal = relationship("Goal", back_populates="tasks")
    roadmap_task = relationship("RoadmapTask", back_populates="daily_tasks")
    submission = relationship("Submission", uselist=False, back_populates="task")
    resources = relationship("TaskResource", back_populates="daily_task", cascade="all, delete-orphan")

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("daily_tasks.id"), unique=True, nullable=False)
    text = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    ai_feedback = Column(Text, nullable=True)
    score = Column(Integer, nullable=True)
    submitted_at = Column(DateTime, default=datetime.datetime.utcnow)

    task = relationship("DailyTask", back_populates="submission")

class TaskResource(Base):
    __tablename__ = "task_resources"

    id = Column(Integer, primary_key=True, index=True)
    daily_task_id = Column(Integer, ForeignKey("daily_tasks.id"), nullable=True)
    roadmap_task_id = Column(Integer, ForeignKey("roadmap_tasks.id"), nullable=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    platform = Column(String, nullable=True) # e.g., "YouTube", "GitHub"
    resource_type = Column(String, nullable=True) # e.g., "video", "article", "docs"
    rationale = Column(Text, nullable=True)
    video_confidence = Column(String, nullable=True) # "high" | "fallback"
    validated = Column(Boolean, default=False)
    fallback_used = Column(Boolean, default=False)
    
    # New fields for YouTube validation
    video_id = Column(String, nullable=True)  # YouTube video ID (11 chars)
    validated_at = Column(DateTime, nullable=True)  # When video was last validated
    is_embeddable = Column(Boolean, default=False)  # Whether video is embeddable
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    daily_task = relationship("DailyTask", back_populates="resources")
    roadmap_task = relationship("RoadmapTask", back_populates="resources")
