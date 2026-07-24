# Wireless Channel Security for iPACE-CHIP

## Overview

The iPACE-CHIP implantable pacemaker communicates wirelessly with external programmers
and patient controllers using a combination of near-field (NFC), medical implant
communication (MICS), and Bluetooth Low Energy (BLE) protocols. Securing these
wireless channels is paramount — an adversary who can intercept, inject, or
modify wireless communications could potentially deliver lethal therapy or disable
life-sustaining pacing. This chapter details the wireless security architecture
from physical layer through application layer.

## 1. Wireless Communication Interfaces

### 1.1 Communication Topology

The iPACE-CHIP supports three distinct wireless interfaces, each serving different
use cases:

```
┌──────────────────────────────────────────────────────────────┐
│                      iPACE-CHIP Implant                      │
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐               │
│  │ NFC      │    │ MICS     │    │ BLE      │               │
│  │ 13.56 MHz│    │ 402-405  │    │ 2.4 GHz  │               │
│  │ 10 cm    │    │ MHz      │    │ 10 m     │               │
│  │ 424 kbps │    │ 400 kbps │    │ 1 Mbps   │               │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘               │
│       │              │              │                        │
│       └──────────────┼──────────────┘                        │
│                      │                                       │
│              ┌───────┴───────┐                               │
│              │ Secure Comms  │                               │
│              │ Manager (SCM) │                               │
│              └───────┬───────┘                               │
│                      │                                       │
│              ┌───────┴───────┐                               │
│              │ Crypto Engine │                               │
│              └───────────────┘                               │
└──────────────────────────────────────────────────────────────┘
```

### 1.2 Interface Specifications

| Parameter | NFC | MICS | BLE |
|-----------|-----|------|-----|
| Frequency | 13.56 MHz | 402-405 MHz | 2.4 GHz ISM |
| Range | ≤10 cm | 2-10 m | 1-10 m |
| Data rate | 424 kbps | 400 kbps | 1 Mbps |
| Modulation | ASK/PPM | FSK | GFSK |
| Regulatory | ISO 14443 | FCC Part 95 | FCC Part 15 |
| Typical use | Programming | Telemetry | Patient controller |
| Power | Harvested (NFC) | Battery | Battery |
| Duty cycle | Intermittent | Continuous | Periodic |

## 2. Medical Implant Communication Service (MICS)

### 2.1 MICS Band Security

The MICS band (402-405 MHz) is an internationally allocated frequency band
dedicated to communication with implanted medical devices. While the dedicated
allocation provides some inherent protection, it is not immune to attack.

**Regulatory Security Features:**

- Transmit power limited to -16 dBm (25 μW) at the implant
- Mandatory frequency hopping across 10 channels (402.0-405.0 MHz, 300 kHz spacing)
- Maximum dwell time per channel: 400 ms
- Mandatory listen-before-talk protocol

**Inherent Limitations:**

- Low transmit power limits range but does not prevent nearby eavesdropping
- Frequency hopping provides limited security (10 channels easily swept)
- No built-in encryption at the physical layer
- Regulatory compliance does not guarantee security

### 2.2 MICS Link Security Architecture

The iPACE-CHIP implements a multi-layer security approach for MICS:

```
Layer 5: Application Security (telemetry encryption, command authentication)
Layer 4: Session Security (session keys, replay protection)
Layer 3: Transport Security (message authentication, fragmentation)
Layer 2: Link Security (device pairing, access control)
Layer 1: Physical Security (frequency hopping, power control)
```

### 2.3 Frequency Hopping Spread Spectrum

The iPACE-CHIP uses adaptive frequency hopping (AFH) with a cryptographically
secure hopping pattern:

**Hopping Sequence Generation:**

```
channel[i] = AES-CTR-128(
    key = hop_key,
    nonce = frame_counter || device_id,
    output = 1 byte mod 10
)
```

The hop key is derived from the session key, ensuring that only authorized
devices can predict the hopping sequence. An attacker without the hop key
must simultaneously monitor all 10 channels, increasing the difficulty of
real-time interception.

**Hopping Parameters:**

| Parameter | Value |
|-----------|-------|
| Number of channels | 10 |
| Channel bandwidth | 300 kHz |
| Dwell time | 200 ms (typical) |
| Hop rate | 5 hops/second |
| Hop sequence length | 2^32 before repeat |
| Sync method | Timestamp-based |

