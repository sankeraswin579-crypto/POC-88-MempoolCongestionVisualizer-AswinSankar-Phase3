
"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";

import type {
  IntelligenceResult,
  IntelligenceSummary,
  ValidationMetrics,
} from "@/types/intelligence";

import { loadIntelligenceData } from "@/lib/intelligence";
import GroundedAssistant from "@/components/GroundedAssistant";

type DataState = "loading" | "ready" | "error";

type FreshnessState = "fresh" | "stale" | "unknown";

export default function DataIntelligencePage() {
  const [state, setState] = useState<DataState>("loading");
  const [error, setError] = useState("");

  const [results, setResults] = useState<IntelligenceResult[]>([]);
  const [summary, setSummary] =
    useState<IntelligenceSummary | null>(null);
  const [metrics, setMetrics] =
    useState<ValidationMetrics | null>(null);

  const [categoryFilter, setCategoryFilter] = useState("all");
  const [findingFilter, setFindingFilter] = useState("all");

  const [selectedResult, setSelectedResult] =
    useState<IntelligenceResult | null>(null);

  useEffect(() => {
    let active = true;

    async function load() {
      try {
        setState("loading");
        setError("");

        const data = await loadIntelligenceData();

        if (!active) return;

        setResults(data.results.results);
        setSummary(data.summary);
        setMetrics(data.metrics);
        setState("ready");
      } catch (err) {
        if (!active) return;

        setError(
          err instanceof Error
            ? err.message
            : "Unable to load Data Intelligence."
        );

        setState("error");
      }
    }

    load();

    return () => {
      active = false;
    };
  }, []);

  const categories = useMemo(
    () => [...new Set(results.map((item) => item.category))],
    [results]
  );

  const findingTypes = useMemo(
    () => [...new Set(results.map((item) => item.finding_type))],
    [results]
  );

  const filteredResults = useMemo(() => {
    return results.filter((item) => {
      const categoryMatch =
        categoryFilter === "all" ||
        item.category === categoryFilter;

      const findingMatch =
        findingFilter === "all" ||
        item.finding_type === findingFilter;

      return categoryMatch && findingMatch;
    });
  }, [results, categoryFilter, findingFilter]);

  const insufficientEvidenceCount = results.filter(
    (item) =>
      item.finding_type ===
      "insufficient_comparative_evidence"
  ).length;

  const freshness = useMemo<FreshnessState>(() => {
    if (!summary?.generated_at) {
      return "unknown";
    }

    const generatedAt =
      new Date(summary.generated_at).getTime();

    if (Number.isNaN(generatedAt)) {
      return "unknown";
    }

    const ageInDays =
      (Date.now() - generatedAt) /
      (1000 * 60 * 60 * 24);

    return ageInDays <= 7 ? "fresh" : "stale";
  }, [summary]);

  if (state === "loading") {
    return (
      <main className="min-h-screen p-6">
        <div className="mx-auto max-w-7xl animate-pulse space-y-6">
          <div className="h-10 w-80 rounded bg-gray-200" />

          <div className="grid gap-4 md:grid-cols-4">
            {[1, 2, 3, 4].map((item) => (
              <div
                key={item}
                className="h-28 rounded-xl bg-gray-200"
              />
            ))}
          </div>

          <div className="h-96 rounded-xl bg-gray-200" />
        </div>
      </main>
    );
  }

  if (state === "error") {
    return (
      <main className="min-h-screen p-6">
        <div className="mx-auto max-w-3xl rounded-xl border border-red-200 bg-red-50 p-6">
          <h1 className="text-xl font-bold text-red-800">
            Data Intelligence Error
          </h1>

          <p className="mt-3 text-sm text-red-700">
            {error}
          </p>

          <button
            onClick={() => window.location.reload()}
            className="mt-5 rounded-lg bg-red-700 px-4 py-2 text-sm font-medium text-white"
          >
            Retry
          </button>
        </div>
      </main>
    );
  }

  if (!summary || !metrics) {
    return (
      <main className="min-h-screen p-6">
        <div className="mx-auto max-w-3xl rounded-xl border bg-white p-6 shadow-sm">
          <h1 className="text-xl font-bold">
            No intelligence data available
          </h1>

          <p className="mt-2 text-sm text-gray-600">
            The approved intelligence package did not contain
            the required summary or validation metadata.
          </p>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen p-6">
      <div className="mx-auto max-w-7xl space-y-6">

        {/* HEADER */}

        <section className="rounded-2xl border bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">

            <div>
              <p className="text-sm font-medium uppercase tracking-wide text-blue-600">
                Data Intelligence
              </p>

              <h1 className="mt-1 text-3xl font-bold">
                Track A - Comparative
              </h1>

              <p className="mt-3 max-w-3xl text-sm text-gray-600">
                Decision-oriented comparative intelligence generated
                from the approved Phase 3 Post #3 analytical outputs.
              </p>

              <div className="mt-4">
                <Link
                  href="/"
                  className="inline-flex items-center rounded-lg border border-gray-300 px-4 py-2 text-sm font-medium text-gray-700 transition hover:bg-gray-50"
                >
                  ? Operational View
                </Link>
              </div>
            </div>

            <div className="rounded-xl border bg-gray-50 p-4 text-sm">

              <div>
                <span className="font-semibold">
                  Quality:
                </span>{" "}
                <QualityBadge
                  status={summary.validation_status}
                />
              </div>

              <div className="mt-2">
                <span className="font-semibold">
                  Data:
                </span>{" "}
                {summary.data_version}
              </div>

              <div className="mt-2">
                <span className="font-semibold">
                  Method:
                </span>{" "}
                {results[0]?.method_version ?? "Unavailable"}
              </div>

              <div className="mt-2">
                <span className="font-semibold">
                  Freshness:
                </span>{" "}
                <FreshnessBadge
                  freshness={freshness}
                />
              </div>

              <div className="mt-2">
                <span className="font-semibold">
                  Generated:
                </span>{" "}
                {new Date(
                  summary.generated_at
                ).toLocaleString()}
              </div>
            </div>
          </div>
        </section>

        {/* SUMMARY */}

        <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

          <SummaryCard
            label="Canonical Records"
            value={summary.record_count}
          />

          <SummaryCard
            label="Comparative Groups"
            value={summary.comparative_group_count}
          />

          <SummaryCard
            label="Findings"
            value={summary.finding_count}
          />

          <SummaryCard
            label="Single-Observation Cases"
            value={insufficientEvidenceCount}
          />

        </section>

        {/* VALIDATION */}

        <section className="rounded-xl border bg-white p-5 shadow-sm">

          <div className="flex flex-wrap items-center justify-between gap-3">

            <div>
              <h2 className="text-lg font-semibold">
                Validation Status
              </h2>

              <p className="mt-1 text-sm text-gray-600">
                Approved Post #3 comparative validation result.
              </p>
            </div>

            <QualityBadge status={metrics.status} />

          </div>

        </section>

        {/* GROUNDED ASSISTANT */}
<GroundedAssistant />

        {/* SINGLE OBSERVATION WARNING */}

        {insufficientEvidenceCount > 0 && (
          <section className="rounded-xl border border-amber-300 bg-amber-50 p-5">

            <h2 className="font-semibold text-amber-900">
              Comparative evidence limitation
            </h2>

            <p className="mt-2 text-sm text-amber-800">
              {insufficientEvidenceCount} result(s) contain only
              a single observation. These results are retained as
              approved outputs, but they do not provide sufficient
              comparative evidence for a stability interpretation.
            </p>

          </section>
        )}

        {/* FILTERS */}

        <section className="rounded-xl border bg-white p-5 shadow-sm">

          <div className="flex flex-col gap-4 md:flex-row">

            <label className="flex flex-1 flex-col gap-2 text-sm font-medium">
              Category

              <select
                value={categoryFilter}
                onChange={(event) =>
                  setCategoryFilter(event.target.value)
                }
                className="rounded-lg border px-3 py-2 font-normal"
              >
                <option value="all">
                  All categories
                </option>

                {categories.map((category) => (
                  <option
                    key={category}
                    value={category}
                  >
                    {category}
                  </option>
                ))}
              </select>
            </label>

            <label className="flex flex-1 flex-col gap-2 text-sm font-medium">
              Finding type

              <select
                value={findingFilter}
                onChange={(event) =>
                  setFindingFilter(event.target.value)
                }
                className="rounded-lg border px-3 py-2 font-normal"
              >
                <option value="all">
                  All finding types
                </option>

                {findingTypes.map((type) => (
                  <option
                    key={type}
                    value={type}
                  >
                    {type}
                  </option>
                ))}
              </select>
            </label>

          </div>

        </section>

        {/* RESULTS */}

        <section className="rounded-xl border bg-white shadow-sm">

          <div className="border-b p-5">

            <h2 className="text-lg font-semibold">
              Comparative Intelligence Results
            </h2>

            <p className="mt-1 text-sm text-gray-600">
              {filteredResults.length} approved result(s) shown.
            </p>

          </div>

          {filteredResults.length === 0 ? (
            <div className="p-10 text-center">

              <h3 className="font-semibold">
                No matching results
              </h3>

              <p className="mt-2 text-sm text-gray-600">
                Change the filters or select all categories.
              </p>

            </div>
          ) : (
            <div className="overflow-x-auto">

              <table className="w-full text-left text-sm">

                <thead className="border-b bg-gray-50">
                  <tr>

                    <th className="px-5 py-3">
                      Metric
                    </th>

                    <th className="px-5 py-3">
                      Category
                    </th>

                    <th className="px-5 py-3">
                      Baseline
                    </th>

                    <th className="px-5 py-3">
                      Range
                    </th>

                    <th className="px-5 py-3">
                      Observations
                    </th>

                    <th className="px-5 py-3">
                      Finding
                    </th>

                    <th className="px-5 py-3">
                      Evidence
                    </th>

                  </tr>
                </thead>

                <tbody>

                  {filteredResults.map((item) => {

                    const limited =
                      item.finding_type ===
                      "insufficient_comparative_evidence";

                    return (
                      <tr
                        key={item.result_id}
                        className="border-b last:border-0"
                      >

                        <td className="px-5 py-4 font-medium">
                          {item.metric_name}
                        </td>

                        <td className="px-5 py-4">
                          {item.category}
                        </td>

                        {/* FIXED UNIT SPACING */}

                        <td className="px-5 py-4">

                          <span>
                            {formatNumber(
                              item.result_value
                            )}
                          </span>

                          {" "}

                          <span className="text-xs text-gray-500">
                            {item.result_unit}
                          </span>

                        </td>

                        <td className="px-5 py-4">
                          {formatNumber(
                            item.evidence.range
                          )}
                        </td>

                        <td className="px-5 py-4">
                          {item.evidence.observation_count}
                        </td>

                        <td className="max-w-md px-5 py-4">
                          {item.finding}
                        </td>

                        <td className="px-5 py-4">

                          <button
                            onClick={() =>
                              setSelectedResult(item)
                            }
                            className="rounded-lg border px-3 py-2 text-xs font-medium hover:bg-gray-50"
                          >
                            View evidence
                          </button>

                          {limited && (
                            <div className="mt-2 text-xs font-medium text-amber-700">
                              Limited evidence
                            </div>
                          )}

                        </td>

                      </tr>
                    );
                  })}

                </tbody>

              </table>

            </div>
          )}

        </section>

        {/* EVIDENCE DETAIL */}

        {selectedResult && (
          <section className="rounded-xl border bg-white p-6 shadow-sm">

            <div className="flex items-start justify-between gap-4">

              <div>

                <p className="text-xs uppercase tracking-wide text-gray-500">
                  Evidence Detail
                </p>

                <h2 className="mt-1 text-xl font-bold">
                  {selectedResult.metric_name}
                </h2>

              </div>

              <button
                onClick={() =>
                  setSelectedResult(null)
                }
                className="rounded-lg border px-3 py-2 text-sm"
              >
                Close
              </button>

            </div>

            <div className="mt-5 grid gap-4 md:grid-cols-2 lg:grid-cols-5">

              <DetailCard
                label="Observations"
                value={
                  selectedResult.evidence
                    .observation_count
                }
              />

              <DetailCard
                label="Baseline"
                value={`${formatNumber(
                  selectedResult.evidence
                    .baseline_value
                )} ${selectedResult.result_unit}`}
              />

              <DetailCard
                label="Minimum"
                value={`${formatNumber(
                  selectedResult.evidence.minimum
                )} ${selectedResult.result_unit}`}
              />

              <DetailCard
                label="Maximum"
                value={`${formatNumber(
                  selectedResult.evidence.maximum
                )} ${selectedResult.result_unit}`}
              />

              <DetailCard
                label="Range"
                value={`${formatNumber(
                  selectedResult.evidence.range
                )} ${selectedResult.result_unit}`}
              />

            </div>

            <div className="mt-6 space-y-4">

              <div>
                <h3 className="font-semibold">
                  Approved Finding
                </h3>

                <p className="mt-1 text-sm text-gray-700">
                  {selectedResult.finding}
                </p>
              </div>

              <div>
                <h3 className="font-semibold">
                  Limitation
                </h3>

                <p className="mt-1 text-sm text-gray-700">
                  {selectedResult.limitation}
                </p>
              </div>

              <div>
                <h3 className="font-semibold">
                  Traceability
                </h3>

                <p className="mt-1 text-sm text-gray-700">
                  Result ID: {selectedResult.result_id}
                  <br />
                  Method: {selectedResult.method_version}
                  <br />
                  Baseline method:{" "}
                  {selectedResult.baseline_method}
                  <br />
                  Data version:{" "}
                  {selectedResult.data_version}
                  <br />
                  Quality status:{" "}
                  {selectedResult.quality_status}
                </p>
              </div>

            </div>

          </section>
        )}

        {/* METHODOLOGY */}

        <section className="rounded-xl border bg-white p-6 shadow-sm">

          <h2 className="text-lg font-semibold">
            Methodology
          </h2>

          <div className="mt-4 space-y-3 text-sm text-gray-700">

            <p>
              <strong>Approved track:</strong>{" "}
              {summary.primary_track}
            </p>

            <p>
              <strong>Analysis:</strong>{" "}
              {summary.analysis_type}
            </p>

            <p>
              <strong>Baseline method:</strong>{" "}
              Arithmetic mean, as provided by the approved
              comparative result outputs.
            </p>

            <p>
              <strong>Validation:</strong>{" "}
              {metrics.status}
            </p>

            <p>
              <strong>Canonical records:</strong>{" "}
              {summary.record_count.toLocaleString()}
            </p>

            <p>
              <strong>Comparative groups:</strong>{" "}
              {summary.comparative_group_count.toLocaleString()}
            </p>

            <p>
              <strong>Findings:</strong>{" "}
              {summary.finding_count.toLocaleString()}
            </p>

            <p>
              {summary.interpretation}
            </p>

          </div>

        </section>

        {/* LIMITATIONS */}

        <section className="rounded-xl border border-amber-200 bg-amber-50 p-6">

          <h2 className="text-lg font-semibold text-amber-900">
            Limitations
          </h2>

          <div className="mt-4 space-y-3 text-sm text-amber-900">

            <p>
              <strong>Temporal context:</strong>{" "}
              {summary.temporal_context}
            </p>

            <p>
              <strong>Predictive capability:</strong>{" "}
              The approved analysis does not establish
              forecasting or predictive capability.
            </p>

            <p>
              Comparative findings are limited to compatible
              metric groups in the captured operational sample.
            </p>

            <p>
              Single-observation results are retained as
              approved outputs but should not be interpreted
              as sufficient comparative evidence for stability.
            </p>

          </div>

        </section>

        {/* FRESHNESS / METADATA */}

        <section className="rounded-xl border bg-white p-5 text-sm text-gray-600 shadow-sm">

          <div className="flex flex-wrap items-center gap-x-4 gap-y-2">

            <span>
              Generated at{" "}
              <strong>
                {new Date(
                  summary.generated_at
                ).toLocaleString()}
              </strong>
            </span>

            <span>�</span>

            <span>
              Data version{" "}
              <strong>
                {summary.data_version}
              </strong>
            </span>

            <span>�</span>

            <span>
              Validation{" "}
              <strong>
                {metrics.status}
              </strong>
            </span>

            <span>�</span>

            <span>
              Freshness{" "}
              <FreshnessBadge
                freshness={freshness}
              />
            </span>

          </div>

        </section>

      </div>
    </main>
  );
}

function SummaryCard({
  label,
  value,
}: {
  label: string;
  value: number;
}) {
  return (
    <div className="rounded-xl border bg-white p-5 shadow-sm">

      <p className="text-sm text-gray-500">
        {label}
      </p>

      <p className="mt-2 text-3xl font-bold">
        {value.toLocaleString()}
      </p>

    </div>
  );
}

function DetailCard({
  label,
  value,
}: {
  label: string;
  value: string | number;
}) {
  return (
    <div className="rounded-lg border bg-gray-50 p-4">

      <p className="text-xs text-gray-500">
        {label}
      </p>

      <p className="mt-1 font-semibold">
        {value}
      </p>

    </div>
  );
}

function QualityBadge({
  status,
}: {
  status: string;
}) {
  const normalized = status.toLowerCase();

  if (
    normalized === "pass" ||
    normalized === "validated"
  ) {
    return (
      <span className="inline-flex rounded-full border border-green-300 bg-green-50 px-3 py-1 text-sm font-semibold text-green-700">
        {status}
      </span>
    );
  }

  if (normalized === "conditional") {
    return (
      <span className="inline-flex rounded-full border border-amber-300 bg-amber-50 px-3 py-1 text-sm font-semibold text-amber-700">
        {status}
      </span>
    );
  }

  if (normalized === "rejected") {
    return (
      <span className="inline-flex rounded-full border border-red-300 bg-red-50 px-3 py-1 text-sm font-semibold text-red-700">
        {status}
      </span>
    );
  }

  return (
    <span className="inline-flex rounded-full border bg-gray-50 px-3 py-1 text-sm font-semibold text-gray-700">
      {status}
    </span>
  );
}

function FreshnessBadge({
  freshness,
}: {
  freshness: FreshnessState;
}) {
  if (freshness === "fresh") {
    return (
      <span className="inline-flex rounded-full border border-green-300 bg-green-50 px-2 py-0.5 text-xs font-semibold text-green-700">
        Fresh
      </span>
    );
  }

  if (freshness === "stale") {
    return (
      <span className="inline-flex rounded-full border border-amber-300 bg-amber-50 px-2 py-0.5 text-xs font-semibold text-amber-700">
        Stale
      </span>
    );
  }

  return (
    <span className="inline-flex rounded-full border bg-gray-50 px-2 py-0.5 text-xs font-semibold text-gray-600">
      Unknown
    </span>
  );
}

function formatNumber(value: number) {
  return new Intl.NumberFormat("en-US", {
    maximumFractionDigits: 2,
  }).format(value);
}


