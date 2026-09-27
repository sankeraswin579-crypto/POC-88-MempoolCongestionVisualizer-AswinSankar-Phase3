"use client";

import Link from "next/link";

import {
  useCallback,
  useEffect,
  useState,
} from "react";

import { Topbar } from "@/components/Topbar";
import MempoolVisualizer from "@/components/MempoolVisualizer";
import MempoolChart from "@/components/MempoolChart";
import IntelligencePanel from "@/components/IntelligencePanel";
import AboutModal from "@/components/AboutModal";

const API =
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  "http://127.0.0.1:8000";

/* =========================================================
   TYPES
========================================================= */

type MempoolData = {
  count?: number;
  vsize?: number;
  total_fee?: number;
  total_fee_rate?: number;
  memory_usage?: number;
};

type CongestionData = {
  score?: number;
  level?: string;
  transaction_count?: number;
  virtual_size?: number;
  memory_usage_percent?: number;
};

type IntelligenceData = {
  congestion_score?: number;
  congestion_level?: string;
  recommendation?: string;
  fastest_fee?: number;
  economy_fee?: number;
};

type FeeData = {
  fastest?: number;
  half_hour?: number;
  hour?: number;
  economy?: number;
  minimum?: number;
};

/*
 * IMPORTANT:
 * This type matches the actual MempoolChart.tsx component.
 */
type FeeBucket = {
  fee_rate: number;
  vsize: number;
};

/*
 * Backend /api/mempool/blocks response fields.
 *
 * The verified backend response contains:
 *   blockSize
 *   blockVSize
 *   nTx
 *   totalFees
 *   medianFee
 *   feeRange
 *
 * It does NOT contain:
 *   height
 *   timestamp
 *   hash
 */
type BlockApiData = {
  id?: string | number;
  hash?: string | number;

  height?: number;
  timestamp?: number;

  size?: number;
  weight?: number;

  tx_count?: number;
  txCount?: number;

  blockSize?: number;
  blockVSize?: number;
  nTx?: number;

  totalFees?: number;
  medianFee?: number;
  feeRange?: number[];
};

type BlockData = {
  id?: string;
  height: number;
  timestamp: number;
  size: number;
  weight: number;
  tx_count: number;
};

type CongestionSnapshot = {
  score: number;
  timestamp: number;
};

/* =========================================================
   PHASE 3 TYPES
========================================================= */

type ComparativeEvidence = {
  observation_count: number;
  baseline_value: number;
  minimum: number;
  maximum: number;
  range: number;
};

type ComparativeResult = {
  result_id: string;
  result_type: string;
  primary_track: string;
  metric_name: string;
  result_value: number;
  result_unit: string;
  category: string;
  finding_type: string;
  finding: string;
  evidence: ComparativeEvidence;
  method_version: string;
  baseline_method: string;
  data_version: string;
  generated_at: string;
  quality_status: string;
  limitation: string;
};

type Phase3IntelligenceData = {
  primary_track: string;
  results: ComparativeResult[];
};

/* =========================================================
   PAGE
========================================================= */

