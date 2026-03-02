"use client";

import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell,
} from "recharts";

interface StatsChartProps {
  data: { name: string; total: number }[];
}

export function StatsChart({ data }: StatsChartProps) {
  const max = Math.max(...data.map(d => d.total), 1);

  return (
    <div className="h-[220px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 4, right: 0, left: -24, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="rgba(206,0,51,0.08)" />
          <XAxis
            dataKey="name"
            axisLine={false}
            tickLine={false}
            tick={{ fontSize: 10, fill: "#71717a", fontWeight: 700 }}
            dy={8}
          />
          <YAxis
            axisLine={false}
            tickLine={false}
            tick={{ fontSize: 10, fill: "#71717a" }}
            allowDecimals={false}
          />
          <Tooltip
            cursor={{ fill: "rgba(206,0,51,0.05)", radius: 8 }}
            contentStyle={{
              borderRadius: "12px",
              border: "1px solid rgba(206,0,51,0.2)",
              background: "rgba(13,13,31,0.95)",
              backdropFilter: "blur(12px)",
              color: "#f0f0ff",
              fontSize: "12px",
              fontWeight: "bold",
              boxShadow: "0 8px 32px rgba(0,0,0,0.4)",
            }}
            itemStyle={{ color: "#ff4d6d" }}
            labelStyle={{ color: "#a1a1aa", fontSize: "10px", fontWeight: 900, textTransform: "uppercase" }}
          />
          <Bar dataKey="total" radius={[6, 6, 0, 0]} barSize={28} maxBarSize={36}>
            {data.map((entry, index) => {
              const intensity = max > 0 ? entry.total / max : 0;
              const isMax = entry.total === max && max > 0;
              return (
                <Cell
                  key={`cell-${index}`}
                  fill={isMax ? "#CE0033" : `rgba(206,0,51,${0.15 + intensity * 0.4})`}
                />
              );
            })}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
