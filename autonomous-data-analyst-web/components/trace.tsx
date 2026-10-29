"use client";

import { motion } from "motion/react";
import type { EvidenceRecord, ToolCall } from "@/lib/types";
import { Section } from "./section";

type CallState = "executed" | "failed";

/**
 * The backend records a tool call before running it and writes an evidence
 * record only after it succeeds. Matching calls to evidence in order therefore
 * shows which calls completed; a call without evidence did not.
 */
function callStates(calls: ToolCall[], evidence: EvidenceRecord[]): CallState[] {
  let pointer = 0;
  return calls.map((call) => {
    const record = evidence[pointer];
    if (record && record.operation === call.action && JSON.stringify(record.parameters ?? {}) === JSON.stringify(call.parameters ?? {})) {
      pointer += 1;
      return "executed";
    }
    return "failed";
  });
}

export function TraceSection({ calls, evidence }: { calls: ToolCall[]; evidence: EvidenceRecord[] }) {
  const states = callStates(calls, evidence);

  return (
    <Section title="Execution trace" note="Tool calls in the order they ran. Reasoning is not shown.">
      {calls.length === 0 ? (
        <p className="text-[15px] text-muted">No tool calls were recorded.</p>
      ) : (
        <ol className="border-t border-line">
          {calls.map((call, index) => {
            const parameters = Object.entries(call.parameters ?? {});
            return (
              <motion.li
                key={`${call.action}-${index}`}
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.25, delay: Math.min(index, 5) * 0.04 }}
                className="border-b border-line py-4"
              >
                <details className="group">
                  <summary className="grid cursor-pointer list-none grid-cols-[32px_minmax(0,1fr)_auto] items-baseline gap-4">
                    <span className="mono-label">{String(index + 1).padStart(2, "0")}</span>
                    <span className="min-w-0">
                      <span className="font-mono text-[15px]">{call.action}</span>
                      {parameters.length > 0 && (
                        <span className="mt-0.5 block truncate font-mono text-[12.5px] text-muted">
                          {parameters.map(([k, v]) => `${k}=${typeof v === "string" ? v : JSON.stringify(v)}`).join("  ")}
                        </span>
                      )}
                    </span>
                    <span className={`mono-label ${states[index] === "executed" ? "!text-ok" : "!text-bad"}`}>
                      {states[index]}
                    </span>
                  </summary>
                  <pre className="ml-[48px] mt-3 max-h-56 overflow-auto border border-line bg-surface p-3 font-mono text-[12.5px] leading-5">
                    {JSON.stringify(call, null, 2)}
                  </pre>
                </details>
              </motion.li>
            );
          })}
        </ol>
      )}
    </Section>
  );
}
