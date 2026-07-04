"use client";

import { ChevronRightIcon } from "lucide-react";
import { motion } from "motion/react";
import { type ReactNode } from "react";

const easeOut = [0.16, 1, 0.3, 1] as const;

export function FinalCTA(): ReactNode {
  return (
    <section className="px-6 py-24 md:py-36">
      <motion.div
        className="border-accent relative mx-auto max-w-4xl overflow-hidden rounded-3xl border bg-accent/5 px-6 py-12 text-center md:rounded-4xl md:px-12 md:py-24"
        initial={{ opacity: 0, y: 40 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.3 }}
        transition={{ duration: 0.8, ease: easeOut }}
      >
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(220,38,38,0.08),transparent_70%)]" />

        <div className="relative z-10">
          <motion.h2
            className="mx-auto mb-4 font-mono text-3xl font-bold tracking-tighter text-accent md:text-4xl lg:text-5xl"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.1, ease: easeOut }}
          >
            READY TO DEPLOY
          </motion.h2>

          <motion.p
            className="text-muted-foreground mx-auto mb-10 max-w-md text-lg"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2, ease: easeOut }}
          >
            Point Legion at a codebase. Get a security score in seconds.
          </motion.p>

          <motion.a
            href="https://github.com/legion"
            className="group inline-flex w-full items-center justify-center gap-3 rounded-md bg-accent px-6 py-3 font-medium text-white transition-all duration-500 ease-out hover:rounded-[50px] hover:bg-accent/90 sm:w-auto"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.3, ease: easeOut }}
          >
            <span>Deploy Legion</span>
            <span className="flex h-8 w-8 items-center justify-center rounded-full bg-white/20 transition-all duration-300 group-hover:scale-110">
              <ChevronRightIcon className="h-4 w-4" />
            </span>
          </motion.a>
        </div>
      </motion.div>
    </section>
  );
}
