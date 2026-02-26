"use client";

import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    Cell
} from "recharts";

const data = [
    { name: "Jan", total: 45 },
    { name: "Feb", total: 52 },
    { name: "Mar", total: 48 },
    { name: "Apr", total: 61 },
    { name: "May", total: 55 },
    { name: "Jun", total: 67 },
];

export function StatsChart() {
    return (
        <div className="h-[240px] w-full">
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={data} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                    <XAxis
                        dataKey="name"
                        axisLine={false}
                        tickLine={false}
                        tick={{ fontSize: 12, fill: "#94a3b8" }}
                        dy={10}
                    />
                    <YAxis
                        axisLine={false}
                        tickLine={false}
                        tick={{ fontSize: 12, fill: "#94a3b8" }}
                    />
                    <Tooltip
                        cursor={{ fill: '#f8fafc' }}
                        contentStyle={{
                            borderRadius: '12px',
                            border: 'none',
                            boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)'
                        }}
                    />
                    <Bar
                        dataKey="total"
                        radius={[6, 6, 0, 0]}
                        barSize={32}
                    >
                        {data.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={index === 5 ? '#2563eb' : '#93c5fd'} />
                        ))}
                    </Bar>
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}
