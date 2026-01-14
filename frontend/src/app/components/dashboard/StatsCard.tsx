import { Card } from '../ui/card';
import { LucideIcon } from 'lucide-react';

interface StatsCardProps {
    title: string;
    value: string | number;
    label: string;
    icon: LucideIcon;
    iconColor: string;
    iconBg: string;
    loading?: boolean;
}

export function StatsCard({ title, value, label, icon: Icon, iconColor, iconBg, loading }: StatsCardProps) {
    return (
        <Card className="bg-[#25252a] p-6 border-[#35353a] hover:bg-[#2a2a2f] transition-all group">
            <div className={`p-3 ${iconBg} ${iconColor} w-fit rounded-xl mb-4 group-hover:scale-110 transition-transform`}>
                <Icon className="h-5 w-5" />
            </div>
            <div>
                <p className="text-sm font-bold text-white">{title}</p>
                <div className="flex items-baseline gap-2 mt-1">
                    {loading ? (
                        <div className="h-7 w-12 bg-gray-700 animate-pulse rounded" />
                    ) : (
                        <h4 className="text-2xl font-bold text-white">{value}</h4>
                    )}
                    <p className="text-xs text-gray-500 uppercase font-black tracking-widest">{label}</p>
                </div>
            </div>
        </Card>
    );
}
