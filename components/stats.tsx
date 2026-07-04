"use client";

import { motion, useInView, useSpring, useTransform } from "motion/react";
import { useEffect, useRef, type ReactNode } from "react";

const easeOut = [0.16, 1, 0.3, 1] as const;

const stats = [
  { value: 47, suffix: "K+", label: "Vulnerabilities Detected" },
  { value: 12, suffix: "M+", label: "Lines Scanned" },
  { value: 94.7, suffix: "%", label: "Detection Rate", decimals: 1 },
  { value: 3, suffix: "s", label: "Average Scan Time" },
];

function AnimatedNumber({
  value,
  suffix,
  decimals = 0,
}: {
  value: number;
  suffix: string;
  decimals?: number;
}): ReactNode {
  const ref = useRef<HTMLSpanElement>(null);
  const isInView = useInView(ref, { once: true, amount: 0.5 });
  const spring = useSpring(0, { stiffness: 50, damping: 30, restDelta: 0.001 });
  const display = useTransform(spring, (current) =>
    decimals > 0 ? current.toFixed(decimals) : Math.floor(current).toString(),
  );

  useEffect(() => {
    if (isInView) spring.set(value);
  }, [isInView, spring, value]);

  useEffect(() => {
    const unsubscribe = display.on("change", (latest) => {
      if (ref.current) ref.current.textContent = latest + suffix;
    });
    return () => unsubscribe();
  }, [display, suffix]);

  return <span ref={ref}>0{suffix}</span>;
}

function StatCard({
  stat,
  index,
}: {
  stat: (typeof stats)[0];
  index: number;
}): ReactNode {
  const ref = useRef<HTMLDivElement>(null);
  const isInView = useInView(ref, { once: true, amount: 0.5 });

  return (
    <motion.div
      ref={ref}
      className="text-center"
      initial={{ opacity: 0, y: 30 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 30 }}
      transition={{ duration: 0.6, delay: index * 0.1, ease: easeOut }}
    >
      <div className="font-mono text-5xl font-bold tracking-tighter text-accent md:text-6xl lg:text-7xl">
        <AnimatedNumber
          value={stat.value}
          suffix={stat.suffix}
          decimals={stat.decimals ?? 0}
        />
      </div>
      <p className="text-muted-foreground mt-3 text-base md:text-lg">
        {stat.label}
      </p>
    </motion.div>
  );
}

export function Stats(): ReactNode {
  return (
    <section className="bg-muted border-border border-y px-6 py-16 md:py-32">
      <div className="mx-auto max-w-6xl">
        <div className="grid grid-cols-2 gap-8 md:grid-cols-4 md:gap-12">
          {stats.map((stat, index) => (
            <StatCard key={stat.label} stat={stat} index={index} />
          ))}
        </div>
      </div>
    </section>
  );
}
