"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";

type FeeBucket = {
  fee_rate: number;
  vsize: number;
};

type Props = {
  data?: FeeBucket[];
};

export default function MempoolChart({
  data = [],
}: Props) {
  const chartData = data
    .slice(0, 20)
    .map((item) => ({
      feeRate: item.fee_rate,
      vsize: Math.round(
        item.vsize / 1000
      ),
    }));

  return (
    <div className="h-full w-full rounded-2xl border border-cyan-500/20 bg-[#071019] p-6">
      <div className="mb-5">
        <p className="text-[10px] uppercase tracking-[3px] text-slate-500">
          Mempool Analytics
        </p>

        <h2 className="mt-1 text-xl font-bold text-cyan-300">
          Fee Rate Distribution
        </h2>

        <p className="mt-1 text-xs text-slate-500">
          Virtual transaction volume by fee rate
        </p>
      </div>

      <div className="h-[300px]">
        {chartData.length === 0 ? (
          <div className="flex h-full items-center justify-center text-sm text-slate-500">
            Waiting for mempool data...
          </div>
        ) : (
          <ResponsiveContainer
            width="100%"
            height="100%"
          >
            <BarChart data={chartData}>
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#1e293b"
              />

              <XAxis
                dataKey="feeRate"
                tick={{
                  fill: "#94a3b8",
                  fontSize: 11,
                }}
                label={{
                  value: "sat/vB",
                  position: "insideBottom",
                  offset: -5,
                  fill: "#64748b",
                }}
              />

              <YAxis
                tick={{
                  fill: "#94a3b8",
                  fontSize: 11,
                }}
                label={{
                  value: "vKB",
                  angle: -90,
                  position: "insideLeft",
                  fill: "#64748b",
                }}
              />

              <Tooltip
                contentStyle={{
                  backgroundColor: "#071019",
                  border:
                    "1px solid rgba(34,211,238,.25)",
                  borderRadius: "12px",
                  color: "#fff",
                }}
                formatter={(value) => [
                  `${value} KB`,
                  "Mempool Volume",
                ]}
                labelFormatter={(label) =>
                  `${label} sat/vB`
                }
              />

              <Bar
                dataKey="vsize"
                fill="#22d3ee"
                radius={[4, 4, 0, 0]}
              />
            </BarChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
}