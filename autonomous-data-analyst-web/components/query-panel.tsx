"use client";

import { useRef } from "react";

export const EXAMPLE_QUESTIONS = [
  "Which region generated the most revenue?",
  "Show monthly revenue trends.",
  "Which products have the highest profit?",
] as const;

interface QueryPanelProps {
  query: string;
  onQueryChange: (value: string) => void;
  onRun: () => void;
  running: boolean;
  hasDataset: boolean;
}

export function QueryPanel({ query, onQueryChange, onRun, running, hasDataset }: QueryPanelProps) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const hasQuery = query.trim().length > 0;
  const canRun = hasDataset && hasQuery && !running;
  const hint = !hasDataset ? "Upload a dataset to run an analysis." : !hasQuery ? "Enter a question." : "Cmd/Ctrl + Enter to run.";

  return (
    <section aria-label="Question">
      <label htmlFor="question" className="mono-label block">
        Question
      </label>
      <p className="mt-2 text-2xl font-medium tracking-tight sm:text-3xl">What would you like to understand?</p>

      <textarea
        id="question"
        ref={textareaRef}
        value={query}
        maxLength={2000}
        rows={3}
        disabled={running}
        placeholder="Ask in plain language."
        onChange={(event) => onQueryChange(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === "Enter" && (event.metaKey || event.ctrlKey) && canRun) {
            event.preventDefault();
            onRun();
          }
        }}
        className="mt-5 block w-full resize-y border border-[#c9c9c4] bg-surface px-5 py-4 text-lg leading-7 outline-none transition-colors duration-150 placeholder:text-[#a3a3a0] focus:border-ink disabled:opacity-60"
      />

      <div className="mt-4 flex flex-wrap items-center justify-between gap-x-6 gap-y-3">
        <p className="mono-label" aria-live="polite">
          {hint}
        </p>
        <button
          type="button"
          onClick={onRun}
          disabled={!canRun}
          className="bg-ink px-7 py-3 text-[15px] font-medium text-white transition-[background-color,transform] duration-150 hover:bg-accent active:scale-[0.98] disabled:cursor-not-allowed disabled:bg-[#c9c9c4] disabled:hover:bg-[#c9c9c4] disabled:active:scale-100"
        >
          {running ? "Running analysis" : "Run analysis"}
        </button>
      </div>

      <div className="mt-8">
        <p className="mono-label">Examples</p>
        <ul className="mt-3 border-t border-line">
          {EXAMPLE_QUESTIONS.map((example) => (
            <li key={example} className="border-b border-line">
              <button
                type="button"
                disabled={running}
                onClick={() => {
                  onQueryChange(example);
                  textareaRef.current?.focus();
                }}
                className="flex w-full items-baseline justify-between gap-4 py-3 text-left text-[16px] transition-colors duration-150 hover:text-accent disabled:opacity-50 disabled:hover:text-ink"
              >
                <span>{example}</span>
                <span className="mono-label shrink-0">Use</span>
              </button>
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
