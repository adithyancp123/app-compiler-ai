import { StageOutput } from "@/types/pipeline";

type StageOutputPanelProps = {
  outputs: StageOutput[];
  progress?: number;
  progressLabel?: string;
};

const STATUS_STYLE: Record<string, string> = {
  success: "text-emerald-300",
  warning: "text-amber-300",
  failed: "text-rose-300",
};

export default function StageOutputPanel({ outputs, progress = 0, progressLabel = "" }: StageOutputPanelProps) {
  return (
    <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-4">
      <h2 className="text-sm font-semibold text-slate-200">Pipeline Stage Outputs</h2>
      <div className="mt-2 h-2 w-full rounded bg-slate-800">
        <div className="h-2 rounded bg-indigo-500 transition-all" style={{ width: `${progress}%` }} />
      </div>
      {progressLabel ? <p className="mt-1 text-xs text-slate-400">{progressLabel}</p> : null}

      <div className="mt-3 space-y-3">
        {outputs.length === 0 ? <p className="text-sm text-slate-400">No stage output yet.</p> : null}
        {outputs.map((output) => (
          <article key={output.stage} className="rounded-lg border border-slate-800 bg-slate-950 p-3">
            <div className="flex items-center justify-between">
              <p className="text-xs uppercase tracking-wide text-indigo-300">{output.stage}</p>
              <p className={`text-xs font-semibold uppercase ${STATUS_STYLE[output.status] ?? "text-slate-300"}`}>
                {output.status}
              </p>
            </div>
            <pre className="mt-2 overflow-x-auto rounded border border-slate-800 p-2 text-xs text-slate-300">
              {JSON.stringify(output.content, null, 2)}
            </pre>
          </article>
        ))}
      </div>
    </section>
  );
}
