# AERIS — Architecture Decision Record

This file records decisions that constrain implementation. Revisit a decision only when new evidence justifies the change.

## ADR-001 — Read-only initial product

**Decision:** The initial product monitors and advises. It does not actuate compressors, valves or plant control systems.

**Reason:** The first commercial value proposition can be tested without introducing control-system hazards. Actuation would require a separate safety case and qualified site engineering.

**Consequence:** Initial hardware interfaces are read-only. Product language must not imply autonomous control.

## ADR-002 — Evidence before inference

**Decision:** Every diagnostic finding references validated measurements, time windows, rule/model versions and data-quality state.

**Reason:** Operators need to distinguish a real physical issue from sensor faults, missing data or ordinary operating changes.

**Consequence:** Analytics outputs carry provenance and uncertainty. AERIS does not label a suspected cause as confirmed without independent evidence.

## ADR-003 — Canonical SI units internally

**Decision:** Store pressure in pascals and volumetric flow in cubic metres per second in the initial core contract.

**Reason:** Unit ambiguity is a major source of calculation errors.

**Consequence:** Device adapters convert at a validated boundary and retain source-unit metadata where needed. The initial telemetry contract rejects non-canonical units.

## ADR-004 — Modular monolith before distributed services

**Decision:** Begin with clearly separated modules and service boundaries in a small deployable system.

**Reason:** Early product uncertainty is high. Distributed infrastructure would add operational burden before scale requires it.

**Consequence:** Keep domain logic independent of web frameworks, databases and cloud vendors. Split components only when deployment, scaling or security boundaries justify it.

## ADR-005 — Edge store-and-forward

**Decision:** Acquisition and local buffering must continue during cloud/network outages.

**Reason:** Industrial connectivity cannot be assumed to be continuously available.

**Consequence:** Device events require stable IDs, sequence numbers, event timestamps and idempotent ingestion.

## ADR-006 — Deterministic methods before machine learning

**Decision:** Begin with transparent validation, contextual baselines and rule-based detection. Introduce ML only when sufficient labelled field data and a measurable performance advantage exist.

**Reason:** A model trained on synthetic or poorly contextualised data can create false confidence.

**Consequence:** Initial analytics must be reproducible and explainable. Any later model requires versioning, evaluation, drift monitoring and a fallback.

## ADR-007 — No unsupported customer-value claims

**Decision:** Savings, leak detection accuracy, uptime and ROI are reported only when supported by measured evidence and explicit assumptions.

**Reason:** Technical output is not proof of commercial value.

**Consequence:** Field validation and customer acceptance are release gates.
