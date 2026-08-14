"use client";

type Props = {
  congestion?: {
    score?: number;
    level?: string;
    transaction_count?: number;
    virtual_size?: number;
    memory_usage_percent?: number;
  } | null;

  fees?: {
    fastest?: number;
    half_hour?: number;
    hour?: number;
    economy?: number;
    minimum?: number;
  } | null;

  onRefresh?: () => void;
};

export function Sidebar({
  congestion,
  fees,
  onRefresh,
}: Props) {
  return (
    <aside className="flex h-full w-[340px] flex-col border-l border-cyan-400/20 bg-[#050b12]/95 text-white shadow-2xl backdrop-blur-xl">

      {/* ================= HEADER ================= */}
      <div className="border-b border-cyan-400/10 px-6 py-6">

        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-xl border border-cyan-400/30 bg-cyan-400/10 text-xl text-cyan-300 shadow-[0_0_25px_rgba(34,211,238,.15)]">
            ◈
          </div>

          <div>
            <p className="text-[10px] font-bold uppercase tracking-[3px] text-cyan-400">
              Project
            </p>

            <h1 className="text-lg font-black tracking-wide text-white">
              Intelligence
            </h1>
          </div>
        </div>

        <div className="mt-5 flex items-center justify-between rounded-xl border border-emerald-400/20 bg-emerald-400/5 px-4 py-3">
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-400" />

            <span className="text-xs font-semibold text-emerald-300">
              SYSTEM ONLINE
            </span>
          </div>

          <span className="text-[10px] uppercase tracking-widest text-slate-500">
            LIVE
          </span>
        </div>
      </div>

      {/* ================= CONTENT ================= */}
      <div className="flex-1 overflow-y-auto px-5 py-5">

        {/* Navigation */}
        <section>
          <p className="mb-3 px-2 text-[10px] font-bold uppercase tracking-[3px] text-slate-600">
            Intelligence
          </p>

          <div className="space-y-1">

            <NavItem
              icon="⌂"
              label="Dashboard"
            />

            <NavItem
              icon="⚡"
              label="Mempool Monitor"
              active
            />

            <NavItem
              icon="◉"
              label="Network Activity"
            />

            <NavItem
              icon="◫"
              label="Analytics"
            />

            <NavItem
              icon="⚠"
              label="Alerts"
            />

          </div>
        </section>

        {/* Current Project */}
        <section className="mt-7">

          <p className="mb-3 px-2 text-[10px] font-bold uppercase tracking-[3px] text-slate-600">
            Current Project
          </p>

          <div className="rounded-2xl border border-cyan-400/20 bg-gradient-to-br from-cyan-400/10 to-transparent p-4">

            <div className="flex items-start justify-between">

              <div>
                <p className="text-[10px] uppercase tracking-widest text-cyan-400">
                  POC-88
                </p>

                <h2 className="mt-1 text-base font-bold text-white">
                  Mempool Pulse
                </h2>

                <p className="mt-1 text-xs leading-relaxed text-slate-500">
                  Bitcoin Congestion Intelligence
                </p>
              </div>

              <span className="rounded-lg border border-emerald-400/20 bg-emerald-400/10 px-2 py-1 text-[9px] font-bold text-emerald-300">
                ACTIVE
              </span>

            </div>

          </div>
        </section>

        {/* Live Metrics */}
        <section className="mt-7">

          <div className="mb-3 flex items-center justify-between px-2">

            <p className="text-[10px] font-bold uppercase tracking-[3px] text-slate-600">
              Live Intelligence
            </p>

            <span className="text-[9px] uppercase tracking-widest text-cyan-500">
              BTC
            </span>

          </div>

          <div className="grid grid-cols-2 gap-3">

            <MetricCard
              label="Congestion"
              value={congestion?.level ?? "N/A"}
              accent
            />

            <MetricCard
              label="Score"
              value={`${(congestion?.score ?? 0).toFixed(1)} / 100`}
            />

            <MetricCard
              label="Transactions"
              value={(congestion?.transaction_count ?? 0).toLocaleString()}
            />

            <MetricCard
              label="Memory"
              value={`${(
                congestion?.memory_usage_percent ?? 0
              ).toFixed(1)}%`}
            />

          </div>
        </section>

        {/* Recommended Fees */}
        <section className="mt-7 border-t border-cyan-400/10 pt-6">

          <div className="mb-4 flex items-center justify-between">

            <p className="text-[10px] font-bold uppercase tracking-[3px] text-slate-600">
              Fee Intelligence
            </p>

            <span className="text-[9px] text-slate-600">
              sat/vB
            </span>

          </div>

          <div className="space-y-2">

            <FeeRow
              label="Fastest"
              value={fees?.fastest}
            />

            <FeeRow
              label="30 Minutes"
              value={fees?.half_hour}
            />

            <FeeRow
              label="1 Hour"
              value={fees?.hour}
            />

            <FeeRow
              label="Economy"
              value={fees?.economy}
            />

          </div>

        </section>

        {/* Refresh */}
        <section className="mt-7">

          <button
            onClick={onRefresh}
            className="group flex w-full items-center justify-center gap-3 rounded-xl border border-cyan-400/30 bg-cyan-400/10 py-3 text-xs font-bold uppercase tracking-[2px] text-cyan-300 transition-all duration-300 hover:border-cyan-300 hover:bg-cyan-400/20 hover:shadow-[0_0_25px_rgba(34,211,238,.15)]"
          >

            <span className="text-base transition-transform duration-500 group-hover:rotate-180">
              ↻
            </span>

            Refresh Intelligence

          </button>

          <p className="mt-3 text-center text-[9px] uppercase tracking-widest text-slate-600">
            Update network intelligence
          </p>

        </section>

      </div>

      {/* ================= FOOTER ================= */}
      <div className="border-t border-cyan-400/10 bg-[#040910] px-6 py-5">

        <div className="flex items-center gap-3">

          <div className="flex h-10 w-10 items-center justify-center rounded-full border border-cyan-400/20 bg-cyan-400/10 text-sm font-black text-cyan-300">
            AS
          </div>

          <div className="min-w-0">

            <p className="truncate text-sm font-bold text-white">
              Aswin Sankar P.S.
            </p>

            <p className="text-[9px] uppercase tracking-widest text-slate-500">
              Project Developer
            </p>

          </div>

        </div>

        <div className="mt-4 flex items-center justify-between">

          <span className="text-[9px] uppercase tracking-[2px] text-slate-600">
            Real Rails • Batch 7
          </span>

          <span className="text-[9px] font-bold text-cyan-500">
            POC-88
          </span>

        </div>

      </div>

    </aside>
  );
}


