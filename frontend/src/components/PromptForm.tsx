"use client";

import { useState } from "react";

type PromptFormProps = {
  onGenerate: (prompt: string) => Promise<void>;
  onRunDemo: (prompt: string) => Promise<void>;
  onRunBenchmark: () => Promise<void>;
  loading: boolean;
};

type Preset = {
  id: string;
  icon: string;
  title: string;
  description: string;
  prompt: string;
};

const PRESETS: Preset[] = [
  {
    id: "crm",
    icon: "🏢",
    title: "CRM Platform",
    description: "Role-based dashboards, billing, notifications",
    prompt: "Build a CRM with premium billing, lead scoring, role-based dashboards, and notifications.",
  },
  {
    id: "ecommerce",
    icon: "🛒",
    title: "E-commerce",
    description: "Payments, inventory, checkout, order tracking",
    prompt: "Create an e-commerce app with payments, inventory, checkout, and order tracking.",
  },
  {
    id: "hospital",
    icon: "🏥",
    title: "Hospital Management",
    description: "Appointments, prescriptions, billing",
    prompt: "Build hospital management with doctors, patients, appointments, billing, and prescriptions.",
  },
  {
    id: "school",
    icon: "🏫",
    title: "School Management",
    description: "Students, teachers, attendance, reports",
    prompt: "Develop a school management system with students, teachers, classes, attendance, and reports.",
  },
  {
    id: "marketplace",
    icon: "🧾",
    title: "Marketplace",
    description: "Listings, buyers/sellers, payments",
    prompt: "Build a marketplace with sellers, buyers, listings, payments, and settlement reports.",
  },
  {
    id: "saas",
    icon: "⚡",
    title: "Subscription SaaS",
    description: "Workspaces, plans, analytics, invoices",
    prompt: "Create a subscription SaaS app with workspaces, plans, invoices, analytics, and role permissions.",
  },
  {
    id: "inventory",
    icon: "📦",
    title: "Inventory Management",
    description: "Warehouses, stock movements, reorder alerts",
    prompt: "Create an inventory management platform with warehouses, stock movements, and reorder alerts.",
  },
  {
    id: "vague",
    icon: "🧠",
    title: "Vague Prompt",
    description: "Triggers assumptions / clarifications",
    prompt: "Build an app for my business.",
  },
  {
    id: "conflict",
    icon: "⚠️",
    title: "Conflicting Requirements",
    description: "Surfaces contradictions explicitly",
    prompt: "Everyone is admin but admins only can view analytics.",
  },
];

const HELPER_CHIPS = [
  { id: "chip-crm", label: "CRM", prompt: PRESETS[0].prompt },
  { id: "chip-ecom", label: "E-commerce", prompt: PRESETS[1].prompt },
  { id: "chip-hosp", label: "Hospital", prompt: PRESETS[2].prompt },
  { id: "chip-school", label: "School", prompt: PRESETS[3].prompt },
  { id: "chip-market", label: "Marketplace", prompt: PRESETS[4].prompt },
  { id: "chip-saas", label: "SaaS", prompt: PRESETS[5].prompt },
];

export default function PromptForm({ onGenerate, onRunDemo, onRunBenchmark, loading }: PromptFormProps) {
  const [selectedPreset, setSelectedPreset] = useState<string>("crm");
  const [prompt, setPrompt] = useState(PRESETS[0].prompt);

  return (
    <section className="rounded-2xl border border-slate-200 bg-white/70 p-4 shadow-sm backdrop-blur transition hover:shadow-md">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-slate-900">Prompt Studio</h2>
          <p className="mt-1 text-sm text-slate-600">Describe the software you want to generate.</p>
        </div>
        <div className="hidden items-center gap-2 md:flex">
          {HELPER_CHIPS.map((chip) => (
            <button
              key={chip.id}
              type="button"
              onClick={() => setPrompt(chip.prompt)}
              className="rounded-full border border-slate-200 bg-white px-3 py-1 text-xs font-semibold text-slate-700 shadow-sm transition hover:bg-slate-50"
            >
              {chip.label}
            </button>
          ))}
        </div>
      </div>

      <textarea
        id="prompt"
        value={prompt}
        onChange={(event) => setPrompt(event.target.value)}
        placeholder="Example: Build a role-based CRM with billing, analytics, and approval workflows..."
        className="mt-3 min-h-[140px] w-full resize-none rounded-2xl border border-slate-200 bg-slate-50/70 p-4 text-sm text-slate-900 shadow-inner outline-none transition focus:border-blue-400 focus:ring-4 focus:ring-blue-100"
      />

      <div className="mt-4">
        <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">Demo Presets</p>
        <div className="mt-3 grid gap-2.5 md:grid-cols-2 lg:grid-cols-3">
          {PRESETS.map((preset) => {
            const selected = selectedPreset === preset.id;
            return (
              <button
                key={preset.id}
                type="button"
                onClick={() => {
                  setSelectedPreset(preset.id);
                  setPrompt(preset.prompt);
                }}
                className={[
                  "group rounded-2xl border p-4 text-left shadow-sm transition-all",
                  "hover:-translate-y-0.5 hover:shadow-md",
                  selected ? "border-blue-300 bg-blue-50/60 ring-2 ring-blue-100" : "border-slate-200 bg-white hover:bg-slate-50",
                ].join(" ")}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2">
                    <span className="text-xl">{preset.icon}</span>
                    <p className="text-sm font-bold text-slate-900">{preset.title}</p>
                  </div>
                  <span className={selected ? "text-blue-600" : "text-slate-300 group-hover:text-slate-400"}>▸</span>
                </div>
                <p className="mt-2 text-xs leading-5 text-slate-600">{preset.description}</p>
              </button>
            );
          })}
        </div>
      </div>

      <div className="mt-5 flex flex-wrap items-center gap-2">
        <button
          type="button"
          disabled={loading || !prompt.trim()}
          onClick={() => onGenerate(prompt)}
          className="inline-flex h-10 items-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 px-4 text-sm font-semibold text-white shadow-sm transition-all hover:-translate-y-0.5 hover:shadow-md disabled:cursor-not-allowed disabled:opacity-50"
        >
          <span>⚡</span>
          {loading ? "Compiling..." : "Generate"}
        </button>
        <button
          type="button"
          disabled={loading || !prompt.trim()}
          onClick={() => onRunDemo(prompt)}
          className="inline-flex h-10 items-center gap-2 rounded-xl bg-slate-900 px-4 text-sm font-semibold text-white shadow-sm transition-all hover:-translate-y-0.5 hover:bg-slate-800 hover:shadow-md disabled:cursor-not-allowed disabled:opacity-50"
        >
          <span>▶</span>
          Run Full Pipeline Demo
        </button>
        <button
          type="button"
          disabled={loading}
          onClick={onRunBenchmark}
          className="ml-auto inline-flex h-10 items-center gap-2 rounded-xl border border-slate-200 bg-white/70 px-4 text-sm font-semibold text-slate-800 shadow-sm backdrop-blur transition-all hover:-translate-y-0.5 hover:bg-white hover:shadow-md disabled:cursor-not-allowed disabled:opacity-50"
        >
          <span>📈</span>
          Run Benchmark
        </button>
      </div>
    </section>
  );
}
