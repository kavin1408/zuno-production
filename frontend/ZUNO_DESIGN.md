# Zuno - AI-Powered Student Mentor

## Design System

### Color Palette
- **Background**: Deep charcoal (`#1a1a1e`) - Easy on the eyes, not pure black
- **Cards**: Slightly lighter (`#25252a`) for subtle depth
- **Borders**: Minimal contrast (`#35353a`) for calm structure
- **Accent**: Indigo (`#4f46e5` / indigo-600) - Used sparingly for:
  - Primary CTAs
  - Today's Task highlight
  - Progress indicators
  - Active states

### Typography
- **Font**: Inter (premium sans-serif)
- **Hierarchy**: Strong, confident
- **Copy**: Short, direct, motivational without hype

### Design Principles
1. **One primary action per screen** - Reduces cognitive load
2. **Productivity over decoration** - No unnecessary animations
3. **Calm pressure** - Motivational without being overwhelming
4. **Visual hierarchy** - Clear separation of content importance

## Application Structure

### Authentication Flow
- **Login** (`/login`) - Clean, centered card with minimal friction
- **Signup** (`/signup`) - Same visual language, email/password only
- **Onboarding** (`/onboarding`) - 3-step flow with progress indicator

### Main Application
- **Dashboard** (`/dashboard`) - Hero screen with Today's Task
  - Minimal sidebar navigation
  - Large task card (visual focal point)
  - AI mentor message section
  - Quick stats overview
  
- **Task Execution** (`/task/:id`) - Distraction-free focus mode
  - Two-column layout (Resource | Submission)
  - Clear learning resource section
  - Simple submission area with text + image upload
  
- **Feedback** (`/feedback/:id`) - Mentor-style performance review
  - Score displayed prominently
  - Detailed strengths and improvements
  - Clear next steps
  - Encouraging, honest tone
  
- **Progress** (`/progress`) - Notion-style structured dashboard
  - Key metrics (Streak, Tasks, Score, Consistency)
  - Performance over time visualization
  - Strengths and improvement areas
  
- **Weekly Summary** (`/weekly-summary`) - Performance report
  - Weekly stats overview
  - What went well / What to improve
  - Top performing topics
  - Focus for next week

## Component Architecture

### Shared Components (from ui/)
- Button, Card, Input, Textarea, Label
- Progress, RadioGroup
- All styled for dark theme with Indigo accents

### Page Components
- Each screen is a self-contained component
- Mock data demonstrates functionality
- Navigation via React Router

## UX Features

### Motivation Without Gamification
- Streak tracking (simple flame icon)
- Progress bars (clean, minimal)
- Scores (0-10, honest assessment)
- No badges, no points, no leaderboards

### AI Mentor Personality
- Speaks like a mentor, not a tutor
- Concise, focused responses
- Honest feedback with encouragement
- Emphasizes consistency over intensity

### Daily Execution Flow
1. User logs in → Dashboard
2. Sees Today's Task immediately
3. Clicks "Start Task"
4. Completes work in focus mode
5. Submits → Receives feedback
6. Returns tomorrow for next task

## Key Screens Purpose

### Dashboard
**Goal**: User instantly knows what to do today
- Large "Today's Task" card (impossible to miss)
- AI mentor provides context and encouragement
- Side navigation for Progress/Weekly views

### Task Execution
**Goal**: Remove all distractions, focus on learning
- Udemy-like clarity with resource on left
- Submission area on right
- No clutter, no unnecessary options

### Feedback
**Goal**: Honest assessment + clear improvement path
- Score first (what they want to know)
- Strengths (what worked)
- Improvements (what to focus on)
- One clear action for tomorrow

### Progress
**Goal**: Show consistency and growth patterns
- Streak (accountability)
- Task completion (momentum)
- Score trends (improvement)
- Insights (actionable feedback)

### Weekly Summary
**Goal**: Reflection and planning
- Weekly performance report
- Honest highlights and challenges
- Focus for next week
- Option to export/share

## Design Inspiration Realized

### ChatGPT Influence
- Clean conversational interface in mentor message
- AI feels intelligent and helpful
- Clear user/AI separation

### Notion Influence
- Structured card-based layouts
- Calm, organized workspace
- Strong visual hierarchy
- Generous whitespace

### Udemy Influence
- Clear "what to do next" on every screen
- Strong learning flow
- Visible progress through topics
- Resource + task instruction clarity

## Technical Stack
- React 18.3
- React Router 7 (navigation)
- Tailwind CSS 4 (styling)
- Radix UI (accessible components)
- Lucide React (minimal icons)

## Future Enhancements (Not Implemented)
- Real authentication with backend
- Actual AI responses (OpenAI integration)
- Database for user progress
- Video/resource embedding
- Code editor for programming tasks
- Calendar view of tasks
- Mobile app version
- Export functionality for summaries
