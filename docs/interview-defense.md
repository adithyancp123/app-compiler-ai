# Interview Defense Notes (Reviewer Q&A)

## Why a multi-stage pipeline instead of one big prompt?
- **Engineering control**: each stage has a clear contract and deterministic outputs.
- **Debuggability**: validation can pinpoint *where* the inconsistency occurs (intent vs schema vs auth).
- **Targeted repair**: fixes can be applied only to the failing module instead of re-generating everything.
- **Testability**: stage logic can be unit-tested with stable fixtures.

## Why deterministic generation?
- **Reviewer confidence**: same prompt produces near-identical output.
- **Production safety**: deterministic ordering and defaults reduce “random drift”.
- **Measurable evaluation**: benchmarks are meaningful only when outputs are stable.

## How does the repair engine work?
- The validator emits structured diagnostics (`errors`, `repair_candidates`).
- Repair is **module-scoped** (UI/API/DB/Auth) and only addresses failing constraints:
  - field insertion (e.g., missing request field)
  - schema alignment (e.g., missing access rule)
  - dependency reconciliation (e.g., API field requires DB column)
- Repair loop is **bounded** by `MAX_REPAIR_ATTEMPTS`.

## How is validation different from retries?
- Validation is **static analysis** over the produced artifacts:
  - UI→API→DB lineage checks
  - role/access policy checks
  - navigation integrity checks
  - feature semantic consistency checks
- Retries are the **controlled repair loop** executing deterministic patch strategies.
  - No brute-force full pipeline re-run.

## How is execution awareness implemented?
- Runtime simulator performs a deterministic “dry-run”:
  - UI renderability assumptions (paths, pages)
  - API reachability from UI forms
  - DB table/relation integrity
  - Auth rule integrity and feature gates
- Produces `executable`, `confidence_score`, and `issues`.

## How does the system handle ambiguity?
- Intent extraction adds deterministic defaults (e.g., auth baseline).
- Constraints and clarification questions are produced for:
  - vague prompts (“Build an app for my business”)
  - conflicting prompts (“everyone is admin but admins only…”)
- The goal is explicit visibility: assumptions/constraints are part of the output.

## What are the key tradeoffs?
- **Pros**: predictable outputs, easier debugging, measurable benchmarks, safer repairs.
- **Cons**: deterministic heuristics may miss niche requirements; templates reduce creative variance.
- Future improvement path: add provider-backed LLM adapters with strict decoding while keeping the same stage contracts.

## If a reviewer asks “Is this production-ready?”
Honest answer:
- **Architecture & safety controls** (contracts, validation, repair bounds, CI, docker docs) are production-minded.
- The “compiler output” is a configuration/spec generator; a full app code generator is intentionally out of scope for this assignment phase.

