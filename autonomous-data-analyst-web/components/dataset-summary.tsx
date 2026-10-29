"use client";

import { motion } from "motion/react";
import { formatBytes, formatInt } from "@/lib/format";
import type { UploadResponse } from "@/lib/types";

export function DatasetSummary({ dataset, onReplace, disabled }: { dataset: UploadResponse; onReplace: () => void; disabled: boolean }) {
  const v = dataset.validation;
  const facts: Array<{ label: string; value: string; tone?: "ok" | "warn" }> = [
    { label: "Rows", value: formatInt(v.rows) },
    { label: "Columns", value: formatInt(v.columns) },
    { label: "Missing values", value: formatInt(v.missing_values), tone: v.missing_values > 0 ? "warn" : undefined },
    { label: "Duplicates", value: formatInt(v.duplicate_rows), tone: v.duplicate_rows > 0 ? "warn" : undefined },
    { label: "File size", value: formatBytes(dataset.size_bytes) },
  ];

  return (
    <motion.section
      aria-label="Dataset"
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: [0.23, 1, 0.32, 1] }}
    >
      <div className="flex items-start justify-between gap-6">
        <div className="min-w-0">
          <p className="mono-label flex items-center gap-2">
            Dataset
            <span className={v.valid ? "text-ok" : "text-bad"}>{v.valid ? "Validation pass" : "Validation fail"}</span>
          </p>
          <h2 className="mt-2 break-words text-2xl font-medium tracking-tight sm:text-3xl">{dataset.filename}</h2>
        </div>
        <button
          type="button"
          onClick={onReplace}
          disabled={disabled}
          className="mono-label shrink-0 border border-line bg-surface px-3 py-2 transition-colors duration-150 hover:border-ink hover:!text-ink disabled:opacity-40 disabled:hover:border-line"
        >
          Replace
        </button>
      </div>

      <dl className="mt-6 grid grid-cols-2 border-t border-ink sm:grid-cols-3 lg:grid-cols-5">
        {facts.map((fact, i) => (
          <motion.div
            key={fact.label}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.25, delay: 0.05 * i }}
            className="border-b border-line py-4 pr-4 [&:not(:first-child)]:lg:pl-5 lg:border-l lg:first:border-l-0"
          >
            <dt className="mono-label">{fact.label}</dt>
            <dd
              className={`mt-1 text-2xl font-medium tabular-nums tracking-tight ${fact.tone === "warn" ? "text-warn" : ""}`}
            >
              {fact.value}
            </dd>
          </motion.div>
        ))}
      </dl>

      <details className="group mt-4">
        <summary className="mono-label cursor-pointer select-none list-none transition-colors hover:!text-ink">
          <span className="mr-2 inline-block transition-transform duration-150 group-open:rotate-90" aria-hidden>
            ›
          </span>
          Columns ({v.column_names.length})
        </summary>
        <ul className="mt-3 flex flex-wrap gap-1.5">
          {v.column_names.map((name) => (
            <li key={name} className="border border-line bg-surface px-2 py-1 font-mono text-[12.5px]">
              {name}
            </li>
          ))}
        </ul>
      </details>
    </motion.section>
  );
}