export default function HomePage() {
  /* =======================================================
     STATE
  ======================================================= */

  const [aboutOpen, setAboutOpen] =
    useState(false);

  const [intelligenceOpen, setIntelligenceOpen] =
    useState(false);

  const [mempool, setMempool] =
    useState<MempoolData | null>(null);

  const [congestion, setCongestion] =
    useState<CongestionData | null>(null);

  const [fees, setFees] =
    useState<FeeData | null>(null);

  const [intelligence, setIntelligence] =
    useState<IntelligenceData | null>(null);

  const [phase3Intelligence, setPhase3Intelligence] =
    useState<Phase3IntelligenceData | null>(null);

  const [feeBuckets, setFeeBuckets] =
    useState<FeeBucket[]>([]);

  const [blocks, setBlocks] =
    useState<BlockData[]>([]);

  const [congestionHistory, setCongestionHistory] =
    useState<CongestionSnapshot[]>([]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState<string | null>(null);

  const [lastUpdated, setLastUpdated] =
    useState<Date | null>(null);

  /* =========================================================
     FETCH DASHBOARD
  ========================================================= */

  const fetchDashboard = useCallback(
    async () => {
      try {
        const response = await fetch(
          `${API}/api/analytics/dashboard`,
          {
            cache: "no-store",
          }
        );

        if (!response.ok) {
          throw new Error(
            `Dashboard API returned ${response.status}`
          );
        }

        const data: {
          mempool?: MempoolData;
          fees?: FeeData;
        } = await response.json();

        setMempool(
          data.mempool ?? null
        );

        setFees(
          data.fees ?? null
        );

        setLastUpdated(
          new Date()
        );

        setError(null);
      } catch (err) {
        console.error(
          "Dashboard error:",
          err
        );

        setError(
          err instanceof Error
            ? err.message
            : "Unable to load dashboard data."
        );
      }
    },
    []
  );

  /* =========================================================
     FETCH CONGESTION

     VERIFIED BACKEND ROUTE:
     /api/mempool/congestion
  ========================================================= */

  const fetchCongestion = useCallback(
    async () => {
      try {
        const response = await fetch(
          `${API}/api/mempool/congestion`,
          {
            cache: "no-store",
          }
        );

        if (!response.ok) {
          throw new Error(
            `Congestion API returned ${response.status}`
          );
        }

        const data: CongestionData =
          await response.json();

        setCongestion(data);
      } catch (err) {
        console.error(
          "Congestion error:",
          err
        );
      }
    },
    []
  );

  /* =========================================================
     FETCH LIVE INTELLIGENCE
  ========================================================= */

  const fetchIntelligence = useCallback(
    async () => {
      try {
        const response = await fetch(
          `${API}/api/analytics/intelligence`,
          {
            cache: "no-store",
          }
        );

        if (!response.ok) {
          throw new Error(
            `Intelligence API returned ${response.status}`
          );
        }

        const data: IntelligenceData =
          await response.json();

        setIntelligence(data);
      } catch (err) {
        console.error(
          "Intelligence error:",
          err
        );
      }
    },
    []
  );

  /* =========================================================
     FETCH APPROVED PHASE 3 INTELLIGENCE

     SOURCE OF TRUTH:
     data-science/outputs/intelligence_results.json

     Track:
     Track A â€” Comparative
  ========================================================= */

  const fetchPhase3Intelligence =
    useCallback(async () => {
      try {
        const response = await fetch(
          `${API}/api/analytics/phase3-intelligence`,
          {
            cache: "no-store",
          }
        );

        if (!response.ok) {
          throw new Error(
            `Phase 3 Intelligence API returned ${response.status}`
          );
        }

        const data: Phase3IntelligenceData =
          await response.json();

        if (
          data.primary_track !==
          "Track A â€” Comparative"
        ) {
          throw new Error(
            "Phase 3 output does not match the approved Track A â€” Comparative track."
          );
        }

        setPhase3Intelligence(data);
      } catch (err) {
        console.error(
          "Phase 3 intelligence error:",
          err
        );

        setPhase3Intelligence(null);
      }
    }, []);

  /* =========================================================
     FETCH FEE BUCKETS

     MempoolChart expects:
       fee_rate
       vsize
  ========================================================= */

  const fetchFeeBuckets = useCallback(
    async () => {
      try {
        const response = await fetch(
          `${API}/api/fees/buckets`,
          {
            cache: "no-store",
          }
        );

        if (!response.ok) {
          throw new Error(
            `Fee buckets API returned ${response.status}`
          );
        }

        const rawData: unknown =
          await response.json();

        if (!Array.isArray(rawData)) {
          setFeeBuckets([]);
          return;
        }

        const normalizedBuckets: FeeBucket[] =
          rawData
            .map((item): FeeBucket => {
              const bucket =
                item as Record<
                  string,
                  unknown
                >;

              return {
                fee_rate: Number(
                  bucket.fee_rate ?? 0
                ),
                vsize: Number(
                  bucket.vsize ?? 0
                ),
              };
            })
            .filter(
              (bucket) =>
                Number.isFinite(
                  bucket.fee_rate
                ) &&
                Number.isFinite(
                  bucket.vsize
                )
            );

        setFeeBuckets(
          normalizedBuckets
        );
      } catch (err) {
        console.error(
          "Fee buckets error:",
          err
        );

        setFeeBuckets([]);
      }
    },
    []
  );

  /* =========================================================
     FETCH RECENT BLOCKS

     VERIFIED BACKEND ROUTE:
     /api/mempool/blocks

     VERIFIED RESPONSE SHAPE:
     {
       "data": [
         {
           "blockSize": number,
           "blockVSize": number,
           "nTx": number,
           "totalFees": number,
           "medianFee": number,
           "feeRange": number[]
         }
       ]
     }

     NOTE:
     This endpoint does not provide block height,
     timestamp, or hash.
  ========================================================= */

  const fetchBlocks = useCallback(
    async () => {
      try {
        const response = await fetch(
          `${API}/api/mempool/blocks`,
          {
            cache: "no-store",
          }
        );

        if (!response.ok) {
          throw new Error(
            `Blocks API returned ${response.status}`
          );
        }

        const rawData =
          await response.json();

        /*
         * Backend returns:
         * {
         *   data: [...]
         * }
         *
         * Support both wrapped and direct arrays.
         */
        const data: BlockApiData[] =
          Array.isArray(rawData)
            ? rawData
            : Array.isArray(
                rawData?.data
              )
              ? rawData.data
              : [];

        const normalizedBlocks: BlockData[] =
          data.map(
            (
              block: BlockApiData,
              index: number
            ): BlockData => ({
              /*
               * The verified endpoint does not provide
               * a block hash/id, so create a stable
               * frontend identifier for rendering.
               */
              id: String(
                block.id ??
                  block.hash ??
                  `mempool-block-${index + 1}`
              ),

              /*
               * /api/mempool/blocks does not expose
               * actual blockchain height.
               */
              height: Number(
                block.height ?? 0
              ),

              /*
               * /api/mempool/blocks does not expose
               * a block timestamp.
               */
              timestamp: Number(
                block.timestamp ?? 0
              ),

              /*
               * Backend:
               * blockSize
               */
              size: Number(
                block.size ??
                  block.blockSize ??
                  0
              ),

              /*
               * Backend:
               * blockVSize
               */
              weight: Number(
                block.weight ??
                  block.blockVSize ??
                  0
              ),

              /*
               * Backend:
               * nTx
               */
              tx_count: Number(
                block.tx_count ??
                  block.txCount ??
                  block.nTx ??
                  0
              ),
            })
          );

        /*
         * IMPORTANT:
         * Do NOT filter by block.height.
         *
         * The verified /api/mempool/blocks endpoint
         * does not return height.
         */
        setBlocks(
          normalizedBlocks
        );
      } catch (err) {
        console.error(
          "Blocks error:",
          err
        );

        setBlocks([]);
      }
    },
    []
  );

  /* =========================================================
     REFRESH
  ========================================================= */

  const refreshData = useCallback(
    async () => {
      setLoading(true);

      await Promise.all([
        fetchDashboard(),
        fetchCongestion(),
        fetchIntelligence(),
        fetchPhase3Intelligence(),
        fetchFeeBuckets(),
        fetchBlocks(),
      ]);

      setLoading(false);
    },
    [
      fetchDashboard,
      fetchCongestion,
      fetchIntelligence,
      fetchPhase3Intelligence,
      fetchFeeBuckets,
      fetchBlocks,
    ]
  );

  /* =========================================================
     INITIAL LOAD
  ========================================================= */

  useEffect(() => {
    refreshData();
  }, [refreshData]);

  /* =========================================================
     CONGESTION HISTORY

     NOTE:
     Dashboard display context only.
     This does NOT replace approved Phase 3
     Comparative analysis.
  ========================================================= */

  useEffect(() => {
    const score =
      congestion?.score;

    if (
      score === undefined ||
      score === null ||
      Number.isNaN(Number(score))
    ) {
      return;
    }

    const numericScore =
      Number(score);

    setCongestionHistory(
      (previous) => {
        const last =
          previous[
            previous.length - 1
          ];

        if (
          last &&
          last.score ===
            numericScore
        ) {
          return previous;
        }

        return [
          ...previous,
          {
            score: numericScore,
            timestamp:
              Date.now(),
          },
        ].slice(-20);
      }
    );
  }, [congestion?.score]);

  /* =========================================================
     FORMATTERS
  ========================================================= */

  const formatNumber = (
    value?: number
  ) => {
    return (
      value ?? 0
    ).toLocaleString();
  };

  const formatMB = (
    value?: number
  ) => {
    if (!value) {
      return "0 MB";
    }

    return `${(
      value /
      (1024 * 1024)
    ).toFixed(2)} MB`;
  };

  const formatBTC = (
    satoshis?: number
  ) => {
    if (!satoshis) {
      return "0 BTC";
    }

    return `${(
      satoshis /
      100000000
    ).toFixed(6)} BTC`;
  };

  /* =========================================================
     CURRENT VALUES
  ========================================================= */

  const congestionScore =
    congestion?.score ??
    intelligence?.congestion_score ??
    0;

  const congestionLevel =
    congestion?.level ??
    intelligence?.congestion_level ??
    "UNKNOWN";

  const transactionCount =
    mempool?.count ??
    congestion?.transaction_count ??
    0;

  const mempoolSize =
    mempool?.vsize ??
    congestion?.virtual_size ??
    0;

  const memoryUsage =
    congestion?.memory_usage_percent ??
    0;

  const fastestFee =
    fees?.fastest ??
    intelligence?.fastest_fee ??
    0;

  const economyFee =
    fees?.economy ??
    intelligence?.economy_fee ??
    0;

  /* =========================================================
     CONGESTION TREND

     NOTE:
     This is dashboard display context only.
     It does NOT replace the approved Phase 3
     Comparative analysis.
  ========================================================= */

  const currentScore =
    congestionHistory.length > 0
      ? congestionHistory[
          congestionHistory.length - 1
        ].score
      : Number(
          congestionScore
        );

  const previousScore =
    congestionHistory.length > 1
      ? congestionHistory[
          congestionHistory.length - 2
        ].score
      : null;

  let congestionChange = 0;

  if (
    previousScore !== null &&
    previousScore !== 0
  ) {
    congestionChange =
      ((currentScore -
        previousScore) /
        Math.abs(
          previousScore
        )) *
      100;
  }

  const congestionTrend =
    previousScore === null
      ? "INITIALIZING"
      : congestionChange > 2
      ? "INCREASING"
      : congestionChange < -2
      ? "IMPROVING"
      : "STABLE";

  /* =========================================================
     VISUALIZER DATA
  ========================================================= */

  const visualizerData = {
    pendingTransactions:
      transactionCount,

    mempoolSize:
      mempoolSize /
      (1024 * 1024),

    congestionScore:
      Number(
        congestionScore
      ),

    fastFee:
      Number(
        fastestFee
      ),

    economyFee:
      Number(
        economyFee
      ),

    totalFees:
      Number(
        mempool?.total_fee ?? 0
      ) /
      100000000,

    memoryUsage:
      Number(
        memoryUsage
      ),

    history:
      congestionHistory.map(
        (snapshot) =>
          snapshot.score
      ),
  };

  /* =========================================================
     UI
  ========================================================= */

  return (
    <main className="min-h-screen overflow-x-hidden bg-[#02070d] text-white">

      <Topbar
        stationCount={
          transactionCount
        }
        dataSource="Mempool.space"
        isLoading={loading}
        onAbout={() =>
          setAboutOpen(true)
        }
      />

      <section className="relative min-h-[calc(100vh-72px)] overflow-hidden">

        <div className="pointer-events-none absolute inset-0">

          <div className="absolute left-1/2 top-1/2 h-[700px] w-[700px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-cyan-400/[0.035] blur-3xl" />

          <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,rgba(34,211,238,0.07),transparent_55%)]" />

          <div className="absolute inset-0 bg-[linear-gradient(rgba(34,211,238,0.025)_1px,transparent_1px),linear-gradient(90deg,rgba(34,211,238,0.025)_1px,transparent_1px)] bg-[size:60px_60px]" />

        </div>

        <div className="absolute left-5 top-6 z-20 max-w-xl sm:left-8 sm:top-8">

          <p className="text-[9px] font-semibold uppercase tracking-[4px] text-cyan-400">
            Bitcoin Network Intelligence
          </p>

          <h1 className="mt-2 text-2xl font-black tracking-tight text-white sm:text-4xl">
            Mempool Congestion
            <span className="text-cyan-300">
              {" "}Visualizer
            </span>
          </h1>

          <p className="mt-2 text-xs leading-5 text-slate-500 sm:text-sm">
            Real-time network pressure,
            transaction activity and
            fee-market intelligence.
          </p>

        </div>

        <div className="absolute right-5 top-6 z-20 hidden rounded-2xl border border-cyan-400/15 bg-black/30 px-5 py-4 text-right backdrop-blur-xl sm:right-8 sm:top-8 sm:block">

          <p className="text-[8px] uppercase tracking-[3px] text-slate-600">
            Network State
          </p>

          <p className="mt-1 text-lg font-black uppercase text-cyan-300">
            {congestionLevel}
          </p>

          <p className="text-xs text-slate-500">
            Score{" "}
            {Number(
              congestionScore
            ).toFixed(1)}
            {" "} / 100
          </p>

        </div>

        <div className="relative z-10 flex min-h-[calc(100vh-72px)] items-center justify-center px-4 pb-24 pt-36 sm:px-8">

          <div className="w-full max-w-7xl">

            <MempoolVisualizer
              data={
                visualizerData
              }
              onPointClick={(
                score,
                index
              ) => {
                console.log(
                  `Selected congestion observation ${
                    index + 1
                  }: ${score}`
                );

                setIntelligenceOpen(
                  true
                );
              }}
            />

          </div>

        </div>

        <div className="absolute bottom-6 left-5 z-30 hidden items-center gap-5 rounded-2xl border border-cyan-400/10 bg-black/30 px-5 py-3 backdrop-blur-xl lg:flex">

          <HudItem
            label="Pending"
            value={formatNumber(
              transactionCount
            )}
          />

          <div className="h-7 w-px bg-white/10" />

          <HudItem
            label="Mempool"
            value={formatMB(
              mempoolSize
            )}
          />

          <div className="h-7 w-px bg-white/10" />

          <HudItem
            label="Fast Fee"
            value={`${fastestFee} sat/vB`}
          />

        </div>

        <button
          type="button"
          onClick={() =>
            setIntelligenceOpen(
              true
            )
          }
          className="absolute bottom-5 right-5 z-30 rounded-xl border border-cyan-400/30 bg-cyan-400/10 px-4 py-3 text-[10px] font-semibold uppercase tracking-[2px] text-cyan-300 backdrop-blur-xl transition hover:bg-cyan-400 hover:text-slate-950 lg:hidden"
        >
          Intelligence
        </button>

      </section>

      <IntelligencePanel
        open={
          intelligenceOpen
        }
        onClose={() =>
          setIntelligenceOpen(
            false
          )
        }
        intelligence={
          intelligence
        }
        transactionCount={
          transactionCount
        }
        mempoolSize={
          mempoolSize
        }
        congestionTrend={
          congestionTrend
        }
        congestionChange={
          congestionChange
        }
        previousCongestionScore={
          previousScore
        }
        phase3Intelligence={
          phase3Intelligence
        }
      />

      <section className="relative z-10 mx-auto w-full max-w-7xl px-4 pb-16 sm:px-8">

        <div className="grid grid-cols-1 gap-4 md:grid-cols-3">

          <MetricCard
            title="Congestion Score"
            value={`${Number(
              congestionScore
            ).toFixed(1)} / 100`}
            description={`${congestionLevel} network pressure`}
          />

          <MetricCard
            title="Pending Transactions"
            value={formatNumber(
              transactionCount
            )}
            description="Transactions currently waiting"
          />

          <MetricCard
            title="Fast Confirmation Fee"
            value={`${fastestFee} sat/vB`}
            description="Current recommended fee"
          />

        </div>

        <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-3">

          <SmallMetric
            label="Total Mempool Fees"
            value={formatBTC(
              mempool?.total_fee
            )}
          />

          <SmallMetric
            label="Memory Usage"
            value={`${Number(
              memoryUsage
            ).toFixed(2)}%`}
          />

          <SmallMetric
            label="Economy Fee"
            value={`${economyFee} sat/vB`}
          />

        </div>

      </section>

      <section className="relative z-10 mx-auto w-full max-w-7xl px-4 pb-16 sm:px-8">

        <div className="rounded-3xl border border-cyan-400/10 bg-[#071019]/50 p-5 backdrop-blur-xl sm:p-8">

          <div className="mb-6">

            <p className="text-[9px] uppercase tracking-[3px] text-slate-600">
              Network Economics
            </p>

            <h2 className="mt-2 text-2xl font-black text-white">
              Fee Market
            </h2>

          </div>

          <MempoolChart
            data={feeBuckets}
          />

        </div>

      </section>

      <section className="relative z-10 mx-auto w-full max-w-7xl px-4 pb-16 sm:px-8">

        <div className="rounded-3xl border border-cyan-400/10 bg-[#071019]/50 p-5 backdrop-blur-xl sm:p-8">

          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">

            <div>

              <p className="text-[9px] uppercase tracking-[3px] text-slate-600">
                Blockchain Activity
              </p>

              <h2 className="mt-2 text-2xl font-black text-white">
                Recent Bitcoin Blocks
              </h2>

            </div>

            <span className="w-fit rounded-lg border border-cyan-400/15 bg-cyan-400/5 px-3 py-2 text-xs text-cyan-300">
              {blocks.length} blocks
            </span>

          </div>

          <div className="mt-6 overflow-x-auto">

            <table className="w-full min-w-[650px] text-left">

              <thead>

                <tr className="border-b border-white/[0.06] text-[9px] uppercase tracking-[2px] text-slate-600">

                  <th className="px-4 py-3">
                    Block Height
                  </th>

                  <th className="px-4 py-3">
                    Transactions
                  </th>

                  <th className="px-4 py-3">
                    Size
                  </th>

                  <th className="px-4 py-3">
                    Weight
                  </th>

                  <th className="px-4 py-3">
                    Block ID
                  </th>

                </tr>

              </thead>

              <tbody>

                {blocks
                  .slice(0, 8)
                  .map(
                    (
                      block,
                      index
                    ) => (
                      <tr
                        key={
                          block.id ??
                          index
                        }
                        className="border-b border-white/[0.035] transition hover:bg-cyan-400/[0.025]"
                      >

                        <td className="px-4 py-4 font-bold text-cyan-300">
                          {block.height > 0
                            ? formatNumber(
                                block.height
                              )
                            : "â€”"}
                        </td>

                        <td className="px-4 py-4 text-slate-300">
                          {formatNumber(
                            block.tx_count
                          )}
                        </td>

                        <td className="px-4 py-4 text-slate-400">
                          {formatMB(
                            block.size
                          )}
                        </td>

                        <td className="px-4 py-4 text-slate-400">
                          {formatNumber(
                            block.weight
                          )}
                        </td>

                        <td className="max-w-[220px] truncate px-4 py-4 font-mono text-xs text-slate-600">
                          {block.id ??
                            "-"}
                        </td>

                      </tr>
                    )
                  )}

              </tbody>

            </table>

            {blocks.length ===
              0 && (
              <div className="py-10 text-center text-sm text-slate-600">
                No block data available.
              </div>
            )}

          </div>

        </div>

      </section>

      <footer className="relative z-10 border-t border-white/[0.05] px-5 py-8 sm:px-8">

        <div className="mx-auto flex max-w-7xl flex-col gap-3 text-[10px] uppercase tracking-[1.5px] text-slate-600 md:flex-row md:items-center md:justify-between">

          <span>
            Data Source:
            {" "}Mempool.space
          </span>

          <span>
            POC-88 â€¢ Mempool
            Congestion Intelligence
          </span>

          <span>
            {lastUpdated
              ? `Updated ${lastUpdated.toLocaleTimeString()}`
              : "Waiting for live data"}
          </span>

        </div>

      </footer>

      <AboutModal
        open={aboutOpen}
        onClose={() =>
          setAboutOpen(false)
        }
      />

      {error && (
        <div className="fixed bottom-5 left-1/2 z-[700] w-[calc(100%-2rem)] max-w-lg -translate-x-1/2 rounded-2xl border border-red-500/20 bg-[#16090b]/95 p-5 shadow-2xl backdrop-blur-xl">

          <p className="text-sm font-semibold text-red-300">
            Backend Connection Error
          </p>

          <p className="mt-1 text-xs text-red-400">
            {error}
          </p>

          <p className="mt-2 text-[10px] text-slate-600">
            Backend:
            {" "}
            {API}
          </p>

        </div>
      )}

    </main>
  );
}

