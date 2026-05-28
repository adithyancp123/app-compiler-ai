"use client";

import { useState } from "react";

import PromptForm from "@/components/PromptForm";
import ResultsPanel from "@/components/ResultsPanel";
import SidebarNav from "@/components/SidebarNav";
import StageOutputPanel from "@/components/StageOutputPanel";
import { compilePrompt, runBenchmark } from "@/lib/api";
import { CompileResponse, EvaluationReport } from "@/types/pipeline";

type Tab = "pipeline" | "validation" | "repairs" | "runtime" | "evaluation";

export default function HomePage() {
  const [loading, setLoading] = useState(false);
  const [benchmarkLoading, setBenchmarkLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<CompileResponse | null>(null);
  const [benchmark, setBenchmark] = useState<EvaluationReport | null>(null);
  const [tab, setTab] = useState<Tab>("pipeline");
  const [activePrompt, setActivePrompt] = useState("");
  const [progress, setProgress] = useState(0);
  const [progressLabel, setProgressLabel] = useState("");

  const runProgressDemo = async (prompt: string) => {
    const steps = [
      "Intent Extraction",
      "System Design",
      "Schema Generation",
      "Validation",
      "Repair",
      "Runtime Simulation",
      "Benchmark Metrics",
    ];
    for (let i = 0; i < steps.length; i += 1) {
      setProgress(Math.round(((i + 1) / steps.length) * 100));
      setProgressLabel(`Running: ${steps[i]}`);
      // eslint-disable-next-line no-await-in-loop
      await new Promise((resolve) => setTimeout(resolve, 220));
    }
    await handleGenerate(prompt);
    await handleBenchmark();
    setProgressLabel("Demo complete");
  };

  const handleGenerate = async (prompt: string) => {
    setLoading(true);
    setError(null);
    setActivePrompt(prompt);

    try {
      const response = await compilePrompt(prompt);
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  const handleBenchmark = async () => {
    setBenchmarkLoading(true);
    setError(null);
    try {
      const report = await runBenchmark();
      setBenchmark(report);
      setTab("evaluation");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setBenchmarkLoading(false);
    }
  };

  const navItems = [
    { id: "pipeline", label: "Pipeline", icon: "🧬" },
    { id: "validation", label: "Validation", icon: "✅" },
    { id: "repairs", label: "Repairs", icon: "🛠️" },
    { id: "runtime", label: "Runtime", icon: "⚙️" },
    { id: "evaluation", label: "Evaluation", icon: "📊" },
  ];

  return (
    <main className="mx-auto max-w-7xl space-y-5 px-4 py-6 sm:px-6 lg:px-8">
      <nav className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl border border-slate-200 bg-white shadow-sm">
            ⚡
          </div>
          <div>
            <p className="text-sm font-bold text-slate-900">AI Software Compiler</p>
            <p className="text-xs text-slate-500">Deterministic multi-stage compilation</p>
          </div>
        </div>
        <div className="hidden items-center gap-2 md:flex">
          <span className="rounded-full border border-slate-200 bg-white px-3 py-1 text-xs font-semibold text-slate-700 shadow-sm">
            v1
          </span>
        </div>
      </nav>

      <section className="relative overflow-hidden rounded-3xl border border-slate-200 bg-white/70 p-5 shadow-sm backdrop-blur">
        <div className="pointer-events-none absolute -right-24 -top-24 h-72 w-72 rounded-full bg-gradient-to-br from-blue-200/70 to-indigo-100/40 blur-3xl" />
        <div className="pointer-events-none absolute -left-24 -bottom-24 h-72 w-72 rounded-full bg-gradient-to-tr from-sky-200/50 to-blue-100/30 blur-3xl" />

        <div className="grid gap-5 lg:grid-cols-2 lg:items-center">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">
              AI Software Compiler
            </h1>
            <p className="mt-3 text-sm leading-6 text-slate-600">
              Transform natural language into deterministic software system architecture through multi-stage compilation, validation, repair, runtime simulation, and evaluation.
            </p>
            <div className="mt-4 flex flex-wrap gap-2">
              {["Deterministic", "Runtime-aware", "Validation Engine", "Benchmark Ready"].map((badge) => (
                <span
                  key={badge}
                  className="rounded-full border border-blue-100 bg-blue-50 px-3 py-1 text-xs font-medium text-blue-700"
                >
                  {badge}
                </span>
              ))}
            </div>
          </div>

          <div className="rounded-2xl border border-slate-200 bg-white/60 p-4 shadow-sm backdrop-blur">
            <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Status</p>
            <div className="mt-3 space-y-2 text-sm text-slate-800">
              {[
                "Deterministic",
                "Runtime-aware",
                "Validation Engine",
                "Benchmark Ready",
              ].map((item) => (
                <div key={item} className="flex items-center gap-2">
                  <span className="text-emerald-600">✓</span>
                  <span className="font-semibold">{item}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <PromptForm
        onGenerate={handleGenerate}
        onRunDemo={runProgressDemo}
        onRunBenchmark={handleBenchmark}
        loading={loading || benchmarkLoading}
      />

      {loading ? <p className="text-sm font-semibold text-blue-700">Compiling pipeline…</p> : null}
      {error ? <p className="rounded-xl border border-rose-200 bg-rose-50 px-3 py-2 text-sm text-rose-700">{error}</p> : null}

      <section className="grid gap-5 lg:grid-cols-[260px_1fr]">
        <SidebarNav items={navItems} activeId={tab} onChange={(id) => setTab(id as Tab)} />

        <div className="space-y-6">
          {tab === "pipeline" ? (
            <StageOutputPanel
              outputs={result?.stage_outputs ?? []}
              progress={progress}
              progressLabel={progressLabel}
              loading={loading || benchmarkLoading}
            />
          ) : (
            <section className="rounded-2xl border border-slate-200 bg-white/70 p-4 shadow-sm backdrop-blur transition hover:shadow-md">
              <h2 className="text-sm font-semibold text-slate-900">
                {tab[0].toUpperCase() + tab.slice(1)}
              </h2>
              <p className="mt-1 text-xs text-slate-600">Focused view for deeper inspection.</p>
              <pre className="mt-3 max-h-[440px] overflow-auto rounded-2xl border border-slate-800/90 bg-slate-950/95 p-4 font-mono text-xs leading-5 text-slate-100">
                {JSON.stringify(
                  tab === "validation"
                    ? result?.validation_report
                    : tab === "repairs"
                      ? result?.repair_actions
                      : tab === "runtime"
                        ? result?.simulation_result
                        : tab === "evaluation"
                          ? benchmark
                          : result?.stage_outputs,
                  null,
                  2,
                )}
              </pre>
            </section>
          )}

          <ResultsPanel result={result} benchmark={benchmark} activePrompt={activePrompt} />
        </div>
      </section>
    </main>
  );
}
