from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Date, Text
from sqlalchemy.orm import relationship
from database import Base
import datetime

# Define Roadmap and RoadmapTask FIRST to avoid forward reference issues
class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    goal = Column(String, nullable=False)
    total_hours = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="roadmaps")
    tasks = relationship("RoadmapTask", back_populates="roadmap")

class RoadmapTask(Base):
    __tablename__ = "roadmap_tasks"

    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id"), nullable=False)
    phase = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    estimated_time_hours = Column(Integer, nullable=True)
    status = Column(String, default="pending") 
    order_index = Column(Integer, default=0)
    completed_at = Column(DateTime, nullable=True)

    roadmap = relationship("Roadmap", back_populates="tasks")
    daily_tasks = relationship("DailyTask", back_populates="roadmap_task")

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

    user = relationship("User", back_populates="goals")
    tasks = relationship("DailyTask", back_populates="goal")

class DailyTask(Base):
    __tablename__ = "daily_tasks"
    __table_args__ = (
        # Ensure one task per goal per day
        # Note: This uses a unique constraint on (user_id, goal_id, date)
        # to prevent duplicate tasks
        {'sqlite_autoincrement': True}
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    goal_id = Column(Integer, ForeignKey("goals.id"), nullable=True) # Linked to a specific goal
    topic = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    resource_link = Column(String, nullable=True)
    date = Column(Date, default=datetime.date.today, nullable=False)
    is_completed = Column(Boolean, default=False)
    roadmap_task_id = Column(Integer, ForeignKey("roadmap_tasks.id"), nullable=True)

    user = relationship("User", back_populates="tasks")
    goal = relationship("Goal", back_populates="tasks")
    submission = relationship("Submission", uselist=False, back_populates="task")
    roadmap_task = relationship("RoadmapTask", back_populates="daily_tasks")

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
