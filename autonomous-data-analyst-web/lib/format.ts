import { BACKEND_ORIGIN } from "./config";
import type { Finding, Json, Row } from "./types";

export function formatInt(value: number): string {
  return value.toLocaleString("en-US");
}

export function formatExact(value: number): string {
  if (Number.isInteger(value)) return formatInt(value);
  return value.toLocaleString("en-US", { maximumFractionDigits: Math.abs(value) >= 1 ? 2 : 4 });
}

export function formatCompact(value: number): { figure: string; suffix: string } {
  const units: Array<[number, string]> = [
    [1e12, "T"],
    [1e9, "B"],
    [1e6, "M"],
    [1e3, "K"],
  ];
  for (const [limit, suffix] of units) {
    if (Math.abs(value) >= limit) {
      return { figure: (value / limit).toFixed(2).replace(/\.?0+$/, ""), suffix };
    }
  }
  return { figure: formatExact(value), suffix: "" };
}

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  const units = ["KB", "MB", "GB"];
  let amount = bytes / 1024;
  let unit = 0;
  while (amount >= 1024 && unit < units.length - 1) {
    amount /= 1024;
    unit += 1;
  }
  return `${amount.toFixed(amount >= 100 ? 0 : 1)} ${units[unit]}`;
}

export function humanize(key: string): string {
  const text = key.replace(/[_-]+/g, " ").trim();
  return text.charAt(0).toUpperCase() + text.slice(1);
}

export function basename(path: string): string {
  return path.split(/[\\/]/).filter(Boolean).pop() ?? path;
}

export function pluralize(word: string): string {
  if (/[^aeiou]y$/i.test(word)) return `${word.slice(0, -1)}ies`;
  if (/(s|x|z|ch|sh)$/i.test(word)) return `${word}es`;
  return `${word}s`;
}

export function isRow(value: Json | undefined): value is Row {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

/**
 * Backend chart paths look like `reports\charts\bar_chart.png` (Windows) or an
 * absolute path. Returns a browser URL under the backend's /reports mount, or
 * null if the path cannot be mapped. `version` busts the cache because the
 * backend overwrites charts under fixed file names.
 */
export function chartUrl(path: string, version: string): string | null {
  const normalized = path.replace(/\\/g, "/");
  const index = normalized.toLowerCase().lastIndexOf("reports/");
  if (index === -1) return null;
  const relative = normalized
    .slice(index + "reports/".length)
    .split("/")
    .filter(Boolean)
    .map(encodeURIComponent)
    .join("/");
  if (!relative) return null;
  return `${BACKEND_ORIGIN}/reports/${relative}?v=${encodeURIComponent(version)}`;
}

export interface PrimaryFinding {
  entity: string;
  entityKey: string;
  metric: string;
  value: number;
  lowEntity?: string;
  lowValue?: number;
  message: string;
}

function splitRow(
  row: Row,
  metricHint: string | undefined,
): { entity: string; entityKey: string; metric: string; value: number } | null {
  const numeric = Object.keys(row).filter((key) => typeof row[key] === "number");
  if (numeric.length === 0) return null;
  const metric = metricHint && numeric.includes(metricHint) ? metricHint : numeric[numeric.length - 1];
  const entityKey = Object.keys(row).find((key) => key !== metric);
  if (!entityKey) return null;
  return { entity: String(row[entityKey]), entityKey, metric, value: row[metric] as number };
}

/** Reads the backend's group_aggregate finding. Returns null if none exists. */
export function primaryFinding(findings: Finding[]): PrimaryFinding | null {
  for (const finding of findings) {
    if (!isRow(finding.highest)) continue;
    const high = splitRow(finding.highest, finding.metric);
    if (!high) continue;
    const low = isRow(finding.lowest) ? splitRow(finding.lowest, finding.metric) : null;
    return {
      entity: high.entity,
      entityKey: high.entityKey,
      metric: high.metric,
      value: high.value,
      lowEntity: low?.entity,
      lowValue: low?.value,
      message: finding.message ?? "",
    };
  }
  return null;
}
