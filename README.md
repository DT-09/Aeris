# AERIS

**Industrial Utility Intelligence**

AERIS is an industrial intelligence system that connects physical utility infrastructure to reliable measurement, edge computing, diagnostics, prediction and verified operational improvement.

The first commercial product targets **compressed-air systems** in manufacturing facilities. The platform architecture is designed to support additional industrial utilities later, but no future utility capability is represented as implemented.

## Product promise

Turn trustworthy physical measurements into explainable operational findings:

- What is happening?
- Where and when is it happening?
- Is the observation real, or could it be a sensor/data-quality issue?
- What evidence supports the diagnosis?
- What is the estimated operational and financial consequence?
- What action should an operator consider?
- Did the intervention produce a measured improvement?

AERIS is not a generic sensor dashboard. Its core product is the evidence chain from measurement to verified outcome.

## Current status

**Repository bootstrap / specification stage.** This repository began empty. No hardware, firmware, backend, dashboard, field integration, validated diagnostic model or customer deployment is claimed to exist.

## Initial product boundary

The first release is a read-only monitoring and decision-support system for a controlled compressed-air installation. It measures pressure and flow, records equipment and operating context, detects defined anomalies, and produces evidence-backed investigations. It does not autonomously operate compressors, valves or other machinery.

## Engineering principles

1. Measurement provenance and timestamps are mandatory.
2. Data quality is evaluated before operational inference.
3. Diagnostics distinguish observation, hypothesis and verified cause.
4. Financial estimates expose assumptions and uncertainty.
5. Edge collection continues through network outages.
6. Device identity, secure transport, access control and auditability are designed in.
7. Physical actuation is out of scope until a separate safety case, authorization model and supervised validation exist.
8. Tests and reproducible verification accompany every subsystem.

## Documentation

- [Product requirements](docs/PRODUCT_REQUIREMENTS.md)
- [System architecture](docs/ARCHITECTURE.md)
- [Execution roadmap](docs/ROADMAP.md)
- [Safety, security and data integrity](docs/SAFETY_SECURITY.md)

## Proposed repository layout

```text
aeris/
├── docs/
│   ├── PRODUCT_REQUIREMENTS.md
│   ├── ARCHITECTURE.md
│   ├── ROADMAP.md
│   └── SAFETY_SECURITY.md
├── firmware/              # embedded device software
├── edge/                  # local gateway and buffering
├── services/              # ingestion and application APIs
├── analytics/             # baselines, diagnostics and estimates
├── web/                   # operator application
├── shared/                # schemas and protocol definitions
├── tests/                 # integration, simulation and acceptance tests
└── infrastructure/        # deployment and operational configuration
```

Directories will be introduced with their first working implementation rather than populated with empty placeholders.

## Development status

Work is governed by explicit acceptance criteria. A feature is not complete because it compiles or renders; it is complete when its behaviour is tested against the requirement it claims to satisfy.
