"use client";

import type { ReactNode } from "react";
import { motion } from "motion/react";

/** Editorial row: narrow label column on the left, content on the right. */
export function Section({ title, note, children }: { title: string; note?: string; children: ReactNode }) {
  return (
    <motion.section
      initial={{ opacity: 0, y: 10 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "0px 0px -60px 0px" }}
      transition={{ duration: 0.3, ease: [0.23, 1, 0.32, 1] }}
      className="grid gap-5 border-t border-line pt-8 md:grid-cols-[200px_minmax(0,1fr)] md:gap-10"
    >
      <header>
        <h3 className="text-[17px] font-medium tracking-tight">{title}</h3>
        {note ? <p className="mt-1 text-[14px] leading-5 text-muted">{note}</p> : null}
      </header>
      <div className="min-w-0">{children}</div>
    </motion.section>
  );
}
