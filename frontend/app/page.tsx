"use client";

import {
  useCallback,
  useEffect,
  useState,
} from "react";

import { Topbar } from "@/components/Topbar";
import { Sidebar } from "@/components/Sidebar";
import FilterPanel from "@/components/Filterpanel";
import MempoolChart from "@/components/MempoolChart";
import MempoolVisualizer from "@/components/MempoolVisualizer";
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
  total_fee_btc?: number;
  mempoolminfee?: number;
  incrementalrelayfee?: number;
  fee_histogram?: number[][];
};

type CongestionData = {
  score?: number;
  level?: string;
  transaction_count?: number;
  virtual_size?: number;
  memory_usage_percent?: number;
  total_fee?: number;
};

type FeeData = {
  fastest?: number;
  half_hour?: number;
  hour?: number;
  economy?: number;
  minimum?: number;
};

type IntelligenceData = {
  congestion_level?: string;
  congestion_score?: number;
  fastest_fee?: number;
  economy_fee?: number;
  recommendation?: string;
};

type FeeBucket = {
  fee_rate: number;
  vsize: number;
};

type BlockData = {
  id?: string;
  height?: number;
  timestamp?: number;
  size?: number;
  weight?: number;
  tx_count?: number;
};

type CongestionSnapshot = {
  score: number;
  timestamp: number;
};

/* =========================================================
   PAGE
========================================================= */

