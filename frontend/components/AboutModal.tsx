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
        <motion.div
          initial={{
            opacity: 0,
          }}
          animate={{
            opacity: 1,
          }}
          exit={{
            opacity: 0,
          }}
          className="fixed inset-0 z-[500] flex items-center justify-center bg-black/70 p-6 backdrop-blur-sm"
        >
          <motion.div
            initial={{
              scale: 0.95,
              y: 20,
            }}
            animate={{
              scale: 1,
              y: 0,
            }}
            exit={{
              scale: 0.95,
              y: 20,
            }}
            className="w-full max-w-3xl rounded-3xl border border-cyan-500/30 bg-[#071019] p-8 shadow-[0_0_40px_rgba(34,211,238,.25)]"
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-xs uppercase tracking-[4px] text-cyan-300">
                  About / Metadata
                </p>

                <h2 className="mt-2 text-3xl font-black text-white">
                  Mempool Pulse
                </h2>

                <p className="text-slate-400">
                  Bitcoin Mempool Congestion
                  Intelligence Platform
                </p>
              </div>

              <button
                onClick={onClose}
                className="rounded-xl border border-cyan-500/30 px-3 py-2 text-slate-300 transition hover:bg-cyan-500 hover:text-white"
              >
                ✕
              </button>
            </div>

            <div className="mt-8 grid grid-cols-1 gap-5 md:grid-cols-2">
              <Card
                title="Application"
                value="POC-88 Mempool Congestion Visualizer"
              />

              <Card
                title="Network"
                value="Bitcoin Mainnet"
              />

              <Card
                title="Developer"
                value="Aswin Sankar P.S."
              />

              <Card
                title="Program"
                value="Real Rails Internship • Batch 7"
              />

              <Card
                title="Frontend"
                value="Next.js • TypeScript • Tailwind CSS"
              />

              <Card
                title="Backend"
                value="FastAPI • Python"
              />

              <Card
                title="Data Source"
                value="Mempool.space REST API"
              />

              <Card
                title="Project Purpose"
                value="Visualize Bitcoin mempool congestion, fee pressure, transaction activity and recent block data."
              />
            </div>

            <div className="mt-8 rounded-2xl border border-cyan-500/20 bg-[#0b1722] p-5 text-center">
              <p className="text-xs uppercase tracking-[4px] text-slate-400">
                Designed & Built By
              </p>

              <p className="mt-2 text-xl font-bold text-cyan-300">
                Aswin Sankar P.S.
              </p>

              <p className="mt-1 text-sm text-slate-400">
                Real Rails Internship • Batch 7
              </p>

              <p className="mt-2 text-[11px] uppercase tracking-[3px] text-cyan-400">
                POC-88 • Mempool Congestion Visualizer
              </p>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

function Card({
  title,
  value,
}: {
  title: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl border border-cyan-500/20 bg-[#0b1722] p-4">
      <p className="text-[11px] uppercase tracking-[3px] text-slate-400">
        {title}
      </p>

      <p className="mt-2 text-sm text-white">
        {value}
      </p>
    </div>
  );
}