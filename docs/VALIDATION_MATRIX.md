# AERIS — Validation Matrix

This matrix links product requirements to verification evidence. Status reflects repository evidence, not intended future work.

| Requirement | Verification method | Current evidence | Status |
|---|---|---|---|
| FR-01 Device identity | Contract tests and provisioning tests | Telemetry envelope requires device_id | Partial |
| FR-02 Measurement metadata | Contract tests and sensor acceptance tests | Metric/unit validation in core | Partial |
| FR-03 Telemetry envelope | Unit tests for required fields and types | Python telemetry tests | Implemented in core |
| FR-04 Data validation | Invalid schema, unit, timestamp and value tests | Python telemetry tests | Partial |
| FR-05 Offline resilience | Gateway outage/restart/replay integration tests | Not implemented | Not started |
| FR-06 Contextual baselines | Dataset evaluation across operating modes | Not implemented | Not started |
| FR-07 Anomaly evidence | Finding contract and rule-version tests | Sustained excess-flow rule and unit tests | Partial |
| FR-08 Observation/hypothesis/cause distinction | Domain model and workflow tests | Specified in requirements | Not started |
| FR-09 Impact estimation | Unit tests, independent calculation review | Excess-volume primitive only | Partial |
| FR-10 Investigation workflow | API and UI integration tests | Not implemented | Not started |
| FR-11 Outcome verification | Comparable-window and confounder tests | Not implemented | Not started |
| FR-12 Reporting | Snapshot/export and provenance tests | Not implemented | Not started |
| FR-13 Auditability | Append-only audit tests | Not implemented | Not started |
| FR-14 Access control | Authorization and tenant-isolation tests | Not implemented | Not started |

## Implemented automated checks

The current Python test suite covers:
- Valid telemetry parsing.
- Canonical unit enforcement.
- Timezone-aware timestamps.
- Rejection of booleans as numeric measurements.
- Rejection of negative flow.
- Schema-version enforcement.
- Constant excess-flow integration.
- Trapezoidal integration.
- Clamping negative deviations to zero excess.
- Exclusion of invalid or non-comparable intervals.
- Exclusion of large sampling gaps.
- Rejection of non-monotonic and timezone-naive time series.
- Deterministic synthetic event generation and canonical-contract validation.
- Synthetic dropout and duplicate-event simulation.
- Sustained excess-flow findings with duration, threshold, evidence window and integrated volume.
- Suppression of short spikes and breaks across invalid intervals.

## Required next tests

1. Missing required telemetry fields.
2. NaN and infinity.
3. Pressure zero and negative values.
4. Duplicate event IDs and sequence handling.
5. Clock skew and late arrival.
6. Irregular sample intervals.
7. Coverage thresholds for estimates.
8. Unit conversion at device-adapter boundary.
9. Property-based tests for volume integration.
10. Integration tests against durable ingestion storage.

## Status definitions

- **Not started:** no implementation or test evidence.
- **Partial:** some lower-level behaviour exists, but the complete requirement is not satisfied.
- **Implemented in core:** code and automated tests exist for the stated core behaviour; this does not imply field validation.
- **Field validated:** tested at a supervised site against appropriate references and documented operating conditions.
- **Accepted:** product owner/customer acceptance evidence exists.
