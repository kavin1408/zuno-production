import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Button } from '../ui/button';
import { Card } from '../ui/card';
import { Textarea } from '../ui/textarea';
import { Badge } from '../ui/badge';
import { ArrowLeft, Upload, CheckCircle2, Loader2 } from 'lucide-react';
import { api } from '../../../lib/api';

export function TaskExecution() {
  const navigate = useNavigate();
  const { taskId } = useParams();
  const [workSubmission, setWorkSubmission] = useState('');
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [task, setTask] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    async function fetchTask() {
      try {
        const dailyPlans = await api.get('/daily-plan');
        const foundTask = Array.isArray(dailyPlans)
          ? dailyPlans.find((t: any) => t.id === parseInt(taskId || '0'))
          : (dailyPlans.id === parseInt(taskId || '0') ? dailyPlans : null);

        if (foundTask) {
          setTask(foundTask);
        }
      } catch (error) {
        console.error("Failed to fetch task", error);
      } finally {
        setLoading(false);
      }
    }
    fetchTask();
  }, [taskId]);

  const handleSubmit = async () => {
    if (!workSubmission.trim() || !task) return;

    setSubmitting(true);
    try {
      const result = await api.post('/submit-task', {
        task_id: task.id,
        submission_text: workSubmission,
        submission_image_url: uploadedImage
      });

      // Store feedback for the feedback page
      sessionStorage.setItem(`feedback_${task.id}`, JSON.stringify(result));

      navigate(`/feedback/${task.id}`);
    } catch (error) {
      console.error("Failed to submit task", error);
      alert("Failed to submit. Please try again.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setUploadedImage(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#1a1a1e] flex items-center justify-center text-white">
        <Loader2 className="w-8 h-8 animate-spin" />
        <span className="ml-2">Loading task...</span>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="min-h-screen bg-[#1a1a1e] flex items-center justify-center text-white">
        <p>Task not found</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#1a1a1e]">
      {/* Header */}
      <header className="bg-[#25252a] border-b border-[#35353a] sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 md:px-6 py-3 md:py-4 flex items-center justify-between">
          <button
            onClick={() => navigate('/dashboard')}
            className="flex items-center gap-2 text-gray-400 hover:text-white transition-colors"
          >
            <ArrowLeft className="w-5 h-5" />
            <span>Back to Dashboard</span>
          </button>
        </div>
      </header>

      <div className="max-w-5xl mx-auto p-4 md:p-6 space-y-4 md:space-y-6">
        {/* Task Header */}
        <div className="space-y-2">
          <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-3">
            <h1 className="text-2xl md:text-3xl font-medium text-white">{task.topic}</h1>
            {task.level && (
              <Badge variant="secondary" className="bg-indigo-500/20 text-indigo-200 hover:bg-indigo-500/30 border-0 h-6 md:h-7 self-start">
                {task.level}
              </Badge>
            )}
          </div>
          <p className="text-base md:text-xl text-gray-400">Today's Learning Task</p>
        </div>

        {/* Two Column Layout */}
        <div className="grid lg:grid-cols-2 gap-4 md:gap-6">
          {/* Left Column - Resource */}
          <div className="space-y-4 md:space-y-6">
            <Card className="bg-[#25252a] border-[#35353a] p-4 md:p-6 space-y-3 md:space-y-4">
              <h3 className="text-base md:text-lg font-medium text-white">Learning Resource</h3>

              {task.resource_link && (
                <a
                  href={task.resource_link}
                  target="_blank"
                  rel="noreferrer"
                  className="block aspect-video bg-[#1a1a1e] rounded-lg flex items-center justify-center border border-[#35353a] hover:border-indigo-500 transition-colors"
                >
                  <div className="text-center space-y-3">
                    <div className="w-16 h-16 bg-indigo-600 rounded-full flex items-center justify-center mx-auto">
                      <svg className="w-8 h-8 text-white ml-1" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M8 5v14l11-7z" />
                      </svg>
                    </div>
                    <p className="text-gray-400">Click to open resource</p>
                  </div>
                </a>
              )}

              <div className="pt-3 md:pt-4 space-y-2 md:space-y-3">
                <h4 className="text-xs md:text-sm font-medium text-gray-300">What to do</h4>
                <p className="text-sm md:text-base text-gray-400 leading-relaxed whitespace-pre-wrap">{task.task_description}</p>
              </div>
            </Card>
          </div>

          {/* Right Column - Submission */}
          <div className="space-y-4 md:space-y-6">
            <Card className="bg-[#25252a] border-[#35353a] p-4 md:p-6 space-y-4 md:space-y-6">
              <div>
                <h3 className="text-base md:text-lg font-medium text-white mb-2">Submit Your Work</h3>
                <p className="text-sm text-gray-400">
                  Share your notes, code, or screenshots of completed exercises.
                </p>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm text-gray-300 mb-3">Your notes or code</label>
                  <Textarea
                    placeholder="Paste your code, share your learnings, or explain concepts in your own words..."
                    value={workSubmission}
                    onChange={(e) => setWorkSubmission(e.target.value)}
                    rows={12}
                    className="bg-[#1a1a1e] border-[#35353a] text-white placeholder:text-gray-500 focus:border-indigo-500 focus:ring-indigo-500/20 resize-none font-mono text-sm"
                  />
                </div>

                <div>
                  <label className="block text-sm text-gray-300 mb-3">Upload screenshots (optional)</label>
                  <div className="border-2 border-dashed border-[#35353a] rounded-lg p-6 text-center hover:border-indigo-500/50 transition-colors">
                    <input
                      type="file"
                      accept="image/*"
                      onChange={handleImageUpload}
                      className="hidden"
                      id="file-upload"
                    />
                    <label
                      htmlFor="file-upload"
                      className="cursor-pointer flex flex-col items-center gap-2"
                    >
                      {uploadedImage ? (
                        <div className="space-y-2">
                          <img
                            src={uploadedImage}
                            alt="Uploaded"
                            className="max-h-32 rounded-lg"
                          />
                          <p className="text-sm text-indigo-400">Click to change</p>
                        </div>
                      ) : (
                        <>
                          <Upload className="w-8 h-8 text-gray-500" />
                          <p className="text-sm text-gray-400">
                            Click to upload or drag and drop
                          </p>
                          <p className="text-xs text-gray-500">PNG, JPG up to 5MB</p>
                        </>
                      )}
                    </label>
                  </div>
                </div>
              </div>

              <Button
                onClick={handleSubmit}
                disabled={!workSubmission.trim() || submitting}
                className="w-full bg-indigo-600 hover:bg-indigo-700 text-white h-12 text-lg disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {submitting ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Submitting...
                  </>
                ) : (
                  'Submit Work'
                )}
              </Button>
            </Card>

            {/* Help */}
            <Card className="bg-indigo-950/30 border-indigo-900/50 p-4 md:p-5">
              <p className="text-xs md:text-sm text-indigo-200 leading-relaxed">
                <span className="font-medium">Need help?</span> Submit what you have, even if incomplete.
                Zuno will provide feedback and guidance on what to improve.
              </p>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
