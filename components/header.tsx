"use client";

import { ChevronRightIcon } from "lucide-react";
import { motion } from "motion/react";
import Link from "next/link";
import type { ReactNode } from "react";

const easeOut = [0.16, 1, 0.3, 1] as const;

export function Header(): ReactNode {
  return (
    <motion.header
      className="fixed top-0 left-0 z-50 flex w-full justify-center px-4 pt-4"
      initial={{ y: -100, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.8, delay: 0.3, ease: easeOut }}
    >
      <nav className="bg-foreground/5 border border-foreground/5 flex w-full max-w-6xl items-center justify-between rounded-md px-4 py-3 backdrop-blur-xl">
        <Link href="/" className="flex items-center gap-2">
          <span className="font-mono text-xl font-bold tracking-tighter text-accent">
            //
          </span>
          <span className="text-lg font-semibold tracking-tight">LEGION</span>
        </Link>
        <div className="flex items-center gap-4">
          <Link
            href="#how-it-works"
            className="text-muted-foreground hover:text-foreground hidden text-sm transition-colors sm:block"
          >
            How It Works
          </Link>
          <Link
            href="#features"
            className="text-muted-foreground hover:text-foreground hidden text-sm transition-colors sm:block"
          >
            Features
          </Link>
          <Link
            href="#deploy"
            className="group inline-flex items-center gap-2 rounded-md bg-accent px-4 py-2 text-sm font-medium text-white transition-all duration-500 ease-out hover:rounded-[50px] hover:bg-accent/90"
          >
            <span>Deploy Agents</span>
            <span className="flex h-6 w-6 items-center justify-center rounded-full bg-white/20 transition-all duration-300 group-hover:scale-110">
              <ChevronRightIcon className="h-3 w-3" />
            </span>
          </Link>
        </div>
      </nav>
    </motion.header>
  );
}
