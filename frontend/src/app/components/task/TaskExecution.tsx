import { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Button } from '../ui/button';
import { Card } from '../ui/card';
import { Textarea } from '../ui/textarea';
import { Badge } from '../ui/badge';
import { ArrowLeft, Upload, CheckCircle2, Loader2, Youtube, FileText, BookOpen, RefreshCw, ExternalLink } from 'lucide-react';
import { api } from '../../../lib/api';

export function TaskExecution() {
  const navigate = useNavigate();
  const { taskId } = useParams();
  const [workSubmission, setWorkSubmission] = useState('');
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [task, setTask] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [regenerating, setRegenerating] = useState(false);
  const [iframeErrors, setIframeErrors] = useState<Record<number, boolean>>({});

  useEffect(() => {
    async function fetchTask() {
      try {
        const foundTask = await api.get(`/task/${taskId}`);
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
      console.log("DEBUG: Submitting task...", task.id);
      const result = await api.post('/submit-task', {
        task_id: task.id,
        submission_text: workSubmission,
        submission_image_url: uploadedImage
      });
      console.log("DEBUG: Submission result:", result);

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

  const handleRegenerate = async () => {
    setRegenerating(true);
    try {
      const res = await api.post(`/task/${taskId}/regenerate-resources`, {});
      setTask({ ...task, resources: res.resources });
      setIframeErrors({}); // Reset iframe errors on regenerate
    } catch (err) {
      console.error("Failed to regenerate resources", err);
      alert("Failed to regenerate resources. Try again later.");
    } finally {
      setRegenerating(false);
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

  const handleIframeError = (resourceId: number) => {
    setIframeErrors(prev => ({ ...prev, [resourceId]: true }));
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

        {/* Two Column Layout - Stacks on mobile */}
        <div className="flex flex-col lg:grid lg:grid-cols-2 gap-4 md:gap-6">
          {/* Left Column - Resource */}
          <div className="space-y-4 md:space-y-6">
            <Card className="bg-[#25252a] border-[#35353a] p-4 md:p-6 flex flex-col h-full">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-base md:text-lg font-medium text-white">Learning Resources</h3>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={handleRegenerate}
                  disabled={regenerating}
                  className="text-gray-400 hover:text-white"
                >
                  <RefreshCw className={`w-4 h-4 mr-2 ${regenerating ? 'animate-spin' : ''}`} />
                  {regenerating ? 'Finding...' : 'Regenerate'}
                </Button>
              </div>

              <div className="space-y-3 flex-1">
                {task.resources && task.resources.length > 0 ? (
                  task.resources.map((res: any, idx: number) => {
                    const isVideo = res.type === 'video' || (res.url && res.url.includes('youtube.com'));
                    const isHighConfidence = true; // For testing/mock, assume high confidence to force embed

                    const getEmbedUrl = (url: string) => {
                      if (!url) return '';
                      if (url.includes('youtube.com/embed/')) return url;
                      if (url.includes('youtube.com/watch?v=')) return url.replace('watch?v=', 'embed/');
                      if (url.includes('youtu.be/')) return url.replace('youtu.be/', 'youtube.com/embed/');
                      return url;
                    };

                    const embedUrl = getEmbedUrl(res.url);
                    const isEmbed = isVideo && (res.url?.includes('/embed/') || res.url?.includes('watch?v=') || res.url?.includes('youtu.be/'));
                    const hasIframeError = iframeErrors[res.id || idx];

                    return (
                      <div key={res.id || idx} className="space-y-3">
                        {isEmbed && isHighConfidence && !hasIframeError ? (
                          <div className="rounded-xl overflow-hidden border border-[#35353a] bg-[#1a1a1e]">
                            <div className="flex items-center gap-2 px-4 py-2 bg-[#2a2a2f] border-b border-[#35353a]">
                              <Youtube className="w-4 h-4 text-red-500" />
                              <span className="text-xs font-medium text-gray-200">✅ Verified Video</span>
                            </div>
                            <div className="aspect-video">
                              <iframe
                                src={embedUrl}
                                className="w-full h-full"
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                allowFullScreen
                                title={res.title}
                                loading="lazy"
                                onError={() => handleIframeError(res.id || idx)}
                              />
                            </div>
                            <div className="p-3">
                              <p className="font-medium text-white text-sm truncate">{res.title}</p>
                              {res.rationale && (
                                <p className="text-xs text-gray-400 mt-1 italic">{res.rationale}</p>
                              )}
                              <a
                                href={res.url.replace('/embed/', '/watch?v=')}
                                target="_blank"
                                rel="noreferrer"
                                className="inline-flex items-center gap-1 text-xs text-indigo-400 hover:text-indigo-300 mt-2"
                              >
                                <ExternalLink className="w-3 h-3" />
                                Watch on YouTube
                              </a>
                            </div>
                          </div>
                        ) : (
                          <a
                            href={res.url}
                            target="_blank"
                            rel="noreferrer"
                            className="group block p-4 bg-[#1a1a1e] rounded-xl border border-[#35353a] hover:border-indigo-500/50 transition-all hover:bg-indigo-500/5"
                          >
                            <div className="flex items-start gap-4">
                              <div className="p-2.5 bg-indigo-500/10 rounded-lg text-indigo-400 group-hover:bg-indigo-500 group-hover:text-white transition-colors">
                                {isVideo ? <Youtube className="w-5 h-5" /> :
                                  res.type === 'docs' ? <BookOpen className="w-5 h-5" /> :
                                    <FileText className="w-5 h-5" />}
                              </div>
                              <div className="flex-1 min-w-0">
                                <div className="flex items-center justify-between gap-2">
                                  <div className="flex items-center gap-2">
                                    <span className="text-[10px] uppercase tracking-wider font-bold text-indigo-400/80">
                                      {isVideo && !isHighConfidence ? "🔍 Curated YouTube Search" :
                                        isVideo && hasIframeError ? "🎥 Watch on YouTube" :
                                          isVideo ? "🎥 Verified Video" : res.platform}
                                    </span>
                                  </div>
                                  <ExternalLink className="w-3.5 h-3.5 text-gray-500 group-hover:text-indigo-400" />
                                </div>
                                <p className="font-medium text-white truncate mt-1">{res.title}</p>
                                {res.rationale && (
                                  <p className="text-xs text-gray-400 mt-2 line-clamp-2 italic">{res.rationale}</p>
                                )}
                              </div>
                            </div>
                          </a>
                        )}
                      </div>
                    );
                  })
                ) : (
                  <div className="text-center py-10 bg-[#1a1a1e] rounded-xl border border-dashed border-[#35353a]">
                    <p className="text-gray-500 text-sm">No curated resources found.</p>
                    <Button variant="link" onClick={handleRegenerate} className="text-indigo-400 p-0 h-auto text-sm mt-2">
                      Generate now
                    </Button>
                  </div>
                )}
              </div>

              <div className="mt-6 pt-6 border-t border-[#35353a] space-y-3">
                <h4 className="text-xs md:text-sm font-medium text-gray-300 flex items-center gap-2">
                  <CheckCircle2 className="w-4 h-4 text-indigo-400" />
                  What to learn
                </h4>
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
