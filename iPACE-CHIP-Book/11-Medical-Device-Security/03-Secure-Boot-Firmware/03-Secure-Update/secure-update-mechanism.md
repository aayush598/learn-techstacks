# Secure Update Mechanism for iPACE-CHIP

## Overview

The iPACE-CHIP implantable pacemaker requires periodic firmware updates to address
security vulnerabilities, add features, and comply with evolving regulatory
requirements. The update mechanism must maintain the integrity and authenticity
of firmware while operating within the constraints of an implantable medical
device: limited bandwidth, finite battery life, and zero tolerance for update
failures that could disrupt life-sustaining therapy. This chapter details the
secure update architecture, protocols, and safety mechanisms.

## 1. Update Architecture

### 1.1 Update Topology

```
┌─────────────────────────────────────────────────────────────┐
│                  Firmware Update Infrastructure              │
│                                                             │
│  ┌──────────────┐     ┌──────────────┐                     │
│  │ Manufacturer │     │ Regulatory   │                     │
│  │ Build System │────→│ Approval     │                     │
│  └──────────────┘     │ (FDA/CE)     │                     │
│                       └──────┬───────┘                     │
│                              │                             │
│                       ┌──────┴───────┐                     │
│                       │ Secure       │                     │
│                       │ Update Server│                     │
│                       │ (cloud)      │                     │
│                       └──────┬───────┘                     │
│                              │                             │
│              ┌───────────────┼───────────────┐             │
│              │               │               │             │
│       ┌──────┴───────┐ ┌────┴────┐ ┌───────┴──────┐      │
│       │ Clinic       │ │ Hospital│ │ Patient      │      │
│       │ Programmer   │ │ Network │ │ Controller   │      │
│       │ (NFC/MICS)   │ │ (BLE)   │ │ (BLE)        │      │
│       └──────┬───────┘ └────┬────┘ └───────┬──────┘      │
│              │               │               │             │
│              └───────────────┼───────────────┘             │
│                              │                             │
│                       ┌──────┴───────┐                     │
│                       │  iPACE-CHIP  │                     │
│                       │  Implant     │                     │
│                       └──────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Update Channels

| Channel | Bandwidth | Security | Use Case |
|---------|-----------|----------|----------|
| NFC (clinic) | 424 kbps | High (physical proximity) | Major updates, emergency patches |
| MICS (remote) | 400 kbps | High (encrypted link) | Scheduled updates |
| BLE (patient) | 1 Mbps | Medium (paired device) | Minor updates, data updates |

### 1.3 Update Types

| Type | Size | Frequency | Priority |
|------|------|-----------|----------|
| Major firmware | 256-512 KB | 1-2 per year | Planned |
| Minor firmware | 16-64 KB | 2-4 per year | Planned |
| Security patch | 8-32 KB | As needed | Emergency |
| Configuration | 1-4 KB | As needed | Routine |
| Calibration data | 0.5-2 KB | Per session | Routine |

## 2. Update Protocol Design

### 2.1 Update State Machine

```
┌────────┐    ┌────────────┐    ┌──────────┐    ┌────────────┐
│  IDLE  │───→│ NOTIFIED   │───→│ DOWNLOAD │───→│ VERIFYING  │
└────────┘    └────────────┘    └──────────┘    └─────┬──────┘
                                                       │
                          ┌────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
              ▼                       ▼
        ┌──────────┐           ┌──────────┐
        │ INSTALLING│           │ REJECTED │
        └────┬─────┘           └──────────┘
             │
     ┌───────┴───────┐
     │               │
     ▼               ▼
┌──────────┐   ┌──────────┐
│ TESTING  │   │ ROLLBACK │
└────┬─────┘   └──────────┘
     │
     ├──→ ┌──────────┐
     │    │ ACTIVE   │
     │    └──────────┘
     │
     └──→ ┌──────────┐
          │ FAILED   │──→ ROLLBACK
          └──────────┘
