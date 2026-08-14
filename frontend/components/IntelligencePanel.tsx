"use client";

import { AnimatePresence, motion } from "framer-motion";
import { useState } from "react";

type IntelligenceData = {
  congestion_level?: string;
  congestion_score?: number;
  fastest_fee?: number;
  economy_fee?: number;
  recommendation?: string;
};

type Props = {
  open?: boolean;
  onClose?: () => void;
  intelligence?: IntelligenceData | null;
  transactionCount?: number;
  mempoolSize?: number;
  congestionTrend?: string;
  congestionChange?: number;
  previousCongestionScore?: number | null;
};

const questions = [
  "Is congestion currently high?",
  "What is driving fee pressure?",
  "How severe is the mempool backlog?",
  "Are confirmation conditions improving?",
  "What should low-fee users expect?",
  "What does the current fee market indicate?",
  "What network signal should users monitor?",
  "What should users watch next?",
];

export default function IntelligencePanel({
  open = false,
  onClose,
  intelligence,
  transactionCount = 0,
  mempoolSize = 0,
  congestionTrend = "STABLE",
  congestionChange = 0,
  previousCongestionScore = null,
}: Props) {
  const [selectedQuestion, setSelectedQuestion] =
    useState<string | null>(null);

  const level =
    intelligence?.congestion_level ?? "Analyzing";

  const score =
    intelligence?.congestion_score ?? 0;

  const safeScore = Math.min(
    Math.max(score, 0),
    100
  );

  const fastestFee =
    intelligence?.fastest_fee;

  const economyFee =
    intelligence?.economy_fee;

  const getWhyThisMatters = () => {
    if (safeScore >= 80) {
      return "Critical congestion indicates strong competition for block space. Lower-fee transactions may experience significantly longer confirmation times.";
    }

    if (safeScore >= 60) {
      return "High congestion indicates increased competition for block space. Users prioritizing confirmation speed may need higher fees.";
    }

    if (safeScore >= 30) {
      return "Moderate network pressure suggests increasing competition for block space. Fee conditions should be monitored before submitting low-priority transactions.";
    }

    return "Current network pressure is relatively low, indicating less competition for available block space and generally favorable confirmation conditions.";
  };

  const getFeePressure = () => {
    if (safeScore >= 70) {
      return "HIGH";
    }

    if (safeScore >= 40) {
      return "MODERATE";
    }

    return "LOW";
  };

  const getQuestionAnswer = (
    question: string
  ) => {
    if (
      question ===
      "Is congestion currently high?"
    ) {
      return safeScore >= 60
        ? `Yes. Current congestion is ${level.toLowerCase()} with a score of ${score.toFixed(
            1
          )}/100.`
        : `No. Current congestion is ${level.toLowerCase()} with a score of ${score.toFixed(
            1
          )}/100.`;
    }

    if (
      question ===
      "What is driving fee pressure?"
    ) {
      return `Current fee pressure is ${getFeePressure().toLowerCase()}. The signal is derived from current network congestion and fee conditions.`;
    }

    if (
      question ===
      "How severe is the mempool backlog?"
    ) {
      return `The mempool currently contains approximately ${transactionCount.toLocaleString()} pending transactions with about ${(
        mempoolSize /
        (1024 * 1024)
      ).toFixed(2)} MB of virtual transaction data.`;
    }

    if (
      question ===
      "Are confirmation conditions improving?"
    ) {
      if (
        previousCongestionScore !== null &&
        congestionChange < -2
      ) {
        return `Conditions are currently improving. The congestion score has decreased by approximately ${Math.abs(
          congestionChange
        ).toFixed(1)}%.`;
      }

      if (
        previousCongestionScore !== null &&
        congestionChange > 2
      ) {
        return `Conditions are currently becoming more pressured. The congestion score has increased by approximately ${congestionChange.toFixed(
          1
        )}%.`;
      }

      return "Current conditions are relatively stable. Continue monitoring subsequent observations for a sustained change.";
    }

    if (
      question ===
      "What should low-fee users expect?"
    ) {
      if (safeScore >= 70) {
        return "Low-fee transactions may face longer confirmation times while competition for block space remains elevated.";
      }

      if (safeScore >= 40) {
        return "Low-fee transactions may experience moderate delays depending on changes in network activity.";
      }

      return "Current congestion is relatively low, so low-fee transactions may experience comparatively favorable confirmation conditions.";
    }

    if (
      question ===
      "What does the current fee market indicate?"
    ) {
      return `The current fee market shows a fastest-confirmation rate of ${
        fastestFee ?? "-"
      } sat/vB and an economy rate of ${
        economyFee ?? "-"
      } sat/vB.`;
    }

    if (
      question ===
      "What network signal should users monitor?"
    ) {
      return "Monitor pending transaction volume, congestion score, recommended fee rates, and recent block capacity.";
    }

    return "Watch the next few refresh cycles for changes in congestion, transaction volume, and fee recommendations.";
  };

  return (
    <AnimatePresence>
      {open && (
        <>
          {/* =====================================================
              BACKDROP
          ====================================================== */}

          <motion.button
            type="button"
            aria-label="Close intelligence panel"
            onClick={onClose}
            initial={{
              opacity: 0,
            }}
            animate={{
              opacity: 1,
            }}
            exit={{
              opacity: 0,
            }}
            transition={{
              duration: 0.25,
            }}
            className="fixed inset-0 z-[80] cursor-default bg-black/45 backdrop-blur-[2px]"
          />

          {/* =====================================================
              CINEMATIC INTELLIGENCE RAIL
          ====================================================== */}

          <motion.aside
            initial={{
              x: "100%",
              opacity: 0,
            }}
            animate={{
              x: 0,
              opacity: 1,
            }}
            exit={{
              x: "100%",
              opacity: 0,
            }}
            transition={{
              type: "spring",
              stiffness: 280,
              damping: 30,
            }}
            className="fixed right-0 top-0 z-[90] flex h-screen w-full flex-col border-l border-cyan-400/20 bg-[#030a11]/95 shadow-[-30px_0_80px_rgba(0,0,0,0.55)] backdrop-blur-2xl sm:w-[460px] lg:w-[520px]"
          >
            {/* =================================================
                TOP BAR
            ================================================== */}

            <div className="flex shrink-0 items-center justify-between border-b border-white/10 px-5 py-5">

              <div className="flex items-center gap-3">

                <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-cyan-400/20 bg-cyan-400/10">

                  <span className="h-2.5 w-2.5 animate-pulse rounded-full bg-cyan-300 shadow-[0_0_14px_rgba(34,211,238,0.8)]" />

                </div>

                <div>

                  <p className="text-[9px] font-semibold uppercase tracking-[3px] text-cyan-400">
                    Live Analysis
                  </p>

                  <h2 className="mt-1 text-lg font-black tracking-tight text-white">
                    Mempool Intelligence
                  </h2>

                </div>

              </div>

              <button
                type="button"
                onClick={onClose}
                aria-label="Close intelligence panel"
                className="flex h-9 w-9 items-center justify-center rounded-xl border border-white/10 bg-white/[0.03] text-slate-400 transition-all hover:border-cyan-400/40 hover:bg-cyan-400/10 hover:text-cyan-300"
              >
                ✕
              </button>

            </div>

            {/* =================================================
                SCROLLABLE CONTENT
            ================================================== */}

            <div className="min-h-0 flex-1 overflow-y-auto px-5 pb-8 pt-5">

              {/* Network status */}

              <div className="rounded-2xl border border-emerald-500/20 bg-emerald-500/[0.06] p-4">

                <div className="flex items-center justify-between">

                  <div>

                    <p className="text-[9px] uppercase tracking-[3px] text-emerald-300">
                      Network Status
                    </p>

                    <p className="mt-1 text-sm font-bold text-white">
                      ONLINE • Bitcoin Mainnet
                    </p>

                  </div>

                  <span className="h-2 w-2 animate-pulse rounded-full bg-emerald-400 shadow-[0_0_12px_rgba(52,211,153,0.8)]" />

                </div>

              </div>

              {/* =================================================
                  CONGESTION
              ================================================== */}

              <div className="mt-4 rounded-2xl border border-cyan-400/15 bg-[#07131e]/80 p-5">

                <div className="flex items-center justify-between">

                  <div>

                    <p className="text-[9px] uppercase tracking-[3px] text-slate-500">
                      Congestion Level
                    </p>

                    <p className="mt-2 text-3xl font-black uppercase text-cyan-300">
                      {level}
                    </p>

                  </div>

                  <div className="text-right">

                    <p className="text-3xl font-black text-white">
                      {score.toFixed(1)}
                    </p>

                    <p className="text-[10px] uppercase tracking-[2px] text-slate-600">
                      / 100
                    </p>

                  </div>

                </div>

                <div className="mt-5 h-2 overflow-hidden rounded-full bg-slate-900">

                  <motion.div
                    initial={{
                      width: 0,
                    }}
                    animate={{
                      width: `${safeScore}%`,
                    }}
                    transition={{
                      duration: 0.7,
                    }}
                    className="h-full rounded-full bg-cyan-400 shadow-[0_0_15px_rgba(34,211,238,0.35)]"
                  />

                </div>

                <div className="mt-2 flex justify-between text-[8px] uppercase tracking-[2px] text-slate-700">
                  <span>Low</span>
                  <span>Moderate</span>
                  <span>High</span>
                  <span>Critical</span>
                </div>

              </div>

              {/* =================================================
                  LIVE TREND
              ================================================== */}

              <div className="mt-4 grid grid-cols-2 gap-3">

                <div className="rounded-2xl border border-white/5 bg-white/[0.02] p-4">

                  <p className="text-[9px] uppercase tracking-[2px] text-slate-600">
                    Trend
                  </p>

                  <p className="mt-2 text-sm font-black text-cyan-300">
                    {congestionTrend}
                  </p>

                </div>

                <div className="rounded-2xl border border-white/5 bg-white/[0.02] p-4">

                  <p className="text-[9px] uppercase tracking-[2px] text-slate-600">
                    Change
                  </p>

                  <p
                    className={`mt-2 text-sm font-black ${
                      congestionChange > 2
                        ? "text-amber-300"
                        : congestionChange < -2
                        ? "text-emerald-300"
                        : "text-cyan-300"
                    }`}
                  >
                    {congestionChange > 0
                      ? "+"
                      : ""}
                    {congestionChange.toFixed(
                      1
                    )}
                    %
                  </p>

                </div>

              </div>

              {/* =================================================
                  WHY THIS MATTERS
              ================================================== */}

              <div className="mt-4 rounded-2xl border border-cyan-400/15 bg-[#07131e]/80 p-5">

                <p className="text-[9px] uppercase tracking-[3px] text-slate-500">
                  Why This Matters
                </p>

                <p className="mt-3 text-sm leading-6 text-slate-300">
                  {getWhyThisMatters()}
                </p>

              </div>

              {/* =================================================
                  FEES
              ================================================== */}

              <div className="mt-4 grid grid-cols-2 gap-3">

                <Info
                  label="Fast Confirmation"
                  value={
                    fastestFee !== undefined
                      ? `${fastestFee} sat/vB`
                      : "-"
                  }
                />

                <Info
                  label="Economy Fee"
                  value={
                    economyFee !== undefined
                      ? `${economyFee} sat/vB`
                      : "-"
                  }
                />

              </div>

              {/* =================================================
                  FEE MARKET
              ================================================== */}

              <div className="mt-4 rounded-2xl border border-cyan-400/15 bg-[#07131e]/80 p-5">

                <div className="flex items-center justify-between">

                  <p className="text-[9px] uppercase tracking-[3px] text-slate-500">
                    Fee Market Signal
                  </p>

                  <span className="rounded-full border border-cyan-400/20 bg-cyan-400/5 px-2 py-1 text-[8px] uppercase tracking-[2px] text-cyan-300">
                    {getFeePressure()}
                  </span>

                </div>

                <div className="mt-4 flex items-center justify-between">

                  <span className="text-sm text-slate-400">
                    Current Pressure
                  </span>

                  <span className="font-bold text-cyan-300">
                    {getFeePressure()}
                  </span>

                </div>

                <p className="mt-3 text-xs leading-5 text-slate-600">
                  Fee pressure is interpreted from current
                  congestion and network conditions.
                </p>

              </div>

              {/* =================================================
                  INTELLIGENCE SUMMARY
              ================================================== */}

              <div className="mt-4 rounded-2xl border border-cyan-400/15 bg-[#07131e]/80 p-5">

                <p className="text-[9px] uppercase tracking-[3px] text-slate-500">
                  Intelligence Summary
                </p>

                <p className="mt-3 text-sm leading-7 text-slate-300">
                  {intelligence?.recommendation ??
                    "Analyzing current Bitcoin network conditions..."}
                </p>

              </div>

              {/* =================================================
                  WHAT TO WATCH
              ================================================== */}

              <div className="mt-4 rounded-2xl border border-cyan-400/20 bg-cyan-400/[0.04] p-5">

                <p className="text-[9px] uppercase tracking-[3px] text-cyan-300">
                  What To Watch
                </p>

                <ul className="mt-4 space-y-3 text-xs leading-5 text-slate-400">

                  <li className="flex gap-3">
                    <span className="text-cyan-400">
                      01
                    </span>
                    <span>
                      Pending transaction volume
                    </span>
                  </li>

                  <li className="flex gap-3">
                    <span className="text-cyan-400">
                      02
                    </span>
                    <span>
                      Recommended fee rates
                    </span>
                  </li>

                  <li className="flex gap-3">
                    <span className="text-cyan-400">
                      03
                    </span>
                    <span>
                      Congestion score changes
                    </span>
                  </li>

                  <li className="flex gap-3">
                    <span className="text-cyan-400">
                      04
                    </span>
                    <span>
                      Recent block capacity
                    </span>
                  </li>

                </ul>

              </div>

              {/* =================================================
                  QUESTIONS
              ================================================== */}

              <div className="mt-4 rounded-2xl border border-white/5 bg-white/[0.02] p-5">

                <p className="text-[9px] uppercase tracking-[3px] text-cyan-300">
                  Intelligence Questions
                </p>

                <div className="mt-4 space-y-2">

                  {questions.map(
                    (question) => (
                      <button
                        key={question}
                        type="button"
                        onClick={() =>
                          setSelectedQuestion(
                            selectedQuestion ===
                              question
                              ? null
                              : question
                          )
                        }
                        className="w-full rounded-xl border border-slate-800/80 bg-black/20 px-3 py-3 text-left text-xs text-slate-300 transition hover:border-cyan-400/30 hover:bg-cyan-400/[0.04] hover:text-cyan-300"
                      >

                        <div className="flex items-center justify-between gap-3">

                          <span>
                            {question}
                          </span>

                          <span className="shrink-0 text-cyan-500">
                            {selectedQuestion ===
                            question
                              ? "−"
                              : "+"}
                          </span>

                        </div>

                        <AnimatePresence>
                          {selectedQuestion ===
                            question && (
                            <motion.p
                              initial={{
                                height: 0,
                                opacity: 0,
                              }}
                              animate={{
                                height: "auto",
                                opacity: 1,
                              }}
                              exit={{
                                height: 0,
                                opacity: 0,
                              }}
                              className="mt-3 overflow-hidden border-t border-slate-800 pt-3 leading-5 text-slate-400"
                            >
                              {getQuestionAnswer(
                                question
                              )}
                            </motion.p>
                          )}
                        </AnimatePresence>

                      </button>
                    )
                  )}

                </div>

              </div>

            </div>

            {/* =================================================
                BOTTOM STATUS
            ================================================== */}

            <div className="shrink-0 border-t border-white/10 bg-black/20 px-5 py-4">

              <div className="flex items-center justify-between text-[9px] uppercase tracking-[2px]">

                <span className="text-slate-600">
                  Infocreon Intelligence Layer
                </span>

                <span className="text-cyan-500">
                  POC-88
                </span>

              </div>

            </div>

          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
}

/* ===============================================================
   INFO COMPONENT
================================================================ */

function Info({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl border border-white/5 bg-white/[0.02] px-4 py-4">

      <p className="text-[9px] uppercase tracking-[2px] text-slate-600">
        {label}
      </p>

      <p className="mt-2 text-sm font-bold text-white">
        {value}
      </p>

    </div>
  );
}