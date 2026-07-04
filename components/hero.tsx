"use client";

import { motion } from "motion/react";
import Link from "next/link";
import { ChevronRightIcon, Shield, Bug, ScanLine } from "lucide-react";
import type { ReactNode } from "react";

const easeOut = [0.16, 1, 0.3, 1] as const;

export function Hero(): ReactNode {
  return (
    <section className="relative flex min-h-dvh flex-col items-center justify-center overflow-hidden px-6 pt-24">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,rgba(220,38,38,0.08),transparent_50%)]" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom_left,rgba(220,38,38,0.04),transparent_50%)]" />

      <div className="relative z-10 mx-auto max-w-3xl text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: easeOut }}
          className="mb-6 inline-flex items-center gap-2 rounded-full border border-foreground/10 bg-foreground/5 px-4 py-1.5"
        >
          <span className="h-1.5 w-1.5 rounded-full bg-accent" />
          <span className="font-mono text-xs tracking-wider text-muted-foreground">
            NOW RUNNING ON BITTENSOR SUBNET 0
          </span>
        </motion.div>

        <h1 className="mb-6 font-mono text-5xl font-bold tracking-tighter md:text-7xl lg:text-8xl">
          <motion.span
            initial={{ opacity: 0, filter: "blur(10px)" }}
            animate={{ opacity: 1, filter: "blur(0px)" }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="block"
          >
            YOUR CODE
          </motion.span>
          <motion.span
            initial={{ opacity: 0, filter: "blur(10px)" }}
            animate={{ opacity: 1, filter: "blur(0px)" }}
            transition={{ duration: 0.5, delay: 0.5 }}
            className="block text-accent"
          >
            UNDER ATTACK
          </motion.span>
        </h1>

        <motion.p
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8, ease: easeOut }}
          className="text-muted-foreground mx-auto max-w-xl text-lg leading-relaxed md:text-xl"
        >
          Legion deploys autonomous adversarial agents that probe your legacy
          systems before attackers do. Find injection points, auth bypasses, and
          data leaks with line-level evidence.
        </motion.p>

        <motion.div
          className="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 1.0, ease: easeOut }}
        >
          <Link
            href="#deploy"
            className="group inline-flex w-full items-center justify-center gap-3 rounded-md bg-accent px-6 py-3 font-medium text-white transition-all duration-500 ease-out hover:rounded-[50px] hover:bg-accent/90 sm:w-auto"
          >
            <span>Deploy Red-Team Agents</span>
            <span className="flex h-8 w-8 items-center justify-center rounded-full bg-white/20 transition-all duration-300 group-hover:scale-110">
              <ChevronRightIcon className="h-4 w-4" />
            </span>
          </Link>
        </motion.div>
      </div>

      <motion.div
        className="relative z-10 mt-20 grid max-w-4xl grid-cols-1 gap-4 sm:grid-cols-3"
        initial={{ opacity: 0, y: 40 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 1.2, ease: easeOut }}
      >
        {[
          {
            icon: Bug,
            label: "Vulnerability Discovery",
            stat: "94% detection rate",
          },
          {
            icon: ScanLine,
            label: "Line-Level Evidence",
            stat: "Zero false positives",
          },
          {
            icon: Shield,
            label: "Autonomous Remediation",
            stat: "Patch generation",
          },
        ].map((item) => (
          <div
            key={item.label}
            className="rounded-lg border border-foreground/5 bg-foreground/5 p-6 backdrop-blur-sm"
          >
            <item.icon className="mb-3 h-6 w-6 text-accent" />
            <h3 className="mb-1 font-medium">{item.label}</h3>
            <p className="text-muted-foreground text-sm">{item.stat}</p>
          </div>
        ))}
      </motion.div>
    </section>
  );
}
