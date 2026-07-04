"use client";

import { ChevronDown } from "lucide-react";
import { AnimatePresence, motion } from "motion/react";
import { useState, type ReactNode } from "react";

const easeOut = [0.16, 1, 0.3, 1] as const;

const faqs = [
  {
    question: "What does Legion actually test for?",
    answer:
      "Legion probes for prompt injection vulnerabilities, authentication bypass vectors, data exfiltration paths, and privilege escalation in agent-connected systems. Each finding includes exact file paths and line numbers.",
  },
  {
    question: "How does the Bittensor subnet work?",
    answer:
      "Miners run attack templates against registered codebases. Validators verify the findings are real and score them for quality. The subnet produces a tamper-proof security rating that updates continuously as new attacks are discovered.",
  },
  {
    question: "Is my code sent off my infrastructure?",
    answer:
      "No. Legion agents run locally or in your cloud environment. Only cryptographic hashes of findings are submitted to the Bittensor subnet. The actual code and vulnerability details stay on your infrastructure.",
  },
  {
    question: "What's the Venice TEE for?",
    answer:
      "The validator that scores vulnerabilities runs inside a Venice Trusted Execution Environment. This means the scoring methodology is private and tamper-proof — nobody can game the system by knowing exactly how findings are evaluated.",
  },
  {
    question: "How does this compare to traditional SAST tools?",
    answer:
      "SAST tools use static rules that attackers already know how to bypass. Legion uses autonomous AI agents that adapt their attack strategies. The Bittensor subnet ensures the scoring is decentralized — no single company controls your security rating.",
  },
];

function FAQItem({
  faq,
  index,
  isOpen,
  onToggle,
}: {
  faq: (typeof faqs)[0];
  index: number;
  isOpen: boolean;
  onToggle: () => void;
}): ReactNode {
  return (
    <motion.div
      className="border-foreground/5 border-b last:border-b-0"
      initial={{ opacity: 0, y: 20 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, amount: 0.5 }}
      transition={{ duration: 0.5, delay: index * 0.05, ease: easeOut }}
    >
      <button
        onClick={onToggle}
        className="group flex w-full items-center justify-between py-6 text-left"
      >
        <span className="pr-8 text-lg font-medium md:text-xl">
          {faq.question}
        </span>
        <motion.div
          className="text-muted-foreground shrink-0"
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.3, ease: easeOut }}
        >
          <ChevronDown className="h-5 w-5" />
        </motion.div>
      </button>
      <AnimatePresence initial={false}>
        {isOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3, ease: easeOut }}
            className="overflow-hidden"
          >
            <p className="text-muted-foreground pb-6 text-base leading-relaxed">
              {faq.answer}
            </p>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}

export function FAQ(): ReactNode {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

  return (
    <section className="bg-background px-6 py-16 md:py-32">
      <div className="mx-auto max-w-3xl">
        <motion.div
          className="mb-12 md:mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6, ease: easeOut }}
        >
          <span className="font-mono text-sm tracking-wider text-accent">
            FAQ
          </span>
          <h2 className="mt-2 text-3xl font-medium tracking-tight md:text-4xl lg:text-5xl">
            How Legion works
          </h2>
        </motion.div>

        <motion.div
          className="border-border rounded-2xl border px-6 py-2 md:px-10"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.3 }}
          transition={{ duration: 0.6, ease: easeOut }}
        >
          {faqs.map((faq, index) => (
            <FAQItem
              key={faq.question}
              faq={faq}
              index={index}
              isOpen={openIndex === index}
              onToggle={() =>
                setOpenIndex(openIndex === index ? null : index)
              }
            />
          ))}
        </motion.div>
      </div>
    </section>
  );
}
