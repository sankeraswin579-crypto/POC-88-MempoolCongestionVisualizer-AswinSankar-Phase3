"use client";

import React from "react";

type MempoolData = {
  pendingTransactions?: number;
  mempoolSize?: number;
  congestionScore?: number;
  fastFee?: number;
  economyFee?: number;
  totalFees?: number;
  memoryUsage?: number;
  history?: number[];
};

interface MempoolVisualizerProps {
  data?: MempoolData;
}

const DEFAULT_HISTORY = [
  18, 20, 19, 23, 25, 22, 27, 30, 28, 31, 29, 26, 24, 22, 21, 20,
];

function formatNumber(value: number) {
  return new Intl.NumberFormat("en-US").format(value);
}

function getCongestionLevel(score: number) {
  if (score < 25) return "LOW";
  if (score < 50) return "MODERATE";
  if (score < 75) return "HIGH";
  return "CRITICAL";
}

function getCongestionDescription(score: number) {
  if (score < 25) {
    return "Network pressure is relatively low with favorable block-space conditions.";
  }

  if (score < 50) {
    return "Network pressure is moderate. Fee competition may increase during activity spikes.";
  }

  if (score < 75) {
    return "Network pressure is high. Users may need higher fees for faster confirmation.";
  }

  return "Network pressure is critical. Block space is highly competitive and fees may rise quickly.";
}

