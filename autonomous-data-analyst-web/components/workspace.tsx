"use client";

import { useEffect, useRef, useState } from "react";
import { AnimatePresence, MotionConfig, motion, useReducedMotion } from "motion/react";
import { analyze, ApiError } from "@/lib/api";
import type { AnalyzeResponse, UploadResponse } from "@/lib/types";
import { DatasetSummary } from "./dataset-summary";
import { QueryPanel } from "./query-panel";
import { Result } from "./result";
import { RunStages, STAGES, type Stage } from "./run-stages";
import { UploadZone } from "./upload-zone";

type Run =
  | { kind: "idle" }
  | { kind: "running"; stage: Stage }
  | { kind: "done"; result: AnalyzeResponse }
  | { kind: "error"; stage: Stage; message: string };

const STAGE_INTERVAL_MS = 2200;
const ease = [0.23, 1, 0.32, 1] as const;

export function Workspace() {
  const [dataset, setDataset] = useState<UploadResponse | null>(null);
  const [query, setQuery] = useState("");
  const [run, setRun] = useState<Run>({ kind: "idle" });
  const abortRef = useRef<AbortController | null>(null);
  const resultRef = useRef<HTMLDivElement>(null);
  const reduceMotion = useReducedMotion();

  useEffect(() => () => abortRef.current?.abort(), []);

  useEffect(() => {
    if (run.kind === "done") {
      resultRef.current?.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
    }
  }, [run.kind, reduceMotion]);

  const running = run.kind === "running";

  async function runAnalysis() {
    if (!dataset || query.trim() === "" || running) return;

    const controller = new AbortController();
    abortRef.current = controller;
    setRun({ kind: "running", stage: "planning" });

    // The backend replies once, so the stage advances on a timer and holds at
    // "validating" until the response arrives. It reflects the request, not backend events.
    const timer = window.setInterval(() => {
      setRun((current) => {
        if (current.kind !== "running") return current;
        const next = STAGES.indexOf(current.stage) + 1;
        return next <= STAGES.indexOf("validating") ? { kind: "running", stage: STAGES[next] } : current;
      });
    }, STAGE_INTERVAL_MS);

    try {
      // dataset_id is forwarded exactly as /upload returned it.
      const result = await analyze(query.trim(), dataset.dataset_id, controller.signal);
      setRun({ kind: "done", result });
    } catch (error) {
      if (error instanceof ApiError && error.kind === "aborted") return;
      setRun((current) => ({
        kind: "error",
        stage: current.kind === "running" ? current.stage : "planning",
        message: error instanceof Error ? error.message : "Analysis failed.",
      }));
    } finally {
      window.clearInterval(timer);
    }
  }

  function replaceDataset() {
    abortRef.current?.abort();
    setDataset(null);
    setRun({ kind: "idle" });
  }

  const showStages = run.kind !== "idle";
  const stage: Stage = run.kind === "done" ? "complete" : run.kind === "idle" ? "planning" : run.stage;

  return (
    <MotionConfig reducedMotion="user">
      <div className="mx-auto w-full max-w-[1080px] px-5 py-10 sm:px-10 lg:px-14 lg:py-16">
        <motion.header
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, ease }}
        >
          <h1
            className={`font-medium leading-[0.98] tracking-[-0.04em] transition-[font-size] duration-300 ${
              dataset ? "text-[clamp(2rem,4vw,3rem)]" : "text-[clamp(2.75rem,7vw,5.5rem)]"
            }`}
          >
            Ask questions.
            <span className="block text-muted">Get answers.</span>
          </h1>
          {!dataset && (
            <p className="mt-6 max-w-xl text-lg leading-7 text-[#3b3b39]">
              Upload a dataset, ask a question in plain language, and let the analytical engine plan, execute, validate
              and document the work.
            </p>
          )}
        </motion.header>

        <div className="mt-12 space-y-12 lg:mt-14">
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, ease, delay: 0.08 }}
          >
            <AnimatePresence mode="wait" initial={false}>
              {dataset ? (
                <DatasetSummary key={dataset.dataset_id} dataset={dataset} onReplace={replaceDataset} disabled={running} />
              ) : (
                <motion.div key="upload" exit={{ opacity: 0 }} transition={{ duration: 0.15 }}>
                  <p className="mono-label mb-3">Dataset</p>
                  <UploadZone
                    onUploaded={(uploaded) => {
                      setDataset(uploaded);
                      setRun({ kind: "idle" });
                    }}
                  />
                </motion.div>
              )}
            </AnimatePresence>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, ease, delay: 0.16 }}
          >
            <QueryPanel
              query={query}
              onQueryChange={setQuery}
              onRun={() => void runAnalysis()}
              running={running}
              hasDataset={dataset !== null}
            />
          </motion.div>

          <AnimatePresence initial={false}>
            {showStages && (
              <motion.div
                key="stages"
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                transition={{ duration: 0.25, ease }}
              >
                <RunStages stage={stage} failed={run.kind === "error"} />
                {run.kind === "error" && (
                  <p role="alert" className="mt-5 border-l-2 border-bad pl-3 text-[14px] leading-6 text-bad">
                    {run.message}
                  </p>
                )}
              </motion.div>
            )}
          </AnimatePresence>

          {run.kind === "done" && (
            <div ref={resultRef} className="scroll-mt-8 border-t border-ink pt-10">
              <Result result={run.result} />
            </div>
          )}
        </div>
      </div>
    </MotionConfig>
  );
}