/* =========================================================
   NAVIGATION ITEM
========================================================= */

function NavItem({
  icon,
  label,
  active = false,
}: {
  icon: string;
  label: string;
  active?: boolean;
}) {
  return (
    <button
      className={`group flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left transition-all duration-200 ${
        active
          ? "border border-cyan-400/20 bg-cyan-400/10 text-cyan-300 shadow-[inset_3px_0_0_rgba(34,211,238,.8)]"
          : "border border-transparent text-slate-500 hover:bg-white/[0.03] hover:text-slate-200"
      }`}
    >
      <span
        className={`flex h-8 w-8 items-center justify-center rounded-lg text-sm ${
          active
            ? "bg-cyan-400/10 text-cyan-300"
            : "bg-white/[0.03] text-slate-600 group-hover:text-slate-300"
        }`}
      >
        {icon}
      </span>

      <span className="text-xs font-semibold">
        {label}
      </span>

      {active && (
        <span className="ml-auto h-1.5 w-1.5 rounded-full bg-cyan-300 shadow-[0_0_10px_rgba(34,211,238,.8)]" />
      )}
    </button>
  );
}


/* =========================================================
   METRIC CARD
========================================================= */

function MetricCard({
  label,
  value,
  accent,
}: {
  label: string;
  value: string;
  accent?: boolean;
}) {
  return (
    <div className="group relative overflow-hidden rounded-xl border border-cyan-400/10 bg-[#08121c] p-3 transition-all duration-300 hover:border-cyan-300/40 hover:bg-cyan-400/[0.03]">

      <p
        className={`truncate text-lg font-black ${
          accent ? "text-cyan-300" : "text-white"
        }`}
      >
        {value}
      </p>

      <div className="mt-3 h-px w-full bg-cyan-400/10">
        <div className="h-full w-3/4 bg-cyan-400/50" />
      </div>

      <p className="mt-2 text-[9px] uppercase tracking-[2px] text-slate-500">
        {label}
      </p>

    </div>
  );
}


/* =========================================================
   FEE ROW
========================================================= */

function FeeRow({
  label,
  value,
}: {
  label: string;
  value?: number;
}) {
  return (
    <div className="flex items-center justify-between rounded-xl border border-cyan-400/10 bg-[#08121c] px-4 py-3 transition hover:border-cyan-400/30">

      <span className="text-xs text-slate-500">
        {label}
      </span>

      <span className="font-bold text-cyan-300">
        {value ?? 0}

        <span className="ml-1 text-[9px] font-normal text-slate-600">
          sat/vB
        </span>
      </span>

    </div>
  );
}