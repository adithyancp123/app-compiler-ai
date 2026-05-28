# Implementation Roadmap

## Phase 1: Contracts + Core Policies
- [ ] Finalize Pydantic contracts per stage
- [ ] Generate JSON Schema snapshots
- [ ] Add deterministic generation policy layer

## Phase 2: Stage Implementations
- [ ] Intent extraction parser + ambiguity detector
- [ ] System design synthesizer
- [ ] Schema generator for UI/API/DB/Auth
- [ ] Cross-layer consistency validators

## Phase 3: Validation + Repair
- [ ] JSON syntax and schema enforcement
- [ ] Mismatch categorization
- [ ] Targeted module repair strategies

## Phase 4: Runtime Simulation
- [ ] UI renderability checks
- [ ] API-route and handler map checks
- [ ] DB migration/schema dry-run checks
- [ ] Auth policy simulation

## Phase 5: Evaluation + Metrics
- [ ] Add 10 real product prompts
- [ ] Add 10 edge-case prompts
- [ ] Track latency, retries, failures, quality score
- [ ] Estimate token/cost usage by stage

## Phase 6: Hardening
- [ ] Add robust tests (unit/integration/e2e)
- [ ] Add CI pipeline
- [ ] Add Dockerized production setup
