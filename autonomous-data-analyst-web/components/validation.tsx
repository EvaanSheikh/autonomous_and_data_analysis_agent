"use client";

import { motion } from "motion/react";
import type { ValidationCheck } from "@/lib/types";
import { Section } from "./section";

export function ValidationSection({ checks }: { checks: ValidationCheck[] }) {
  const passed = checks.filter((c) => c.passed).length;
  const allPassed = checks.length > 0 && passed === checks.length;

  return (
    <Section title="Validation" note="Automated checks run on the result before it is reported.">
      {checks.length === 0 ? (
        <p className="text-[15px] text-muted">No validation checks were returned.</p>
      ) : (
        <>
          <p className={`mono-label ${allPassed ? "!text-ok" : "!text-bad"}`}>
            {passed} of {checks.length} checks passed
          </p>
          <ul className="mt-3 border-t border-line">
            {checks.map((check, index) => (
              <motion.li
                key={check.check}
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.25, delay: index * 0.05 }}
                className="grid grid-cols-[48px_minmax(0,1fr)] gap-4 border-b border-line py-3 sm:grid-cols-[48px_220px_minmax(0,1fr)]"
              >
                <span className={`mono-label !font-medium ${check.passed ? "!text-ok" : "!text-bad"}`}>
                  {check.passed ? "PASS" : "FAIL"}
                </span>
                <span className="font-mono text-[13px]">{check.check}</span>
                <span className="col-span-2 text-[15px] leading-6 text-[#3b3b39] sm:col-span-1">{check.message}</span>
              </motion.li>
            ))}
          </ul>
        </>
      )}
    </Section>
  );
}
