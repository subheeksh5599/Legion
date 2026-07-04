"use client";

import { motion } from "motion/react";
import type { ReactNode } from "react";

const easeOut = [0.16, 1, 0.3, 1] as const;

const integrations = [
  {
    name: "Bittensor",
    role: "Decentralized vulnerability scoring",
    desc: "Miners compete to discover exploits. Validators score findings. The subnet produces tamper-proof security ratings.",
  },
  {
    name: "Venice.ai",
    role: "TEE-encrypted detection",
    desc: "Vulnerabilities are verified inside a Trusted Execution Environment. Scoring methodology is private and attestable.",
  },
  {
    name: "Fetch.ai",
    role: "Agent orchestration",
    desc: "Every scanner, exploiter, and patcher is a uAgent. Discoverable on Agentverse. Composable with other agents.",
  },
  {
    name: "Solana",
    role: "On-chain audit trail",
    desc: "Security scores minted as SBTs. Agent bounties paid in USDC. Every scan verifiable on-chain.",
  },
  {
    name: "Conduct AI",
    role: "Enterprise governance",
    desc: "Human-in-the-loop approval for Critical findings. Graduated autonomy controls. Audit-ready compliance reports.",
  },
  {
    name: "Microsoft Azure",
    role: "Infrastructure & orchestration",
    desc: "Scalable agent hosting. Attack corpus storage. Azure OpenAI powers novel attack template generation.",
  },
];

function IntegrationCard({
  integration,
  index,
}: {
  integration: (typeof integrations)[0];
  index: number;
}): ReactNode {
  return (
    <motion.div
      className="border-border bg-muted rounded-2xl border p-6 md:p-8"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.5, delay: index * 0.05, ease: easeOut }}
    >
      <h3 className="mb-1 font-mono text-lg font-semibold tracking-tight">
        {integration.name}
      </h3>
      <p className="mb-3 text-sm text-accent">{integration.role}</p>
      <p className="text-muted-foreground text-sm leading-relaxed">
        {integration.desc}
      </p>
    </motion.div>
  );
}

export function Testimonials(): ReactNode {
  return (
    <section className="bg-background px-6 py-16 md:py-32">
      <div className="mx-auto max-w-6xl">
        <motion.div
          className="mb-12 md:mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, ease: easeOut }}
        >
          <span className="font-mono text-sm tracking-wider text-accent">
            POWERED BY
          </span>
          <h2 className="mt-2 text-3xl font-medium tracking-tight md:text-4xl lg:text-5xl">
            Built on decentralized infrastructure
          </h2>
        </motion.div>

        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {integrations.map((integration, index) => (
            <IntegrationCard
              key={integration.name}
              integration={integration}
              index={index}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