```

### 2.2 Full Update Protocol

```
Phase 1: Discovery and Authorization

  Implant → Programmer: DeviceInfo{
    current_version,
    hardware_revision,
    available_flash,
    battery_level,
    last_update_timestamp
  }

  Programmer → Server: UpdateQuery{
    device_type,
    current_version,
    hardware_revision
  }

  Server → Programmer: UpdateAvailable{
    new_version,
    size,
    sha384_hash,
    release_notes,
    required_battery_level,
    estimated_update_time,
    signature
  }

Phase 2: Pre-Update Checks

  Programmer performs:
    1. Verify update signature (ECDSA-P384)
    2. Verify version > current_version
    3. Verify hardware compatibility
    4. Verify battery level > minimum threshold (30%)
    5. Verify no active therapy session
    6. Obtain patient consent (if required)
    7. Inform clinician (if required)

Phase 3: Secure Download

  Programmer → Server: RequestEncrypted{
    device_id (encrypted),
    update_version,
    nonce
  }

  Server → Programmer: EncryptedFirmware{
    AES-256-GCM encrypted firmware image
    Encryption key: derived from device DRK + server secret
    IV: unique per device
  }

Phase 4: Image Verification (Programmer)

  Programmer:
    1. Decrypt firmware image
    2. Verify SHA-384 hash matches announcement
    3. Verify ECDSA-P384 signature
    4. Verify certificate chain
    5. Verify anti-rollback counter
    6. Store verified image locally

Phase 5: Transfer to Implant

  (via NFC, MICS, or BLE - see Section 3)

Phase 6: Implant Verification

  Implant:
    1. Verify image signature (ECDSA-P384)
    2. Verify all segment hashes
    3. Verify Merkle tree root
    4. Verify version compatibility
    5. Write to inactive flash bank

Phase 7: Testing and Activation

  Implant:
    1. Boot from new firmware (sandbox mode)
    2. Run self-test suite
    3. Verify therapy parameters intact
    4. If all tests pass: activate new firmware
    5. If any test fails: revert to previous firmware
    6. Report result to programmer
```

### 2.3 Differential Updates

For minor updates, the iPACE-CHIP supports differential (delta) updates:

```
Differential Update Process:

Server-side:
  1. Compute binary diff between old and new firmware
  2. Generate delta using xdelta3 algorithm
  3. Sign delta with ECDSA-P384
  4. Package delta with metadata

  Delta size: typically 5-15% of full image
  Example: 256 KB firmware → 15-40 KB delta

Device-side:
  1. Receive delta
  2. Verify delta signature
  3. Apply delta to current firmware in flash
  4. Compute hash of result
  5. Compare with expected hash of new firmware
  6. If match: activate new firmware
  7. If mismatch: discard delta, request full image
```

## 3. Transfer Protocols

### 3.1 NFC Transfer Protocol

```
NFC Update Transfer:
  Mode: ISO 14443-4 (T=CL)
  Speed: 424 kbps
  Maximum frame size: 256 bytes
  Transfer method: Block-oriented

  Protocol:
    1. Programmer sends UPDATE_START command
    2. Implant allocates receive buffer (inactive bank)
    3. Programmer sends data blocks sequentially
    4. Implant verifies each block hash
    5. After all blocks: Implant computes full image hash
    6. Programmer sends UPDATE_VERIFY with expected hash
    7. Implant compares and responds with result

  NFC Update Timing:
    256 KB image: ~5 seconds
    512 KB image: ~10 seconds
    Power: Harvested from NFC field (no battery drain)
