"use client";

import { useState } from "react";

type PromptFormProps = {
  onGenerate: (prompt: string) => Promise<void>;
  onRunDemo: (prompt: string) => Promise<void>;
  loading: boolean;
};

export const DEMO_PRESETS = [
  "Build a CRM with premium billing, lead scoring, role-based dashboards, and notifications.",
  "Create an e-commerce app with payments, inventory, checkout, and order tracking.",
  "Build hospital management with doctors, patients, appointments, billing, and prescriptions.",
  "Develop a school management system with students, teachers, classes, attendance, and reports.",
  "Create a subscription SaaS app with workspaces, plans, invoices, analytics, and role permissions.",
  "Build a marketplace with sellers, buyers, listings, payments, and settlement reports.",
  "Create an inventory management platform with warehouses, stock movements, and reorder alerts.",
  "Build an app for my business.",
  "Everyone is admin but admins only can view analytics.",
  "Build hospital app.",
];

export default function PromptForm({ onGenerate, onRunDemo, loading }: PromptFormProps) {
  const [prompt, setPrompt] = useState(DEMO_PRESETS[0]);

  return (
    <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-4 shadow-lg shadow-slate-950/20">
      <label htmlFor="preset" className="text-xs font-semibold uppercase text-slate-400">
        Demo Prompt Presets
      </label>
      <div className="mt-2 grid gap-2 sm:grid-cols-2">
        {DEMO_PRESETS.map((preset) => (
          <button
            type="button"
            key={preset}
            onClick={() => setPrompt(preset)}
            className="rounded border border-slate-700 bg-slate-950 px-3 py-2 text-left text-xs text-slate-300 hover:border-indigo-500"
          >
            {preset}
          </button>
        ))}
      </div>

      <label htmlFor="prompt" className="mt-4 block text-sm font-medium text-slate-200">
        Product Prompt
      </label>
      <textarea
        id="prompt"
        value={prompt}
        onChange={(event) => setPrompt(event.target.value)}
        className="mt-2 h-32 w-full rounded-lg border border-slate-700 bg-slate-950 p-3 text-sm text-slate-100 outline-none focus:border-indigo-500"
      />

      <div className="mt-3 flex flex-wrap gap-2">
        <button
          type="button"
          disabled={loading || !prompt.trim()}
          onClick={() => onGenerate(prompt)}
          className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {loading ? "Compiling..." : "Generate"}
        </button>
        <button
          type="button"
          disabled={loading || !prompt.trim()}
          onClick={() => onRunDemo(prompt)}
          className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-emerald-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
          Run Full Pipeline Demo
        </button>
      </div>
    </section>
  );
}
