"use client";

import { useState } from "react";
import { motion } from "motion/react";
import { basename, formatExact, isRow } from "@/lib/format";
import type { EvidenceRecord, Json, Row } from "@/lib/types";
import { Section } from "./section";

function isFlatRows(value: Json | undefined): value is Row[] {
  return (
    Array.isArray(value) &&
    value.length > 0 &&
    value.every((item) => isRow(item) && Object.values(item).every((v) => typeof v !== "object" || v === null))
  );
}

function cell(value: Json): string {
  if (typeof value === "number") return formatExact(value);
  if (value === null) return "";
  return String(value);
}

function ResultView({ result }: { result: Json | undefined }) {
  const [expanded, setExpanded] = useState(false);

  if (result === undefined || result === null) return <span className="text-muted">None</span>;

  if (typeof result === "string") return <span className="break-all font-mono text-[13px]">{result}</span>;

  if (isFlatRows(result)) {
    const columns = Object.keys(result[0]);
    const shown = expanded ? result : result.slice(0, 8);
    return (
      <div>
        <p className="mono-label mb-2">{result.length} rows</p>
        <div className="overflow-x-auto border border-line bg-surface">
          <table className="w-full border-collapse text-left text-[13px]">
            <thead>
              <tr className="border-b border-line">
                {columns.map((column) => (
                  <th key={column} className="mono-label whitespace-nowrap px-3 py-2 font-normal">
                    {column}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {shown.map((row, index) => (
                <tr key={index} className="border-b border-line last:border-b-0">
                  {columns.map((column) => (
                    <td
                      key={column}
                      className={`whitespace-nowrap px-3 py-1.5 ${typeof row[column] === "number" ? "text-right font-mono tabular-nums" : ""}`}
                    >
                      {cell(row[column])}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {result.length > 8 && (
          <button
            type="button"
            onClick={() => setExpanded((open) => !open)}
            className="mono-label mt-2 transition-colors hover:!text-ink"
          >
            {expanded ? "Show first 8" : `Show all ${result.length}`}
          </button>
        )}
      </div>
    );
  }

  return (
    <pre className="max-h-64 overflow-auto border border-line bg-surface p-3 font-mono text-[12.5px] leading-5">
      {JSON.stringify(result, null, 2)}
    </pre>
  );
}

function Parameters({ parameters }: { parameters: Row | undefined }) {
  const entries = parameters ? Object.entries(parameters) : [];
  if (entries.length === 0) return <span className="text-muted">None</span>;
  return (
    <ul className="space-y-0.5 font-mono text-[13px]">
      {entries.map(([key, value]) => (
        <li key={key}>
          <span className="text-muted">{key}</span> = {typeof value === "string" ? value : JSON.stringify(value)}
        </li>
      ))}
    </ul>
  );
}

function Line({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <div className="grid gap-1 border-b border-line py-3 sm:grid-cols-[110px_minmax(0,1fr)] sm:gap-6">
      <dt className="mono-label pt-0.5">{label}</dt>
      <dd className="min-w-0 text-[15px]">{children}</dd>
    </div>
  );
}

export function EvidenceSection({ evidence, findingMessage }: { evidence: EvidenceRecord[]; findingMessage: string | undefined }) {
  return (
    <Section title="Evidence" note="Dataset, columns, operation, parameters and result for each executed step.">
      {evidence.length === 0 ? (
        <p className="text-[15px] text-muted">No evidence was recorded.</p>
      ) : (
        <ol className="space-y-8">
          {evidence.map((record, index) => (
            <motion.li
              key={`${record.operation}-${index}`}
              initial={{ opacity: 0, y: 8 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "0px 0px -40px 0px" }}
              transition={{ duration: 0.3, ease: [0.23, 1, 0.32, 1], delay: Math.min(index, 3) * 0.05 }}
              className="border-l border-ink pl-5"
            >
              <p className="mono-label !text-ink">
                {String(index + 1).padStart(2, "0")} <span className="ml-2">{record.operation}</span>
              </p>
              <dl className="mt-2 border-t border-line">
                <Line label="Dataset">
                  <span className="font-mono text-[13px]" title={record.dataset_id}>
                    {record.dataset_id ? basename(record.dataset_id) : "Unknown"}
                  </span>
                </Line>
                <Line label="Columns">
                  {record.columns && record.columns.length > 0 ? (
                    <span className="flex flex-wrap gap-1.5">
                      {record.columns.map((column) => (
                        <span key={column} className="border border-line bg-surface px-2 py-0.5 font-mono text-[12.5px]">
                          {column}
                        </span>
                      ))}
                    </span>
                  ) : (
                    <span className="text-muted">None</span>
                  )}
                </Line>
                <Line label="Operation">
                  <span className="font-mono text-[13px]">{record.operation}</span>
                </Line>
                <Line label="Parameters">
                  <Parameters parameters={record.parameters} />
                </Line>
                <Line label="Result">
                  <ResultView result={record.result} />
                </Line>
                {record.timestamp && (
                  <Line label="Recorded">
                    <span className="font-mono text-[12.5px] text-muted">{record.timestamp}</span>
                  </Line>
                )}
              </dl>
            </motion.li>
          ))}
        </ol>
      )}
      {evidence.length > 0 && findingMessage && (
        <p className="mt-8 border-l border-accent pl-5">
          <span className="mono-label !text-accent">Finding</span>
          <span className="mt-1 block break-words font-mono text-[12.5px] leading-5 text-[#3b3b39]">{findingMessage}</span>
        </p>
      )}
    </Section>
  );
}
