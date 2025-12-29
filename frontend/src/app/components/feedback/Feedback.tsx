import { useNavigate, useParams } from 'react-router-dom';
import { Button } from '../ui/button';
import { Card } from '../ui/card';
import { Progress } from '../ui/progress';
import { TrendingUp, ChevronRight, Loader2 } from 'lucide-react';
import { useState, useEffect } from 'react';

export function Feedback() {
  const navigate = useNavigate();
  const { taskId } = useParams();
  const [feedback, setFeedback] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real implementation, we'd fetch the submission feedback
    // For now, we'll simulate it since the submission just happened
    const storedFeedback = sessionStorage.getItem(`feedback_${taskId}`);
    if (storedFeedback) {
      setFeedback(JSON.parse(storedFeedback));
      setLoading(false);
    } else {
      // Fallback if no feedback stored
      setFeedback({
        score: 0,
        ai_feedback: "Submission received. Great job completing the task!"
      });
      setLoading(false);
    }
  }, [taskId]);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#1a1a1e] flex items-center justify-center text-white">
        <Loader2 className="w-8 h-8 animate-spin" />
        <span className="ml-2">Analyzing your work...</span>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#1a1a1e] flex items-center justify-center p-6">
      <div className="w-full max-w-3xl space-y-6">
        {/* Score Card */}
        <Card className="bg-gradient-to-br from-indigo-900/40 to-purple-900/40 border-indigo-700/50 p-8 text-center space-y-4">
          <div className="inline-flex items-center justify-center w-24 h-24 rounded-full bg-indigo-600/30 border-4 border-indigo-500">
            <span className="text-4xl font-medium text-white">{feedback.score}</span>
          </div>
          <div>
            <h2 className="text-2xl font-medium text-white mb-2">
              {feedback.score >= 80 ? 'Excellent work!' : feedback.score >= 60 ? 'Good effort!' : 'Keep practicing!'}
            </h2>
            <p className="text-indigo-200">You're making progress</p>
          </div>
          <div className="pt-2">
            <Progress value={feedback.score} className="h-2 bg-indigo-950" />
          </div>
        </Card>

        {/* Mentor Feedback */}
        <Card className="bg-[#25252a] border-[#35353a] p-6 space-y-4">
          <div className="flex items-start gap-4">
            <div className="w-10 h-10 rounded-full bg-indigo-600 flex items-center justify-center flex-shrink-0">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <div className="flex-1 space-y-3">
              <div>
                <p className="text-sm text-gray-400 mb-2">Zuno's Assessment</p>
                <p className="text-white leading-relaxed whitespace-pre-wrap">{feedback.ai_feedback}</p>
              </div>
            </div>
          </div>
        </Card>

        {/* CTA */}
        <div className="flex gap-4">
          <Button
            variant="outline"
            onClick={() => navigate('/progress')}
            className="flex-1 border-[#35353a] text-gray-300 hover:bg-[#35353a] hover:text-white"
          >
            View Progress
          </Button>
          <Button
            onClick={() => navigate('/dashboard')}
            className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white group"
          >
            Back to Dashboard
            <ChevronRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
          </Button>
        </div>

        {/* Motivational Note */}
        <div className="text-center">
          <p className="text-sm text-gray-500 italic">
            "One day at a time. One task at a time."
          </p>
        </div>
      </div>
    </div>
  );
}
