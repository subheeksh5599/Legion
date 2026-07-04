/**
 * Site Configuration
 *
 * Central configuration file for easy customization.
 * Update these values to personalize your template.
 */

export const siteConfig = {
  name: "TLDR",
  tagline: "Read smarter, not longer",
  description: "AI-powered summaries for articles, videos, and documents. Save hours every week.",
  url: "https://example.com",
  social: {
    twitter: "@tldr",
    github: "https://github.com/tldr",
  },
  nav: {
    cta: {
      text: "Get Started",
      href: "#",
    },
    signIn: {
      text: "Sign in",
      href: "#",
    },
  },
} as const;

export const heroConfig = {
  headline: {
    prefix: "Get the",
    accent: "TLDR",
    suffix: "on anything",
  },
  description: "Summarize articles, videos, podcasts, and PDFs instantly. Read smarter, not longer.",
  cta: {
    primary: {
      text: "Add to Chrome — It's Free",
      href: "#",
    },
    secondary: {
      text: "See How It Works",
      href: "#how-it-works",
    },
  },
  carousel: [
    "Tech News",
    "Research Papers",
    "YouTube Videos",
    "Podcasts",
    "Blog Posts",
    "Documentation",
    "Email Threads",
    "Meeting Notes",
    "Legal Documents",
    "Financial Reports",
    "Product Reviews",
    "Academic Articles",
  ],
} as const;

export const howItWorksConfig = {
  title: "Three steps to clarity",
  description: "Get key insights from any content in seconds. No more endless scrolling.",
  cta: {
    text: "Start Summarizing",
    href: "#",
  },
} as const;

export const featuresConfig = {
  title: "Everything you need",
  description: "Powerful features to help you consume content faster and smarter.",
} as const;

export const statsConfig = {
  title: "Trusted by thousands",
  description: "Join the growing community of smarter readers.",
} as const;

export const testimonialsConfig = {
  title: "What People Are Saying",
} as const;

export const pricingConfig = {
  title: "Pricing",
  description: "Start for free and upgrade to unlock more features.",
  cta: {
    primary: {
      text: "Go Pro",
      href: "#",
    },
    secondary: {
      text: "Start For Free",
      href: "#",
    },
  },
} as const;

export const faqConfig = {
  title: "Common Questions",
  contact: {
    text: "Still have questions? We're here to help.",
    cta: {
      text: "Get in Touch",
      href: "mailto:hello@tldr.app",
    },
  },
} as const;

export const finalCtaConfig = {
  headline: "Ready to save hours every week?",
  description: "Join thousands who read smarter. Install the extension and start summarizing in seconds.",
  cta: {
    text: "Add to Chrome",
    href: "#",
  },
} as const;

export const footerConfig = {
  description: "Ready to read smarter? TLDR transforms any article into a concise summary, helping you stay informed without the time commitment.",
  cta: {
    text: "Get Started Free",
    href: "#",
  },
  links: {
    product: [
      { label: "Chrome Extension", href: "#" },
      { label: "Safari Extension", href: "#" },
      { label: "API Access", href: "#" },
      { label: "Enterprise", href: "#" },
    ],
    company: [
      { label: "About", href: "#" },
      { label: "Blog", href: "#" },
      { label: "Careers", href: "#" },
      { label: "Contact", href: "#" },
    ],
  },
  contact: {
    location: "San Francisco",
    address: "548 Market St, Suite 95000\nSan Francisco, CA 94104",
    hours: "Mon-Fri 9:00 am - 6:00 pm (PST)",
    email: "hello@tldr.app",
  },
  copyright: `© ${new Date().getFullYear()} TLDR Technologies Inc.`,
} as const;

/**
 * Feature Flags
 *
 * Toggle features on/off for easy customization.
 */
export const features = {
  smoothScroll: true,
  darkMode: true,
  ditherCursor: true,
  statsSection: true,
} as const;