```

### 3.2 MICS Transfer Protocol

```
MICS Update Transfer:
  Mode: Reliable data transfer with ACK/NACK
  Speed: 400 kbps (effective: ~200 kbps with FEC)
  Maximum frame size: 255 bytes
  Transfer method: Windowed (sliding window, size 16)

  Protocol:
    1. Programmer sends UPDATE_START with image metadata
    2. Implant acknowledges, enters update mode
    3. Programmer sends window of 16 frames
    4. Implant ACKs received frames
    5. Programmer retransmits lost frames
    6. Continue until all frames sent
    7. Implant verifies complete image
    8. Programmer sends UPDATE_COMPLETE

  MICS Update Timing:
    256 KB image: ~12 seconds (with FEC overhead)
    512 KB image: ~24 seconds
    Power: Battery-powered (implant TX: 25 μW)

  Anti-Jamming During Update:
    - Frequency hopping maintained
    - Store-and-forward for interruptions
    - Resume from last ACKed frame
    - Timeout: 60 seconds per window
```

### 3.3 BLE Transfer Protocol

```
BLE Update Transfer:
  Mode: GATT Characteristic (write-with-response)
  Speed: 1 Mbps (effective: ~200 kbps)
  Maximum ATT_MTU: 247 bytes (BLE 5.0)
  Transfer method: Sequential with progress notification

  Protocol:
    1. Patient controller discovers DFU service
    2. Controller authenticates (LE Secure Connections)
    3. Controller sends firmware image in chunks
    4. Implant verifies each chunk
    5. Progress notification: every 10% complete
    6. After complete: full verification
    7. Activation or rollback

  BLE Update Timing:
    256 KB image: ~12 seconds
    512 KB image: ~24 seconds
    Power: Battery-powered (both devices)
    Note: Patient controller must remain within 10m

  BLE Connection Parameters During Update:
    - Connection interval: 7.5 ms (minimum)
    - Slave latency: 0 (no skipping)
    - Supervision timeout: 4 seconds
```

## 4. Safety Mechanisms

### 4.1 Battery Safety

```
Battery Safety Rules:
  Minimum battery for update: 30% (critical for safety)
  Battery monitoring: Continuous during update
  Threshold breach response:
    - If battery drops below 20% during update:
      1. Pause update (save progress)
      2. Wait for charging or NFC power
      3. Resume when battery > 30%
    - If battery drops below 10%:
      1. Abort update
      2. Revert to previous firmware if needed
      3. Enter safe mode
```

### 4.2 Therapy Continuity

```
Therapy Continuity During Update:
  Rule: Never interrupt ongoing therapy

  Implementation:
    1. Check for active pacing before starting
    2. If active: delay update until session ends
    3. During transfer: maintain current therapy parameters
    4. During activation: switch parameters atomically
    5. Post-activation: verify therapy parameters match expected

  Emergency Override:
    If life-threatening issue detected:
    1. Emergency patch can be applied during therapy
    2. Uses separate, pre-verified emergency partition
    3. Minimal disruption: < 100 ms therapy pause
    4. Automatic revert if emergency patch fails
```

### 4.3 Power Loss Recovery

```
Power Loss During Update:

Scenario 1: Power loss during transfer
  - Partial data in inactive bank is invalid
  - Active bank unchanged
  - On power恢复: resume from beginning (full transfer)
  - No data corruption possible

Scenario 2: Power loss during verification
  - Inactive bank may contain partial data
  - Active bank unchanged
  - On power恢复: discard inactive bank, restart update

Scenario 3: Power loss during activation
  - Both banks may be in unknown state
  - Recovery mechanism: hardware watchdog triggers boot from
    recovery partition
  - Recovery partition loads known-good firmware
  - Update must be retried

Scenario 4: Power loss during self-test
  - New firmware may be partially tested
  - On power恢复: revert to previous firmware (safe default)
  - Self-test must complete successfully before activation
```

### 4.4 Flash Wear Management

```
Flash Write Limits:
  Application flash: 10,000 erase cycles
  Update bank: alternated to distribute wear
  Wear tracking: maintained in OTP

  Wear Management:
    1. Alternate active bank between updates
    2. Track erase count per bank
    3. If one bank approaching limit: use as read-only
    4. Minimum 2 banks always available
    5. Alert clinician when wear exceeds 80%