### 2.4 MICS Frame Security

Each MICS data frame includes security fields:

```
┌────────┬────────┬─────────┬──────────┬─────────┬────────┬──────────┐
│ Preamble│ Sync   │ Device  │ Frame    │ Payload │ Tag    │ CRC-16   │
│ (4B)   │ (2B)   │ ID (4B) │ Counter  │ (0-255B)│ (8B)   │ (2B)     │
│        │        │         │ (4B)     │         │        │          │
└────────┴────────┴─────────┴──────────┴─────────┴────────┴──────────┘
   ← Clear  ← Clear  ← Encrypted  ← Encrypted  ← Auth   ← Clear
```

- **Device ID:** 32-bit identifier, encrypted to prevent tracking
- **Frame Counter:** 32-bit monotonic counter, encrypted, provides replay protection
- **Tag:** 64-bit truncated CMAC-AES for message authentication
- **CRC-16:** Error detection (not security, covers unencrypted fields)

## 3. Near-Field Communication (NFC) Security

### 3.1 NFC Security for Programming Sessions

NFC provides the highest-bandwidth, lowest-latency interface for programming
operations. The short range (≤10 cm) provides physical security, but is insufficient
for high-security operations without cryptographic protection.

**NFC Security Modes:**

| Mode | Security Level | Use Case |
|------|---------------|----------|
| Clear | None | Initial discovery only |
| Authenticated | Mutual authentication | Session establishment |
| Encrypted | AES-128-GCM | Programming commands |
| Signed | ECDSA-P256 | Critical therapy changes |

### 3.2 NFC Anti-Collision Security

Standard NFC anti-collision (ISO 14443-3) exchanges UIDs in clear, potentially
allowing device tracking. The iPACE-CHIP mitigates this with:

**Randomized UID Mode:**

During discovery, the implant generates a random 32-bit temporary identifier
instead of exposing its permanent UID. The permanent UID is only revealed after
mutual authentication.

```
Discovery Protocol:
  Reader → Implant: REQA
  Implant → Reader: ATQA (with random temporary ID)
  Reader → Implant: SELECT(temporary_id)
  Implant → Reader: SAK + encrypted permanent UID
```

### 3.3 NFC Secure Channel Protocol

The iPACE-CHIP implements an ISO 7816-4 compatible secure channel:

```
Phase 1: Mutual Authentication
  Reader → Implant: AUTH1(Reader_nonce || Reader_certificate)
  Implant → Reader: AUTH2(Implant_nonce || Implant_certificate || Sig)

Phase 2: Key Agreement
  shared_secret = ECDH_P256(Reader_priv, Implant_pub)
  session_key = HKDF-SHA256(shared_secret, nonce_R || nonce_I)

Phase 3: Secure Channel
  All subsequent commands encrypted with AES-128-GCM
  Sequence counter provides replay protection
  MAC tag length: 128 bits
```

### 3.4 NFC Relay Attack Mitigation

Relay attacks involve an adversary extending the NFC range by relaying
communication between a legitimate reader and the implant through a proxy.
The iPACE-CHIP counters relay attacks with:

**Distance Bounding Protocol:**

```
Step 1: Reader sends challenge C1 at time t1
Step 2: Implant immediately responds with C1 ⊕ C2 at time t2
Step 3: Reader sends C2 at time t3
Step 4: Reader verifies: (t2 - t1) + (t3 - t2) < max_propagation_delay
```

The maximum propagation delay is set to 50 ns (corresponding to ~15 meters),
ensuring the implant is within NFC range.

**Timing Verification:**

| Parameter | Value |
|-----------|-------|
| Maximum distance | 15 cm (verified to 50 ns precision) |
| Clock resolution | 10 ns |
| Jitter tolerance | ±5 ns |
| Challenge-response time | < 100 ns (hardware enforced) |

## 4. Bluetooth Low Energy (BLE) Security

### 4.1 BLE Security for Patient Controller

The patient controller communicates with the iPACE-CHIP via BLE for routine
monitoring and alerts. BLE security must balance usability (patient convenience)
with medical device security requirements.

**BLE Security Modes:**

| Mode | Level | Use Case |
|------|-------|----------|
| No security | SL1 | Never used |
| Unauthenticated pairing | SL2 | Never used |
| Authenticated pairing (LE Secure Connections) | SL4 | Patient controller |
| Authenticated pairing + encryption | SL4 | Therapy adjustment |

