"use client";

import { ChevronRightIcon, Check } from "lucide-react";
import { motion } from "motion/react";
import type { ReactNode } from "react";

const easeOut = [0.16, 1, 0.3, 1] as const;

interface Plan {
  name: string;
  tagline: string;
  price: string;
  features: string[];
  highlighted?: boolean;
}

const plans: Plan[] = [
  {
    name: "Open Source",
    tagline: "Scan public repositories for free",
    price: "Free",
    features: [
      "5 scans per day",
      "Public repo support",
      "Basic vulnerability detection",
      "Community attack templates",
    ],
  },
  {
    name: "Enterprise",
    tagline: "Full red-team agent swarm on your infrastructure",
    price: "Custom",
    highlighted: true,
    features: [
      "Unlimited scans",
      "Private repository support",
      "All attack vectors",
      "Bittensor subnet scoring",
      "Venice TEE verification",
      "Solana audit trail",
      "Conduct governance dashboard",
      "24/7 autonomous monitoring",
    ],
  },
];

function PlanCard({ plan, index }: { plan: Plan; index: number }): ReactNode {
  return (
    <motion.div
      className={`rounded-2xl border p-6 md:p-8 ${
        plan.highlighted
          ? "border-accent bg-accent/5 transition-[border-color,box-shadow] duration-300 hover:border-accent/80 hover:shadow-lg hover:shadow-accent/10"
          : "border-border bg-muted"
      }`}
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.3 }}
      transition={{
        opacity: { duration: 0.6, delay: index * 0.15, ease: easeOut },
        y: { duration: 0.3, ease: easeOut },
      }}
    >
      <div className="mb-6">
        <h3 className="font-mono text-lg font-semibold">{plan.name}</h3>
        <p className="text-muted-foreground text-sm">{plan.tagline}</p>
      </div>
      <div className="mb-8 flex items-baseline gap-1">
        <span className="font-mono text-4xl font-bold tracking-tighter text-accent md:text-5xl">
          {plan.price}
        </span>
      </div>
      <ul className="space-y-3">
        {plan.features.map((feature) => (
          <li key={feature} className="flex items-start gap-3 text-sm">
            <Check className="mt-0.5 h-4 w-4 shrink-0 text-accent" />
            <span>{feature}</span>
          </li>
        ))}
      </ul>
    </motion.div>
  );
}

export function Pricing(): ReactNode {
  return (
    <section
      id="deploy"
      className="bg-muted border-border border-y px-6 py-16 md:py-32"
    >
      <div className="mx-auto max-w-6xl">
        <motion.div
          className="mb-12 md:mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, ease: easeOut }}
        >
          <span className="font-mono text-sm tracking-wider text-accent">
            DEPLOY
          </span>
          <h2 className="mt-2 text-3xl font-medium tracking-tight md:text-4xl lg:text-5xl">
            Put Legion on your codebase
          </h2>
        </motion.div>

        <div className="mx-auto grid max-w-2xl grid-cols-1 gap-6 md:grid-cols-2">
          {plans.map((plan, index) => (
            <PlanCard key={plan.name} plan={plan} index={index} />
          ))}
        </div>

        <motion.div
          className="mt-12 flex flex-col items-center gap-4 md:mt-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, delay: 0.2, ease: easeOut }}
        >
          <a
            href="https://github.com/Legion"
            className="group inline-flex w-full items-center justify-center gap-3 rounded-md bg-accent px-6 py-3 font-medium text-white transition-all duration-500 ease-out hover:rounded-[50px] hover:bg-accent/90 sm:w-auto"
          >
            <span>Get Started on GitHub</span>
            <span className="flex h-8 w-8 items-center justify-center rounded-full bg-white/20 transition-all duration-300 group-hover:scale-110">
              <ChevronRightIcon className="h-4 w-4" />
            </span>
          </a>
        </motion.div>
      </div>
    </section>
  );
}
