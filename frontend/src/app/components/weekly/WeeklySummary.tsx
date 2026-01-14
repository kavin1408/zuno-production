import { Link } from 'react-router-dom';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { ArrowLeft, Target, Loader2 } from 'lucide-react';
import { useState, useEffect } from 'react';
import { api } from '../../../lib/api';

export function WeeklySummary() {
  const [summary, setSummary] = useState<any>(null);
  const [progress, setProgress] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      try {
        const [summaryData, progressData] = await Promise.all([
          api.get('/weekly-summary'),
          api.get('/progress')
        ]);
        setSummary(summaryData);
        setProgress(progressData);
      } catch (error) {
        console.error("Failed to fetch weekly summary", error);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#1a1a1e] flex items-center justify-center text-white">
        <Loader2 className="w-8 h-8 animate-spin" />
        <span className="ml-2">Generating summary...</span>
      </div>
    );
  }

  if (!summary || !progress) {
    return (
      <div className="min-h-screen bg-[#1a1a1e] flex items-center justify-center text-white">
        <p>No summary data available</p>
      </div>
    );
  }

  const currentWeek = `${new Date(Date.now() - 6 * 24 * 60 * 60 * 1000).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} - ${new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}`;

  return (
    <div className="min-h-screen bg-[#1a1a1e]">
      {/* Header */}
      <header className="bg-[#25252a] border-b border-[#35353a] sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 md:px-6 py-3 md:py-4 flex items-center justify-between">
          <Link
            to="/dashboard"
            className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back to Dashboard</span>
          </Link>
        </div>
      </header>

      <div className="max-w-4xl mx-auto p-4 md:p-6 space-y-6 md:space-y-8">
        {/* Header */}
        <div className="text-center space-y-2 md:space-y-3">
          <h1 className="text-2xl md:text-4xl font-medium text-white">Weekly Summary</h1>
          <p className="text-base md:text-xl text-gray-400">{currentWeek}</p>
        </div>

        {/* Overview Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4">
          <Card className="bg-[#25252a] border-[#35353a] p-4 md:p-5 text-center space-y-1 md:space-y-2">
            <p className="text-xs md:text-sm text-gray-400">Tasks Done</p>
            <p className="text-2xl md:text-3xl font-medium text-white">{progress.completed_tasks}/{progress.total_tasks}</p>
          </Card>
          <Card className="bg-[#25252a] border-[#35353a] p-4 md:p-5 text-center space-y-1 md:space-y-2">
            <p className="text-xs md:text-sm text-gray-400">Avg Score</p>
            <p className="text-2xl md:text-3xl font-medium text-white">{progress.average_score}</p>
          </Card>
          <Card className="bg-[#25252a] border-[#35353a] p-4 md:p-5 text-center space-y-1 md:space-y-2">
            <p className="text-xs md:text-sm text-gray-400">Completion</p>
            <p className="text-2xl md:text-3xl font-medium text-white">{Math.round(progress.completion_percentage)}%</p>
          </Card>
          <Card className="bg-[#25252a] border-[#35353a] p-4 md:p-5 text-center space-y-1 md:space-y-2">
            <p className="text-xs md:text-sm text-gray-400">Streak</p>
            <p className="text-2xl md:text-3xl font-medium text-white">{progress.current_streak}</p>
            <p className="text-xs text-gray-500">days</p>
          </Card>
        </div>

        {/* Mentor's Summary */}
        <Card className="bg-[#25252a] border-[#35353a] p-4 md:p-6 space-y-3 md:space-y-4">
          <div className="flex items-center gap-2">
            <Target className="w-4 h-4 md:w-5 md:h-5 text-indigo-500" />
            <h3 className="text-base md:text-lg font-medium text-white">Zuno's Weekly Review</h3>
          </div>
          <p className="text-sm md:text-base text-gray-300 leading-relaxed whitespace-pre-wrap">
            {summary.mentor_summary_text || "Keep up the great work! Your consistency is building real skill."}
          </p>
        </Card>

        {/* CTA */}
        <div className="flex justify-center pt-4">
          <Link to="/dashboard">
            <Button className="bg-indigo-600 hover:bg-indigo-700 text-white px-8">
              Back to Dashboard
            </Button>
          </Link>
        </div>

        {/* Footer Quote */}
        <div className="text-center pt-6 pb-12">
          <p className="text-gray-500 italic">
            "Excellence is not an act, but a habit."
          </p>
        </div>
      </div>
    </div>
  );
}
