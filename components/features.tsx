"use client";

import { motion } from "motion/react";
import type { ReactNode } from "react";

const easeOut = [0.16, 1, 0.3, 1] as const;

interface Feature {
  number: string;
  title: string;
  description: string;
  details: string[];
}

const features: Feature[] = [
  {
    number: "01",
    title: "Adversarial Agent Swarm",
    description:
      "Three specialized agent types execute parallel attack vectors. Each finding is cryptographically verified before appearing on your dashboard.",
    details: [
      "Prompt injection probes",
      "Auth bypass attempts",
      "Data exfiltration tests",
      "Race condition exploitation",
    ],
  },
  {
    number: "02",
    title: "Line-Level Evidence",
    description:
      "Every vulnerability is pinned to the exact line of code. No vague severity ratings. No false positives. You see what we found and where.",
    details: [
      "File path + line number",
      "Exploit reproduction steps",
      "Severity classification",
      "Patch diff generation",
    ],
  },
  {
    number: "03",
    title: "Decentralized Scoring",
    description:
      "A Bittensor subnet validates every finding. Multiple miners compete to find vulnerabilities. Validators score the quality. The network decides what's real.",
    details: [
      "Bittensor subnet consensus",
      "Venice TEE-encrypted scoring",
      "Solana on-chain audit trail",
      "Fetch.ai agent orchestration",
    ],
  },
];

function FeatureCard({
  feature,
  index,
}: {
  feature: Feature;
  index: number;
}): ReactNode {
  return (
    <motion.div
      className="border-border bg-muted grid grid-cols-1 gap-6 overflow-hidden rounded-2xl border p-8 md:grid-cols-2"
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.3 }}
      transition={{ duration: 0.6, delay: index * 0.1, ease: easeOut }}
    >
      <div>
        <span className="mb-4 block font-mono text-sm tracking-wider text-accent">
          {feature.number}
        </span>
        <h3 className="mb-4 font-mono text-2xl font-medium tracking-tight md:text-3xl">
          {feature.title}
        </h3>
        <p className="text-muted-foreground max-w-md text-base leading-relaxed">
          {feature.description}
        </p>
      </div>
      <div className="flex flex-col justify-center">
        <ul className="space-y-3">
          {feature.details.map((detail) => (
            <li
              key={detail}
              className="text-muted-foreground flex items-center gap-3 text-sm"
            >
              <span className="h-1 w-1 rounded-full bg-accent" />
              {detail}
            </li>
          ))}
        </ul>
      </div>
    </motion.div>
  );
}

export function Features(): ReactNode {
  return (
    <section
      id="features"
      className="bg-background px-6 py-16 md:py-32"
    >
      <div className="mx-auto max-w-6xl">
        <motion.div
          className="mb-12 md:mb-20"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, ease: easeOut }}
        >
          <span className="font-mono text-sm tracking-wider text-accent">
            CAPABILITIES
          </span>
          <h2 className="mt-2 max-w-2xl text-3xl font-medium tracking-tight md:text-4xl lg:text-5xl">
            Autonomous security testing that never sleeps
          </h2>
        </motion.div>

        <div className="flex flex-col gap-6">
          {features.map((feature, index) => (
            <FeatureCard
              key={feature.number}
              feature={feature}
              index={index}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
