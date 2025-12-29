import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../ui/button';
import { Card } from '../ui/card';
import { Badge } from '../ui/badge';
import {
  Target,
  TrendingUp,
  Calendar,
  MessageSquare,
  ChevronRight,
  Flame,
  Loader2,
  Plus,
  Menu,
  X
} from 'lucide-react';
import { useState, useEffect } from 'react';
import { api } from '../../../lib/api';

export function Dashboard() {
  const navigate = useNavigate();
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [chatMessage, setChatMessage] = useState('');
  const [chatHistory, setChatHistory] = useState<{ role: string, content: string }[]>([
    { role: 'assistant', content: "I'm Zuno. Need help with your tasks or have a doubt?" }
  ]);
  const [isTyping, setIsTyping] = useState(false);

  const [dailyTasks, setDailyTasks] = useState<any[]>([]);
  const [progress, setProgress] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  async function fetchData() {
    try {
      const [taskData, progressData] = await Promise.all([
        api.get('/daily-plan'),
        api.get('/progress')
      ]);
      setDailyTasks(Array.isArray(taskData) ? taskData : [taskData]);
      setProgress(progressData);
    } catch (error: any) {
      console.error("Failed to fetch dashboard data", error);
      if (error.message?.includes("no goals set") || error.status === 400) {
      } else {
        alert("Error loading dashboard. Please check your connection.");
      }
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchData();
  }, []);

  const handleStartTask = (taskId: number) => {
    navigate(`/task/${taskId}`);
  };

  const handleSendMessage = async () => {
    if (!chatMessage.trim() || isTyping) return;

    const userMsg = chatMessage;
    setChatHistory(prev => [...prev, { role: 'user', content: userMsg }]);
    setChatMessage('');
    setIsTyping(true);

    try {
      const res = await api.post('/chat', {
        message: userMsg,
        goal_id: dailyTasks[0]?.goal_id,
        task_id: dailyTasks[0]?.id // Send context of first task
      });
      setChatHistory(prev => [...prev, { role: 'assistant', content: res.response }]);

      // If AI updated the database, refresh the UI
      if (res.action_taken || res.task_updated) {
        fetchData();
      }
    } catch (err) {
      console.error("Chat failed", err);
      setChatHistory(prev => [...prev, { role: 'assistant', content: "Sorry, I'm having trouble connecting right now. Let's focus on your tasks." }]);
    } finally {
      setIsTyping(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#1a1a1e] flex items-center justify-center text-white">
        <div className="text-center">
          <Loader2 className="w-10 h-10 animate-spin text-indigo-500 mx-auto mb-4" />
          <p className="text-xl">Loading your tailored plans...</p>
        </div>
      </div>
    );
  }

  // Fallback if no tasks yet (e.g. need onboarding)
  if ((!dailyTasks || dailyTasks.length === 0)) {
    return (
      <div className="min-h-screen bg-[#1a1a1e] flex flex-col items-center justify-center text-white p-4 text-center">
        <Target className="w-16 h-16 text-gray-600 mb-6" />
        <h2 className="text-3xl font-medium mb-4">No Learning Paths Yet</h2>
        <p className="mb-8 text-gray-400 max-w-md">
          You haven't set up your learning goals yet, or we're still preparing your initial tasks.
        </p>
        <Button onClick={() => navigate('/onboarding')} className="bg-indigo-600 hover:bg-indigo-700 px-8 h-12 text-lg">
          Setup your Goals
        </Button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#1a1a1e]">
      <div className="flex h-screen overflow-hidden">
        {/* Mobile Header with Hamburger */}
        <div className="md:hidden fixed top-0 left-0 right-0 bg-[#25252a] border-b border-[#35353a] z-50 px-4 py-3 flex items-center justify-between">
          <span className="text-xl font-bold bg-gradient-to-r from-indigo-500 to-purple-500 bg-clip-text text-transparent">Zuno</span>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="text-white p-2"
          >
            {isSidebarOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </Button>
        </div>

        {/* Sidebar Overlay for Mobile */}
        {isSidebarOpen && (
          <div
            className="md:hidden fixed inset-0 bg-black/50 z-40"
            onClick={() => setIsSidebarOpen(false)}
          />
        )}

        {/* Sidebar */}
        <aside className={`
          fixed md:static inset-y-0 left-0 z-40
          w-64 bg-[#25252a] border-r border-[#35353a] flex flex-col flex-shrink-0
          transform transition-transform duration-300 ease-in-out
          ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
        `}>
          <div className="p-6 border-b border-[#35353a]">
            <span className="text-2xl font-bold bg-gradient-to-r from-indigo-500 to-purple-500 bg-clip-text text-transparent">Zuno</span>
          </div>

          <nav className="flex-1 p-4 space-y-2">
            <Link
              to="/dashboard"
              onClick={() => setIsSidebarOpen(false)}
              className="flex items-center gap-3 px-4 py-3 text-white bg-[#35353a] rounded-lg"
            >
              <Target className="w-5 h-5" />
              <span>Today</span>
            </Link>
            <Link
              to="/progress"
              onClick={() => setIsSidebarOpen(false)}
              className="flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-[#35353a] rounded-lg transition-colors"
            >
              <TrendingUp className="w-5 h-5" />
              <span>Progress</span>
            </Link>
            <Link
              to="/weekly-summary"
              onClick={() => setIsSidebarOpen(false)}
              className="flex items-center gap-3 px-4 py-3 text-gray-400 hover:text-white hover:bg-[#35353a] rounded-lg transition-colors"
            >
              <Calendar className="w-5 h-5" />
              <span>Weekly Summary</span>
            </Link>

            <div className="pt-4 mt-4 border-t border-[#35353a]">
              <Link
                to="/onboarding?force=true"
                onClick={() => setIsSidebarOpen(false)}
                className="w-full bg-indigo-600 hover:bg-indigo-700 text-white flex items-center justify-center gap-2 h-11 rounded-lg transition-colors no-underline"
              >
                <Plus className="w-4 h-4" />
                <span>Learn New Topic</span>
              </Link>
            </div>
          </nav>

          <div className="p-4 border-t border-[#35353a]">
            <div className="bg-[#1a1a1e] rounded-lg p-4 space-y-2 mb-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-400">Current Streak</span>
                <Flame className="w-5 h-5 text-orange-500" />
              </div>
              <p className="text-3xl font-medium text-white">{progress?.current_streak || 0} days</p>
            </div>
            <a
              href="https://forms.gle/gKkPCVY2pKWKDFZP8"
              target="_blank"
              rel="noopener noreferrer"
              className="w-full mb-2 border border-[#35353a] text-gray-400 hover:bg-indigo-900/20 hover:text-indigo-400 hover:border-indigo-700 flex items-center justify-center gap-2 h-11 rounded-lg transition-colors no-underline"
            >
              <MessageSquare className="w-4 h-4" />
              <span>Share Feedback</span>
            </a>
            <Button
              onClick={() => {
                api.logout();
                navigate('/login');
              }}
              variant="outline"
              className="w-full border-[#35353a] text-gray-400 hover:bg-red-900/20 hover:text-red-400 hover:border-red-700"
            >
              Logout
            </Button>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-auto relative pt-16 md:pt-0">
          <div className="max-w-4xl mx-auto p-4 md:p-8 space-y-6 md:space-y-8 pb-32">
            {/* Header */}
            <div className="space-y-2">
              <h2 className="text-2xl md:text-3xl font-medium text-white">
                {new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'short', day: 'numeric' })}
              </h2>
              <p className="text-gray-400 text-sm md:text-base">Show up today. That's all that matters.</p>
            </div>

            {/* Today's Tasks Cards */}
            <div className="grid grid-cols-1 gap-4 md:gap-6">
              {dailyTasks.map((task) => (
                <Card key={task.id} className="bg-gradient-to-br from-indigo-900/40 to-purple-900/40 border-indigo-700/50 p-5 md:p-8 space-y-4 md:space-y-6">
                  <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2 flex-wrap">
                        <p className="text-xs md:text-sm text-indigo-300 uppercase tracking-wider">{task.subject || "Skill Goal"}</p>
                        {task.level && (
                          <Badge variant="secondary" className="bg-indigo-500/20 text-indigo-200 hover:bg-indigo-500/30 border-0 text-xs">
                            {task.level}
                          </Badge>
                        )}
                      </div>
                      <h3 className="text-xl md:text-2xl font-medium text-white">{task.topic}</h3>
                    </div>
                    <div className="bg-indigo-600/30 px-3 md:px-4 py-2 rounded-lg self-start">
                      <p className="text-xs md:text-sm text-indigo-200">~45 min</p>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <p className="text-xs md:text-sm text-gray-400 mb-2">Resource</p>
                      <a href={task.resource_link} target="_blank" rel="noreferrer" className="text-sm md:text-lg text-indigo-400 hover:underline truncate block">
                        {task.resource_link}
                      </a>
                    </div>

                    <div>
                      <p className="text-xs md:text-sm text-gray-400 mb-2">What to do</p>
                      <p className="text-sm md:text-base text-white whitespace-pre-wrap">{task.task_description}</p>
                    </div>
                  </div>

                  <Button
                    onClick={() => handleStartTask(task.id)}
                    disabled={task.is_completed}
                    className={`w-full h-11 md:h-12 text-base md:text-lg group ${task.is_completed ? 'bg-green-600 hover:bg-green-700' : 'bg-indigo-600 hover:bg-indigo-700'} text-white`}
                  >
                    {task.is_completed ? 'Completed' : 'Start Task'}
                    {!task.is_completed && <ChevronRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />}
                  </Button>
                </Card>
              ))}
            </div>

            {/* AI Mentor Message (Only shown if chat is closed) */}
            {!isChatOpen && (
              <Card className="bg-[#25252a] border-[#35353a] p-4 md:p-6 space-y-4">
                <div className="flex items-start gap-3 md:gap-4">
                  <div className="w-8 h-8 md:w-10 md:h-10 rounded-full bg-indigo-600 flex items-center justify-center flex-shrink-0">
                    <MessageSquare className="w-4 h-4 md:w-5 md:h-5 text-white" />
                  </div>
                  <div className="flex-1 space-y-3">
                    <div>
                      <p className="text-xs md:text-sm text-gray-400 mb-1">Zuno says</p>
                      <p className="text-sm md:text-base text-white leading-relaxed">
                        {dailyTasks.every(t => t.is_completed)
                          ? "Absolute legend! You finished everything for today."
                          : "You've got a busy day ahead. Click the chat icon below if you have any doubts!"}
                      </p>
                    </div>
                  </div>
                </div>
              </Card>
            )}

            {/* Quick Stats */}
            <div className="grid grid-cols-3 gap-2 md:gap-4">
              <Card className="bg-[#25252a] border-[#35353a] p-3 md:p-5">
                <p className="text-xs md:text-sm text-gray-400 mb-1 md:mb-2">Tasks Completed</p>
                <p className="text-lg md:text-2xl font-medium text-white">{progress?.completed_tasks || 0} / {progress?.total_tasks || 0}</p>
              </Card>
              <Card className="bg-[#25252a] border-[#35353a] p-3 md:p-5">
                <p className="text-xs md:text-sm text-gray-400 mb-1 md:mb-2">Avg Score</p>
                <p className="text-lg md:text-2xl font-medium text-white">{progress?.average_score || 0}</p>
              </Card>
              <Card className="bg-[#25252a] border-[#35353a] p-3 md:p-5">
                <p className="text-xs md:text-sm text-gray-400 mb-1 md:mb-2">Consistency</p>
                <p className="text-lg md:text-2xl font-medium text-white">{Math.round(progress?.completion_percentage || 0)}%</p>
              </Card>
            </div>
          </div>

          {/* Chat Interface Fixed at Bottom */}
          <div className={`fixed bottom-0 right-0 left-0 md:left-64 transition-all duration-300 z-50 ${isChatOpen ? 'h-[400px]' : 'h-16'}`}>
            <div className="max-w-4xl mx-auto px-4 md:px-8 h-full">
              <div className="bg-[#25252a] border-t border-x border-[#35353a] rounded-t-2xl h-full flex flex-col shadow-2xl overflow-hidden">
                {/* Chat Header */}
                <div className="p-3 md:p-4 flex items-center justify-between border-b border-[#35353a] bg-[#2a2a2f] cursor-pointer" onClick={() => setIsChatOpen(!isChatOpen)}>
                  <div className="flex items-center gap-2 md:gap-3">
                    <div className="w-7 h-7 md:w-8 md:h-8 rounded-full bg-indigo-600 flex items-center justify-center">
                      <MessageSquare className="w-3.5 h-3.5 md:w-4 md:h-4 text-white" />
                    </div>
                    <div>
                      <h4 className="text-white font-medium text-xs md:text-sm">Chat with Zuno</h4>
                      <p className="text-xs text-indigo-400 flex items-center gap-1">
                        <span className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
                        AI Mentor Active
                      </p>
                    </div>
                  </div>
                  <Button variant="ghost" size="sm" className="text-gray-400 text-xs md:text-sm">
                    {isChatOpen ? 'Collapse' : 'Ask a doubt...'}
                  </Button>
                </div>

                {/* Chat Messages */}
                {isChatOpen && (
                  <>
                    <div className="flex-1 overflow-y-auto p-3 md:p-4 space-y-3 md:space-y-4 bg-[#1a1a1e]">
                      {chatHistory.map((msg, i) => (
                        <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                          <div className={`max-w-[85%] md:max-w-[80%] p-2.5 md:p-3 rounded-2xl text-xs md:text-sm ${msg.role === 'user'
                            ? 'bg-indigo-600 text-white rounded-tr-none'
                            : 'bg-[#35353a] text-gray-200 rounded-tl-none'
                            }`}>
                            {msg.content}
                          </div>
                        </div>
                      ))}
                      {isTyping && (
                        <div className="flex justify-start">
                          <div className="bg-[#35353a] p-2.5 md:p-3 rounded-2xl rounded-tl-none flex gap-1">
                            <span className="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce"></span>
                            <span className="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce delay-75"></span>
                            <span className="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce delay-150"></span>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Chat Input */}
                    <div className="p-3 md:p-4 bg-[#25252a] border-t border-[#35353a]">
                      <div className="flex gap-2">
                        <input
                          type="text"
                          value={chatMessage}
                          onChange={(e) => setChatMessage(e.target.value)}
                          onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                          placeholder="Ask anything about your tasks..."
                          className="flex-1 bg-[#1a1a1e] border border-[#35353a] rounded-xl px-3 md:px-4 py-2 text-white focus:outline-none focus:border-indigo-500 text-xs md:text-sm"
                        />
                        <Button
                          onClick={handleSendMessage}
                          disabled={!chatMessage.trim() || isTyping}
                          className="bg-indigo-600 hover:bg-indigo-700 text-white h-9 w-9 md:h-10 md:w-10 p-0 rounded-xl"
                        >
                          <ChevronRight className="w-4 h-4 md:w-5 md:h-5" />
                        </Button>
                      </div>
                    </div>
                  </>
                )}
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
