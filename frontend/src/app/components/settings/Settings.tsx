import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Label } from '../ui/label';
import { RadioGroup, RadioGroupItem } from '../ui/radio-group';
import { ArrowLeft, Save, Loader2, CheckCircle2 } from 'lucide-react';
import { api } from '../../../lib/api';

export function Settings() {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [success, setSuccess] = useState(false);

    const [email, setEmail] = useState('');
    const [fullName, setFullName] = useState('');
    const [hoursPerDay, setHoursPerDay] = useState('1');
    const [targetGoal, setTargetGoal] = useState('job-ready');
    const [learningStyle, setLearningStyle] = useState('mixed');

    useEffect(() => {
        async function fetchProfile() {
            try {
                const profile = await api.get('/user/profile');
                setEmail(profile.email || '');
                setFullName(profile.full_name || '');
                setHoursPerDay(String((profile.daily_time_minutes || 60) / 60));
                setTargetGoal(profile.target_goal || 'job-ready');
                setLearningStyle(profile.learning_style || 'mixed');
            } catch (err) {
                console.error("Failed to fetch profile", err);
            } finally {
                setLoading(false);
            }
        }
        fetchProfile();
    }, []);

    const handleSave = async () => {
        setSaving(true);
        setSuccess(false);
        try {
            await api.put('/user/settings', {
                email,
                full_name: fullName,
                daily_time_minutes: parseFloat(hoursPerDay) * 60,
                learning_style: learningStyle,
                target_goal: targetGoal
            });
            setSuccess(true);
            setTimeout(() => setSuccess(false), 3000);
        } catch (err) {
            console.error("Failed to save settings", err);
            alert("Failed to save settings.");
        } finally {
            setSaving(false);
        }
    };

    if (loading) return <div className="min-h-screen bg-[#131316] flex items-center justify-center"><Loader2 className="animate-spin text-indigo-500 w-10 h-10" /></div>;

    return (
        <div className="min-h-screen bg-[#131316] text-white p-8">
            <div className="max-w-2xl mx-auto space-y-8">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')} className="text-gray-400 hover:text-white">
                            <ArrowLeft className="w-6 h-6" />
                        </Button>
                        <h1 className="text-3xl font-bold">Settings</h1>
                    </div>
                    <Button onClick={handleSave} disabled={saving} className="bg-indigo-600 hover:bg-indigo-700">
                        {saving ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : success ? <CheckCircle2 className="w-4 h-4 mr-2" /> : <Save className="w-4 h-4 mr-2" />}
                        {success ? 'Saved!' : 'Save Changes'}
                    </Button>
                </div>

                <Card className="p-8 bg-[#1a1a1e] border-[#35353a] space-y-8">
                    <div className="space-y-4">
                        <Label className="text-gray-300">Display Name</Label>
                        <Input
                            value={fullName}
                            onChange={(e) => setFullName(e.target.value)}
                            className="bg-[#131316] border-[#35353a] text-white"
                            placeholder="Your name"
                        />
                    </div>

                    <div className="space-y-4">
                        <Label className="text-gray-300">Email Address</Label>
                        <Input
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            className="bg-[#131316] border-[#35353a] text-white"
                        />
                    </div>

                    <div className="space-y-4">
                        <Label className="text-gray-300">Daily Commitment</Label>
                        <RadioGroup value={hoursPerDay} onValueChange={setHoursPerDay} className="grid grid-cols-2 gap-3">
                            {[0.5, 1, 2, 3].map((h) => (
                                <div key={h} className="flex items-center space-x-3 bg-[#131316] p-4 rounded-lg border border-[#35353a] cursor-pointer hover:border-indigo-500/50">
                                    <RadioGroupItem value={String(h)} id={`h-${h}`} className="border-gray-600 text-indigo-600" />
                                    <Label htmlFor={`h-${h}`} className="cursor-pointer text-white flex-1 whitespace-nowrap">
                                        {h === 0.5 ? '30 mins' : `${h} hour${h > 1 ? 's' : ''}`}
                                    </Label>
                                </div>
                            ))}
                        </RadioGroup>
                    </div>

                    <div className="space-y-4">
                        <Label className="text-gray-300">Primary Goal</Label>
                        <RadioGroup value={targetGoal} onValueChange={setTargetGoal} className="grid grid-cols-2 gap-3">
                            {['job-ready', 'certification', 'project-focused', 'exam-prep'].map((g) => (
                                <div key={g} className="flex items-center space-x-3 bg-[#131316] p-4 rounded-lg border border-[#35353a] cursor-pointer hover:border-indigo-500/50">
                                    <RadioGroupItem value={g} id={g} className="border-gray-600 text-indigo-600" />
                                    <Label htmlFor={g} className="cursor-pointer text-white flex-1 text-sm capitalize">
                                        {g.replace('-', ' ')}
                                    </Label>
                                </div>
                            ))}
                        </RadioGroup>
                    </div>

                    <div className="space-y-4">
                        <Label className="text-gray-300">Learning Style</Label>
                        <RadioGroup value={learningStyle} onValueChange={setLearningStyle} className="grid grid-cols-2 gap-3">
                            {['mixed', 'videos', 'articles', 'hands-on'].map((s) => (
                                <div key={s} className="flex items-center space-x-3 bg-[#131316] p-4 rounded-lg border border-[#35353a] cursor-pointer hover:border-indigo-500/50">
                                    <RadioGroupItem value={s} id={s} className="border-gray-600 text-indigo-600" />
                                    <Label htmlFor={s} className="cursor-pointer text-white flex-1 text-sm capitalize">
                                        {s.replace('-', ' ')}
                                    </Label>
                                </div>
                            ))}
                        </RadioGroup>
                    </div>
                </Card>
            </div>
        </div>
    );
}
