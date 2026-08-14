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
  open = true,
  onClose,
  intelligence,
  transactionCount = 0,
  mempoolSize = 0,
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
    if (question === "Is congestion currently high?") {
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
      return "Current conditions should be evaluated against previous observations. A sustained decline in transaction volume and fee pressure would indicate improving confirmation conditions.";
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
        <motion.aside
          initial={{
            x: 40,
            opacity: 0,
          }}
          animate={{
            x: 0,
            opacity: 1,
          }}
          exit={{
            x: 40,
            opacity: 0,
          }}
          transition={{
            duration: 0.35,
          }}
          className="h-full w-full rounded-2xl border border-cyan-500/20 bg-[#071019]/95 p-6 backdrop-blur-xl"
        >
          {/* HEADER */}

          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs uppercase tracking-[4px] text-cyan-300">
                Live Analysis
              </p>

              <h2 className="mt-2 text-2xl font-black text-white">
                Mempool Intelligence
              </h2>
            </div>

            {onClose && (
              <button
                onClick={onClose}
                aria-label="Close intelligence panel"
                className="rounded-lg border border-cyan-500/30 px-3 py-1 text-slate-300 transition hover:bg-cyan-500 hover:text-white"
              >
                ✕
              </button>
            )}
          </div>

          {/* NETWORK STATUS */}

          <div className="mt-5 rounded-xl border border-emerald-500/30 bg-emerald-500/10 p-4">
            <p className="text-xs uppercase tracking-[3px] text-emerald-300">
              Network Status
            </p>

            <p className="mt-1 font-bold text-white">
              ONLINE • Bitcoin Mainnet
            </p>
          </div>

          {/* CONGESTION */}

          <div className="mt-5 rounded-xl border border-cyan-500/20 bg-[#0b1722] p-5">
            <div className="flex items-center justify-between">
              <p className="text-xs uppercase tracking-[3px] text-slate-400">
                Congestion Level
              </p>

              <span className="rounded-full border border-cyan-500/20 bg-cyan-500/5 px-2 py-1 text-[10px] uppercase tracking-[2px] text-cyan-300">
                LIVE
              </span>
            </div>

            <div className="mt-3 flex items-end justify-between">
              <p className="text-3xl font-black text-cyan-300">
                {level}
              </p>

              <p className="text-lg font-bold text-white">
                {score.toFixed(1)}
                <span className="text-xs text-slate-500">
                  {" "}
                  / 100
                </span>
              </p>
            </div>

            <div className="mt-4 h-2 overflow-hidden rounded-full bg-slate-800">
              <div
                className="h-full rounded-full bg-cyan-400 transition-all duration-500"
                style={{
                  width: `${safeScore}%`,
                }}
              />
            </div>

            <div className="mt-2 flex justify-between text-[9px] uppercase tracking-[2px] text-slate-600">
              <span>Low</span>
              <span>Moderate</span>
              <span>High</span>
              <span>Critical</span>
            </div>
          </div>

          {/* WHY THIS MATTERS */}

          <div className="mt-5 rounded-xl border border-cyan-500/20 bg-[#0b1722] p-5">
            <p className="text-xs uppercase tracking-[3px] text-slate-400">
              Why This Matters
            </p>

            <p className="mt-3 text-sm leading-6 text-slate-300">
              {getWhyThisMatters()}
            </p>
          </div>

          {/* FEES */}

          <div className="mt-5 space-y-3">
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

          {/* FEE MARKET SIGNAL */}

          <div className="mt-5 rounded-xl border border-cyan-500/20 bg-[#0b1722] p-5">
            <p className="text-xs uppercase tracking-[3px] text-slate-400">
              Fee Market Signal
            </p>

            <div className="mt-3 flex items-center justify-between">
              <span className="text-sm text-slate-400">
                Current Pressure
              </span>

              <span className="font-bold text-cyan-300">
                {getFeePressure()}
              </span>
            </div>

            <p className="mt-2 text-xs leading-5 text-slate-500">
              Fee pressure is interpreted from current
              congestion and network conditions.
            </p>
          </div>

          {/* INTELLIGENCE SUMMARY */}

          <div className="mt-5 rounded-xl border border-cyan-500/20 bg-[#0b1722] p-5">
            <p className="text-xs uppercase tracking-[3px] text-slate-400">
              Intelligence Summary
            </p>

            <p className="mt-3 text-sm leading-7 text-slate-300">
              {intelligence?.recommendation ??
                "Analyzing current Bitcoin network conditions..."}
            </p>
          </div>

          {/* WHAT TO WATCH */}

          <div className="mt-5 rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-5">
            <p className="text-xs uppercase tracking-[3px] text-cyan-300">
              What To Watch
            </p>

            <ul className="mt-3 space-y-2 text-xs leading-5 text-slate-400">
              <li>
                • Pending transaction volume
              </li>

              <li>
                • Recommended fee rates
              </li>

              <li>
                • Congestion score changes
              </li>

              <li>
                • Recent block capacity
              </li>
            </ul>
          </div>

          {/* INTELLIGENCE QUESTIONS */}

          <div className="mt-5 rounded-xl border border-cyan-500/20 bg-[#0b1722] p-5">
            <p className="text-xs uppercase tracking-[3px] text-cyan-300">
              Intelligence Questions
            </p>

            <div className="mt-4 space-y-2">
              {questions.map((question) => (
                <button
                  key={question}
                  onClick={() =>
                    setSelectedQuestion(
                      selectedQuestion === question
                        ? null
                        : question
                    )
                  }
                  className="w-full rounded-lg border border-slate-800 bg-black/20 px-3 py-3 text-left text-xs text-slate-300 transition hover:border-cyan-500/40 hover:bg-cyan-500/5 hover:text-cyan-300"
                >
                  <div className="flex items-center justify-between gap-3">
                    <span>{question}</span>

                    <span className="text-cyan-500">
                      {selectedQuestion === question
                        ? "−"
                        : "+"}
                    </span>
                  </div>

                  {selectedQuestion === question && (
                    <p className="mt-3 border-t border-slate-800 pt-3 leading-5 text-slate-400">
                      {getQuestionAnswer(
                        question
                      )}
                    </p>
                  )}
                </button>
              ))}
            </div>
          </div>
        </motion.aside>
      )}
    </AnimatePresence>
  );
}

// ======================================================
// INFO COMPONENT
// ======================================================

function Info({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-slate-800 bg-[#0b1722] px-4 py-3">
      <p className="text-xs uppercase tracking-[2px] text-slate-500">
        {label}
      </p>

      <p className="mt-1 text-white">
        {value}
      </p>
    </div>
  );
}