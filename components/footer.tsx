"use client";

import { ChevronRightIcon } from "lucide-react";
import { motion } from "motion/react";
import Link from "next/link";
import type { ReactNode } from "react";

const easeOut = [0.16, 1, 0.3, 1] as const;

const fadeInUp = {
  initial: { opacity: 0, y: 30 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, amount: 0.5 },
  transition: { duration: 0.8, ease: easeOut },
};

const links = [
  { label: "GitHub", href: "https://github.com/legion" },
  { label: "Documentation", href: "#" },
  { label: "Bittensor Subnet", href: "#" },
  { label: "Agentverse", href: "#" },
];

export function Footer(): ReactNode {
  return (
    <footer className="border-border border-t px-6 py-16 md:px-12 lg:px-20">
      <div className="mx-auto max-w-6xl">
        <div className="grid grid-cols-1 gap-12 lg:grid-cols-2 lg:gap-20">
          <motion.div className="max-w-md" {...fadeInUp}>
            <span className="font-mono text-xl font-bold tracking-tighter text-accent">
              //
            </span>
            <span className="ml-2 text-xl font-bold tracking-tighter">
              LEGION
            </span>
            <p className="text-muted-foreground mt-4 text-base leading-relaxed">
              Autonomous adversarial agents that probe legacy systems for
              vulnerabilities. Decentralized scoring on Bittensor. Private
              verification in Venice TEE. On-chain audit trail on Solana.
            </p>
            <Link
              href="https://github.com/legion"
              className="group mt-6 inline-flex items-center gap-3 rounded-md border border-foreground/10 px-4 py-2 font-medium transition-all duration-300 hover:border-accent/50"
            >
              <span>View on GitHub</span>
              <ChevronRightIcon className="h-4 w-4" />
            </Link>
          </motion.div>

          <div className="grid grid-cols-2 gap-8 lg:justify-items-end">
            <motion.div
              {...fadeInUp}
              transition={{ ...fadeInUp.transition, delay: 0.1 }}
            >
              <h4 className="mb-4 font-mono text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Links
              </h4>
              <ul className="space-y-3">
                {links.map((link) => (
                  <li key={link.label}>
                    <Link
                      href={link.href}
                      className="text-muted-foreground inline-block transition-colors hover:text-foreground"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </motion.div>
            <motion.div
              {...fadeInUp}
              transition={{ ...fadeInUp.transition, delay: 0.2 }}
            >
              <h4 className="mb-4 font-mono text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Sponsors
              </h4>
              <ul className="space-y-3 text-muted-foreground text-sm">
                <li>Conduct AI</li>
                <li>Bittensor</li>
                <li>Venice.ai</li>
                <li>Fetch.ai</li>
              </ul>
            </motion.div>
          </div>
        </div>

        <div className="border-border my-12 border-t" />

        <div className="flex flex-col items-center justify-between gap-4 sm:flex-row">
          <p className="text-muted-foreground text-sm">
            &copy; {new Date().getFullYear()} Legion. Built for UK AI Agent
            Hackathon EP5.
          </p>
          <p className="font-mono text-xs text-muted-foreground">
            BITTENSOR &middot; VENICE TEE &middot; FETCH.AI &middot; SOLANA
          </p>
        </div>
      </div>
    </footer>
  );
}
