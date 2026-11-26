# AERIS — Product Requirements

**Status:** Baseline proposal; customer discovery and field validation required.

## 1. Product definition

AERIS is an industrial utility intelligence platform. The initial product monitors compressed-air systems in manufacturing facilities and turns validated measurements into explainable operational findings and verified improvement reports.

### 1.1 Target users and buyers

- Plant or facility manager: operational performance and accountability.
- Maintenance manager: investigation and corrective work.
- Energy manager: resource consumption and cost analysis.
- Factory owner or finance lead: investment justification and verified savings.

The economic buyer, technical approver, installer and daily operator may be different people. Discovery must identify each role.

### 1.2 Initial customer profile hypothesis

A manufacturing site with:
- A continuously or frequently operated compressed-air system.
- Multiple production loads or distribution branches.
- Meaningful electricity expenditure associated with compressed air.
- Existing maintenance or energy-efficiency responsibilities.
- A practical means to install sensors safely and obtain operating context.

This is a hypothesis, not a validated customer segment.

## 2. Jobs to be done

1. Establish a trustworthy baseline for pressure and flow.
2. Understand consumption across relevant operating modes.
3. Detect sustained deviations and unusual idle consumption.
4. Separate likely operational anomalies from bad sensor data.
5. Prioritise investigations by estimated impact and confidence.
6. Preserve evidence for maintenance teams.
7. Compare before/after operating conditions after an intervention.
8. Produce a transparent report for operational and financial review.

## 3. Initial release scope

### Included

- Read-only pressure and flow acquisition.
- Device identity and sensor metadata.
- Timestamped, provenance-preserving telemetry.
- Local buffering during connectivity loss.
- Secure upload and server-side validation.
- Equipment, sensor and site registry.
- Configurable operating schedules and operating-state annotations.
- Baseline calculations conditioned on operating context.
- Rule-based anomaly detection for explicitly defined conditions.
- Investigation records with evidence references.
- Transparent excess-consumption estimates.
- Operator alerts and reports.
- Audit trail for configuration changes and acknowledgements.
- Device health and data-quality monitoring.

### Excluded from initial release

- Automatic compressor or valve control.
- Claims of exact leak localisation from aggregate measurements.
- Unsupervised AI diagnosis.
- Guaranteed savings or recovery claims.
- Predictive maintenance claims without validated failure labels.
- Multi-utility optimisation.
- Cross-customer benchmarking using identifiable customer data.
- Safety or regulatory certification claims.

## 4. Functional requirements

### FR-01 — Device identity
Every device must have a stable unique identity, provisioned credentials and an assigned site/asset relationship.

### FR-02 — Measurement metadata
Every sensor channel must declare measurement type, unit, range, accuracy specification, calibration metadata where available, installation location and device identity.

### FR-03 — Telemetry envelope
Every measurement must include event time, receive time, device ID, channel ID, value, unit, sequence number and quality/status metadata. Schema versioning is required.

### FR-04 — Data validation
Reject or quarantine malformed, impossible, stale, duplicated or out-of-order data according to explicit policies. Preserve rejected-event metadata for diagnostics without treating it as valid operational evidence.

### FR-05 — Offline resilience
The edge system must buffer measurements durably when the network is unavailable and deliver them after recovery without silently duplicating accepted records.

### FR-06 — Baselines
Baseline comparisons must be conditioned on relevant context such as operating schedule, pressure setpoint, production state and equipment configuration. Comparisons across unlike conditions must be marked invalid or uncertain.

### FR-07 — Anomaly events
An anomaly must include a rule/model version, time interval, affected asset, evidence references, severity rationale, confidence/uncertainty and lifecycle status.

### FR-08 — Diagnosis
AERIS must label statements as measured observation, inferred hypothesis or verified cause. A suspected leak must not be reported as a confirmed leak without independent confirmation.

### FR-09 — Impact estimation
Consumption and financial estimates must expose formula, units, tariff/energy assumptions, time window, missing inputs and uncertainty. If required inputs are absent, show an incomplete estimate rather than fabricate a value.

### FR-10 — Investigation workflow
Operators must be able to acknowledge a finding, add notes, assign an investigation, record a maintenance action and attach verification evidence.

### FR-11 — Outcome verification
Before/after comparisons must account for comparable operating conditions and identify confounders. Report measured differences separately from causal claims.

### FR-12 — Reporting
Reports must include site/asset context, measurement coverage, findings, evidence, calculations, assumptions, uncertainty and actions. Exported reports must retain timestamps and version information.

### FR-13 — Auditability
Changes to device configuration, thresholds, user permissions, investigation status and report generation must be attributable and timestamped.

### FR-14 — Access control
Users must only access sites and functions assigned to their role. Administrative actions require stronger authentication and audit records.

## 5. Non-functional requirements

- Reliability: no silent loss of buffered telemetry.
- Integrity: idempotent ingestion and explicit duplicate handling.
- Availability: local acquisition must not depend on cloud availability.
- Security: authenticated devices, encrypted transport, least privilege and managed secrets.
- Maintainability: versioned schemas, migrations, documented interfaces and automated tests.
- Observability: structured logs, health metrics and actionable failure states.
- Portability: hardware and cloud providers must be replaceable behind defined interfaces.
- Performance: latency and throughput targets will be set after sampling rates, channel counts and deployment scale are measured.
- Cost: total hardware, installation, connectivity and service costs must be included in customer economics.

## 6. Product acceptance gates

A release cannot be called field-ready until:
1. Measurements are compared with suitable reference instruments.
2. Sensor installation and calibration constraints are documented.
3. Offline buffering and recovery are tested.
4. Duplicate, delayed and malformed data cases are tested.
5. Detection performance is evaluated on labelled test data.
6. False-positive and false-negative rates are reported.
7. Impact calculations are independently checked.
8. Security and access-control tests pass.
9. Operators can understand and act on findings.
10. A supervised site trial confirms the product's operational usefulness.

## 7. Commercial hypotheses to validate

- Target sites experience recurring compressed-air losses or lack adequate visibility.
- Existing tools leave a meaningful gap for the selected customer segment.
- The buyer values continuous, evidence-backed monitoring over periodic audits alone.
- The product can be installed without unacceptable production disruption.
- Verified operational value exceeds total deployment and subscription cost.
- Customers will pay for continuing monitoring and investigation workflow.

No pricing, savings or demand claim is approved until supported by customer evidence.
