# AERIS — Safety, Security and Data Integrity

**Status:** Baseline controls; formal risk assessment required before any industrial deployment.

## 1. Safety boundary

The initial AERIS product is read-only monitoring and decision support.

It must not:
- Start or stop compressors.
- Open or close valves.
- Change pressure setpoints.
- Bypass interlocks.
- Replace safety instrumentation or certified control systems.
- Present an inferred anomaly as a safety alarm.

Any future actuation capability requires a separate hazard analysis, control-system architecture, independent safeguards, qualified engineering review, site authorization and supervised commissioning. It is not part of the initial product.

## 2. Installation safety

- Use a controlled, low-pressure test rig for early development.
- Do not modify pressurised industrial pipework as an unsupervised activity.
- Pressure-rated components must be selected for the actual service conditions and installed by qualified personnel.
- Electrical work on industrial mains and machinery must be performed by qualified personnel under site procedures.
- Sensor placement must not obstruct access, guards, emergency stops or existing safety devices.
- Follow site isolation, permit-to-work and lockout/tagout requirements where applicable.

## 3. Measurement integrity

- Store raw measurements with source identity and timestamps.
- Preserve units and conversion history.
- Track calibration/verification metadata.
- Detect out-of-range, stuck, drifting, stale and disconnected sensors.
- Distinguish event time from receive time.
- Record missing-data intervals.
- Never interpolate data silently for financial or diagnostic claims.
- Version every transformation, baseline and detection rule.
- Keep original data immutable or append corrections with an audit trail.

## 4. Security baseline

### Device
- Unique device identity.
- Per-device credentials or certificates.
- No shared default passwords.
- Secure boot and signed firmware where supported by selected hardware.
- Disable unused interfaces and services.
- Protect credentials at rest.
- Support credential rotation and revocation.

### Transport
- TLS for network communication.
- Authenticated device connections.
- Replay and duplicate handling.
- Restrict outbound and inbound network paths.
- Do not expose device management interfaces publicly.

### Platform
- Role-based access control and site-level tenant isolation.
- Strong authentication for privileged users.
- Managed secrets; no credentials in source control.
- Encryption in transit and at rest.
- Audit logs for privileged actions and configuration changes.
- Dependency scanning and patch management.
- Rate limiting and input validation.
- Tested backup and restore procedures.

## 5. Data governance

- Collect only data needed for the product.
- Define customer ownership and permitted processing in contracts.
- Separate tenants and access scopes.
- Define retention and deletion procedures.
- Do not use identifiable customer telemetry for cross-customer model training or benchmarking without explicit contractual permission.
- Record data export and administrative access.
- Establish incident response and breach notification procedures with qualified legal guidance.

## 6. Analytics safety

Every finding must distinguish:
- **Observation:** directly supported by validated measurements.
- **Hypothesis:** a possible explanation requiring investigation.
- **Verified cause:** confirmed by an independent inspection or other accepted evidence.

Every financial estimate must expose:
- Formula and units.
- Measurement interval.
- Baseline method.
- Assumptions.
- Missing inputs.
- Uncertainty or confidence limitations.

The interface must not imply that a recommended action is safe for every installation. Site procedures and qualified personnel govern physical work.

## 7. Failure handling

Required failure cases include:
- Sensor disconnected.
- Sensor stuck or drifting.
- Gateway power loss.
- Network outage.
- Clock unsynchronised.
- Queue storage full.
- Duplicate and out-of-order messages.
- Invalid schema or unit.
- Expired/revoked credentials.
- Database unavailable.
- Analytics job failure.
- Incorrect asset mapping.

Each failure must have a detectable state, an operational response and a test. Failure must not silently produce a normal-looking dashboard or false savings report.
