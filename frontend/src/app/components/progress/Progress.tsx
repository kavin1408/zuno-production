import { Link } from 'react-router-dom';
import { Card } from '../ui/card';
import { Progress as ProgressBar } from '../ui/progress';
import { ArrowLeft, Flame, Target, TrendingUp, Calendar, Loader2 } from 'lucide-react';
import { useState, useEffect } from 'react';
import { api } from '../../../lib/api';

export function Progress() {
  const [progress, setProgress] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchProgress() {
      try {
        const data = await api.get('/progress');
        setProgress(data);
      } catch (error) {
        console.error("Failed to fetch progress", error);
      } finally {
        setLoading(false);
      }
    }
    fetchProgress();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#1a1a1e] flex items-center justify-center text-white">
        <Loader2 className="w-8 h-8 animate-spin" />
        <span className="ml-2">Loading progress...</span>
      </div>
    );
  }

  if (!progress) {
    return (
      <div className="min-h-screen bg-[#1a1a1e] flex items-center justify-center text-white">
        <p>No progress data available</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#1a1a1e]">
      {/* Header */}
      <header className="bg-[#25252a] border-b border-[#35353a] sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 md:px-6 py-3 md:py-4">
          <Link
            to="/dashboard"
            className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back to Dashboard</span>
          </Link>
        </div>
      </header>

      <div className="max-w-6xl mx-auto p-4 md:p-6 space-y-6 md:space-y-8">
        {/* Page Header */}
        <div>
          <h1 className="text-2xl md:text-3xl font-medium text-white mb-2">Your Progress</h1>
          <p className="text-sm md:text-base text-gray-400">Track your consistency and growth</p>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4">
          <Card className="bg-[#25252a] border-[#35353a] p-4 md:p-6 space-y-2 md:space-y-3">
            <div className="flex items-center justify-between">
              <p className="text-xs md:text-sm text-gray-400">Current Streak</p>
              <Flame className="w-4 h-4 md:w-5 md:h-5 text-orange-500" />
            </div>
            <p className="text-2xl md:text-3xl font-medium text-white">{progress.current_streak}</p>
            <p className="text-xs text-gray-500">days in a row</p>
          </Card>

          <Card className="bg-[#25252a] border-[#35353a] p-4 md:p-6 space-y-2 md:space-y-3">
            <div className="flex items-center justify-between">
              <p className="text-xs md:text-sm text-gray-400">Tasks Completed</p>
              <Target className="w-4 h-4 md:w-5 md:h-5 text-indigo-500" />
            </div>
            <p className="text-2xl md:text-3xl font-medium text-white">{progress.completed_tasks}</p>
            <ProgressBar
              value={progress.completion_percentage}
              className="h-1.5 bg-[#1a1a1e]"
            />
          </Card>

          <Card className="bg-[#25252a] border-[#35353a] p-4 md:p-6 space-y-2 md:space-y-3">
            <div className="flex items-center justify-between">
              <p className="text-xs md:text-sm text-gray-400">Average Score</p>
              <TrendingUp className="w-4 h-4 md:w-5 md:h-5 text-green-500" />
            </div>
            <p className="text-2xl md:text-3xl font-medium text-white">{progress.average_score}</p>
            <p className="text-xs text-gray-500">out of 100</p>
          </Card>

          <Card className="bg-[#25252a] border-[#35353a] p-4 md:p-6 space-y-2 md:space-y-3">
            <div className="flex items-center justify-between">
              <p className="text-xs md:text-sm text-gray-400">Consistency</p>
              <Calendar className="w-4 h-4 md:w-5 md:h-5 text-blue-500" />
            </div>
            <p className="text-2xl md:text-3xl font-medium text-white">{Math.round(progress.completion_percentage)}%</p>
            <ProgressBar
              value={progress.completion_percentage}
              className="h-1.5 bg-[#1a1a1e]"
            />
          </Card>
        </div>

        {/* Summary Card */}
        <Card className="bg-[#25252a] border-[#35353a] p-4 md:p-6 space-y-3 md:space-y-4">
          <h3 className="text-base md:text-lg font-medium text-white">Summary</h3>
          <div className="grid grid-cols-3 gap-3 md:gap-4">
            <div>
              <p className="text-xs md:text-sm text-gray-400 mb-1">Total Tasks</p>
              <p className="text-lg md:text-2xl font-medium text-white">{progress.total_tasks}</p>
            </div>
            <div>
              <p className="text-xs md:text-sm text-gray-400 mb-1">Completed</p>
              <p className="text-lg md:text-2xl font-medium text-white">{progress.completed_tasks}</p>
            </div>
            <div>
              <p className="text-xs md:text-sm text-gray-400 mb-1">Completion Rate</p>
              <p className="text-lg md:text-2xl font-medium text-white">{Math.round(progress.completion_percentage)}%</p>
            </div>
          </div>
        </Card>

        {/* Motivational Message */}
        <Card className="bg-gradient-to-br from-indigo-900/40 to-purple-900/40 border-indigo-700/50 p-4 md:p-6">
          <p className="text-sm md:text-base text-indigo-100 leading-relaxed">
            {progress.completed_tasks > 0
              ? `You've completed ${progress.completed_tasks} tasks with an average score of ${progress.average_score}. Keep up the great work!`
              : "Start your journey by completing your first task today!"}
          </p>
        </Card>
      </div>
    </div>
  );
}
