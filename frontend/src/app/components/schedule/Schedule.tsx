import { useNavigate } from 'react-router-dom';
import { Card } from '../ui/card';
import { Calendar, Clock, ArrowLeft, ChevronRight } from 'lucide-react';
import { Button } from '../ui/button';

export function Schedule() {
    const navigate = useNavigate();

    const days = [
        { date: "Today", tasks: ["Python Fundamentals", "Setting up Environment"] },
        { date: "Tomorrow", tasks: ["Variables & Data Types", "Input/Output Basics"] },
        { date: "Wednesday", tasks: ["Control Flow", "If-Else Structures"] },
        { date: "Thursday", tasks: ["Loops and Iteration", "While vs For"] },
    ];

    return (
        <div className="min-h-screen bg-[#131316] text-white p-8">
            <div className="max-w-4xl mx-auto space-y-8">
                <div className="flex items-center gap-4">
                    <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard')} className="text-gray-400 hover:text-white">
                        <ArrowLeft className="w-6 h-6" />
                    </Button>
                    <h1 className="text-3xl font-bold">Your Schedule</h1>
                </div>

                <div className="space-y-4">
                    {days.map((day, i) => (
                        <Card key={i} className="p-6 border-[#35353a] bg-[#1a1a1e] flex flex-col md:flex-row md:items-center justify-between gap-4">
                            <div className="flex items-center gap-4">
                                <div className="p-3 bg-indigo-600/10 text-indigo-400 rounded-xl">
                                    <Calendar className="h-6 w-6" />
                                </div>
                                <div>
                                    <h3 className="text-lg font-bold">{day.date}</h3>
                                    <p className="text-gray-400 text-sm">{day.tasks.length} lessons scheduled</p>
                                </div>
                            </div>
                            <div className="flex flex-col gap-2">
                                {day.tasks.map((t, ti) => (
                                    <div key={ti} className="flex items-center gap-2 text-sm text-gray-300 bg-white/5 px-3 py-1.5 rounded-lg">
                                        <Clock className="w-3.5 h-3.5 text-indigo-400" />
                                        {t}
                                    </div>
                                ))}
                            </div>
                            <ChevronRight className="w-5 h-5 text-gray-600 hidden md:block" />
                        </Card>
                    ))}
                </div>
            </div>
        </div>
    );
}