```

## 5. Verification at Each Stage

### 5.1 Pre-Transfer Verification

```
Programmer-side verification before transfer:
  1. ECDSA-P384 signature verification
  2. SHA-384 image hash verification
  3. Certificate chain verification
  4. Anti-rollback version check
  5. Hardware compatibility check
  6. Image format validation
  7. Segment boundary check

  All checks must pass before transfer begins
  Any failure: abort update, notify user
```

### 5.2 In-Transit Verification

```
During transfer verification:
  1. Frame-level: CRC-16 on each frame
  2. Block-level: SHA-256 per block (16 frames)
  3. Segment-level: SHA-256 per segment header
  4. Connection-level: ACK/NACK with sequence numbers
  5. Integrity-level: HMAC on each data block

  If any verification fails:
    - Retransmit failed block (up to 3 retries)
    - If still failing: pause and alert
    - Resume or abort based on failure pattern
```

### 5.3 Post-Transfer Verification

```
Implant-side verification after complete transfer:
  1. Reassemble complete image from received blocks
  2. Compute full image SHA-384 hash
  3. Verify hash matches expected value
  4. Verify ECDSA-P384 signature over image hash
  5. Verify certificate chain to manufacturer CA
  6. Verify segment hashes via Merkle tree
  7. Verify anti-rollback counter

  All checks must pass before proceeding to activation
  Any failure: discard image, report error
```

### 5.4 Activation Verification

```
Post-activation verification:
  1. Boot from new firmware bank
  2. Run hardware self-test (POST)
  3. Verify crypto accelerator functionality
  4. Verify TRNG health
  5. Verify key storage integrity
  6. Verify therapy parameter defaults
  7. Run 10-second observation period
  8. If all pass: mark firmware as active
  9. If any fail: revert to previous firmware
```

## 6. Emergency Update Process

### 6.1 Emergency Patch Definition

An emergency patch addresses:
- Critical security vulnerabilities (CVSS ≥ 9.0)
- Therapy safety issues (potential patient harm)
- Regulatory recall requirements
- Compliance with FDA emergency order

### 6.2 Expedited Emergency Process

```
Emergency Update Timeline:
  Hour 0:  Vulnerability discovered
  Hour 1:  Patch development initiated
  Hour 4:  Patch developed and unit tested
  Hour 6:  Security review (abbreviated)
  Hour 8:  Signed with emergency key
  Hour 10: Deployed to update servers
  Hour 12: Notification sent to all clinics
  Hour 24: All at-risk devices updated (target)

  Emergency key: Separate from regular release key
  Reduced quorum: 2-of-5 signers (vs. 3-of-5 regular)
  Abbreviated testing: Critical path tests only
  Full validation: Within 7 days of emergency release
```

### 6.3 Critical Update Push

For life-threatening vulnerabilities, the iPACE-CHIP supports priority updates:

```
Critical Update Flow:
  1. Server flags update as CRITICAL
  2. Patient controller receives priority notification
  3. If patient controller connected: auto-download update
  4. If implant in range: auto-install (with patient alert)
  5. If not connected: continuous notification until addressed
  6. Clinician portal: alert all affected patients

  Auto-install conditions (all must be met):
    - Update flagged as CRITICAL
    - Battery > 50%
    - No active therapy session
    - Patient consent previously granted for auto-updates
    - Implant in BLE range of patient controller
```

## 7. Update Logging and Audit

### 7.1 Update Event Log

Every update attempt is logged in the implant's tamper-evident audit log:

```
Update Log Entry:
  Timestamp: UTC (8 bytes)
  Event_Type: [NOTIFIED | STARTED | DOWNLOADED | VERIFIED |
               INSTALLING | ACTIVATED | FAILED | ROLLBACK]
  Old_Version: 4 bytes
  New_Version: 4 bytes
  Update_Size: 4 bytes
  Channel: [NFC | MICS | BLE]
  Duration: 4 bytes (ms)
  Result: [SUCCESS | FAILURE | ROLLBACK]
  Failure_Reason: 4 bytes (if applicable)
  Hash: SHA-256 of all preceding fields (32 bytes)

  Total: 72 bytes per entry
  Storage: 256 entries (18 KB)
