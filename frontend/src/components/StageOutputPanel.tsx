import { StageOutput } from "@/types/pipeline";

type StageOutputPanelProps = {
  outputs: StageOutput[];
  progress?: number;
  progressLabel?: string;
  loading?: boolean;
};

const STATUS_STYLE: Record<string, string> = {
  success: "bg-emerald-50 text-emerald-700 border-emerald-200",
  warning: "bg-amber-50 text-amber-700 border-amber-200",
  failed: "bg-rose-50 text-rose-700 border-rose-200",
};

const STAGE_ICON: Record<string, string> = {
  intent_extraction: "🧠",
  system_design: "🧩",
  schema_generation: "🗂️",
  validation: "✅",
  repair: "🛠️",
  runtime_simulation: "⚙️",
  evaluation: "📊",
};

export default function StageOutputPanel({
  outputs,
  progress = 0,
  progressLabel = "",
  loading = false,
}: StageOutputPanelProps) {
  const copyStage = async (content: unknown) => {
    await navigator.clipboard.writeText(JSON.stringify(content, null, 2));
  };

  return (
    <section className="rounded-2xl border border-slate-200 bg-white/70 p-4 shadow-sm backdrop-blur transition hover:shadow-md">
      <div className="sticky top-0 z-10 -mx-4 -mt-4 rounded-t-2xl border-b border-slate-200 bg-white/70 px-4 py-3 backdrop-blur">
        <h2 className="text-sm font-semibold text-slate-900">Live Pipeline Results</h2>
        <p className="mt-0.5 text-xs text-slate-600">Stage-by-stage outputs with deterministic contracts.</p>
      </div>
      <div className="mt-2 h-2 w-full rounded bg-slate-100">
        <div className="h-2 rounded bg-blue-600 transition-all" style={{ width: `${progress}%` }} />
      </div>
      {progressLabel ? <p className="mt-1 text-xs text-slate-500">{progressLabel}</p> : null}

      <div className="mt-3 space-y-3">
        {loading ? (
          <div className="space-y-2 rounded-xl border border-slate-200 bg-slate-50 p-4">
            <div className="h-4 w-1/3 animate-pulse rounded bg-slate-200" />
            <div className="h-20 animate-pulse rounded bg-slate-200" />
          </div>
        ) : null}
        {!loading && outputs.length === 0 ? (
          <div className="rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-8 text-center">
            <p className="text-sm font-semibold text-slate-800">Generate software architecture to inspect deterministic pipeline stages.</p>
            <p className="mt-2 text-xs text-slate-500">Validation insights, repairs, and runtime confidence will appear here.</p>
          </div>
        ) : null}
        {outputs.map((output) => (
          <details
            key={output.stage}
            className="group rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:shadow-md"
            open
          >
            <summary className="flex cursor-pointer list-none items-center justify-between gap-3 rounded-2xl px-4 py-3">
              <div className="flex items-center gap-3">
                <div className="flex h-9 w-9 items-center justify-center rounded-xl border border-slate-200 bg-slate-50 text-base">
                  {STAGE_ICON[output.stage] ?? "📄"}
                </div>
                <div>
                  <p className="text-sm font-semibold text-slate-900">{output.stage}</p>
                  <p className="text-xs text-slate-500">{new Date().toLocaleTimeString()}</p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span
                  className={`rounded-full border px-2 py-0.5 text-[10px] font-semibold uppercase ${
                    STATUS_STYLE[output.status] ?? "border-slate-200 bg-slate-100 text-slate-600"
                  }`}
                >
                  {output.status}
                </span>
                <span className="text-slate-400 transition group-open:rotate-90">▸</span>
              </div>
            </summary>
            <div className="px-4 pb-4">
              <div className="flex justify-end">
                <button
                  type="button"
                  onClick={() => copyStage(output.content)}
                  className="inline-flex h-9 items-center rounded-lg border border-slate-200 bg-white px-3 text-xs font-semibold text-slate-700 transition hover:bg-slate-50"
                >
                  Copy JSON
                </button>
              </div>
              <pre className="mt-3 max-h-72 overflow-auto rounded-2xl border border-slate-800/90 bg-slate-950/95 p-4 font-mono text-xs leading-5 text-slate-100">
                {JSON.stringify(output.content, null, 2)}
              </pre>
            </div>
          </details>
        ))}
      </div>
    </section>
  );
}
