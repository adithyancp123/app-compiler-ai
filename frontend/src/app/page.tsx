"use client";

import { useState } from "react";

import PromptForm from "@/components/PromptForm";
import ResultsPanel from "@/components/ResultsPanel";
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

  const tabClass = (value: Tab) =>
    `rounded px-3 py-1 text-xs font-semibold ${tab === value ? "bg-indigo-600 text-white" : "bg-slate-900 text-slate-300"}`;

  return (
    <main className="mx-auto max-w-7xl space-y-6 px-6 py-8">
      <header className="rounded-xl border border-slate-800 bg-slate-900/70 p-4">
        <h1 className="text-2xl font-bold text-white">AI Software Compiler</h1>
        <p className="mt-1 text-sm text-slate-400">
          Deterministic compiler pipeline with explainability, targeted repair, runtime confidence, and benchmark analytics.
        </p>
      </header>

      <PromptForm onGenerate={handleGenerate} onRunDemo={runProgressDemo} loading={loading || benchmarkLoading} />

      <div className="flex flex-wrap items-center gap-2 rounded-xl border border-slate-800 bg-slate-900/70 p-3">
        <button className={tabClass("pipeline")} onClick={() => setTab("pipeline")} type="button">Pipeline</button>
        <button className={tabClass("validation")} onClick={() => setTab("validation")} type="button">Validation</button>
        <button className={tabClass("repairs")} onClick={() => setTab("repairs")} type="button">Repairs</button>
        <button className={tabClass("runtime")} onClick={() => setTab("runtime")} type="button">Runtime</button>
        <button className={tabClass("evaluation")} onClick={() => setTab("evaluation")} type="button">Evaluation</button>
        <button
          type="button"
          onClick={handleBenchmark}
          disabled={benchmarkLoading}
          className="ml-auto rounded bg-emerald-600 px-3 py-1 text-xs font-semibold text-white disabled:opacity-60"
        >
          {benchmarkLoading ? "Running Benchmark..." : "Run Benchmark"}
        </button>
      </div>

      {loading ? <p className="text-sm text-indigo-300">Pipeline running deterministic compilation...</p> : null}
      {error ? <p className="text-sm text-rose-400">{error}</p> : null}

      <div className="grid gap-6 lg:grid-cols-2">
        <StageOutputPanel outputs={result?.stage_outputs ?? []} progress={progress} progressLabel={progressLabel} />
        <ResultsPanel result={result} benchmark={benchmark} activePrompt={activePrompt} />
      </div>

      {result && tab !== "pipeline" ? (
        <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-4 text-sm">
          <h2 className="font-semibold text-slate-200">{tab[0].toUpperCase() + tab.slice(1)} Focus</h2>
          <pre className="mt-2 overflow-x-auto rounded-lg border border-slate-800 bg-slate-950 p-3 text-xs text-slate-300">
            {JSON.stringify(
              tab === "validation"
                ? result.validation_report
                : tab === "repairs"
                  ? result.repair_actions
                  : tab === "runtime"
                    ? result.simulation_result
                    : tab === "evaluation"
                      ? benchmark
                      : result.stage_outputs,
              null,
              2,
            )}
          </pre>
        </section>
      ) : null}

      {result ? (
        <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-4 text-sm">
          <h2 className="font-semibold text-slate-200">Cost vs Quality Snapshot</h2>
          <pre className="mt-2 overflow-x-auto rounded-lg border border-slate-800 bg-slate-950 p-3 text-xs text-slate-300">
            {JSON.stringify(result.metrics, null, 2)}
          </pre>
        </section>
      ) : null}
    </main>
  );
}
