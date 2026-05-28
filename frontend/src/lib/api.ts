import { CompileResponse, EvaluationReport } from "@/types/pipeline";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function compilePrompt(prompt: string): Promise<CompileResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/compile`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    throw new Error("Failed to compile prompt");
  }

  return (await response.json()) as CompileResponse;
}

export async function runBenchmark(): Promise<EvaluationReport> {
  const response = await fetch(`${API_BASE_URL}/api/v1/evaluation/report`);
  if (!response.ok) {
    throw new Error("Failed to run benchmark report");
  }
  return (await response.json()) as EvaluationReport;
}

async function downloadFromEndpoint(url: string, filename: string): Promise<void> {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Failed download: ${filename}`);
  }
  const blob = await response.blob();
  const objectUrl = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = objectUrl;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(objectUrl);
}

export async function downloadCompileExport(prompt: string, format: "json" | "markdown"): Promise<void> {
  const endpoint = `${API_BASE_URL}/api/v1/compile/export/${format}`;
  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
  });
  if (!response.ok) {
    throw new Error("Failed compile export");
  }
  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = format === "json" ? "compile_output.json" : "compile_output.md";
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

export async function downloadBenchmarkExport(format: "json" | "markdown"): Promise<void> {
  await downloadFromEndpoint(
    `${API_BASE_URL}/api/v1/evaluation/export/${format}`,
    format === "json" ? "benchmark_report.json" : "benchmark_report.md",
  );
}
