"use client";

import { CompileResponse, EvaluationReport } from "@/types/pipeline";
import { downloadBenchmarkExport, downloadCompileExport } from "@/lib/api";

type ResultsPanelProps = {
  result: CompileResponse | null;
  benchmark: EvaluationReport | null;
  activePrompt: string;
};

function JsonCard({ title, data }: { title: string; data: unknown }) {
  const copyJson = async () => {
    await navigator.clipboard.writeText(JSON.stringify(data, null, 2));
  };

  return (
    <article className="rounded-lg border border-slate-800 bg-slate-950 p-3">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-200">{title}</h3>
        <button
          type="button"
          onClick={copyJson}
          className="rounded border border-slate-700 px-2 py-1 text-xs text-slate-300 hover:border-slate-500"
        >
          Copy JSON
        </button>
      </div>
      <pre className="mt-2 overflow-x-auto text-xs text-slate-300">{JSON.stringify(data, null, 2)}</pre>
    </article>
  );
}

function ScoreCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded border border-slate-700 bg-slate-950 p-3">
      <p className="text-xs text-slate-400">{label}</p>
      <p className="text-lg font-bold text-slate-100">{value}%</p>
      <div className="mt-2 h-2 rounded bg-slate-800">
        <div className="h-2 rounded bg-emerald-500" style={{ width: `${Math.min(100, value)}%` }} />
      </div>
    </div>
  );
}

export default function ResultsPanel({ result, benchmark, activePrompt }: ResultsPanelProps) {
  if (!result) {
    return (
      <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-4 text-sm text-slate-400">
        Run generation to inspect schema, validation report, explainability decisions, repairs, runtime confidence, and benchmark metrics.
      </section>
    );
  }

  return (
    <section className="space-y-3 rounded-xl border border-slate-800 bg-slate-900/70 p-4">
      <div className="flex flex-wrap gap-2">
        <button className="rounded border border-slate-700 px-2 py-1 text-xs text-slate-300" onClick={() => downloadCompileExport(activePrompt, "json")} type="button">Download JSON</button>
        <button className="rounded border border-slate-700 px-2 py-1 text-xs text-slate-300" onClick={() => downloadCompileExport(activePrompt, "markdown")} type="button">Download Markdown</button>
        <button className="rounded border border-slate-700 px-2 py-1 text-xs text-slate-300" onClick={() => downloadBenchmarkExport("json")} type="button">Benchmark JSON</button>
        <button className="rounded border border-slate-700 px-2 py-1 text-xs text-slate-300" onClick={() => downloadBenchmarkExport("markdown")} type="button">Benchmark Markdown</button>
      </div>

      <div className="grid grid-cols-2 gap-2">
        <ScoreCard label="Consistency" value={result.validation_report.consistency_score} />
        <ScoreCard label="Confidence" value={result.simulation_result.confidence_score} />
        <ScoreCard label="Quality" value={result.quality_score.final_score} />
        <ScoreCard label="Execution" value={result.simulation_result.executable ? 100 : 0} />
      </div>

      <JsonCard title="Explainability: Why Decisions Were Made" data={result.explainability} />
      <JsonCard title="Validation Report" data={result.validation_report} />
      <JsonCard title="Repair Actions" data={result.repair_actions} />
      <JsonCard title="Runtime Simulation" data={result.simulation_result} />
      <JsonCard title="Final Executable JSON" data={result.generated_schema} />

      {benchmark ? (
        <div className="rounded-lg border border-slate-800 bg-slate-950 p-3">
          <h3 className="text-sm font-semibold text-slate-200">Benchmark Dashboard</h3>
          <div className="mt-2 grid grid-cols-2 gap-2 text-xs text-slate-300">
            <p>Success rate: {benchmark.success_rate}%</p>
            <p>Failure rate: {benchmark.failure_rate}%</p>
            <p>Repair rate: {benchmark.repair_rate}%</p>
            <p>Execution rate: {benchmark.execution_rate}%</p>
            <p>Consistency: {benchmark.consistency_score}</p>
            <p>Runtime failures: {benchmark.runtime_failures}</p>
          </div>
        </div>
      ) : null}
    </section>
  );
}