### 4.2 LE Secure Connections (LESC)

The iPACE-CHIP mandates LE Secure Connections (BLE 4.2+) using ECDH P-256
for pairing:

```
Pairing Process:
  1. Feature exchange (IO capabilities, security requirements)
  2. ECDH key exchange (P-256, LE Secure Connections)
  3. Authentication (Numeric Comparison or Passkey)
  4. Link key derivation (AES-CMAC based)
  5. Encryption start (AES-CCM)
```

**IO Capabilities:**

The iPACE-CHIP implant has no display or input, so it is configured as
"NoInput/NoOutput". The patient controller uses "DisplayOnly" to show a
6-digit numeric comparison code.

### 4.3 BLE Link Encryption

All BLE communication is encrypted using AES-CCM (Counter with CBC-MAC):

```
Encryption parameters:
  Algorithm: AES-128-CCM
  Key: 128-bit LE Secure Connections derived key
  Nonce: 13 bytes (packetCounter + direction + IV)
  MIC length: 4 bytes (minimum for BLE)
  AAD: MAC header (always authenticated)
```

### 4.4 BLE Privacy Features

**Resolvable Private Addresses (RPA):**

The iPACE-CHIP rotates its BLE address every 15 minutes using an identity
resolving key (IRK):

```
hash = ah(IRK, prand)
address = prand || hash (prand = random, hash = AES-128(IRK, prand) mod 2^24)
```

Authorized devices can resolve the address using the stored IRK, while
unauthorized scanners cannot track the device.

**Address Rotation Schedule:**

| Parameter | Value |
|-----------|-------|
| Rotation interval | 15 minutes |
| IRK refresh | Each pairing session |
| Advertising interval | 1-2 seconds (adaptive) |
| Scan window | 100 ms per 10 s |

## 5. Multi-Layer Encryption Architecture

### 5.1 Layered Encryption Design

The iPACE-CHIP implements defense-in-depth encryption across all wireless
interfaces:

```
┌─────────────────────────────────────────────┐
│ Layer 4: Application Encryption             │
│   AES-128-GCM over telemetry/command data   │
│   Key: session_key (derived per session)     │
├─────────────────────────────────────────────┤
│ Layer 3: Transport Encryption               │
│   AES-128-CCM over MICS/BLE frames          │
│   Key: link_key (derived during pairing)     │
├─────────────────────────────────────────────┤
│ Layer 2: Session Encryption                 │
│   AES-128-CTR over session establishment    │
│   Key: DH_shared_secret                      │
├─────────────────────────────────────────────┤
│ Layer 1: Link Encryption                    │
│   AES-128-CMAC for frame authentication     │
│   Key: device_paired_key                     │
└─────────────────────────────────────────────┘
```

### 5.2 Key Hierarchy for Wireless Security

```
Device Root Key (DRK) — stored in OTP
  ├── Link Key (per paired device) — stored in NVM
  │    ├── Session Key (per session) — volatile
  │    │    ├── Telemetry Key — volatile
  │    │    ├── Command Key — volatile
  │    │    └── Hop Key — volatile
  │    └── Frame Authentication Key — volatile
  └── Pairing Key (temporary, during pairing) — volatile
```

### 5.3 Nonce and Counter Management

**Global Frame Counter:**

A 48-bit global frame counter increments with each transmitted frame. The counter
is stored in protected NVM and updated atomically with the frame transmission.

```
Nonce construction:
  nonce = frame_counter (48 bits) || device_id (32 bits) || direction (1 bit)
```

**Replay Window:**

The receiver maintains a sliding window of 32 frame counters. Any frame with
a counter value within the window but already received is rejected. Frames with
counter values more than 32 positions ahead of the last received counter are
buffered for out-of-order delivery.

### 5.4 Session Freshness

Each communication session uses a fresh session key derived from:

```
session_nonce = implant_nonce (64 bits) || programmer_nonce (64 bits)
session_key = HKDF-SHA256(link_key, session_nonce, "iPACE session")
```

The session key is valid for a maximum of 1 hour or 2^20 messages, whichever
comes first.

## 6. Wireless Threat Model

### 6.1 Attack Scenarios

