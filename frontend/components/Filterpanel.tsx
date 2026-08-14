"use client";

type Props = {
  onRefresh?: () => void;
  autoRefresh?: boolean;
  onAutoRefreshChange?: (
    value: boolean
  ) => void;
};

export default function FilterPanel({
  onRefresh,
  autoRefresh = false,
  onAutoRefreshChange,
}: Props) {
  return (
    <div className="flex items-center gap-3 rounded-2xl border border-cyan-500/20 bg-[#071019]/90 px-5 py-4 backdrop-blur-xl shadow-[0_0_30px_rgba(34,211,238,.18)]">
      {/* Network */}

      <div className="rounded-xl border border-cyan-500/20 bg-[#030712] px-4 py-2">
        <p className="text-[9px] uppercase tracking-[2px] text-slate-500">
          Network
        </p>

        <p className="text-sm font-semibold text-cyan-300">
          Bitcoin Mainnet
        </p>
      </div>

      {/* Auto Refresh */}

      <label className="flex cursor-pointer items-center gap-2 rounded-xl border border-slate-800 bg-[#030712] px-4 py-2">
        <input
          type="checkbox"
          checked={autoRefresh}
          onChange={(e) =>
            onAutoRefreshChange?.(
              e.target.checked
            )
          }
          className="accent-cyan-400"
        />

        <span className="text-xs text-slate-300">
          Auto Refresh
        </span>
      </label>

      {/* Refresh */}

      <button
        onClick={onRefresh}
        className="rounded-xl bg-cyan-600 px-4 py-2 text-xs font-semibold text-white transition hover:bg-cyan-500 hover:shadow-[0_0_20px_rgba(34,211,238,.25)]"
      >
        REFRESH
      </button>
    </div>
  );
}