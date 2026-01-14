import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../../../lib/api';
import { Button } from '../ui/button';
import { Card } from '../ui/card';
import { Input } from '../ui/input';
import { Badge } from '../ui/badge';
import { Progress } from '../ui/progress';
import {
  CheckCircle2,
  Clock,
  Layout,
  MessageSquare,
  MoreVertical,
  Settings as SettingsIcon,
  Trophy,
  Search,
  BookOpen,
  ArrowRight,
  Zap,
  Star,
  ChevronRight,
  Map,
  X,
  Send,
  Loader2,
  LogOut,
  Calendar,
  Menu
} from 'lucide-react';
import { StatsCard } from './StatsCard';
import { RoadmapView } from '../roadmap/RoadmapView';

export function Dashboard() {
  const navigate = useNavigate();
  const [dailyTasks, setDailyTasks] = useState<any[]>([]);
  const [roadmap, setRoadmap] = useState<any>(null);
  const [stats, setStats] = useState<any>({ total_tasks: 0, completed_tasks: 0, completion_percentage: 0, average_score: 0, current_streak: 0 });
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'today' | 'roadmap'>('today');

  // Chat State
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [chatMessage, setChatMessage] = useState('');
  const [chatHistory, setChatHistory] = useState<{ role: string, content: string }[]>([
    { role: 'assistant', content: "Hi! I'm Zuno. I can help you with your roadmap or explain specific topics." }
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const userName = user?.email?.split('@')[0] || 'Learner';

  useEffect(() => {
    const handleOpenChat = (e: any) => {
      setIsChatOpen(true);
      if (e.detail?.query) {
        handleSendMessage(e.detail.query);
      }
    };
    window.addEventListener('open-zuno-chat', handleOpenChat);
    return () => window.removeEventListener('open-zuno-chat', handleOpenChat);
  }, [dailyTasks]);

  async function fetchData() {
    try {
      const [taskData, roadmapData, statsData, userData] = await Promise.all([
        api.get('/daily-plan'),
        api.get('/roadmap'),
        api.get('/progress'),
        api.get('/user/profile')
      ]);
      setDailyTasks(Array.isArray(taskData) ? taskData : [taskData]);
      setRoadmap(roadmapData);
      setStats(statsData);
      setUser(userData);
    } catch (error: any) {
      console.error("Failed to fetch dashboard data", error);
      if (error.status === 400 || (error.message && error.message.includes("no goals"))) {
        navigate('/onboarding');
      }
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    fetchData();
  }, [navigate]);

  const handleStartTask = (taskId: number) => {
    navigate(`/task/${taskId}`);
  };

  const handleLogout = async () => {
    await api.logout();
    navigate('/login');
  };

  const calculateOverallProgress = () => {
    if (!roadmap || !roadmap.phases) return 0;
    let total = 0;
    let completed = 0;
    roadmap.phases.forEach((p: any) => {
      p.modules.forEach((m: any) => {
        m.tasks.forEach((t: any) => {
          total++;
          if (t.status === 'completed') completed++;
        });
      });
    });
    return total > 0 ? Math.round((completed / total) * 100) : 0;
  };

  const handleSendMessage = async (overrideMessage?: string) => {
    const messageToSend = overrideMessage || chatMessage;
    if (!messageToSend.trim() || isTyping) return;

    setChatHistory(prev => [...prev, { role: 'user', content: messageToSend }]);
    if (!overrideMessage) setChatMessage('');
    setIsTyping(true);

    try {
      const res = await api.post('/chat', {
        message: messageToSend,
        task_id: dailyTasks[0]?.id
      });
      setChatHistory(prev => [...prev, { role: 'assistant', content: res.response }]);
    } catch (err) {
      setChatHistory(prev => [...prev, { role: 'assistant', content: "Sorry, I'm having trouble connecting right now." }]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleSearchSubmit = () => {
    if (!searchQuery.trim()) return;
    if (activeTab !== 'roadmap') {
      setActiveTab('roadmap');
    }
    // We'll let RoadmapView handle the filtering based on the prop,
    // but if the user presses Enter, we also offer to ask AI.
    if (searchQuery.length > 3) {
      // Just keep the filter, maybe show a "Ask Zuno" button in the roadmap if 0 results
    }
  };

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center bg-[#131316] text-white">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="h-12 w-12 animate-spin text-indigo-600" />
          <p className="text-gray-400">Loading your workspace...</p>
        </div>
      </div>
    );
  }

  const mainTask = dailyTasks[0];
  const roadmapProgress = calculateOverallProgress();

  return (
    <div className="flex h-screen bg-[#131316] text-white overflow-hidden relative">
      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 z-50 border-r border-[#25252a] flex flex-col bg-[#1a1a1e] transition-transform duration-300 transform
        lg:static lg:translate-x-0
        ${sidebarOpen ? 'translate-x-0 w-64' : '-translate-x-full lg:translate-x-0 w-20 lg:w-64'}
      `}>
        <div className="p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3 text-white">
              <div className="h-10 w-10 bg-indigo-600 rounded-xl flex items-center justify-center font-bold text-xl uppercase tracking-wider shrink-0">Z</div>
              <span className={`font-bold text-xl tracking-widest ${sidebarOpen ? 'block' : 'hidden lg:block'}`}>ZUNO</span>
            </div>
            <Button
              variant="ghost"
              size="icon"
              className="lg:hidden text-gray-400 hover:text-white"
              onClick={() => setSidebarOpen(false)}
            >
              <X className="h-6 w-6" />
            </Button>
          </div>
        </div>

        <nav className="flex-1 px-4 space-y-2 mt-4">
          <Button
            variant="ghost"
            className={`w-full justify-start gap-4 transition-all ${activeTab === 'today' ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/20' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}
            onClick={() => setActiveTab('today')}
          >
            <Layout className="h-5 w-5 shrink-0" />
            <span className={`${sidebarOpen ? 'block' : 'hidden lg:block'} font-medium`}>Overview</span>
          </Button>
          <Button
            variant="ghost"
            className={`w-full justify-start gap-4 transition-all ${activeTab === 'roadmap' ? 'bg-indigo-600/10 text-indigo-400 border border-indigo-500/20' : 'text-gray-400 hover:text-white hover:bg-white/5'}`}
            onClick={() => setActiveTab('roadmap')}
          >
            <Map className="h-5 w-5 shrink-0" />
            <span className={`${sidebarOpen ? 'block' : 'hidden lg:block'} font-medium`}>Roadmap</span>
          </Button>
          <Button
            variant="ghost"
            className={`w-full justify-start gap-4 transition-all text-gray-400 hover:text-white hover:bg-white/5`}
            onClick={() => navigate('/achievements')}
          >
            <Trophy className="h-5 w-5 shrink-0" />
            <span className={`${sidebarOpen ? 'block' : 'hidden lg:block'}`}>Achievements</span>
          </Button>
          <Button
            variant="ghost"
            className={`w-full justify-start gap-4 transition-all text-gray-400 hover:text-white hover:bg-white/5`}
            onClick={() => navigate('/schedule')}
          >
            <Calendar className="h-5 w-5 shrink-0" />
            <span className={`${sidebarOpen ? 'block' : 'hidden lg:block'}`}>Schedule</span>
          </Button>
        </nav>

        <div className="p-4 border-t border-[#25252a] mt-auto space-y-2">
          <Button
            variant="ghost"
            className="w-full justify-start gap-4 text-gray-400 hover:text-white"
            onClick={() => navigate('/settings')}
          >
            <SettingsIcon className="h-5 w-5 shrink-0" />
            <span className={`${sidebarOpen ? 'block' : 'hidden lg:block'} font-medium`}>Settings</span>
          </Button>

          <div className="flex items-center gap-3 p-3 rounded-xl bg-gradient-to-r from-indigo-600/10 to-transparent group cursor-pointer" onClick={() => navigate('/settings')}>
            <div className="h-10 w-10 rounded-full bg-indigo-600 flex items-center justify-center font-bold text-lg uppercase shrink-0 text-white">
              {userName?.[0]}
            </div>
            <div className={`${sidebarOpen ? 'block' : 'hidden lg:block'} overflow-hidden`}>
              <p className="text-sm font-bold truncate text-white">{userName}</p>
              <p className="text-xs text-indigo-400 font-medium">Pro Student</p>
            </div>
          </div>

          <Button
            variant="ghost"
            className="w-full justify-start gap-4 text-gray-400 hover:text-red-400 hover:bg-red-400/5"
            onClick={handleLogout}
          >
            <LogOut className="h-5 w-5 shrink-0" />
            <span className={`${sidebarOpen ? 'block' : 'hidden lg:block'} font-medium`}>Logout</span>
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto bg-gradient-to-b from-[#1a1a1e] to-[#131316] w-full relative">
        {/* Mobile Navbar */}
        <div className="lg:hidden flex items-center justify-between p-4 border-b border-[#25252a] sticky top-0 bg-[#1a1a1e]/80 backdrop-blur-md z-30">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 bg-indigo-600 rounded-lg flex items-center justify-center font-bold text-sm uppercase text-white">Z</div>
            <span className="font-bold text-lg tracking-widest text-white">ZUNO</span>
          </div>
          <Button variant="ghost" size="icon" onClick={() => setSidebarOpen(true)}>
            <Menu className="h-6 w-6 text-gray-400" />
          </Button>
        </div>

        <div className="max-w-6xl mx-auto p-4 md:p-8">
          {/* Header */}
          <div className="flex items-center justify-between mb-10">
            <div>
              <h1 className="text-3xl md:text-4xl font-bold mb-2">Welcome back, {userName}</h1>
              <p className="text-gray-400 flex items-center gap-2 text-sm md:text-base">
                <Zap className="h-4 w-4 text-yellow-500 fill-yellow-500" />
                Your <span className="text-white font-medium">streak is active</span>. You're set for success today.
              </p>
            </div>
            <div className="hidden md:block w-72">
              <div className="relative group">
                <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500 group-focus-within:text-indigo-400 transition-colors" />
                <Input
                  placeholder="Search topics or ask Zuno..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && handleSearchSubmit()}
                  className="pl-10 bg-[#25252a] border-[#35353a] text-white placeholder:text-gray-500 focus:border-indigo-500/50 focus:ring-indigo-500/10 h-10 rounded-xl transition-all"
                />
              </div>
            </div>
          </div>

          {activeTab === 'today' ? (
            <div className="flex flex-col lg:grid lg:grid-cols-3 gap-8">
              <div className="flex flex-col lg:col-span-2 space-y-8 order-2 lg:order-1">
                {/* Roadmap Progress highlights */}
                <Card className="bg-[#25252a] p-6 border-[#35353a] relative overflow-hidden">
                  <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-600/5 rounded-full -mr-16 -mt-16" />
                  <div className="relative z-10">
                    <div className="flex items-center gap-2 mb-4 font-bold text-xs">
                      <Badge className="bg-indigo-600/20 text-indigo-400 hover:bg-indigo-600/30 border-none px-2 py-0.5">LEARNING PATH</Badge>
                      <span className="text-gray-600">•</span>
                      <span className="text-gray-400 capitalize">{roadmap?.title || "Your Goals"}</span>
                    </div>
                    <h2 className="text-2xl font-bold mb-6 text-white">{roadmapProgress}% Mastered</h2>
                    <div className="space-y-2">
                      <Progress value={roadmapProgress} className="h-2 bg-[#1a1a1e]" />
                      <div className="flex justify-between text-[10px] text-gray-500 font-bold uppercase tracking-widest">
                        <span>Beginner</span>
                        <span>Intermediate</span>
                        <span>Complete</span>
                      </div>
                    </div>
                  </div>
                </Card>

                {/* Today's Focus Card */}
                <div className="relative group">
                  <div className="absolute -inset-0.5 bg-gradient-to-r from-indigo-500 to-purple-600 rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-1000"></div>
                  <Card className="relative bg-[#25252a] p-6 md:p-8 border-[#35353a] rounded-2xl flex flex-col md:flex-row gap-8">
                    {mainTask ? (
                      <>
                        <div className="flex-1 space-y-6">
                          <div className="flex items-center gap-3">
                            <div className="p-3 bg-indigo-600/20 rounded-xl text-indigo-400">
                              <BookOpen className="h-6 w-6" />
                            </div>
                            <div>
                              <p className="text-[10px] text-gray-500 uppercase font-black tracking-[0.2em]">Today's Task</p>
                              <h3 className="text-xl md:text-2xl font-bold mt-1 text-white">{mainTask.topic}</h3>
                            </div>
                          </div>
                          <p className="text-gray-400 text-sm md:text-lg leading-relaxed">{mainTask.task_description}</p>
                          <div className="flex flex-wrap gap-4">
                            <Badge variant="outline" className="border-[#35353a] text-gray-400 py-1.5 px-3">
                              <Clock className="w-3.5 h-3.5 mr-1.5" /> 45 Mins
                            </Badge>
                            <Badge variant="outline" className="border-[#35353a] text-gray-400 py-1.5 px-3">
                              <Star className="w-3.5 h-3.5 mr-1.5 text-yellow-500" /> {mainTask.level || "Guided"}
                            </Badge>
                          </div>
                        </div>
                        <div className="flex flex-col justify-center items-center gap-6 md:min-w-[180px]">
                          {mainTask.is_completed ? (
                            <div className="text-center space-y-4">
                              <div className="h-20 w-20 rounded-full bg-green-500/20 text-green-500 flex items-center justify-center mx-auto">
                                <CheckCircle2 className="w-10 h-10" />
                              </div>
                              <p className="font-bold text-green-400 uppercase tracking-widest text-xs">Mission Complete</p>
                              <Button variant="outline" disabled className="w-full border-green-500/50 text-green-500 opacity-50 font-bold">Done</Button>
                            </div>
                          ) : (
                            <Button
                              onClick={() => handleStartTask(mainTask.id)}
                              className="w-full h-14 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl shadow-lg shadow-indigo-600/30 text-lg font-bold group"
                            >
                              Get Started
                              <ArrowRight className="h-5 w-5 ml-2 transition-transform group-hover:translate-x-1" />
                            </Button>
                          )}
                        </div>
                      </>
                    ) : (
                      <div className="w-full py-12 text-center">
                        <h3 className="text-xl font-bold text-gray-400 italic text-white">No tasks active for today.</h3>
                      </div>
                    )}
                  </Card>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <Card className="bg-[#25252a] p-6 border-[#35353a] hover:bg-[#2a2a2f] transition-all cursor-pointer group" onClick={() => setIsChatOpen(true)}>
                    <div className="p-3 bg-purple-600/10 text-purple-400 w-fit rounded-xl mb-4 group-hover:bg-purple-600/20">
                      <MessageSquare className="h-5 w-5" />
                    </div>
                    <h4 className="font-bold text-lg text-white mb-1">Study Companion</h4>
                    <p className="text-sm text-gray-500">Ask Zuno anything about the lesson</p>
                  </Card>
                  <Card className="bg-[#25252a] p-6 border-[#35353a] opacity-50 cursor-not-allowed">
                    <div className="p-3 bg-orange-600/10 text-orange-400 w-fit rounded-xl mb-4">
                      <Zap className="h-5 w-5" />
                    </div>
                    <h4 className="font-bold text-lg text-white mb-1">Quick Challenge</h4>
                    <p className="text-sm text-gray-500">Test your recall - Coming soon</p>
                  </Card>
                </div>
              </div>

              <div className="flex flex-col space-y-8 order-1 lg:order-2">
                {/* Stats Grid - Moved to top on mobile */}
                <div className="grid grid-cols-2 lg:grid-cols-2 gap-4 md:gap-6">
                  <StatsCard
                    title="Average Score"
                    value={`${stats.average_score}%`}
                    label="Mastery"
                    icon={Star}
                    iconColor="text-yellow-500"
                    iconBg="bg-yellow-600/10"
                  />
                  <StatsCard
                    title="Current Streak"
                    value={stats.current_streak}
                    label="Days"
                    icon={Zap}
                    iconColor="text-orange-500"
                    iconBg="bg-orange-600/10"
                  />
                </div>

                {/* AI Note */}
                <div className="bg-indigo-950/20 border border-indigo-900/50 rounded-2xl p-6 relative overflow-hidden group">
                  <div className="absolute top-0 right-0 p-2 opacity-10 group-hover:opacity-20 transition-opacity">
                    <Zap className="w-12 h-12" />
                  </div>
                  <p className="text-xs font-black text-indigo-400 uppercase tracking-widest mb-4">Mentor Feedback</p>
                  <p className="text-lg font-medium italic text-indigo-100 leading-relaxed text-white">
                    "Looking at your roadmap, today's topic sets the ground for the entire module. Pay close attention to the examples."
                  </p>
                  <div className="flex items-center gap-2 mt-6">
                    <div className="h-8 w-8 rounded-full bg-indigo-600 flex items-center justify-center text-[10px] font-bold text-white">AI</div>
                    <span className="text-xs font-bold text-indigo-300">Zuno Bot</span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <RoadmapView filter={searchQuery} />
          )}
        </div>
      </main>

      {/* Floating Chat Window */}
      {isChatOpen && (
        <div className="fixed bottom-0 right-0 sm:bottom-6 sm:right-6 w-full sm:w-96 h-full sm:h-[500px] bg-[#1a1a1e] border-t sm:border border-indigo-500/30 rounded-t-2xl sm:rounded-2xl shadow-2xl flex flex-col z-50 overflow-hidden animate-in slide-in-from-bottom-4">
          <div className="p-4 bg-indigo-600 flex items-center justify-between text-white">
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 rounded-full bg-white/20 flex items-center justify-center font-bold text-xs uppercase">Z</div>
              <div>
                <p className="text-sm font-bold">Zuno Mentor</p>
                <p className="text-[10px] opacity-80">Online & Ready to Help</p>
              </div>
            </div>
            <Button variant="ghost" size="sm" onClick={() => setIsChatOpen(false)} className="text-white hover:bg-white/10 p-1 h-fit">
              <X className="w-5 h-5" />
            </Button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-[#1a1a1e]">
            {chatHistory.map((m, i) => (
              <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] p-3 rounded-2xl text-sm ${m.role === 'user' ? 'bg-indigo-600 text-white' : 'bg-[#25252a] text-gray-200 border border-[#35353a]'
                  }`}>
                  {m.content}
                </div>
              </div>
            ))}
            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-[#25252a] p-3 rounded-2xl text-gray-500">
                  <Loader2 className="h-4 w-4 animate-spin text-indigo-600" />
                </div>
              </div>
            )}
          </div>

          <div className="p-4 border-t border-[#25252a] bg-[#1a1a1e] flex gap-2">
            <Input
              placeholder="Type your doubt..."
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
              className="bg-[#25252a] border-[#35353a] text-white h-10"
            />
            <Button size="icon" onClick={() => handleSendMessage()} className="bg-indigo-600 hover:bg-indigo-700 h-10 w-10 shrink-0">
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