export default function MempoolVisualizer({
  data,
}: MempoolVisualizerProps) {
  const pendingTransactions = data?.pendingTransactions ?? 83060;
  const mempoolSize = data?.mempoolSize ?? 39.52;
  const congestionScore = data?.congestionScore ?? 20.7;
  const fastFee = data?.fastFee ?? 3;
  const economyFee = data?.economyFee ?? 1;
  const totalFees = data?.totalFees ?? 0.106351;
  const memoryUsage = data?.memoryUsage ?? 13.81;

  const history = data?.history?.length
    ? data.history
    : DEFAULT_HISTORY;

  const congestionLevel = getCongestionLevel(congestionScore);
  const description = getCongestionDescription(congestionScore);

  const chartWidth = 760;
  const chartHeight = 220;

  const maxValue = Math.max(...history, 100);

  const points = history
    .map((value, index) => {
      const x =
        (index / Math.max(history.length - 1, 1)) *
        chartWidth;

      const y =
        chartHeight -
        (value / maxValue) * (chartHeight - 30);

      return `${x},${y}`;
    })
    .join(" ");

  return (
    <section className="w-full space-y-6">

      {/* =========================================================
          HEADER
      ========================================================== */}

      <div className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.35em] text-cyan-400">
            Network Visualization
          </p>

          <h2 className="mt-2 text-2xl font-bold tracking-tight text-white md:text-3xl">
            Mempool Pressure
          </h2>

          <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-400">
            Visual analysis of Bitcoin transaction pressure, block-space
            competition and fee-market conditions.
          </p>
        </div>

        <div className="flex items-center gap-2 rounded-full border border-cyan-500/20 bg-cyan-500/5 px-4 py-2">
          <span className="h-2 w-2 animate-pulse rounded-full bg-cyan-400" />

          <span className="text-xs font-semibold uppercase tracking-[0.2em] text-cyan-300">
            Live Network
          </span>
        </div>
      </div>

      {/* =========================================================
          PRIMARY VISUALIZATION
      ========================================================== */}

      <div className="overflow-hidden rounded-2xl border border-cyan-500/20 bg-[#07111b]">

        <div className="flex flex-col gap-3 border-b border-white/5 px-5 py-5 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-slate-500">
              Congestion Trend
            </p>

            <p className="mt-1 text-lg font-semibold text-white">
              Network pressure over recent observations
            </p>
          </div>

          <div className="flex items-center gap-5 text-xs text-slate-400">
            <div className="flex items-center gap-2">
              <span className="h-2 w-2 rounded-full bg-cyan-400" />
              Congestion
            </div>

            <div>
              Current{" "}
              <span className="font-semibold text-cyan-300">
                {congestionScore.toFixed(1)}
              </span>
            </div>
          </div>
        </div>

        <div className="p-4 md:p-6">

          <div className="overflow-hidden rounded-xl border border-white/5 bg-[#050c13] p-3 md:p-5">

            <svg
              viewBox={`0 0 ${chartWidth} ${chartHeight}`}
              className="h-[220px] w-full"
              preserveAspectRatio="none"
              role="img"
              aria-label="Bitcoin mempool congestion trend"
            >

              {/* Horizontal grid */}
              {[0, 25, 50, 75, 100].map((value) => {
                const y =
                  chartHeight -
                  (value / 100) * (chartHeight - 30);

                return (
                  <g key={value}>
                    <line
                      x1="0"
                      y1={y}
                      x2={chartWidth}
                      y2={y}
                      stroke="rgba(148,163,184,0.10)"
                      strokeWidth="1"
                    />

                    <text
                      x="8"
                      y={y - 5}
                      fill="rgba(148,163,184,0.45)"
                      fontSize="10"
                    >
                      {value}
                    </text>
                  </g>
                );
              })}

              {/* Area */}
              <polygon
                points={`0,${chartHeight} ${points} ${chartWidth},${chartHeight}`}
                fill="rgba(34,211,238,0.08)"
              />

              {/* Trend line */}
              <polyline
                points={points}
                fill="none"
                stroke="#22d3ee"
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
              />

              {/* Data points */}
              {history.map((value, index) => {
                const x =
                  (index / Math.max(history.length - 1, 1)) *
                  chartWidth;

                const y =
                  chartHeight -
                  (value / maxValue) *
                    (chartHeight - 30);

                return (
                  <circle
                    key={`${value}-${index}`}
                    cx={x}
                    cy={y}
                    r="3"
                    fill="#22d3ee"
                  />
                );
              })}
            </svg>

            <div className="mt-3 flex justify-between px-2 text-[10px] uppercase tracking-[0.2em] text-slate-600">
              <span>Older</span>
              <span>Recent</span>
            </div>
          </div>
        </div>
      </div>

      {/* =========================================================
          CONGESTION INTELLIGENCE
      ========================================================== */}

      <div className="grid grid-cols-1 gap-5 lg:grid-cols-3">

        {/* Score */}
        <div className="rounded-2xl border border-cyan-500/20 bg-[#07111b] p-6 lg:col-span-2">

          <div className="flex items-start justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.28em] text-slate-500">
                Network Pressure
              </p>

              <h3 className="mt-2 text-xl font-bold text-white">
                Congestion Score
              </h3>
            </div>

            <div className="text-right">
              <div className="text-4xl font-bold text-cyan-300">
                {congestionScore.toFixed(1)}
              </div>

              <div className="text-xs text-slate-500">
                / 100
              </div>
            </div>
          </div>

          {/* Progress */}
          <div className="mt-7">

            <div className="h-3 overflow-hidden rounded-full bg-slate-800">
              <div
                className="h-full rounded-full bg-cyan-400 transition-all duration-700"
                style={{
                  width: `${Math.min(
                    Math.max(congestionScore, 0),
                    100
                  )}%`,
                }}
              />
            </div>

            <div className="mt-3 flex justify-between text-[10px] font-semibold uppercase tracking-[0.18em] text-slate-600">
              <span>Low</span>
              <span>Moderate</span>
              <span>High</span>
              <span>Critical</span>
            </div>
          </div>

          {/* Status */}
          <div className="mt-7 rounded-xl border border-white/5 bg-slate-900/40 p-5">

            <div className="flex items-center gap-3">
              <span className="h-3 w-3 rounded-full bg-cyan-400 shadow-[0_0_15px_rgba(34,211,238,0.7)]" />

              <span className="text-sm font-bold uppercase tracking-[0.2em] text-cyan-300">
                {congestionLevel}
              </span>
            </div>

            <p className="mt-3 text-sm leading-6 text-slate-400">
              {description}
            </p>
          </div>
        </div>

        {/* Quick intelligence */}
        <div className="rounded-2xl border border-cyan-500/20 bg-[#07111b] p-6">

          <p className="text-xs uppercase tracking-[0.28em] text-cyan-400">
            Live Intelligence
          </p>

          <h3 className="mt-2 text-xl font-bold text-white">
            What This Means
          </h3>

          <div className="mt-6 space-y-4">

            <div className="rounded-xl border border-white/5 bg-slate-900/40 p-4">
              <p className="text-[10px] uppercase tracking-[0.2em] text-slate-500">
                Fast Confirmation
              </p>

              <p className="mt-2 text-2xl font-bold text-cyan-300">
                {fastFee} sat/vB
              </p>
            </div>

            <div className="rounded-xl border border-white/5 bg-slate-900/40 p-4">
              <p className="text-[10px] uppercase tracking-[0.2em] text-slate-500">
                Economy Fee
              </p>

              <p className="mt-2 text-2xl font-bold text-white">
                {economyFee} sat/vB
              </p>
            </div>

          </div>
        </div>
      </div>

      {/* =========================================================
          NETWORK METRICS
      ========================================================== */}

      <div className="grid grid-cols-2 gap-4 md:grid-cols-4">

        <Metric
          label="Pending Transactions"
          value={formatNumber(pendingTransactions)}
          description="Transactions waiting"
        />

        <Metric
          label="Mempool Size"
          value={`${mempoolSize.toFixed(2)} MB`}
          description="Virtual transaction size"
        />

        <Metric
          label="Memory Usage"
          value={`${memoryUsage.toFixed(2)}%`}
          description="Node memory pressure"
        />

        <Metric
          label="Total Fees"
          value={`${totalFees.toFixed(6)} BTC`}
          description="Fees currently in mempool"
        />

      </div>

      {/* =========================================================
          DECISION SUPPORT
      ========================================================== */}

      <div className="rounded-2xl border border-cyan-500/20 bg-[#07111b] p-6 md:p-7">

        <div className="grid grid-cols-1 gap-6 md:grid-cols-[1fr_auto] md:items-center">

          <div>
            <p className="text-xs uppercase tracking-[0.3em] text-cyan-400">
              Why This Matters
            </p>

            <h3 className="mt-2 text-xl font-bold text-white md:text-2xl">
              Current network conditions are {congestionLevel.toLowerCase()}
            </h3>

            <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-400">
              The current congestion score of{" "}
              <span className="font-semibold text-cyan-300">
                {congestionScore.toFixed(1)}
              </span>{" "}
              indicates the level of competition for available Bitcoin
              block space. The fee recommendations provide a practical
              reference for choosing an appropriate confirmation priority.
            </p>
          </div>

          <div className="rounded-xl border border-cyan-500/20 bg-cyan-500/5 px-6 py-5 text-center">
            <p className="text-[10px] uppercase tracking-[0.25em] text-slate-500">
              Recommended Fast Fee
            </p>

            <p className="mt-2 text-3xl font-bold text-cyan-300">
              {fastFee}
            </p>

            <p className="text-xs text-slate-500">
              sat/vB
            </p>
          </div>

        </div>
      </div>

    </section>
  );
}


/* ===============================================================
   METRIC CARD
================================================================ */

function Metric({
  label,
  value,
  description,
}: {
  label: string;
  value: string;
  description: string;
}) {
  return (
    <div className="rounded-xl border border-cyan-500/15 bg-[#07111b] p-4 md:p-5">

      <p className="text-[10px] uppercase tracking-[0.2em] text-slate-500">
        {label}
      </p>

      <p className="mt-3 break-words text-xl font-bold text-cyan-300 md:text-2xl">
        {value}
      </p>

      <p className="mt-1 text-xs text-slate-600">
        {description}
      </p>

    </div>
  );
}