"use client";
// Legion Dashboard — Real-time scan monitoring and vulnerability tracking.

import { useState, useEffect, useCallback } from "react";
import {
  Bug,
  AlertTriangle,
  CheckCircle2,
  ScanLine,
  Activity,
  RefreshCw,
} from "lucide-react";
import { motion } from "motion/react";

const easeOut = [0.16, 1, 0.3, 1] as const;

interface Finding {
  id: string;
  severity: string;
  title: string;
  file_path: string;
  line_number: number;
  evidence: string;
  confirmed: boolean;
}

interface Scan {
  id: string;
  target: string;
  status: string;
  score: number;
  findings: Finding[];
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  scan_duration_ms: number;
}

const API = "http://localhost:8000";

function SeverityBadge({ severity }: { severity: string }) {
  const colors: Record<string, string> = {
    critical: "bg-red-500/20 text-red-400 border-red-500/30",
    high: "bg-orange-500/20 text-orange-400 border-orange-500/30",
    medium: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
    low: "bg-blue-500/20 text-blue-400 border-blue-500/30",
    info: "bg-zinc-500/20 text-zinc-400 border-zinc-500/30",
  };
  return (
    <span
      className={`rounded border px-2 py-0.5 font-mono text-xs font-medium uppercase ${colors[severity] || colors.low}`}
    >
      {severity}
    </span>
  );
}

