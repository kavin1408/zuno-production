import { useState, useEffect } from 'react';
import { Card } from '../ui/card';
import { Badge } from '../ui/badge';
import { CheckCircle2, Circle, Lock, ChevronDown, ChevronUp, ExternalLink } from 'lucide-react';
import { api } from '../../../lib/api';
import { Button } from '../ui/button';

export function RoadmapView({ filter = "" }: { filter?: string }) {
    const [roadmap, setRoadmap] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [expandedPhases, setExpandedPhases] = useState<string[]>([]);

    useEffect(() => {
        async function fetchRoadmap() {
            try {
                const data = await api.get('/roadmap');
                setRoadmap(data);
                if (data?.phases) {
                    setExpandedPhases([data.phases[0].name]);
                }
            } catch (error) {
                console.error("Failed to fetch roadmap", error);
            } finally {
                setLoading(false);
            }
        }
        fetchRoadmap();
    }, []);

    const togglePhase = (name: string) => {
        setExpandedPhases(prev =>
            prev.includes(name) ? prev.filter(p => p !== name) : [...prev, name]
        );
    };

    if (loading) return <div className="p-8 text-center text-gray-400">Building your journey...</div>;
    if (!roadmap || !roadmap.phases) return null;

    const lowerFilter = filter.toLowerCase();
    const filteredPhases = roadmap.phases.map((phase: any) => {
        const filteredModules = phase.modules.map((module: any) => {
            const filteredTasks = module.tasks.filter((task: any) =>
                task.title.toLowerCase().includes(lowerFilter) ||
                task.description.toLowerCase().includes(lowerFilter)
            );
            return { ...module, tasks: filteredTasks };
        }).filter((module: any) => module.tasks.length > 0);

        return { ...phase, modules: filteredModules };
    }).filter((phase: any) => phase.modules.length > 0);

    return (
        <div className="space-y-8 animate-in fade-in duration-500">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-white mb-2">{roadmap.title}</h2>
                    <p className="text-gray-400">Track your progress through the curriculum.</p>
                </div>
            </div>

            <div className="space-y-4">
                {filteredPhases.length > 0 ? (
                    filteredPhases.map((phase: any, pIdx: number) => (
                        <div key={pIdx} className="bg-[#25252a] rounded-xl border border-[#35353a] overflow-hidden">
                            <button
                                onClick={() => togglePhase(phase.name)}
                                className="w-full flex items-center justify-between p-4 hover:bg-[#2a2a2f] transition-colors"
                            >
                                <div className="flex items-center gap-3">
                                    <div className="w-8 h-8 rounded-full bg-indigo-600/20 text-indigo-400 flex items-center justify-center font-bold">
                                        {pIdx + 1}
                                    </div>
                                    <h3 className="text-lg font-medium text-white">{phase.name}</h3>
                                </div>
                                {expandedPhases.includes(phase.name) ? <ChevronUp className="w-5 h-5 text-gray-400" /> : <ChevronDown className="w-5 h-5 text-gray-400" />}
                            </button>

                            {expandedPhases.includes(phase.name) && (
                                <div className="p-4 pt-0 space-y-6">
                                    {phase.modules.map((module: any, mIdx: number) => (
                                        <div key={mIdx} className="space-y-3">
                                            <h4 className="text-sm font-semibold text-gray-500 uppercase tracking-widest pl-4">{module.name}</h4>
                                            <div className="space-y-2">
                                                {module.tasks.map((task: any, tIdx: number) => (
                                                    <div
                                                        key={task.id}
                                                        className={`flex items-start gap-4 p-4 rounded-xl border transition-all ${task.status === 'completed'
                                                            ? 'bg-green-900/10 border-green-900/30 opacity-70'
                                                            : task.status === 'active'
                                                                ? 'bg-indigo-900/20 border-indigo-700/50 scale-[1.01] shadow-lg shadow-indigo-900/20'
                                                                : 'bg-[#1a1a1e] border-[#35353a] opacity-50'
                                                            }`}
                                                    >
                                                        <div className="mt-1">
                                                            {task.status === 'completed' ? (
                                                                <CheckCircle2 className="w-5 h-5 text-green-500" />
                                                            ) : task.status === 'active' ? (
                                                                <div className="w-5 h-5 rounded-full border-2 border-indigo-500 animate-pulse" />
                                                            ) : (
                                                                <Lock className="w-4 h-4 text-gray-600" />
                                                            )}
                                                        </div>
                                                        <div className="flex-1 space-y-1">
                                                            <div className="flex items-center justify-between">
                                                                <p className={`font-medium ${task.status === 'completed' ? 'text-green-200' : 'text-white'}`}>
                                                                    {task.title}
                                                                </p>
                                                                <span className="text-xs text-gray-500">{task.estimated_time}m</span>
                                                            </div>
                                                            <p className="text-sm text-gray-400 leading-relaxed">{task.description}</p>
                                                            {task.output && (
                                                                <div className="pt-2">
                                                                    <span className="text-[10px] text-indigo-400 uppercase font-bold">Deliverable:</span>
                                                                    <p className="text-xs text-gray-300">{task.output}</p>
                                                                </div>
                                                            )}
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))
                ) : (
                    <div className="py-20 text-center">
                        <div className="w-16 h-16 bg-[#25252a] rounded-2xl flex items-center justify-center mx-auto mb-4 border border-[#35353a]">
                            <Circle className="w-8 h-8 text-gray-600" />
                        </div>
                        <h3 className="text-xl font-bold text-white mb-2">No matching topics</h3>
                        <p className="text-gray-500 max-w-xs mx-auto mb-8">
                            We couldn't find "{filter}" in your roadmap. Try a different term or ask Zuno about it.
                        </p>
                        <Button onClick={() => window.dispatchEvent(new CustomEvent('open-zuno-chat', { detail: { query: filter } }))} className="bg-indigo-600 hover:bg-indigo-700">
                            Ask Zuno about this
                        </Button>
                    </div>
                )}
            </div>
        </div>
    );
}
