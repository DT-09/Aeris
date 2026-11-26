# Simulation and Finding Semantics

## Synthetic simulator

The deterministic simulator generates compressed-air flow events for development and acceptance tests. Supported patterns are normal flow, elevated idle-period flow, and sustained excess flow. Optional controls model dropped events, duplicate event identities, and delayed receipt timestamps.

Every generated event carries the quality flag synthetic. These records are not measurements from a real plant, a calibrated digital twin, or evidence of customer performance. Keep this provenance when exporting or displaying data.

## Sustained excess-flow rule v1

For each adjacent pair of flow points:
1. Both endpoints must be valid and context-comparable.
2. The interval must not exceed the configured maximum gap.
3. Positive excess at each endpoint is max(0, observed flow minus baseline flow).
4. The interval mean is the arithmetic mean of endpoint excess.
5. An interval qualifies when its mean meets the configured threshold.
6. Consecutive qualifying intervals form a run. A finding is emitted only when the run meets the minimum duration.

Each finding reports its time window, duration, mean and peak excess flow, integrated excess volume, interval count, rule identifier, and classification as an observation.

## Limits

The baseline is supplied; this rule does not learn or validate it. A finding does not identify a leak, failed machine, open valve, or root cause. Thresholds require calibration against the actual measurement system and operating modes. Synthetic tests do not establish sensor accuracy, energy savings, site suitability, or commercial value. Duplicate suppression, durable ingestion, clock-quality assessment, and baseline learning remain separate work.
