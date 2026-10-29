"use client";

import { motion } from "motion/react";

export const STAGES = ["planning", "executing", "observing", "validating", "complete"] as const;
export type Stage = (typeof STAGES)[number];

interface RunStagesProps {
  stage: Stage;
  failed: boolean;
}

/**
 * The backend answers in one response, so these stages reflect the progress of
 * the frontend request, not live backend events.
 */
export function RunStages({ stage, failed }: RunStagesProps) {
  const activeIndex = STAGES.indexOf(stage);

  return (
    <div role="status" aria-live="polite">
      <ol className="grid grid-cols-5 gap-2">
        {STAGES.map((name, index) => {
          const done = index < activeIndex || (stage === "complete" && index === activeIndex);
          const active = index === activeIndex && stage !== "complete";
          const errored = failed && active;
          return (
            <li key={name} className="min-w-0">
              <div className="relative h-px bg-line">
                <motion.div
                  className={`absolute inset-y-0 left-0 w-full origin-left ${errored ? "bg-bad" : done ? "bg-ink" : "bg-accent"}`}
                  initial={false}
                  animate={{ scaleX: done || errored ? 1 : active ? 0.5 : 0 }}
                  transition={{ duration: 0.3, ease: [0.23, 1, 0.32, 1] }}
                />
              </div>
              <p
                className={`mono-label mt-2 truncate transition-colors duration-200 ${
                  errored ? "!text-bad" : active ? "!text-accent" : done ? "!text-ink" : ""
                }`}
              >
                {name}
              </p>
            </li>
          );
        })}
      </ol>
      <p className="mono-label mt-3 normal-case tracking-normal">
        Stages show the progress of this request in the browser.
      </p>
    </div>
  );
}
