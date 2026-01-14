import { useNavigate } from 'react-router-dom';
import { Button } from '../ui/button';
import { Card } from '../ui/card';
import {
    Rocket,
    Map,
    Youtube,
    CheckCircle2,
    ArrowRight,
    Zap,
    ShieldAlert,
    Clock,
    Trophy
} from 'lucide-react';

export function IntroPage() {
    const navigate = useNavigate();

    const handleStart = () => {
        localStorage.setItem('zuno_intro_seen', 'true');
        navigate('/login');
    };

    return (
        <div className="min-h-screen bg-[#1a1a1e] text-white selection:bg-indigo-500/30">
            {/* Hero Section - What is ZUNO */}
            <section className="relative pt-20 pb-16 px-6 overflow-hidden">
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-[500px] bg-gradient-to-b from-indigo-500/10 to-transparent blur-3xl opacity-50" />

                <div className="max-w-4xl mx-auto text-center relative z-10 space-y-6">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-sm font-medium mb-4">
                        <Zap className="w-4 h-4" />
                        <span>Meet your new AI Mentor</span>
                    </div>

                    <h1 className="text-5xl md:text-7xl font-bold tracking-tight">
                        Master Any Skill <br />
                        <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 via-white to-indigo-400">Powered by AI</span>
                    </h1>

                    <p className="text-xl md:text-2xl text-gray-400 max-w-2xl mx-auto leading-relaxed">
                        ZUNO is an AI mentor that creates a personalized learning roadmap and finds the best learning resources—especially YouTube videos—so you don’t waste time searching.
                    </p>
                </div>
            </section>

            <div className="max-w-6xl mx-auto px-6 space-y-32 pb-32">
                {/* Section 2: How ZUNO Works */}
                <section className="space-y-12">
                    <div className="text-center space-y-4">
                        <h2 className="text-3xl md:text-4xl font-bold">How ZUNO Works</h2>
                        <p className="text-gray-400">Step by step to mastery.</p>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-6">
                        {[
                            { icon: Rocket, title: "Choose Goal", desc: "Select a skill or exam you want to master." },
                            { icon: Map, title: "AI Roadmap", desc: "ZUNO builds a structured, progressive path." },
                            { icon: Youtube, title: "Curated Content", desc: "Best-in-class YouTube videos and docs." },
                            { icon: CheckCircle2, title: "Learn & Execute", desc: "Follow tasks step-by-step daily." },
                            { icon: Trophy, title: "Track Progress", desc: "Stay consistent and hit your milestones." }
                        ].map((step, idx) => (
                            <div key={idx} className="relative group">
                                <Card className="bg-[#25252a] border-[#35353a] p-6 h-full hover:border-indigo-500/50 transition-all">
                                    <div className="w-12 h-12 rounded-xl bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-4 group-hover:scale-110 transition-transform">
                                        <step.icon className="w-6 h-6" />
                                    </div>
                                    <h3 className="text-lg font-semibold mb-2">{step.title}</h3>
                                    <p className="text-sm text-gray-400 leading-relaxed">{step.desc}</p>
                                </Card>
                                {idx < 4 && (
                                    <div className="hidden lg:block absolute top-1/2 -right-4 -translate-y-1/2 text-gray-700">
                                        <ArrowRight className="w-6 h-6" />
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                </section>

                {/* Section 3: Why ZUNO is Different */}
                <section className="grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
                    <div className="space-y-6">
                        <h2 className="text-3xl md:text-4xl font-bold">Why ZUNO is Different</h2>
                        <div className="space-y-4">
                            {[
                                "AI-generated learning roadmap tailored to you",
                                "Curated best YouTube videos (not random results)",
                                "Task-by-task execution with real accountability",
                                "In-depth progress tracking & streaks",
                                "Built specifically for self-learners"
                            ].map((item, idx) => (
                                <div key={idx} className="flex items-center gap-3">
                                    <div className="flex-shrink-0 w-6 h-6 rounded-full bg-green-500/10 flex items-center justify-center text-green-400">
                                        <CheckCircle2 className="w-4 h-4" />
                                    </div>
                                    <span className="text-gray-300">{item}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="relative aspect-video rounded-2xl bg-gradient-to-br from-indigo-600/20 to-indigo-900/40 border border-[#35353a] flex items-center justify-center overflow-hidden">
                        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20" />
                        <div className="relative text-center p-8 space-y-4">
                            <div className="w-16 h-16 rounded-2xl bg-indigo-500 text-white flex items-center justify-center mx-auto shadow-2xl shadow-indigo-500/20">
                                <Rocket className="w-8 h-8" />
                            </div>
                            <p className="text-sm font-medium text-indigo-300 uppercase tracking-widest">Powered by ZUNO AI</p>
                        </div>
                    </div>
                </section>

                {/* Section 4: What ZUNO is NOT */}
                <section className="bg-red-500/5 border border-red-500/10 rounded-3xl p-8 md:p-12 text-center space-y-8">
                    <div className="max-w-2xl mx-auto space-y-4">
                        <div className="w-12 h-12 rounded-full bg-red-500/10 flex items-center justify-center text-red-400 mx-auto mb-4">
                            <ShieldAlert className="w-6 h-6" />
                        </div>
                        <h2 className="text-3xl font-bold">Setting Expectations</h2>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
                            <div className="p-4 bg-white/5 rounded-xl">
                                <p className="font-semibold text-red-300 mb-1">Not a content dump</p>
                                <p className="text-gray-400">We prioritize quality over quantity.</p>
                            </div>
                            <div className="p-4 bg-white/5 rounded-xl">
                                <p className="font-semibold text-red-300 mb-1">Not just a chatbot</p>
                                <p className="text-gray-400">A full curriculum, not just a conversation.</p>
                            </div>
                            <div className="p-4 bg-white/5 rounded-xl">
                                <p className="font-semibold text-red-300 mb-1">No instant results</p>
                                <p className="text-gray-400">Success requires your effort and consistency.</p>
                            </div>
                        </div>
                    </div>
                </section>

                {/* CTA Section */}
                <section className="text-center space-y-8 py-16 border-t border-[#35353a]">
                    <h2 className="text-3xl md:text-5xl font-bold">Ready to start the grind?</h2>
                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                        <Button
                            size="lg"
                            onClick={handleStart}
                            className="bg-indigo-600 hover:bg-indigo-700 text-white px-10 h-16 text-xl rounded-full shadow-2xl shadow-indigo-500/20 transition-all hover:scale-105"
                        >
                            Start Learning with ZUNO
                            <ArrowRight className="w-6 h-6 ml-3" />
                        </Button>
                    </div>
                    <p className="text-sm text-gray-500">By continuing, you agree to show up and stay consistent.</p>
                </section>
            </div>
        </div>
    );
}
