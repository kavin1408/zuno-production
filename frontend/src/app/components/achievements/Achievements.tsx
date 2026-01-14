import { useNavigate } from 'react-router-dom';
import { Card } from '../ui/card';
import { Badge } from '../ui/badge';
import { Trophy, Star, Zap, Target, ArrowLeft } from 'lucide-react';
import { Button } from '../ui/button';

export function Achievements() {
    const navigate = useNavigate();

    const achievements = [
        { title: "First Step", description: "Complete your first task", icon: Target, completed: true },
        { title: "On Fire", description: "Maintain a 3-day streak", icon: Zap, completed: false },
        { title: "Mastery", description: "Reach 100% on any module", icon: Trophy, completed: false },
        { title: "Top Marks", description: "Get a 95+ score from Zuno", icon: Star, completed: false },
    ];

    return (
        <div className="min-h-screen bg-[#131316] text-white p-8">
            <div className="max-w-4xl mx-auto space-y-8">
                <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')} className="text-gray-400 hover:text-white">
                            <ArrowLeft className="w-6 h-6" />
                        </Button>
                        <h1 className="text-3xl font-bold">Achievements</h1>
                    </div>
                    <Badge variant="outline" className="border-indigo-500/50 text-indigo-400 py-1 px-4">
                        250 XP
                    </Badge>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {achievements.map((a, i) => (
                        <Card key={i} className={`p-6 border-[#35353a] bg-[#1a1a1e] relative overflow-hidden transition-all hover:border-indigo-500/50 ${!a.completed && 'opacity-50'}`}>
                            <div className="flex items-start gap-4">
                                <div className={`p-3 rounded-xl ${a.completed ? 'bg-indigo-600/20 text-indigo-400' : 'bg-gray-800 text-gray-500'}`}>
                                    <a.icon className="h-8 w-8" />
                                </div>
                                <div className="space-y-1">
                                    <h3 className="text-xl font-bold">{a.title} {a.completed && "✅"}</h3>
                                    <p className="text-gray-400 text-sm">{a.description}</p>
                                </div>
                            </div>
                            {a.completed && (
                                <div className="absolute top-0 right-0 w-24 h-24 bg-indigo-600/5 rounded-full -mr-12 -mt-12" />
                            )}
                        </Card>
                    ))}
                </div>
            </div>
        </div>
    );
}