function ScoreRing({ score }: { score: number }) {
  const color = score >= 80 ? "#22c55e" : score >= 50 ? "#eab308" : "#ef4444";
  const radius = 54;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="relative flex h-36 w-36 items-center justify-center">
      <svg className="h-full w-full -rotate-90" viewBox="0 0 120 120">
        <circle
          cx="60"
          cy="60"
          r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.05)"
          strokeWidth="6"
        />
        <circle
          cx="60"
          cy="60"
          r={radius}
          fill="none"
          stroke={color}
          strokeWidth="6"
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 1s ease" }}
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className="font-mono text-3xl font-bold" style={{ color }}>
          {score}
        </span>
        <span className="text-muted-foreground text-xs">/100</span>
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const [scan, setScan] = useState<Scan | null>(null);
  const [loading, setLoading] = useState(false);
  const [target, setTarget] = useState("");
  const [error, setError] = useState("");

  const fetchDashboard = useCallback(async () => {
    try {
      const res = await fetch(`${API}/api/dashboard`);
      if (res.ok) {
        const data = await res.json();
        if (data.recent_scans?.length > 0) {
          const latestId = data.recent_scans[data.recent_scans.length - 1].id;
          const scanRes = await fetch(`${API}/api/scan/${latestId}`);
          if (scanRes.ok) setScan(await scanRes.json());
        }
      }
    } catch {
      // API not running yet
    }
  }, []);

  useEffect(() => {
    fetchDashboard();
    const interval = setInterval(fetchDashboard, 5000);
    return () => clearInterval(interval);
  }, [fetchDashboard]);

  const runScan = async () => {
    if (!target) return;
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${API}/api/scan`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ target }),
      });
      if (res.ok) {
        const data = await res.json();
        setScan(data);
      } else {
        setError("Failed to start scan");
      }
    } catch {
      setError("Cannot connect to Legion API. Start with: legion serve");
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-background px-6 py-24">
      <div className="mx-auto max-w-6xl">
        <div className="mb-12 flex items-center justify-between">
          <div>
            <h1 className="font-mono text-2xl font-bold tracking-tighter">
              <span className="text-accent">//</span> DASHBOARD
            </h1>
            <p className="text-muted-foreground mt-1 text-sm">
              Monitor active scans and vulnerability findings
            </p>
          </div>
          <a
            href="/"
            className="text-muted-foreground hover:text-foreground text-sm transition-colors"
          >
            &larr; Back to site
          </a>
        </div>

        {/* Scan input */}
        <motion.div
          className="border-border mb-8 rounded-xl border bg-muted p-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, ease: easeOut }}
        >
          <div className="flex flex-col gap-4 sm:flex-row">
            <input
              type="text"
              value={target}
              onChange={(e) => setTarget(e.target.value)}
              placeholder="Path to codebase... (/home/user/project)"
              className="border-border flex-1 rounded-md border bg-background px-4 py-3 font-mono text-sm text-foreground placeholder:text-muted-foreground focus:border-accent focus:outline-none"
              onKeyDown={(e) => e.key === "Enter" && runScan()}
            />
            <button
              onClick={runScan}
              disabled={loading || !target}
              className="inline-flex items-center gap-2 rounded-md bg-accent px-6 py-3 font-medium text-white transition-all hover:bg-accent/90 disabled:opacity-50"
            >
              {loading ? (
                <RefreshCw className="h-4 w-4 animate-spin" />
              ) : (
                <ScanLine className="h-4 w-4" />
              )}
              {loading ? "Scanning..." : "Deploy Agents"}
            </button>
          </div>
          {error && <p className="mt-3 text-sm text-red-400">{error}</p>}
        </motion.div>

        {scan && (
          <>
            {/* Score + stats */}
            <div className="mb-8 grid grid-cols-1 gap-6 md:grid-cols-4">
              <div className="border-border flex items-center justify-center rounded-xl border bg-muted p-6">
                <ScoreRing score={scan.score} />
              </div>
              <StatCard
                icon={Bug}
                label="Critical"
                value={scan.critical_count}
                color="text-red-400"
              />
              <StatCard
                icon={AlertTriangle}
                label="High"
                value={scan.high_count}
                color="text-orange-400"
              />
              <StatCard
                icon={Activity}
                label="Total Findings"
                value={scan.findings.length}
                color="text-zinc-400"
              />
            </div>

            {/* Findings table */}
            <motion.div
              className="border-border overflow-hidden rounded-xl border"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.3 }}
            >
              <div className="border-border bg-muted border-b px-6 py-3">
                <h3 className="font-mono text-sm font-semibold">
                  VULNERABILITIES ({scan.findings.length})
                </h3>
              </div>
              <div className="max-h-[600px] overflow-y-auto">
                {scan.findings.length === 0 ? (
                  <div className="flex flex-col items-center justify-center py-16 text-center">
                    <CheckCircle2 className="mb-3 h-10 w-10 text-green-400" />
                    <p className="font-medium">No vulnerabilities detected</p>
                    <p className="text-muted-foreground mt-1 text-sm">
                      Security score: {scan.score}/100
                    </p>
                  </div>
                ) : (
                  <table className="w-full">
                    <thead>
                      <tr className="border-border border-b text-left">
                        <th className="px-6 py-3 font-mono text-xs font-medium text-muted-foreground">
                          SEVERITY
                        </th>
                        <th className="px-6 py-3 font-mono text-xs font-medium text-muted-foreground">
                          FINDING
                        </th>
                        <th className="px-6 py-3 font-mono text-xs font-medium text-muted-foreground">
                          LOCATION
                        </th>
                        <th className="px-6 py-3 font-mono text-xs font-medium text-muted-foreground">
                          STATUS
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {scan.findings.map((f: Finding) => (
                        <tr
                          key={f.id}
                          className="border-border hover:bg-foreground/5 border-b transition-colors"
                        >
                          <td className="px-6 py-4">
                            <SeverityBadge severity={f.severity} />
                          </td>
                          <td className="px-6 py-4">
                            <p className="text-sm font-medium">{f.title}</p>
                            <p className="text-muted-foreground mt-0.5 text-xs">
                              {f.evidence?.slice(0, 80)}
                            </p>
                          </td>
                          <td className="px-6 py-4">
                            <code className="text-muted-foreground font-mono text-xs">
                              {f.file_path}:{f.line_number}
                            </code>
                          </td>
                          <td className="px-6 py-4">
                            {f.confirmed ? (
                              <span className="inline-flex items-center gap-1 text-xs font-medium text-green-400">
                                <CheckCircle2 className="h-3 w-3" /> Confirmed
                              </span>
                            ) : (
                              <span className="text-muted-foreground text-xs">
                                Pending
                              </span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </motion.div>
          </>
        )}
      </div>
    </div>
  );
}

function StatCard({
  icon: Icon,
  label,
  value,
  color,
}: {
  icon: typeof Bug;
  label: string;
  value: number;
  color: string;
}) {
  return (
    <div className="border-border flex flex-col items-center justify-center rounded-xl border bg-muted p-6 text-center">
      <Icon className={`mb-2 h-6 w-6 ${color}`} />
      <span className={`font-mono text-3xl font-bold ${color}`}>{value}</span>
      <span className="text-muted-foreground mt-1 text-sm">{label}</span>
    </div>
  );
}
