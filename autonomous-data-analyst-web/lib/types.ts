/** Response shapes of the existing FastAPI backend (app/api/upload.py, routes.py). */

export type Json =
  | string
  | number
  | boolean
  | null
  | Json[]
  | { [key: string]: Json };

export type Row = Record<string, Json>;

export interface UploadValidation {
  valid: boolean;
  rows: number;
  columns: number;
  column_names: string[];
  missing_values: number;
  duplicate_rows: number;
  file_size_bytes: number;
}

export interface UploadResponse {
  /** Server file path. Must be sent back to /analyze exactly as received. */
  dataset_id: string;
  filename: string;
  size_bytes: number;
  extension: string;
  validation: UploadValidation;
}

export interface PlanStep {
  step?: number;
  action: string;
  parameters?: Row;
}

export interface ToolCall {
  action: string;
  parameters: Row;
}

export interface Finding {
  type?: string;
  metric?: string;
  highest?: Row;
  lowest?: Row;
  message?: string;
}

export interface EvidenceRecord {
  timestamp?: string;
  dataset_id?: string;
  columns?: string[];
  operation: string;
  parameters?: Row;
  result?: Json;
}

export interface ValidationCheck {
  check: string;
  passed: boolean;
  message: string;
}

export interface BackendError {
  type?: string;
  message: string;
}

export interface AnalyzeResponse {
  session_id: string;
  status: string;
  user_query: string;
  dataset_id: string;
  analysis_plan: PlanStep[];
  tool_calls: ToolCall[];
  findings: Finding[];
  visualizations: string[];
  evidence: EvidenceRecord[];
  validation_results: ValidationCheck[];
  errors: BackendError[];
  final_report: string;
}
