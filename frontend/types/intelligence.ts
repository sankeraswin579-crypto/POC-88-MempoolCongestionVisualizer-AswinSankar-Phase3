export type IntelligenceQuality =
  | "PASS"
  | "validated"
  | "conditional"
  | "rejected";

export interface IntelligenceEvidence {
  observation_count: number;
  baseline_value: number;
  minimum: number;
  maximum: number;
  range: number;
}

export interface IntelligenceResult {
  result_id: string;
  result_type: string;
  primary_track: string;
  metric_name: string;
  result_value: number;
  result_unit: string;
  category: string;
  finding_type: string;
  finding: string;
  evidence: IntelligenceEvidence;
  method_version: string;
  baseline_method: string;
  data_version: string;
  generated_at: string;
  quality_status: IntelligenceQuality;
  limitation: string;
}

export interface IntelligenceResultsPackage {
  primary_track: string;
  results: IntelligenceResult[];
}

export interface IntelligenceSummary {
  summary_type: string;
  primary_track: string;
  data_version: string;
  analysis_type: string;
  record_count: number;
  comparative_group_count: number;
  finding_count: number;
  validation_status: string;
  interpretation: string;
  temporal_context: string;
  predictive_capability: string;
  generated_at: string;
}

export interface ValidationMetrics {
  validation_type: string;
  primary_track: string;
  data_version: string;
  input: string;
  status: string;
  record_count: number;
  comparative_group_count: number;
  finding_count: number;
  errors: string[];
  checks: Record<string, boolean>;
}