/* ===========================================================
   HUD ITEM
=========================================================== */

function HudItem({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div>

      <p className="text-[8px] uppercase tracking-[2px] text-slate-600">
        {label}
      </p>

      <p className="mt-1 text-xs font-semibold text-slate-300">
        {value}
      </p>

    </div>
  );
}

/* ===========================================================
   METRIC CARD
=========================================================== */

function MetricCard({
  title,
  value,
  description,
}: {
  title: string;
  value: string;
  description: string;
}) {
  return (
    <div className="group relative overflow-hidden rounded-2xl border border-cyan-400/10 bg-[#071019]/60 p-5 backdrop-blur-xl transition-all duration-300 hover:-translate-y-1 hover:border-cyan-400/25">

      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(34,211,238,0.06),transparent_70%)] opacity-0 transition group-hover:opacity-100" />

      <div className="relative">

        <p className="text-[9px] uppercase tracking-[3px] text-slate-600">
          {title}
        </p>

        <p className="mt-3 text-2xl font-black text-cyan-300">
          {value}
        </p>

        <p className="mt-2 text-xs text-slate-600">
          {description}
        </p>

      </div>

    </div>
  );
}

/* ===========================================================
   SMALL METRIC
=========================================================== */

function SmallMetric({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-2xl border border-white/[0.06] bg-[#071019]/50 px-5 py-4 backdrop-blur-xl">

      <p className="text-[9px] uppercase tracking-[2px] text-slate-600">
        {label}
      </p>

      <p className="mt-2 text-lg font-bold text-white">
        {value}
      </p>

    </div>
  );
}

