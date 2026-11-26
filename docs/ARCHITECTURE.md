# AERIS — System Architecture

**Status:** Proposed architecture baseline. Implementation choices remain subject to prototype measurements and hardware constraints.

## 1. Architecture overview

AERIS uses a layered, store-and-forward architecture:

```text
PHYSICAL COMPRESSED-AIR SYSTEM
  ├── Pressure measurement points
  ├── Flow measurement points
  └── Optional equipment/energy context
              |
              v
SENSOR / ACQUISITION NODE
  ├── Sensor interface and sampling
  ├── Range and plausibility checks
  ├── Device identity and sequence numbers
  └── Local diagnostics
              |
              v
EDGE GATEWAY
  ├── Durable local queue
  ├── Timestamp and schema validation
  ├── Local health monitoring
  ├── Secure MQTT/HTTPS transport
  └── Reconnection and replay
              |
              v
INGESTION SERVICE
  ├── Authentication and authorization
  ├── Schema validation
  ├── Idempotency and deduplication
  ├── Quarantine path
  └── Accepted telemetry stream
              |
       +------+------+
       |             |
       v             v
TIME-SERIES       ASSET / CONFIG
STORAGE           DATABASE
       |             |
       +------+------+
              |
              v
ANALYTICS PIPELINE
  ├── Data-quality assessment
  ├── Operating-state segmentation
  ├── Baseline computation
  ├── Rule-based anomaly detection
  ├── Impact estimation
  └── Evidence-linked investigation
              |
              v
APPLICATION API
              |
              v
OPERATOR WEB APPLICATION
  ├── Command centre
  ├── Infrastructure
  ├── Findings and investigations
  ├── Performance and reports
  └── Administration and audit
```

## 2. Architectural boundaries

### Sensor node
Owns electrical/sensor interfacing, sampling, basic plausibility checks, device identity and monotonic sequence generation. It does not make high-consequence operational decisions.

### Edge gateway
Owns durable buffering, time synchronisation status, transport, retry, local diagnostics and safe configuration rollout. The gateway must retain original event time and distinguish it from receive time.

### Ingestion service
Owns authentication, schema validation, idempotency, quarantine and accepted-event persistence. It must not silently rewrite measurements.

### Analytics
Owns reproducible transformations, baselines, detection rules and estimates. Every output must identify its input window and algorithm/configuration version.

### Application
Owns operator workflows, permissions, investigation lifecycle and presentation. It must not recalculate critical financial or engineering results independently in the browser.

## 3. Proposed technology choices

These are defaults for the first implementation, not irreversible commitments.

| Concern | Initial choice | Rationale |
|---|---|---|
| MCU prototype | ESP32-class board | Accessible prototype ecosystem |
| Firmware | C++ / ESP-IDF | Mature embedded tooling |
| Edge gateway | Linux-capable gateway | Durable storage and protocol flexibility |
| Device protocol | MQTT over TLS | Publish/subscribe telemetry |
| API | Python + FastAPI | Clear service contracts and analytics integration |
| Database | PostgreSQL with time-series extension if justified | Relational asset model plus time-indexed data |
| Analytics | Python, NumPy, pandas, scikit-learn where appropriate | Transparent numerical workflows |
| Frontend | React + TypeScript | Typed operator application |
| Deployment | Containerised services initially | Reproducible development and deployment |
| Tests | Unit, property, integration, simulation and hardware-in-loop | Layered verification |

Avoid adding Kubernetes, microservices, a message broker cluster or an LLM merely for architectural fashion. Begin with a modular monolith and split services only when scale or isolation requires it.

## 4. Measurement and telemetry contract

The canonical telemetry event should contain:

- schema_version
- event_id
- device_id
- site_id
- asset_id
- channel_id
- event_time_utc
- received_time_utc
- sequence_number
- value
- unit
- quality_flags
- calibration_reference (nullable)
- firmware_version

Use explicit SI units internally. Unit conversion belongs at a validated boundary. Never infer a unit from a numeric value.

### Time semantics

- Event time: when the device says the measurement occurred.
- Receive time: when the platform accepted the event.
- Device clock status: synchronised, unsynchronised or unknown.
- Sequence number: monotonically increasing per device/channel stream as specified.

Out-of-order delivery must be supported. Ordering is not guaranteed by network arrival time.

## 5. Data model

Initial logical entities:

- Organisation
- Site
- User
- Role / SitePermission
- Asset
- SensorDevice
- SensorChannel
- CalibrationRecord
- TelemetryEvent
- DataQualityEvent
- OperatingSchedule
- OperatingStateAnnotation
- BaselineVersion
- DetectionRuleVersion
- AnomalyEvent
- Investigation
- MaintenanceAction
- VerificationWindow
- Report
- AuditEvent

Telemetry is append-oriented. Corrections should be represented by explicit quality/correction records rather than destructive rewriting of original observations.

## 6. Analytics pipeline

1. Validate schema, unit, timestamp and sequence.
2. Evaluate sensor health and measurement coverage.
3. Segment data by operating context.
4. Compute a baseline from comparable periods.
5. Apply explicit anomaly rules.
6. Attach source event IDs and calculation version.
7. Estimate excess consumption only when inputs support it.
8. Create or update an investigation.
9. Compare post-maintenance windows under comparable conditions.
10. Publish a versioned report.

### Baseline principle

A baseline must not compare unlike operating states. At minimum, evaluate pressure, production/idle state, schedule and known configuration changes. If context is missing, reduce confidence or withhold the comparison.

### Excess-flow estimate

For a valid interval:

`V_{excess} = \sum_i \max(0, Q_{observed,i} - Q_{baseline,i}) \Delta t_i`

This calculation is only meaningful when flow units, time units, sampling coverage and comparable operating conditions are valid.

Energy and financial estimates require additional measured or documented system-efficiency, compressor-power and tariff inputs. Do not apply a universal conversion factor without evidence.

## 7. Interfaces

- Sensor node to gateway: documented serial, fieldbus or local network interface selected for hardware.
- Gateway to cloud: MQTT over TLS with per-device identity; HTTPS may be used for provisioning and management.
- Service to database: versioned repository layer and migrations.
- Frontend to API: versioned JSON API with typed schemas.
- Analytics to investigation service: versioned finding contract with evidence references.

## 8. Deployment topology

Prototype:
- One controlled test rig.
- One acquisition node.
- One edge gateway.
- One application environment.
- Synthetic and recorded test datasets.

Pilot:
- Isolated customer/site namespace.
- Secure device provisioning.
- Monitored gateway.
- Explicit data retention and support procedures.
- Read-only integration.

Production:
- Tenant isolation.
- Backup and restore tests.
- Monitoring and alerting.
- Credential rotation.
- Release rollback.
- Disaster recovery procedures.
- Documented service-level objectives based on measured capability.

## 9. Key architecture decisions still open

- Required pressure and flow ranges.
- Sensor technology and installation method.
- Sampling frequency and aggregation policy.
- Gateway hardware and operating system.
- Local retention duration.
- Cloud hosting and data residency.
- Customer network constraints.
- Required industrial protocols.
- Calibration and maintenance procedure.

Resolve these through customer/site requirements and measurement tests, not guesswork.
