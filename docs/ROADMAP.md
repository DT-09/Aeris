# AERIS — Execution Roadmap

**Status:** Active plan. Dates and effort estimates are intentionally withheld until hardware access, customer access and requirements are confirmed.

## Operating method

Work proceeds through evidence-based gates. Each work package has an owner, inputs, implementation, tests, artifacts and exit criteria. A feature is not marked complete without test evidence.

## Gate 0 — Repository and product foundation

### Work
- Establish product definition and scope.
- Establish architecture and safety constraints.
- Create repository conventions and contribution workflow.
- Define requirement IDs and traceability.
- Identify customer discovery questions.

### Exit criteria
- Product scope approved.
- Initial requirements documented.
- Architecture boundaries documented.
- No unsupported performance or commercial claims.

## Gate 1 — Customer and site discovery

### Work
- Interview plant, maintenance and energy roles with appropriate supervision.
- Map compressed-air system configurations.
- Understand existing audits, monitoring and maintenance workflows.
- Collect anonymised operating examples where permission is granted.
- Identify measurement locations and safe installation constraints.
- Obtain indicative willingness-to-pay and procurement process evidence.
- Compare against existing products and service providers.

### Artifacts
- Customer interview notes with consent.
- Target customer profile.
- Current workflow map.
- Competitor/substitute matrix.
- Site measurement requirements.
- Commercial hypothesis register.

### Exit criteria
At least three independent prospective buyers validate the recurring problem; at least one credible pilot path exists; the buyer, technical approver and installation authority are identified. Otherwise revise the segment or problem before hardware investment.

## Gate 2 — Measurement feasibility

### Work
- Define pressure/flow operating ranges and required accuracy.
- Select candidate sensors from datasheets and installation constraints.
- Build a low-voltage controlled test rig.
- Compare readings with a suitable reference instrument.
- Evaluate repeatability, drift, response time and noise.
- Test missing, stuck, out-of-range and disconnected sensors.

### Artifacts
- Sensor selection record.
- Wiring and interface documentation.
- Calibration/verification procedure.
- Measurement uncertainty report.
- Test dataset.

### Exit criteria
Measurement performance meets a written requirement under documented test conditions. No industrial installation until the setup is reviewed and supervised by qualified personnel.

## Gate 3 — End-to-end telemetry vertical slice

### Work
- Implement device identity and sample envelope.
- Implement edge queue and durable storage.
- Implement secure ingestion.
- Implement schema validation and idempotency.
- Persist accepted telemetry and quarantine invalid events.
- Expose device and channel health.

### Tests
- Duplicate event replay.
- Out-of-order events.
- Network interruption and recovery.
- Gateway restart.
- Invalid schema and units.
- Device clock drift.
- Storage exhaustion behaviour.

### Exit criteria
A test device can send valid measurements to the platform, survive a network outage, recover without silent data loss and expose data-quality faults.

## Gate 4 — First useful intelligence

### Work
- Define operating modes and annotations.
- Build context-conditioned baselines.
- Implement transparent rule-based anomaly detection.
- Create evidence-linked investigations.
- Implement excess-flow calculations with unit checks.
- Add uncertainty and missing-input handling.

### Tests
- Synthetic normal operation.
- Synthetic idle consumption anomaly.
- Pressure setpoint change.
- Production schedule change.
- Sensor dropout and drift.
- Irregular sampling.
- False-positive/false-negative evaluation against labelled data.

### Exit criteria
Detection performance is measured on a held-out dataset and reviewed. No claim of exact leak location or confirmed root cause without independent evidence.

## Gate 5 — Operator workflow and reporting

### Work
- Site and asset registry.
- Command centre.
- Finding lifecycle.
- Investigation notes and maintenance actions.
- Before/after verification workflow.
- Transparent reports and audit trail.
- Role-based access.

### Exit criteria
A test operator can move from alert to investigation to recorded intervention and evidence-based verification.

## Gate 6 — Supervised field pilot

### Work
- Site survey and installation approval.
- Qualified installation and safety review.
- Baseline data collection.
- Compare AERIS measurements with reference instruments.
- Record operator findings and confirmed maintenance outcomes.
- Evaluate reliability, detection quality and operational usefulness.
- Calculate economics using customer-specific tariffs and measured inputs.

### Exit criteria
A customer accepts the measured value and agrees to a paid deployment or a clearly scoped commercial next step. A free pilot alone is not proof of willingness to pay.

## Gate 7 — Production readiness

### Work
- Secure provisioning and credential rotation.
- Tenant isolation and access review.
- Backup/restore and disaster recovery.
- Monitoring, alerting and support runbooks.
- Versioned firmware and rollback.
- Installation and maintenance documentation.
- Commercial packaging and service costs.
- Legal, privacy, insurance and applicable conformity review with qualified advisers.

### Exit criteria
Repeatable installation, supportable operations, tested recovery, documented product limitations and a paying customer.

## Prioritisation rules

1. Resolve safety, measurement validity and data integrity before adding AI.
2. Build one complete vertical slice before broad feature development.
3. Prefer deterministic, explainable methods before complex ML.
4. Do not expand to other utilities until the first domain has repeatable customer value.
5. Do not implement actuation in the initial product.
6. Keep all estimates and claims tied to evidence.

## Definition of done

A work item is done only when:
- Its requirement and scope are explicit.
- Its implementation is reviewed.
- Tests pass.
- Failure modes are handled.
- Documentation is updated.
- Observability exists where needed.
- The acceptance evidence is recorded.
