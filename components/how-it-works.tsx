"use client";

import {
  Lock,
  Eye,
  Bug,
} from "lucide-react";
import { motion, useInView } from "motion/react";
import type { ReactNode } from "react";
import { useRef } from "react";

const easeOut = [0.16, 1, 0.3, 1] as const;

const steps = [
  {
    icon: Eye,
    title: "Scan the target",
    description:
      "Point Legion at any legacy codebase. Agents fingerprint the stack, map dependencies, and identify attack surfaces in seconds.",
  },
  {
    icon: Bug,
    title: "Deploy the swarm",
    description:
      "Three agent types attack in parallel: injection probes, auth bypass attempts, and data exfiltration tests. Each finding pinned to a line of code.",
  },
  {
    icon: Lock,
    title: "Secure the system",
    description:
      "Agents generate patches with evidence. Human approves. The Bittensor subnet scores the fix. Your security posture updates in real-time.",
  },
];

function StepCard({
  step,
  index,
}: {
  step: (typeof steps)[0];
  index: number;
}): ReactNode {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true, amount: 0.5 });
  const Icon = step.icon;

  return (
    <motion.div
      ref={ref}
      className="border-border bg-muted flex min-h-70 flex-col rounded-2xl border p-6 md:p-8"
      initial={{ opacity: 0, y: 30 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
      transition={{ duration: 0.6, delay: index * 0.1, ease: easeOut }}
    >
      <div className="mb-6 text-accent">
        <Icon className="h-10 w-10" strokeWidth={1.5} />
      </div>
      <h3 className="mb-3 mt-auto font-mono text-lg font-medium tracking-tight md:text-xl">
        {step.title}
      </h3>
      <p className="text-muted-foreground text-base leading-relaxed">
        {step.description}
      </p>
    </motion.div>
  );
}

export function HowItWorks(): ReactNode {
  const headerRef = useRef<HTMLDivElement>(null);
  const isHeaderInView = useInView(headerRef, { once: true, amount: 0.5 });

  return (
    <section
      id="how-it-works"
      className="bg-background px-6 py-16 md:py-32"
    >
      <div className="mx-auto max-w-6xl">
        <motion.div
          ref={headerRef}
          className="mb-8 md:mb-16"
          initial={{ opacity: 0, y: 20 }}
          animate={
            isHeaderInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 20 }
          }
          transition={{ duration: 0.6, ease: easeOut }}
        >
          <span className="font-mono text-sm tracking-wider text-accent">
            HOW IT WORKS
          </span>
          <h2 className="mt-2 text-3xl font-medium tracking-tight md:text-4xl lg:text-5xl">
            Red-team your codebase
            <br />
            before attackers do
          </h2>
        </motion.div>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-3 md:gap-6">
          {steps.map((step, index) => (
            <StepCard key={step.title} step={step} index={index} />
          ))}
        </div>
      </div>
    </section>
  );
}
