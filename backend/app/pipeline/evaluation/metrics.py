"""Cost-vs-quality metrics collector for pipeline runs."""

from __future__ import annotations

import time


class MetricsCollector:
    """Tracks latency, token cost, quality score, and retries."""

    def __init__(self) -> None:
        self._start = time.perf_counter()

    def snapshot(self, *, retries: int, error_count: int, warning_count: int, stage_count: int, quality_score: int) -> dict:
        elapsed_ms = int((time.perf_counter() - self._start) * 1000)
        token_estimate = 140 * max(stage_count, 1) + retries * 60 + warning_count * 20
        repair_cost = round(retries * 0.00045, 6)
        return {
            "latency_ms": elapsed_ms,
            "token_estimate": token_estimate,
            "estimated_token_cost": round(token_estimate * 0.0000025, 6),
            "retry_count": retries,
            "repair_cost": repair_cost,
            "quality_score": float(quality_score),
            "tradeoff_summary": [
                {
                    "mode": "fast",
                    "estimated_latency_ms": int(elapsed_ms * 0.7) if elapsed_ms else 120,
                    "estimated_token_cost": round((token_estimate * 0.75) * 0.0000025, 6),
                    "expected_quality_score": max(0, quality_score - 12),
                    "notes": "Lower checks, faster turnaround, higher risk of inconsistencies.",
                },
                {
                    "mode": "balanced",
                    "estimated_latency_ms": elapsed_ms if elapsed_ms else 180,
                    "estimated_token_cost": round(token_estimate * 0.0000025, 6),
                    "expected_quality_score": quality_score,
                    "notes": "Default mode with full validation and targeted repair.",
                },
                {
                    "mode": "high_reliability",
                    "estimated_latency_ms": int(elapsed_ms * 1.4) if elapsed_ms else 260,
                    "estimated_token_cost": round((token_estimate * 1.25) * 0.0000025, 6),
                    "expected_quality_score": min(100, quality_score + 6),
                    "notes": "Extra checks and repair rounds for maximum consistency.",
                },
            ],
        }
