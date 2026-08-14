"use client";

import { useEffect, useState } from "react";

interface TopbarProps {
  stationCount: number;
  dataSource: string;
  isLoading: boolean;
  onAbout?: () => void;
}

export function Topbar({
  stationCount,
  dataSource,
  isLoading,
  onAbout,
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
    <header className="relative z-50 h-[72px] border-b border-white/[0.06] bg-[#02070d]/80 backdrop-blur-xl">
      
      {/* Subtle cinematic glow */}
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top_left,rgba(34,211,238,0.07),transparent_40%)]" />

      <div className="relative flex h-full items-center justify-between px-5 sm:px-8">

        {/* =====================================================
            LEFT — BRAND
        ====================================================== */}

        <div className="flex items-center gap-3">

          {/* Live indicator */}

          <div className="relative flex h-8 w-8 items-center justify-center">

            <span className="absolute h-2 w-2 animate-pulse rounded-full bg-cyan-300 shadow-[0_0_12px_rgba(34,211,238,0.9)]" />

            <span className="absolute h-6 w-6 rounded-full border border-cyan-400/20" />

          </div>

          <div>

            <p className="text-[9px] font-semibold uppercase tracking-[3px] text-cyan-400">
              Infocreon Internship
            </p>

            <h1 className="text-sm font-bold tracking-tight text-white sm:text-base">
              Mempool Congestion Intelligence
            </h1>

          </div>

        </div>

        {/* =====================================================
            RIGHT — MINIMAL METADATA
        ====================================================== */}

        <div className="flex items-center gap-3 sm:gap-5">

          {/* Live state */}

          <div className="hidden items-center gap-2 md:flex">

            <span
              className={`h-1.5 w-1.5 rounded-full ${
                isLoading
                  ? "bg-amber-400"
                  : "bg-emerald-400"
              }`}
            />

            <span className="text-[9px] uppercase tracking-[2px] text-slate-500">
              {isLoading
                ? "Syncing"
                : "Live"}
            </span>

          </div>

          {/* Transaction count */}

          <div className="hidden border-l border-white/10 pl-5 lg:block">

            <p className="text-[8px] uppercase tracking-[2px] text-slate-600">
              Pending
            </p>

            <p className="mt-0.5 text-xs font-semibold text-slate-300">
              {isLoading
                ? "—"
                : stationCount.toLocaleString()}
            </p>

          </div>

          {/* Data source */}

          <div className="hidden border-l border-white/10 pl-5 lg:block">

            <p className="text-[8px] uppercase tracking-[2px] text-slate-600">
              Data
            </p>

            <p className="mt-0.5 text-xs font-semibold text-cyan-300">
              {dataSource ===
              "Mempool.space"
                ? "MEMPOOL.SPACE"
                : dataSource}
            </p>

          </div>

          {/* Local time */}

          <div className="hidden border-l border-white/10 pl-5 xl:block">

            <p className="text-[8px] uppercase tracking-[2px] text-slate-600">
              Local Time
            </p>

            <p className="mt-0.5 font-mono text-xs text-slate-300">
              {time || "--:--:--"}
            </p>

          </div>

          {/* =================================================
              INFO BUTTON
          ================================================== */}

          <button
            type="button"
            onClick={onAbout}
            aria-label="Open project information"
            title="Project information"
            className="group flex h-9 w-9 items-center justify-center rounded-xl border border-white/10 bg-white/[0.03] text-slate-400 transition-all duration-300 hover:border-cyan-400/40 hover:bg-cyan-400/10 hover:text-cyan-300"
          >
            <span className="text-sm font-semibold">
              i
            </span>
          </button>

        </div>

      </div>

    </header>
  );
}