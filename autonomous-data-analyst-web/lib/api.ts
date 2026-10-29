import { API_BASE_URL } from "./config";
import type { AnalyzeResponse, UploadResponse } from "./types";

export type ApiErrorKind = "network" | "http" | "malformed" | "aborted";

export class ApiError extends Error {
  readonly kind: ApiErrorKind;
  readonly status?: number;

  constructor(kind: ApiErrorKind, message: string, status?: number) {
    super(message);
    this.name = "ApiError";
    this.kind = kind;
    this.status = status;
  }
}

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

function isUploadResponse(value: unknown): value is UploadResponse {
  if (!isRecord(value) || !isRecord(value.validation)) return false;
  const v = value.validation;
  return (
    typeof value.dataset_id === "string" &&
    typeof value.filename === "string" &&
    typeof value.size_bytes === "number" &&
    typeof v.rows === "number" &&
    typeof v.columns === "number" &&
    Array.isArray(v.column_names)
  );
}

function isAnalyzeResponse(value: unknown): value is AnalyzeResponse {
  if (!isRecord(value)) return false;
  return (
    typeof value.session_id === "string" &&
    typeof value.status === "string" &&
    typeof value.final_report === "string" &&
    [
      "analysis_plan",
      "tool_calls",
      "findings",
      "visualizations",
      "evidence",
      "validation_results",
      "errors",
    ].every((key) => Array.isArray(value[key]))
  );
}

/** FastAPI errors arrive as {"detail": string | [{loc, msg}]}. */
function detailMessage(body: unknown, fallback: string): string {
  if (isRecord(body)) {
    const detail = body.detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail)) {
      return detail
        .map((item: unknown) => {
          if (isRecord(item) && typeof item.msg === "string") {
            const where = Array.isArray(item.loc) ? `${item.loc.join(".")}: ` : "";
            return `${where}${item.msg}`;
          }
          return JSON.stringify(item);
        })
        .join("; ");
    }
  }
  return fallback;
}

const unreachable = () =>
  `Cannot reach the backend at ${API_BASE_URL}. Check that FastAPI is running and allows this origin (CORS).`;

export interface UploadProgress {
  loaded: number;
  total: number;
}

/** POST /upload as multipart `file`. XHR is used because fetch cannot report upload progress. */
export function uploadDataset(
  file: File,
  onProgress: (progress: UploadProgress) => void,
  signal?: AbortSignal,
): Promise<UploadResponse> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `${API_BASE_URL}/upload`);

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) onProgress({ loaded: event.loaded, total: event.total });
    };

    xhr.onload = () => {
      let body: unknown = null;
      try {
        body = JSON.parse(xhr.responseText);
      } catch {
        body = null;
      }
      if (xhr.status >= 200 && xhr.status < 300) {
        if (isUploadResponse(body)) resolve(body);
        else reject(new ApiError("malformed", "Upload succeeded but the response was not in the expected format."));
      } else {
        reject(new ApiError("http", detailMessage(body, `Upload failed (HTTP ${xhr.status}).`), xhr.status));
      }
    };

    xhr.onerror = () => reject(new ApiError("network", unreachable()));
    xhr.ontimeout = () => reject(new ApiError("network", "The upload timed out."));
    xhr.onabort = () => reject(new ApiError("aborted", "Upload cancelled."));
    signal?.addEventListener("abort", () => xhr.abort(), { once: true });

    const form = new FormData();
    form.append("file", file);
    xhr.send(form);
  });
}

/** POST /analyze. `datasetId` is forwarded exactly as /upload returned it. */
export async function analyze(
  userQuery: string,
  datasetId: string,
  signal?: AbortSignal,
): Promise<AnalyzeResponse> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_query: userQuery, dataset_id: datasetId }),
      signal,
    });
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new ApiError("aborted", "Analysis cancelled.");
    }
    throw new ApiError("network", unreachable());
  }

  const body: unknown = await response.json().catch(() => null);

  if (!response.ok) {
    throw new ApiError("http", detailMessage(body, `Analysis failed (HTTP ${response.status}).`), response.status);
  }
  if (!isAnalyzeResponse(body)) {
    throw new ApiError("malformed", "The backend returned an analysis in an unexpected format.");
  }
  return body;
}

/** GET /health. Resolves false on any failure. */
export async function checkHealth(signal?: AbortSignal): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, { signal, cache: "no-store" });
    return response.ok;
  } catch {
    return false;
  }
}
