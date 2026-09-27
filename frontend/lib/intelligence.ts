import type {
  IntelligenceResult,
  IntelligenceResultsPackage,
  IntelligenceSummary,
  ValidationMetrics,
} from "@/types/intelligence";

const QUALITY_VALUES = new Set([
  "PASS",
  "validated",
  "conditional",
  "rejected",
]);

function requireString(
  value: unknown,
  field: string
): asserts value is string {
  if (typeof value !== "string" || value.length === 0) {
    throw new Error(`Invalid required field: ${field}`);
  }
}

function requireNumber(
  value: unknown,
  field: string
): asserts value is number {
  if (typeof value !== "number" || Number.isNaN(value)) {
    throw new Error(`Invalid numeric field: ${field}`);
  }
}

export function validateIntelligenceResult(
  value: unknown
): asserts value is IntelligenceResult {
  if (!value || typeof value !== "object") {
    throw new Error("Intelligence result must be an object");
  }

  const item = value as Record<string, unknown>;

  const requiredStrings = [
    "result_id",
    "result_type",
    "primary_track",
    "metric_name",
    "result_unit",
    "category",
    "finding_type",
    "finding",
    "method_version",
    "baseline_method",
    "data_version",
    "generated_at",
    "limitation",
  ];

  for (const field of requiredStrings) {
    requireString(item[field], field);
  }

  requireNumber(item.result_value, "result_value");

  if (!QUALITY_VALUES.has(String(item.quality_status))) {
    throw new Error(
      `Unsupported quality_status: ${String(item.quality_status)}`
    );
  }

  if (!item.evidence || typeof item.evidence !== "object") {
    throw new Error(`Invalid evidence for ${item.result_id}`);
  }

  const evidence = item.evidence as Record<string, unknown>;

  for (const field of [
    "observation_count",
    "baseline_value",
    "minimum",
    "maximum",
    "range",
  ]) {
    requireNumber(evidence[field], `evidence.${field}`);
  }

  if (Number.isNaN(Date.parse(String(item.generated_at)))) {
    throw new Error(`Invalid generated_at for ${item.result_id}`);
  }
}

export function validateResultsPackage(
  value: unknown
): asserts value is IntelligenceResultsPackage {
  if (!value || typeof value !== "object") {
    throw new Error("Intelligence results package must be an object");
  }

  const packageValue = value as Record<string, unknown>;

  requireString(packageValue.primary_track, "primary_track");

  if (!Array.isArray(packageValue.results)) {
    throw new Error("results must be an array");
  }

  const ids = new Set<string>();

  packageValue.results.forEach((item) => {
    validateIntelligenceResult(item);

    if (ids.has(item.result_id)) {
      throw new Error(`Duplicate result_id: ${item.result_id}`);
    }

    ids.add(item.result_id);
  });
}

export function validateSummary(
  value: unknown
): asserts value is IntelligenceSummary {
  if (!value || typeof value !== "object") {
    throw new Error("Intelligence summary must be an object");
  }

  const item = value as Record<string, unknown>;

  for (const field of [
    "summary_type",
    "primary_track",
    "data_version",
    "analysis_type",
    "interpretation",
    "temporal_context",
    "predictive_capability",
    "generated_at",
  ]) {
    requireString(item[field], field);
  }

  for (const field of [
    "record_count",
    "comparative_group_count",
    "finding_count",
  ]) {
    requireNumber(item[field], field);
  }

  requireString(item.validation_status, "validation_status");
}

export function validateMetrics(
  value: unknown
): asserts value is ValidationMetrics {
  if (!value || typeof value !== "object") {
    throw new Error("Validation metrics must be an object");
  }

  const item = value as Record<string, unknown>;

  for (const field of [
    "validation_type",
    "primary_track",
    "data_version",
    "input",
    "status",
  ]) {
    requireString(item[field], field);
  }

  for (const field of [
    "record_count",
    "comparative_group_count",
    "finding_count",
  ]) {
    requireNumber(item[field], field);
  }

  if (!Array.isArray(item.errors)) {
    throw new Error("validation errors must be an array");
  }

  if (!item.checks || typeof item.checks !== "object") {
    throw new Error("validation checks must be an object");
  }
}

export async function loadIntelligenceData() {
  const [resultsResponse, summaryResponse, metricsResponse] =
    await Promise.all([
      fetch("/data/intelligence/results.json", {
        cache: "no-store",
      }),
      fetch("/data/intelligence/summary.json", {
        cache: "no-store",
      }),
      fetch("/data/intelligence/validation_metrics.json", {
        cache: "no-store",
      }),
    ]);

  if (!resultsResponse.ok) {
    throw new Error(
      `Unable to load intelligence results: ${resultsResponse.status}`
    );
  }

  if (!summaryResponse.ok) {
    throw new Error(
      `Unable to load intelligence summary: ${summaryResponse.status}`
    );
  }

  if (!metricsResponse.ok) {
    throw new Error(
      `Unable to load validation metrics: ${metricsResponse.status}`
    );
  }

  const results: unknown = await resultsResponse.json();
  const summary: unknown = await summaryResponse.json();
  const metrics: unknown = await metricsResponse.json();

  validateResultsPackage(results);
  validateSummary(summary);
  validateMetrics(metrics);

  if (results.primary_track !== summary.primary_track) {
    throw new Error("Track mismatch between results and summary");
  }

  if (results.results.some(
    (item) => item.data_version !== summary.data_version
  )) {
    throw new Error("Data version mismatch between summary and results");
  }

  return {
    results,
    summary,
    metrics,
  };
}
