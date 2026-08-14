"use client";

import { AnimatePresence, motion } from "framer-motion";

type Props = {
  open: boolean;
  onClose: () => void;
};

export default function AboutModal({
  open,
  onClose,
}: Props) {
  return (
    <AnimatePresence>
      {open && (
        <>
          {/* BACKDROP */}
          <motion.button
            type="button"
            aria-label="Close project information"
            onClick={onClose}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-[500] cursor-default bg-black/70 backdrop-blur-md"
          />

          {/* MODAL WRAPPER */}
          <motion.div
            initial={{
              opacity: 0,
              scale: 0.97,
              y: 15,
            }}
            animate={{
              opacity: 1,
              scale: 1,
              y: 0,
            }}
            exit={{
              opacity: 0,
              scale: 0.97,
              y: 15,
            }}
            transition={{
              type: "spring",
              stiffness: 260,
              damping: 24,
            }}
            className="fixed inset-0 z-[510] flex items-center justify-center p-4 sm:p-6"
          >

            {/* MODAL */}
            <div className="relative flex max-h-[92vh] w-full max-w-4xl flex-col overflow-hidden rounded-3xl border border-cyan-400/20 bg-[#030a11]/[0.98] shadow-[0_0_80px_rgba(34,211,238,0.12)] backdrop-blur-2xl">

              {/* AMBIENT GLOW */}
              <div className="pointer-events-none absolute -left-32 -top-32 h-72 w-72 rounded-full bg-cyan-400/[0.08] blur-3xl" />

              <div className="pointer-events-none absolute -bottom-32 -right-32 h-72 w-72 rounded-full bg-cyan-400/[0.05] blur-3xl" />

              {/* =================================================
                  HEADER
              ================================================== */}

              <div className="relative shrink-0 border-b border-white/[0.07] px-6 py-5 sm:px-8">

                <div className="flex items-start justify-between gap-5">

                  <div>

                    <p className="text-[9px] font-semibold uppercase tracking-[4px] text-cyan-400">
                      Project Information
                    </p>

                    <h2 className="mt-2 text-2xl font-black tracking-tight text-white sm:text-3xl">
                      Mempool Congestion
                      <span className="text-cyan-300">
                        {" "}Intelligence
                      </span>
                    </h2>

                    <p className="mt-2 text-sm leading-5 text-slate-500">
                      Bitcoin mempool monitoring and congestion
                      intelligence visualization platform.
                    </p>

                  </div>

                  <button
                    type="button"
                    onClick={onClose}
                    aria-label="Close project information"
                    className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl border border-white/10 bg-white/[0.03] text-slate-400 transition-all duration-300 hover:border-cyan-400/40 hover:bg-cyan-400/10 hover:text-cyan-300"
                  >
                    ✕
                  </button>

                </div>

              </div>

              {/* =================================================
                  SCROLLABLE METADATA
              ================================================== */}

              <div className="relative min-h-0 flex-1 overflow-y-auto px-6 py-5 sm:px-8">

                <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">

                  <MetadataCard
                    label="Application"
                    value="POC-88 Mempool Congestion Visualizer"
                  />

                  <MetadataCard
                    label="Network"
                    value="Bitcoin Mainnet"
                  />

                  <MetadataCard
                    label="Architect"
                    value="Aswin Sankar P.S."
                    accent
                  />

                  <MetadataCard
                    label="Batch"
                    value="Batch 7"
                  />

                  <MetadataCard
                    label="Frontend"
                    value="Next.js • TypeScript • Tailwind CSS"
                  />

                  <MetadataCard
                    label="Backend"
                    value="FastAPI • Python"
                  />

                  <MetadataCard
                    label="Data Source"
                    value="Mempool.space REST API"
                  />

                  <MetadataCard
                    label="Visualization"
                    value="Interactive SVG • Bitcoin mempool congestion and fee-market analytics"
                  />

                  <MetadataCard
                    label="GitHub"
                    value="@sankeraswin579-crypto"
                  />

                  <MetadataCard
                    label="Cloud Engineering Version"
                    value="Phase 2"
                  />

                </div>

              </div>

              {/* =================================================
                  DEVELOPER SIGNATURE
              ================================================== */}

              <div className="relative shrink-0 border-t border-white/[0.07] px-6 py-5 sm:px-8">

                <div className="overflow-hidden rounded-2xl border border-cyan-400/20 bg-cyan-400/[0.035]">

                  <div className="relative p-5 text-center sm:p-6">

                    {/* CYAN ACCENT */}
                    <div className="absolute left-0 top-0 h-full w-1 bg-cyan-400" />

                    <p className="text-[9px] font-semibold uppercase tracking-[4px] text-slate-500">
                      Designed & Built By
                    </p>

                    <p className="mt-2 text-xl font-black text-cyan-300 sm:text-2xl">
                      Aswin Sankar P.S.
                    </p>

                    <p className="mt-1 text-sm text-slate-400">
                      Infocreon Internship • Batch 7
                    </p>

                    {/* STACK */}

                    <div className="mx-auto mt-4 max-w-2xl rounded-xl border border-white/[0.07] bg-black/20 px-4 py-3">

                      <p className="text-[8px] font-semibold uppercase tracking-[3px] text-slate-600">
                        Technology Stack
                      </p>

                      <p className="mt-1.5 text-xs leading-5 text-slate-300">
                        Next.js • TypeScript • Tailwind CSS •
                        FastAPI • Python • Interactive SVG
                      </p>

                    </div>

                    {/* BADGES */}

                    <div className="mt-4 flex flex-wrap items-center justify-center gap-2">

                      <span className="rounded-full border border-cyan-400/15 bg-cyan-400/5 px-3 py-1 text-[8px] uppercase tracking-[2px] text-cyan-300">
                        POC-88
                      </span>

                      <span className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1 text-[8px] uppercase tracking-[2px] text-slate-500">
                        Batch 7
                      </span>

                      <span className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1 text-[8px] uppercase tracking-[2px] text-slate-500">
                        Phase 2
                      </span>

                      <span className="rounded-full border border-white/10 bg-white/[0.03] px-3 py-1 text-[8px] uppercase tracking-[2px] text-slate-500">
                        Bitcoin Analytics
                      </span>

                    </div>

                    <p className="mt-3 text-[9px] text-slate-600">
                      GitHub: @sankeraswin579-crypto
                    </p>

                  </div>

                </div>

              </div>

            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

/* ===============================================================
   METADATA CARD
================================================================ */

function MetadataCard({
  label,
  value,
  accent = false,
}: {
  label: string;
  value: string;
  accent?: boolean;
}) {
  return (
    <div className="rounded-2xl border border-white/[0.07] bg-white/[0.02] p-4 transition-all duration-300 hover:border-cyan-400/20 hover:bg-cyan-400/[0.025]">

      <p className="text-[9px] font-semibold uppercase tracking-[2.5px] text-slate-600">
        {label}
      </p>

      <p
        className={`mt-2 text-sm leading-5 ${
          accent
            ? "font-semibold text-cyan-300"
            : "text-slate-300"
        }`}
      >
        {value}
      </p>

    </div>
  );
}