| Threat | Vector | Impact | Mitigation |
|--------|--------|--------|------------|
| Eavesdropping | Passive RF monitor | Data leakage | Encryption (all layers) |
| Replay | Record and resend | False telemetry | Frame counter + nonce |
| Injection | Active RF transmitter | Malicious commands | Authentication + MAC |
| Jamming | RF interference | Denial of service | Frequency hopping + error correction |
| Relay | NFC/BLE relay attack | Unauthorized programming | Distance bounding |
| Tracking | Device fingerprint | Patient privacy | RPA + encrypted device ID |
| Man-in-the-middle | Active interception | Key compromise | Authenticated key exchange |
| Desynchronization | State corruption | Communication failure | Session recovery protocol |

### 6.2 Adversary Capabilities

The iPACE-CHIP security architecture assumes the following adversary model:

- **Class A (Curious Bystant):** Passive eavesdropper within RF range. Can observe
  all wireless transmissions but cannot inject or modify.
- **Class B (Active Attacker):** Can inject, modify, and replay RF signals. Has
  knowledge of the protocol but not the keys.
- **Class C (Compromised Device):** Has obtained a legitimate paired device but
  does not have physical access to the implant.
- **Class D (Insider Threat):** Has access to one programmer device and its keys
  but cannot extract the implant's root key.

### 6.3 Security Properties by Threat Class

| Property | Class A | Class B | Class C | Class D |
|----------|---------|---------|---------|---------|
| Confidentiality | ✓ | ✓ | ✓ | Partial |
| Integrity | ✓ | ✓ | ✓ | ✓ |
| Authentication | ✓ | ✓ | ✓ | ✓ |
| Replay protection | ✓ | ✓ | ✓ | ✓ |
| Forward secrecy | ✓ | ✓ | ✓ | ✗ |
| Patient privacy | ✓ | ✓ | ✗ | ✗ |

## 7. Channel Security Testing

### 7.1 RF Security Assessment

**Eavesdropping Tests:**

- Measure signal reception at distances from 1 cm to 100 m
- Verify encryption prevents plaintext recovery at all distances
- Confirm device ID encryption prevents tracking at > 1 m

**Injection Tests:**

- Attempt to inject malformed frames without valid MAC
- Verify frame counter rejection for replayed frames
- Test authentication bypass attempts

**Jamming Resilience:**

- Measure throughput degradation under narrowband jamming
- Verify frequency hopping recovery after jammer activation
- Confirm graceful degradation (safe mode) under sustained jamming

### 7.2 Protocol Verification

**Formal Analysis:**

The wireless security protocols are formally verified using the Tamarin prover:

```
Security goals:
  - Authentication: programmer ↔ implant
  - Confidentiality: session data
  - Forward secrecy: past sessions
  - Replay protection: frame counter
  - Distance bounding: NFC range
```

**Fuzzing:**

- Protocol state machine fuzzing with 10^6 random input sequences
- Frame format fuzzing with malformed headers, truncated payloads
- Timing fuzzing with accelerated frame delivery

### 7.3 Interoperability Testing

All security features are tested against:

- 5 different programmer models from 3 manufacturers
- Various RF environments (hospital, home, outdoor)
- Concurrent sessions (multiple implants in proximity)
- Battery voltage variations (1.8V to 3.6V)

## 8. Regulatory Compliance

### 8.1 MICS Compliance

- FCC Part 95, Subpart I (Medical Implant Communications)
- RSS-210 (Industry Canada, MICS band)
- EN 301 489-23 (EU MICS EMI)
- ARIB STD-T66 (Japan MICS)

### 8.2 BLE Compliance

- Bluetooth Core Specification 5.3+
- LE Secure Connections mandatory
- Privacy features (RPA) required
- GATT Security Level 4 for medical services

### 8.3 Medical Device Wireless Standards

- IEC 62443-4-2 SL3 (wireless component security)
- IEC 80001-1 (risk management of wireless in medical devices)
- ANSI/AAMI TIR69:2017 (risk management of RF wireless in medical devices)
- FDA guidance on wireless medical device design

## 9. Summary

The iPACE-CHIP wireless security architecture provides defense-in-depth
protection across all three communication interfaces (NFC, MICS, BLE).
Multi-layer encryption ensures that compromise of any single key does not
expose all communication. Cryptographically secure frequency hopping in the
MICS band prevents eavesdropping and jamming. NFC relay attacks are mitigated
through distance bounding protocols. BLE privacy features protect patient
identity through regular address rotation. The comprehensive threat model
addresses adversary capabilities from passive eavesdropping to active protocol
manipulation, with formal verification confirming security properties.
