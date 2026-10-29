"use client";

import { useEffect, useState } from "react";
import { checkHealth } from "@/lib/api";

type Status = "checking" | "online" | "offline";

/** Reads GET /api/health once on mount, then every 30 s. */
export function ApiStatus({ tone = "dark" }: { tone?: "dark" | "light" }) {
  const [status, setStatus] = useState<Status>("checking");

  useEffect(() => {
    const controller = new AbortController();
    const poll = async () => {
      const ok = await checkHealth(controller.signal);
      if (!controller.signal.aborted) setStatus(ok ? "online" : "offline");
    };
    void poll();
    const timer = window.setInterval(poll, 30_000);
    return () => {
      controller.abort();
      window.clearInterval(timer);
    };
  }, []);

  const dot =
    status === "online" ? "bg-[#3ecf8e]" : status === "offline" ? "bg-[#f97066]" : "bg-white/30";
  const label = status === "online" ? "API connected" : status === "offline" ? "API unreachable" : "Checking API";

  return (
    <p
      className={`mono-label flex items-center gap-2 ${tone === "dark" ? "!text-white/60" : ""}`}
      role="status"
    >
      <span className={`size-1.5 rounded-full ${dot}`} aria-hidden />
      {label}
    </p>
  );
}