```

### 7.2 Remote Audit Trail

```
Programmer-side logging:
  - Device ID, firmware versions
  - Update hash and signature
  - All verification results
  - Transfer statistics
  - Patient consent records

Cloud-side logging:
  - Update distribution records
  - Device update status
  - Failure rates and patterns
  - Security event correlation

  All logs: Encrypted, signed, tamper-evident
  Retention: 15 years (device lifetime + 5 years)
```

## 8. Configuration Update

### 8.1 Therapy Parameter Updates

Non-firmware updates to therapy parameters follow a separate, more restrictive
process:

```
Therapy Parameter Update:
  1. Clinician proposes changes via programmer
  2. Changes reviewed by second clinician (four-eyes principle)
  3. Patient consents to changes
  4. Both signatures on change request
  5. Programmer sends signed parameter set to implant
  6. Implant verifies:
     a. Clinician signatures valid
     b. Patient consent valid
     c. Parameters within safe bounds
     d. No conflict with active safety limits
  7. Implant applies parameters atomically
  8. Implant logs parameter change
  9. Verification: read-back and compare
```

### 8.2 Calibration Data Updates

```
Calibration Update:
  Source: Manufacturer calibration database
  Transfer: Via programmer during clinical visit
  Verification: HMAC-SHA256 over calibration data
  Storage: Protected NVM region
  Integrity: Periodic hash verification
```

## 9. Update Performance Metrics

### 9.1 Transfer Speed Benchmarks

| Image Size | NFC | MICS | BLE |
|-----------|-----|------|-----|
| 64 KB | 1.3 s | 3.2 s | 3.2 s |
| 128 KB | 2.5 s | 6.4 s | 6.4 s |
| 256 KB | 5.0 s | 12.8 s | 12.8 s |
| 512 KB | 10.0 s | 25.6 s | 25.6 s |

### 9.2 Verification Benchmarks

| Step | Time | Energy |
|------|------|--------|
| Pre-transfer verification (programmer) | 189 ms | 3.4 mJ |
| Post-transfer verification (implant) | 313 ms | 5.64 mJ |
| Activation verification | 45 ms | 0.81 mJ |
| Self-test | 200 ms | 3.6 mJ |
| **Total verification** | **747 ms** | **13.45 mJ** |

### 9.3 Total Update Time

| Image Size | NFC (total) | MICS (total) | BLE (total) |
|-----------|------------|-------------|------------|
| 128 KB | 3.2 s | 7.1 s | 7.1 s |
| 256 KB | 5.7 s | 13.5 s | 13.5 s |
| 512 KB | 10.7 s | 26.3 s | 26.3 s |

## 10. Compliance

| Standard | Requirement | Status |
|----------|-------------|--------|
| IEC 62304 | Software update process | Compliant |
| IEC 81001-5-1 | Secure update mechanism | Compliant |
| FDA 21 CFR 820 | Design change control | Compliant |
| FDA Cybersecurity | Secure update guidance | Compliant |
| UL 2900-1 | Software integrity verification | Level 3 |
| MDCG 2019-16 | Cybersecurity documentation | Compliant |

## 11. Summary

The iPACE-CHIP secure update mechanism provides end-to-end integrity protection
from firmware creation through installation. Multi-channel support (NFC, MICS,
BLE) enables updates in clinical and home settings. Comprehensive verification
at every stage — pre-transfer, in-transit, post-transfer, and activation —
ensures that only authentic, unmodified firmware is installed. Safety mechanisms
protect against battery exhaustion, therapy interruption, and power loss during
updates. Emergency update capability enables rapid deployment of critical security
patches. The dual-bank architecture provides automatic rollback on failure,
ensuring that a failed update never leaves the device in a non-functional state.
All update activities are logged in tamper-evident audit trails for regulatory
compliance and forensic analysis.