export default function Page() {
  const [aboutOpen, setAboutOpen] =
    useState(false);

  const [mempool, setMempool] =
    useState<MempoolData | null>(null);

  const [congestion, setCongestion] =
    useState<CongestionData | null>(null);

  const [fees, setFees] =
    useState<FeeData | null>(null);

  const [intelligence, setIntelligence] =
    useState<IntelligenceData | null>(null);

  const [feeBuckets, setFeeBuckets] =
    useState<FeeBucket[]>([]);

  const [blocks, setBlocks] =
    useState<BlockData[]>([]);

  const [congestionHistory, setCongestionHistory] =
    useState<CongestionSnapshot[]>([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  const [lastUpdated, setLastUpdated] =
    useState<Date | null>(null);

  const [autoRefresh, setAutoRefresh] =
    useState(false);

  /* =========================================================
     FETCH DASHBOARD
  ========================================================= */

  const fetchDashboard =
    useCallback(async () => {
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

        const data =
          await response.json();

        setMempool(
          data?.mempool ?? null
        );

        setFees(
          data?.fees ?? null
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
          "Unable to connect to the FastAPI backend."
        );
      }
    }, []);

  /* =========================================================
     FETCH CONGESTION
  ========================================================= */

  const fetchCongestion =
    useCallback(async () => {
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

        const data =
          await response.json();

        setCongestion(data);
      } catch (err) {
        console.error(
          "Congestion error:",
          err
        );
      }
    }, []);

  /* =========================================================
     FETCH INTELLIGENCE
  ========================================================= */

  const fetchIntelligence =
    useCallback(async () => {
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

        const data =
          await response.json();

        setIntelligence(data);
      } catch (err) {
        console.error(
          "Intelligence error:",
          err
        );
      }
    }, []);

  /* =========================================================
     FETCH FEE BUCKETS
  ========================================================= */

  const fetchFeeBuckets =
    useCallback(async () => {
      try {
        const response = await fetch(
          `${API}/api/analytics/dashboard`,
          {
            cache: "no-store",
          }
        );

        if (!response.ok) {
          return;
        }

        const data =
          await response.json();

        const histogram =
          data?.mempool?.fee_histogram;

        if (
          Array.isArray(histogram)
        ) {
          const buckets: FeeBucket[] =
            histogram
              .filter(
                (item: unknown) =>
                  Array.isArray(item) &&
                  item.length >= 2
              )
              .map(
                (item: number[]) => ({
                  fee_rate: Number(
                    item[0]
                  ),
                  vsize: Number(
                    item[1]
                  ),
                })
              );

          setFeeBuckets(
            buckets
          );
        }
      } catch (err) {
        console.error(
          "Fee bucket error:",
          err
        );
      }
    }, []);

  /* =========================================================
     FETCH RECENT BLOCKS
  ========================================================= */

  const fetchBlocks =
    useCallback(async () => {
      try {
        const response =
          await fetch(
            "https://mempool.space/api/v1/blocks",
            {
              cache: "no-store",
            }
          );

        if (!response.ok) {
          throw new Error(
            `Mempool.space Blocks API returned ${response.status}`
          );
        }

        const data =
          await response.json();

        if (
          !Array.isArray(data)
        ) {
          throw new Error(
            "Invalid blocks response from Mempool.space"
          );
        }

        const normalizedBlocks:
          BlockData[] =
          data
            .map(
              (block: any) => ({
                id:
                  block.id ??
                  block.hash ??
                  "",

                height: Number(
                  block.height ??
                  0
                ),

                timestamp: Number(
                  block.timestamp ??
                  0
                ),

                size: Number(
                  block.size ??
                  0
                ),

                weight: Number(
                  block.weight ??
                  0
                ),

                tx_count: Number(
                  block.tx_count ??
                  block.txCount ??
                  0
                ),
              })
            )
            .filter(
              (
                block: BlockData
              ) =>
                block.height !==
                  undefined &&
                block.height > 0
            );

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
    }, []);

  /* =========================================================
     TRACK REAL CONGESTION HISTORY
  ========================================================= */

  useEffect(() => {
    const currentScore =
      congestion?.score;

    if (
      currentScore ===
        undefined ||
      currentScore === null ||
      Number.isNaN(
        Number(currentScore)
      )
    ) {
      return;
    }

    const score =
      Number(currentScore);

    setCongestionHistory(
      (previous) => {
        const last =
          previous[
            previous.length - 1
          ];

        if (
          last &&
          last.score === score
        ) {
          return previous;
        }

        const snapshot:
          CongestionSnapshot = {
          score,
          timestamp:
            Date.now(),
        };

        return [
          ...previous,
          snapshot,
        ].slice(-20);
      }
    );
  }, [congestion?.score]);

  /* =========================================================
     REFRESH EVERYTHING
  ========================================================= */

  const refreshData =
    useCallback(async () => {
      setLoading(true);

      await Promise.all([
        fetchDashboard(),
        fetchCongestion(),
        fetchIntelligence(),
        fetchFeeBuckets(),
        fetchBlocks(),
      ]);

      setLoading(false);
    }, [
      fetchDashboard,
      fetchCongestion,
      fetchIntelligence,
      fetchFeeBuckets,
      fetchBlocks,
    ]);

  /* =========================================================
     INITIAL LOAD
  ========================================================= */

  useEffect(() => {
    refreshData();
  }, [refreshData]);

  /* =========================================================
     AUTO REFRESH - 30 SECONDS
  ========================================================= */

  useEffect(() => {
    if (!autoRefresh) {
      return;
    }

    const timer =
      setInterval(() => {
        refreshData();
      }, 30000);

    return () => {
      clearInterval(timer);
    };
  }, [
    autoRefresh,
    refreshData,
  ]);

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
    bytes?: number
  ) => {
    if (!bytes) {
      return "0 MB";
    }

    return `${(
      bytes /
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
     DASHBOARD VALUES
  ========================================================= */

  const congestionLevel =
    congestion?.level ??
    intelligence?.congestion_level ??
    "Unknown";

  const congestionScore =
    congestion?.score ??
    intelligence?.congestion_score ??
    0;

  const memoryUsage =
    congestion?.memory_usage_percent ??
    0;

  const transactionCount =
    mempool?.count ??
    congestion?.transaction_count ??
    0;

  const mempoolSize =
    mempool?.vsize ??
    congestion?.virtual_size ??
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
  ========================================================= */

  const currentCongestionScore =
    congestionHistory.length > 0
      ? congestionHistory[
          congestionHistory.length - 1
        ].score
      : congestionScore;

  const previousCongestionScore =
    congestionHistory.length > 1
      ? congestionHistory[
          congestionHistory.length - 2
        ].score
      : null;

  let congestionChange = 0;

  if (
    previousCongestionScore !== null &&
    previousCongestionScore !== 0
  ) {
    congestionChange =
      ((currentCongestionScore -
        previousCongestionScore) /
        Math.abs(
          previousCongestionScore
        )) *
      100;
  }

  const congestionTrend =
    previousCongestionScore === null
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

    /*
      vsize from your API is bytes.
      The visualizer expects MB.
    */
    mempoolSize:
      mempoolSize /
      (1024 * 1024),

    congestionScore:
      Number(congestionScore),

    fastFee:
      Number(fastestFee),

    economyFee:
      Number(economyFee),

    totalFees:
      Number(
        mempool?.total_fee ?? 0
      ) / 100000000,

    memoryUsage:
      Number(memoryUsage),

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
    <main className="min-h-screen bg-[#03070d] text-white">
      <div className="flex min-h-screen">
        <aside className="hidden lg:block w-[340px] shrink-0">
          <div className="sticky top-0 h-screen">
            <Sidebar
              congestion={congestion}
              fees={fees}
              onRefresh={refreshData}
            />
          </div>
        </aside>

        <div className="min-w-0 flex-1">

      {/* =====================================================
          TOPBAR
      ====================================================== */}

      <Topbar
        stationCount={
          transactionCount
        }
        dataSource="Mempool.space"
        isLoading={loading}
      />

      {/* =====================================================
          MAIN CONTAINER
      ====================================================== */}

      <div className="min-h-[calc(100vh-96px)] px-4 py-6 sm:px-5 md:px-8">

        {/* ===================================================
            HEADER
        ==================================================== */}

        <div className="mb-6 flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">

          <div className="min-w-0">

            <p className="text-xs uppercase tracking-[4px] text-cyan-400">
              POC-88 • Bitcoin Network Analytics
            </p>

            <h1 className="mt-2 text-3xl font-black tracking-tight text-white sm:text-4xl">
              Mempool Congestion
              <br />
              Visualizer
            </h1>

            <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-400">
              Real-time visualization of Bitcoin
              mempool pressure, transaction activity,
              fee markets and congestion intelligence.
            </p>

          </div>

          <div className="flex shrink-0 flex-wrap gap-3">

            <button
              onClick={() =>
                setAboutOpen(true)
              }
              className="rounded-xl border border-cyan-500/30 bg-[#071019] px-5 py-3 text-sm font-semibold text-cyan-300 transition hover:bg-cyan-500 hover:text-white"
            >
              ABOUT
            </button>

          </div>

        </div>

        {/* ===================================================
            FILTER PANEL
        ==================================================== */}

        <div className="mb-6">
          <FilterPanel
            onRefresh={
              refreshData
            }
            autoRefresh={
              autoRefresh
            }
            onAutoRefreshChange={
              setAutoRefresh
            }
          />
        </div>

        {/* ===================================================
            ERROR
        ==================================================== */}

        {error && (
          <div className="mb-6 rounded-2xl border border-red-500/30 bg-red-500/10 p-5">

            <p className="text-sm font-semibold text-red-300">
              Backend Connection Error
            </p>

            <p className="mt-1 text-xs text-red-400">
              {error}
            </p>

            <p className="mt-2 text-xs text-slate-500">
              Check that FastAPI is running at:
              {" "}
              {API}
            </p>

          </div>
        )}

        {/* ===================================================
            KPI CARDS
        ==================================================== */}

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">

          <MetricCard
            title="Pending Transactions"
            value={formatNumber(
              transactionCount
            )}
            description="Transactions in mempool"
          />

          <MetricCard
            title="Mempool Size"
            value={formatMB(
              mempoolSize
            )}
            description="Virtual transaction size"
          />

          <MetricCard
            title="Congestion"
            value={
              congestionLevel
            }
            description={`Score ${congestionScore.toFixed(
              1
            )} / 100`}
          />

          <MetricCard
            title="Fast Fee"
            value={`${fastestFee} sat/vB`}
            description="Recommended confirmation fee"
          />

        </div>

        {/* ===================================================
            SECONDARY METRICS
        ==================================================== */}

        <div className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-3">

          <SmallMetric
            label="Total Mempool Fees"
            value={formatBTC(
              mempool?.total_fee
            )}
          />

          <SmallMetric
            label="Memory Usage"
            value={`${memoryUsage.toFixed(
              2
            )}%`}
          />

          <SmallMetric
            label="Economy Fee"
            value={`${economyFee} sat/vB`}
          />

        </div>

        {/* ===================================================
            MAIN MEMPOOL VISUALIZATION
        ==================================================== */}

        <div className="mt-8">

          <MempoolVisualizer
            data={
              visualizerData
            }
          />

        </div>

        {/* ===================================================
            ANALYTICS + INTELLIGENCE
        ==================================================== */}

        <div className="mt-8 grid grid-cols-1 gap-6 xl:grid-cols-3">

          {/* CONGESTION */}

          <section className="rounded-2xl border border-cyan-500/20 bg-[#071019]/90 p-6 backdrop-blur-xl">

            <div className="flex items-start justify-between">

              <div>
                <p className="text-xs uppercase tracking-[3px] text-slate-500">
                  Network Pressure
                </p>

                <h2 className="mt-2 text-xl font-bold">
                  Congestion Score
                </h2>
              </div>

              <div className="text-right">

                <p className="text-3xl font-black text-cyan-300">
                  {congestionScore.toFixed(
                    1
                  )}
                </p>

                <p className="text-xs text-slate-500">
                  / 100
                </p>

              </div>

            </div>

            <div className="mt-7 h-4 overflow-hidden rounded-full bg-slate-800">

              <div
                className="h-full rounded-full bg-cyan-400 transition-all duration-700"
                style={{
                  width: `${Math.min(
                    Math.max(
                      congestionScore,
                      0
                    ),
                    100
                  )}%`,
                }}
              />

            </div>

            <div className="mt-3 flex justify-between text-[10px] uppercase tracking-[2px] text-slate-500">
              <span>Low</span>
              <span>Moderate</span>
              <span>High</span>
              <span>Critical</span>
            </div>

            <div className="mt-7 grid grid-cols-2 gap-3">

              <InfoCard
                label="Transactions"
                value={formatNumber(
                  transactionCount
                )}
              />

              <InfoCard
                label="Virtual Size"
                value={formatMB(
                  mempoolSize
                )}
              />

              <InfoCard
                label="Memory Usage"
                value={`${memoryUsage.toFixed(
                  2
                )}%`}
              />

              <InfoCard
                label="Fast Fee"
                value={`${fastestFee} sat/vB`}
              />

            </div>

          </section>

          {/* FEE MARKET */}

          <section className="rounded-2xl border border-cyan-500/20 bg-[#071019]/90 p-6 backdrop-blur-xl">

            <p className="text-xs uppercase tracking-[3px] text-slate-500">
              Fee Market
            </p>

            <h2 className="mt-2 text-xl font-bold">
              Recommended Fees
            </h2>

            <div className="mt-6 space-y-3">

              <FeeRow
                label="Fastest"
                value={
                  fees?.fastest
                }
              />

              <FeeRow
                label="30 Minutes"
                value={
                  fees?.half_hour
                }
              />

              <FeeRow
                label="1 Hour"
                value={
                  fees?.hour
                }
              />

              <FeeRow
                label="Economy"
                value={
                  fees?.economy
                }
              />

              <FeeRow
                label="Minimum"
                value={
                  fees?.minimum
                }
              />

            </div>

            <div className="mt-6 rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-4">

              <p className="text-[10px] uppercase tracking-[3px] text-slate-500">
                Current Recommendation
              </p>

              <p className="mt-2 text-2xl font-black text-cyan-300">
                {fastestFee}

                <span className="ml-2 text-sm font-normal text-slate-500">
                  sat/vB
                </span>
              </p>

            </div>

          </section>

          {/* INTELLIGENCE */}

          <IntelligencePanel
            open={true}
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
              previousCongestionScore
            }
          />

        </div>

        {/* ===================================================
            FEE MARKET CHART
        ==================================================== */}

        <div className="mt-8">

          <MempoolChart
            data={
              feeBuckets
            }
          />

        </div>

        {/* ===================================================
            RECENT BLOCKS
        ==================================================== */}

        <section className="mt-8 rounded-2xl border border-cyan-500/20 bg-[#071019]/90 p-6 backdrop-blur-xl">

          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">

            <div>

              <p className="text-xs uppercase tracking-[3px] text-slate-500">
                Blockchain Activity
              </p>

              <h2 className="mt-2 text-xl font-bold">
                Recent Bitcoin Blocks
              </h2>

            </div>

            <span className="w-fit rounded-lg border border-cyan-500/20 bg-cyan-500/5 px-3 py-2 text-xs text-cyan-300">
              {blocks.length} blocks
            </span>

          </div>

          <div className="mt-6 overflow-x-auto">

            <table className="w-full min-w-[650px] text-left">

              <thead>

                <tr className="border-b border-slate-800 text-[10px] uppercase tracking-[2px] text-slate-500">

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
                        className="border-b border-slate-900 transition hover:bg-cyan-500/5"
                      >

                        <td className="px-4 py-4 font-bold text-cyan-300">
                          {formatNumber(
                            block.height
                          )}
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

                        <td className="max-w-[220px] truncate px-4 py-4 font-mono text-xs text-slate-500">
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
              <div className="py-12 text-center text-sm text-slate-500">
                No block data available.
              </div>
            )}

          </div>

        </section>

        {/* ===================================================
            FOOTER
        ==================================================== */}

        <footer className="mt-8 flex flex-col gap-2 border-t border-slate-900 py-6 text-xs text-slate-500 md:flex-row md:items-center md:justify-between">

          <p>
            Data Source:
            {" "}
            Mempool.space
          </p>

          <p>
            POC-88 • Mempool
            Congestion Visualizer
          </p>

          <p>
            {lastUpdated
              ? `Last updated ${lastUpdated.toLocaleTimeString()}`
              : "Waiting for live data"}
          </p>

        </footer>

      </div>

      {/* =====================================================
          ABOUT MODAL
      ====================================================== */}

      <AboutModal
        open={
          aboutOpen
        }
        onClose={() =>
          setAboutOpen(false)
        }
      />

            </div>
      </div>

</main>
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
    <div className="group relative overflow-hidden rounded-2xl border border-cyan-500/20 bg-gradient-to-br from-[#08121d] to-[#0b1722] p-5 transition-all duration-300 hover:-translate-y-1 hover:border-cyan-300 hover:shadow-[0_0_30px_rgba(34,211,238,.25)]">

      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,#22d3ee12,transparent_70%)] opacity-0 transition group-hover:opacity-100" />

      <div className="relative">

        <p className="text-[10px] uppercase tracking-[3px] text-slate-500">
          {title}
        </p>

        <p className="mt-3 truncate text-2xl font-black text-cyan-300 sm:text-3xl">
          {value}
        </p>

        <p className="mt-2 text-xs text-slate-500">
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
    <div className="rounded-2xl border border-cyan-500/10 bg-[#071019]/70 px-5 py-4">

      <p className="text-[10px] uppercase tracking-[3px] text-slate-500">
        {label}
      </p>

      <p className="mt-2 text-lg font-bold text-white">
        {value}
      </p>

    </div>
  );
}

/* ===========================================================
   INFO CARD
=========================================================== */

function InfoCard({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-xl border border-cyan-500/10 bg-black/20 p-4">

      <p className="text-[9px] uppercase tracking-[2px] text-slate-500">
        {label}
      </p>

      <p className="mt-2 text-sm font-bold text-white">
        {value}
      </p>

    </div>
  );
}

/* ===========================================================
   FEE ROW
=========================================================== */

function FeeRow({
  label,
  value,
}: {
  label: string;
  value?: number;
}) {
  return (
    <div className="flex items-center justify-between rounded-xl border border-slate-800 bg-black/20 px-4 py-3">

      <span className="text-sm text-slate-400">
        {label}
      </span>

      <span className="font-bold text-cyan-300">
        {value ?? 0}

        <span className="ml-1 text-xs font-normal text-slate-500">
          sat/vB
        </span>
      </span>

    </div>
  );
}