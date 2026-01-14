import { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { RadioGroup, RadioGroupItem } from '../ui/radio-group';
import { ChevronRight, ChevronLeft, Loader2 } from 'lucide-react';
import { api } from '../../../lib/api';

export function Onboarding() {
  const navigate = useNavigate();
  const location = useLocation();
  const [step, setStep] = useState(1);
  const [skills, setSkills] = useState<string[]>(['']); // Array of skills
  const [hoursPerDay, setHoursPerDay] = useState('1');
  const [targetDate, setTargetDate] = useState('');
  const [targetGoal, setTargetGoal] = useState('job-ready');
  const [learningStyle, setLearningStyle] = useState('mixed');

  const [loading, setLoading] = useState(false);
  const [onboardingResult, setOnboardingResult] = useState<any>(null);

  useEffect(() => {
    async function checkExisting() {
      const params = new URLSearchParams(location.search);
      if (params.get('force') === 'true') {
        return; // Skip redirection if forced
      }

      try {
        const result = await api.get('/daily-plan');
        if (result && Array.isArray(result) && result.length > 0) {
          navigate('/dashboard');
        }
      } catch (error) {
        // Probably no goal yet, which is fine
      }
    }
    checkExisting();
  }, [navigate, location.search]);

  const handleAddSkill = () => {
    setSkills([...skills, '']);
  };

  const handleRemoveSkill = (index: number) => {
    if (skills.length > 1) {
      const newSkills = [...skills];
      newSkills.splice(index, 1);
      setSkills(newSkills);
    }
  };

  const handleSkillChange = (index: number, value: string) => {
    const newSkills = [...skills];
    newSkills[index] = value;
    setSkills(newSkills);
  };

  const handleContinue = async () => {
    if (step < 3) {
      setStep(step + 1);
    } else if (step === 3) {
      // Submit data to backend before moving to step 4
      setLoading(true);
      try {
        const filteredSkills = skills.filter(s => s.trim() !== '');
        const result = await api.post('/onboarding', {
          subjects: filteredSkills,
          exam_or_skill: "General Mastery", // Defaulting for simple UI
          daily_time_minutes: parseFloat(hoursPerDay) * 60,
          target_date: targetDate || new Date(Date.now() + 90 * 24 * 60 * 60 * 1000).toISOString().split('T')[0], // Default 90 days
          target_goal: targetGoal,
          learning_style: learningStyle
        });
        setOnboardingResult(result);
        setStep(4);
      } catch (error) {
        console.error("Onboarding failed", error);
        alert("Failed to save goals. Please try again.");
      } finally {
        setLoading(false);
      }
    } else {
      // Complete onboarding
      navigate('/dashboard');
    }
  };

  const handleBack = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        {/* Progress Indicator */}
        <div className="mb-12">
          <div className="flex items-center justify-center gap-2 mb-3">
            {[1, 2, 3, 4].map((i) => (
              <div
                key={i}
                className={`h-1.5 rounded-full transition-all ${i === step ? 'w-12 bg-indigo-600' : i < step ? 'w-8 bg-indigo-600/40' : 'w-8 bg-gray-700'
                  }`}
              />
            ))}
          </div>
          <p className="text-center text-sm text-gray-500">Step {step} of 4</p>
        </div>

        {/* Step Content */}
        <div className="bg-[#25252a] rounded-2xl p-10 border border-[#35353a]">
          {step === 1 && (
            <div className="space-y-6">
              <div>
                <h2 className="text-3xl font-medium text-white mb-3">
                  What do you want to master?
                </h2>
                <p className="text-gray-400">
                  Choose the subjects or skills you're committed to learning. You can add multiple.
                </p>
              </div>

              <div className="space-y-4">
                <Label className="text-gray-300">Your learning goals</Label>
                {skills.map((skill, index) => (
                  <div key={index} className="flex gap-2">
                    <Input
                      placeholder="e.g., Machine Learning, Spanish, Web Development..."
                      value={skill}
                      onChange={(e) => handleSkillChange(index, e.target.value)}
                      className="bg-[#1a1a1e] border-[#35353a] text-white placeholder:text-gray-500 focus:border-indigo-500 focus:ring-indigo-500/20 h-12 text-lg flex-1"
                    />
                    {skills.length > 1 && (
                      <Button
                        variant="outline"
                        onClick={() => handleRemoveSkill(index)}
                        className="border-[#35353a] text-gray-400 hover:bg-red-900/20 hover:text-red-400 hover:border-red-700 h-12 w-12 p-0"
                      >
                        ✕
                      </Button>
                    )}
                  </div>
                ))}
                <Button
                  variant="outline"
                  onClick={handleAddSkill}
                  className="w-full border-dashed border-gray-600 text-gray-400 hover:text-white"
                >
                  + Add another skill
                </Button>
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-6">
              <div>
                <h2 className="text-3xl font-medium text-white mb-3">
                  How much time can you commit?
                </h2>
                <p className="text-gray-400">
                  Be realistic. Consistency matters more than intensity.
                </p>
              </div>

              <div className="space-y-4">
                <Label className="text-gray-300">Daily commitment</Label>
                <RadioGroup value={hoursPerDay} onValueChange={setHoursPerDay} className="space-y-3">
                  <div className="flex items-center space-x-3 bg-[#1a1a1e] p-4 rounded-lg border border-[#35353a] cursor-pointer hover:border-indigo-500/50 transition-colors">
                    <RadioGroupItem value="0.5" id="half" className="border-gray-600 text-indigo-600" />
                    <Label htmlFor="half" className="cursor-pointer text-white flex-1">
                      30 minutes per day
                    </Label>
                  </div>
                  <div className="flex items-center space-x-3 bg-[#1a1a1e] p-4 rounded-lg border border-[#35353a] cursor-pointer hover:border-indigo-500/50 transition-colors">
                    <RadioGroupItem value="1" id="one" className="border-gray-600 text-indigo-600" />
                    <Label htmlFor="one" className="cursor-pointer text-white flex-1">
                      1 hour per day
                    </Label>
                  </div>
                  <div className="flex items-center space-x-3 bg-[#1a1a1e] p-4 rounded-lg border border-[#35353a] cursor-pointer hover:border-indigo-500/50 transition-colors">
                    <RadioGroupItem value="2" id="two" className="border-gray-600 text-indigo-600" />
                    <Label htmlFor="two" className="cursor-pointer text-white flex-1">
                      2 hours per day
                    </Label>
                  </div>
                  <div className="flex items-center space-x-3 bg-[#1a1a1e] p-4 rounded-lg border border-[#35353a] cursor-pointer hover:border-indigo-500/50 transition-colors">
                    <RadioGroupItem value="3" id="three" className="border-gray-600 text-indigo-600" />
                    <Label htmlFor="three" className="cursor-pointer text-white flex-1">
                      3+ hours per day
                    </Label>
                  </div>
                </RadioGroup>
              </div>

              <div className="space-y-3 pt-4">
                <Label htmlFor="target" className="text-gray-300">Target completion date (optional)</Label>
                <Input
                  id="target"
                  type="date"
                  value={targetDate}
                  onChange={(e) => setTargetDate(e.target.value)}
                  className="bg-[#1a1a1e] border-[#35353a] text-white focus:border-indigo-500 focus:ring-indigo-500/20 h-12"
                />
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="space-y-6">
              <div>
                <h2 className="text-3xl font-medium text-white mb-3">
                  Tailor your roadmap
                </h2>
                <p className="text-gray-400">
                  Help Zuno design the perfect learning path for your goals.
                </p>
              </div>

              <div className="space-y-6">
                <div className="space-y-4">
                  <Label className="text-gray-300">What is your primary goal?</Label>
                  <RadioGroup value={targetGoal} onValueChange={setTargetGoal} className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {['job-ready', 'certification', 'project-focused', 'exam-prep'].map((g) => (
                      <div key={g} className="flex items-center space-x-3 bg-[#1a1a1e] p-4 rounded-lg border border-[#35353a] cursor-pointer hover:border-indigo-500/50 transition-colors">
                        <RadioGroupItem value={g} id={g} className="border-gray-600 text-indigo-600" />
                        <Label htmlFor={g} className="cursor-pointer text-white flex-1 text-sm capitalize">
                          {g.replace('-', ' ')}
                        </Label>
                      </div>
                    ))}
                  </RadioGroup>
                </div>

                <div className="space-y-4">
                  <Label className="text-gray-300">Preferred learning style</Label>
                  <RadioGroup value={learningStyle} onValueChange={setLearningStyle} className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    {['mixed', 'videos', 'articles', 'hands-on'].map((s) => (
                      <div key={s} className="flex items-center space-x-3 bg-[#1a1a1e] p-4 rounded-lg border border-[#35353a] cursor-pointer hover:border-indigo-500/50 transition-colors">
                        <RadioGroupItem value={s} id={s} className="border-gray-600 text-indigo-600" />
                        <Label htmlFor={s} className="cursor-pointer text-white flex-1 text-sm capitalize">
                          {s.replace('-', ' ')}
                        </Label>
                      </div>
                    ))}
                  </RadioGroup>
                </div>
              </div>
            </div>
          )}

          {step === 4 && (
            <div className="space-y-6">
              <div>
                <h2 className="text-3xl font-medium text-white mb-3">
                  You're all set!
                </h2>
                <p className="text-gray-400 mb-6">
                  Zuno has created your personalized learning paths.
                </p>
              </div>

              <div className="space-y-4 max-h-[300px] overflow-y-auto pr-2">
                {onboardingResult?.goals?.map((g: any, i: number) => (
                  <div key={i} className="bg-[#1a1a1e] rounded-xl p-6 border border-[#35353a] space-y-4">
                    <div>
                      <p className="text-sm text-gray-400 mb-1">Goal #{i + 1}</p>
                      <p className="text-xl text-white">{g.subject}</p>
                    </div>
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
                      <div>
                        <p className="text-sm text-gray-400 mb-1">Daily Commitment</p>
                        <p className="text-lg text-white">{hoursPerDay} {parseFloat(hoursPerDay) === 1 ? 'hour' : 'hours'}</p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-400 mb-1">Level Detected</p>
                        <p className="text-lg text-white">{g.detected_level}</p>
                      </div>
                    </div>
                    <div className="bg-indigo-950/30 border border-indigo-900/50 rounded-xl p-4">
                      <p className="text-indigo-200 text-sm leading-relaxed">
                        <span className="font-medium">Zuno says:</span> {g.message}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="flex items-center justify-between mt-8 pt-6 border-t border-[#35353a]">
            {step > 1 ? (
              <Button
                variant="ghost"
                onClick={handleBack}
                disabled={loading}
                className="text-gray-400 hover:text-white"
              >
                <ChevronLeft className="w-4 h-4 mr-1" />
                Back
              </Button>
            ) : (
              <div />
            )}

            <Button
              onClick={handleContinue}
              disabled={(step === 1 && skills.filter(s => s.trim() !== '').length === 0) || loading}
              className="bg-indigo-600 hover:bg-indigo-700 text-white px-8"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  {step === 4 ? 'Start Learning' : 'Continue'}
                  <ChevronRight className="w-4 h-4 ml-1" />
                </>
              )}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
