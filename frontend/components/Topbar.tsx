"use client";

import { useEffect, useState } from "react";

interface TopbarProps {
  stationCount: number;
  dataSource: string;
  isLoading: boolean;
}

export function Topbar({
  stationCount,
  dataSource,
  isLoading,
}: TopbarProps) {
  const [time, setTime] = useState("");

  useEffect(() => {
    const update = () => {
      setTime(
        new Date().toLocaleTimeString([], {
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        })
      );
    };

    update();

    const timer = setInterval(update, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <header className="relative h-24 overflow-hidden border-b border-cyan-500/30 bg-gradient-to-r from-[#030712] via-[#071827] to-[#020617] shadow-[0_0_40px_rgba(34,211,238,.25)]">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,#22d3ee15,transparent_70%)]" />

      <div className="relative z-10 flex h-full items-center justify-between px-8">
        {/* LEFT */}

        <div className="flex items-center gap-5">
          <div className="relative">
            <div className="h-5 w-5 rounded-full bg-cyan-400 animate-pulse" />

            <div className="absolute inset-0 rounded-full border border-cyan-300 animate-ping" />
          </div>

          <div>
            <p className="text-xs uppercase tracking-[6px] text-cyan-300">
              Bitcoin Network Command Center
            </p>

            <h1 className="text-3xl font-black tracking-[5px] text-white">
              MEMPOOL PULSE
            </h1>

            <p className="text-sm uppercase tracking-[4px] text-slate-400">
              Real-Time Congestion Intelligence
            </p>
          </div>
        </div>

        {/* RIGHT */}

        <div className="flex gap-4">
          <StatusCard
            title="Transactions"
            value={
              isLoading
                ? "Loading..."
                : stationCount.toLocaleString()
            }
          />

          <StatusCard
            title="Source"
            value={
              dataSource === "Mempool.space"
                ? "LIVE"
                : "LOCAL"
            }
          />

          <StatusCard
            title="Status"
            value={isLoading ? "SYNCING" : "ONLINE"}
          />

          <StatusCard
            title="Local Time"
            value={time}
          />
        </div>
      </div>
    </header>
  );
}

function StatusCard({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <div className="min-w-[130px] rounded-2xl border border-cyan-500/20 bg-[#071019]/90 px-5 py-3 backdrop-blur-xl shadow-[0_0_25px_rgba(34,211,238,.12)] transition-all duration-300 hover:scale-105 hover:border-cyan-300">
      <p className="text-[10px] uppercase tracking-[3px] text-slate-400">
        {title}
      </p>

      <p className="mt-1 text-xl font-bold text-cyan-300">
        {value}
      </p>
    </div>
  );
}