"""Benchmark framework tests."""

from app.pipeline.evaluation.harness import run_benchmark


def test_benchmark_generates_full_report() -> None:
    artifact = run_benchmark()
    report = artifact.report

    assert len(report.real_prompts) == 10
    assert len(report.edge_prompts) == 10
    assert 0 <= report.success_rate <= 100
    assert 0 <= report.execution_rate <= 100
    assert artifact.markdown_report.startswith("# Evaluation Benchmark Report")
