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
    <article className="rounded-xl border border-slate-200 bg-slate-50 p-3 transition hover:shadow-sm">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-semibold text-slate-800">{title}</h3>
        <button
          type="button"
          onClick={copyJson}
          className="rounded-lg border border-slate-200 bg-white px-2 py-1 text-xs text-slate-600 transition hover:bg-slate-100"
        >
          Copy JSON
        </button>
      </div>
      <pre className="mt-2 max-h-72 overflow-auto rounded-lg border border-slate-200 bg-white p-2 text-xs text-slate-700">{JSON.stringify(data, null, 2)}</pre>
    </article>
  );
}

function ScoreCard({ label, value }: { label: string; value: number }) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-3 shadow-sm transition hover:shadow-md">
      <p className="text-xs text-slate-500">{label}</p>
      <p className="mt-1 text-xl font-bold tracking-tight text-slate-900">{value}%</p>
      <div className="mt-2 h-2 rounded-full bg-slate-100">
        <div className="h-2 rounded bg-blue-600" style={{ width: `${Math.min(100, value)}%` }} />
      </div>
    </div>
  );
}

export default function ResultsPanel({ result, benchmark, activePrompt }: ResultsPanelProps) {
  if (!result) {
    return (
      <section className="rounded-2xl border border-slate-200 bg-white p-4 text-sm text-slate-600 shadow-sm">
        <div className="rounded-xl border border-dashed border-slate-300 bg-slate-50 p-6 text-center">
          <p className="font-medium text-slate-700">🚀 Run generation to inspect pipeline stages</p>
          <p className="mt-1 text-xs text-slate-500">Validation, repairs, runtime confidence, and benchmark analytics will appear here.</p>
        </div>
      </section>
    );
  }

  return (
    <section className="space-y-3 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm transition hover:shadow-md">
      <div className="grid gap-2 sm:grid-cols-2 lg:grid-cols-3">
        <ScoreCard label="Consistency Score" value={result.validation_report.consistency_score} />
        <ScoreCard label="Runtime Confidence" value={result.simulation_result.confidence_score} />
        <ScoreCard label="Quality Score" value={result.quality_score.final_score} />
        <ScoreCard label="Execution Readiness" value={result.simulation_result.executable ? 100 : 0} />
        <ScoreCard label="Repair Count" value={result.metrics.retry_count * 20} />
        <ScoreCard label="Latency" value={Math.min(100, Math.round(result.metrics.latency_ms / 10))} />
      </div>

      <div className="flex flex-wrap gap-2">
        <button className="rounded-lg border border-slate-200 bg-white px-2 py-1 text-xs text-slate-600 transition hover:-translate-y-0.5 hover:bg-slate-100" onClick={() => downloadCompileExport(activePrompt, "json")} type="button">Download JSON</button>
        <button className="rounded-lg border border-slate-200 bg-white px-2 py-1 text-xs text-slate-600 transition hover:-translate-y-0.5 hover:bg-slate-100" onClick={() => downloadCompileExport(activePrompt, "markdown")} type="button">Download Markdown</button>
        <button className="rounded-lg border border-slate-200 bg-white px-2 py-1 text-xs text-slate-600 transition hover:-translate-y-0.5 hover:bg-slate-100" onClick={() => downloadBenchmarkExport("json")} type="button">Benchmark JSON</button>
        <button className="rounded-lg border border-slate-200 bg-white px-2 py-1 text-xs text-slate-600 transition hover:-translate-y-0.5 hover:bg-slate-100" onClick={() => downloadBenchmarkExport("markdown")} type="button">Benchmark Markdown</button>
      </div>

      <JsonCard title="Explainability: Why Decisions Were Made" data={result.explainability} />
      <JsonCard title="Validation Report" data={result.validation_report} />
      <JsonCard title="Repair Actions" data={result.repair_actions} />
      <JsonCard title="Runtime Simulation" data={result.simulation_result} />
      <JsonCard title="Final Executable JSON" data={result.generated_schema} />

      {benchmark ? (
        <div className="rounded-xl border border-slate-200 bg-slate-50 p-3">
          <h3 className="text-sm font-semibold text-slate-800">Benchmark Dashboard</h3>
          <div className="mt-2 grid grid-cols-2 gap-2 md:grid-cols-3">
            {[
              ["Success Rate", `${benchmark.success_rate}%`],
              ["Failure Rate", `${benchmark.failure_rate}%`],
              ["Repair Rate", `${benchmark.repair_rate}%`],
              ["Execution Rate", `${benchmark.execution_rate}%`],
              ["Consistency", `${benchmark.consistency_score}`],
              ["Runtime Failures", `${benchmark.runtime_failures}`],
            ].map(([label, value]) => (
              <div key={label} className="rounded-lg border border-slate-200 bg-white p-2">
                <p className="text-[10px] uppercase tracking-wide text-slate-500">{label}</p>
                <p className="text-sm font-semibold text-slate-800">{value}</p>
              </div>
            ))}
          </div>
        </div>
      ) : null}
    </section>
  );
}
