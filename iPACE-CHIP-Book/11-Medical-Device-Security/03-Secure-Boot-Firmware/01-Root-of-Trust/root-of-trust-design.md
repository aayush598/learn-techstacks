# Root of Trust Design for iPACE-CHIP

## Overview

The root of trust (RoT) is the foundational security anchor from which all other
security mechanisms in the iPACE-CHIP derive their trust. A compromised root of
trust invalidates the entire security architecture, making it the most critical
component to protect. This chapter describes the hardware and software design of
the iPACE-CHIP root of trust, covering immutable boot code, secure key storage,
hardware attestation, and the chain of trust that extends to the entire system.

## 1. Root of Trust Architecture

### 1.1 Trust Model

The iPACE-CHIP root of trust is based on the following principles:

- **Immutable foundation:** The root of trust code and data cannot be modified
  after manufacturing
- **Minimal attack surface:** The RoT contains only the minimum code necessary
  to establish trust
- **Verifiability:** The RoT can prove its integrity through hardware attestation
- **Isolation:** The RoT is isolated from the application processor through
  hardware boundaries

### 1.2 Root of Trust Components

```
┌───────────────────────────────────────────────────────────────┐
│                    Root of Trust (RoT)                         │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │ Immutable    │  │ Hardware     │  │ Device       │       │
│  │ Boot ROM     │  │ RNG/PRNG     │  │ Identity     │       │
│  │ (2 KB)       │  │              │  │ (UDI+Keys)   │       │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘       │
│         │                 │                 │                │
│  ┌──────┴─────────────────┴─────────────────┴───────┐       │
│  │              Secure Boot Controller               │       │
│  │  - Hash comparison engine                         │       │
│  │  - Signature verification accelerator             │       │
│  │  - Anti-rollback counter                          │       │
│  └──────────────────────┬───────────────────────────┘       │
│                         │                                    │
│  ┌──────────────────────┴───────────────────────────┐       │
│  │              Key Management Unit (KMU)            │       │
│  │  - Device Root Key (OTP)                          │       │
│  │  - Attestation Key (derived)                      │       │
│  │  - Tamper Response                                │       │
│  └──────────────────────────────────────────────────┘       │
└───────────────────────────────────────────────────────────────┘
```

## 2. Immutable Boot ROM

### 2.1 Boot ROM Design

The Boot ROM is a 2 KB mask-programmed read-only memory fabricated during
chip manufacturing. It is physically impossible to modify after fabrication.

**Boot ROM Contents:**

| Offset | Size | Content |
|--------|------|---------|
| 0x0000 | 256 B | Reset vector and initialization code |
| 0x0100 | 512 B | Hardware self-test (POST) |
| 0x0300 | 256 B | Secure boot controller initialization |
| 0x0400 | 512 B | First-stage bootloader verification |
| 0x0600 | 256 B | Key derivation (DRK → verification key) |
| 0x0700 | 128 B | Device identity loading |
| 0x0780 | 128 B | Anti-rollback counter initialization |
| 0x0800 | — | Reserved |

### 2.2 Boot Sequence

```
Power-On Reset → Boot ROM Execution:

Step 1: Hardware Initialization (50 μs)
  - Initialize clock oscillator
  - Configure memory controller
  - Enable tamper monitoring
  - Start watchdog timer

Step 2: Power-On Self-Test (POST) (2 ms)
  - SRAM test (March C algorithm)
  - Flash integrity test (CRC-32)
  - Crypto accelerator test (AES known-answer)
  - TRNG health check (NIST SP 800-90B)
  - KMU zeroization verification
  - If any test fails: halt and enter safe mode

Step 3: Secure Boot Controller Init (100 μs)
  - Load verification key from OTP (DRK → SHA-256("verify") → verify_key)
  - Initialize anti-rollback counter
  - Configure hash comparison engine

Step 4: First-Stage Bootloader Verification (500 μs)
  - Read SBL header from protected flash
  - Extract hash and signature
  - Verify: SHA-256(SBL_code) == hash_in_header
  - Verify: ECDSA-verify(Manufacturer_Public, hash, signature)
  - Verify: SBL_version > anti_rollback_counter
  - If verification fails: halt and enter safe mode

Step 5: Transfer Control (10 μs)
  - Zeroize verification key from registers
  - Jump to SBL entry point
  - Boot ROM execution complete
```

### 2.3 Boot ROM Security Properties

| Property | Implementation |
|----------|---------------|
| Immutability | Mask ROM, cannot be reprogrammed |
| Tamper resistance | Physical shielding, active mesh |
| Minimalism | Only essential boot code (2 KB) |
| Self-test | POST validates all security hardware |
| Verification | Cryptographic hash + signature check |
| Anti-rollback | Hardware monotonic counter |

## 3. Hardware Security Modules

### 3.1 True Random Number Generator (TRNG)

The TRNG provides the entropy foundation for all cryptographic operations:

```
TRNG Architecture:
  ┌─────────────────────────────────────────────────┐
  │  Entropy Source: Ring Oscillator (RO) Array      │
  │  ├── 3 independent RO chains (jitter-based)     │
  │  ├── Raw entropy rate: ~50 Mbps                  │
  │  └── Health monitoring: continuous               │
  │                                                   │
  │  Conditioning: SHA-256-based conditioner          │
  │  ├── Input: 512-bit raw entropy blocks            │
  │  ├── Output: 256-bit conditioned entropy          │
  │  └── Backtracking resistance: 256-bit security    │
  │                                                   │
  │  NIST Compliance: SP 800-90B                      │
  │  ├── Min-entropy: ≥ 0.9 bits/bit                 │
  │  ├── Repetition count test: active                │
  │  ├── Adaptive proportion test: active             │
  │  └── Online health tests: every 1024 bits         │
  └─────────────────────────────────────────────────┘
```

**TRNG Output Rate:**

| Mode | Rate | Latency |
|------|------|---------|
| Continuous (background) | 1 Mbps | Zero (background) |
| Burst | 10 Mbps | 10 μs startup |
| Low-power | 100 kbps | 10 μs startup |

### 3.2 Key Management Unit (KMU)

The KMU provides hardware-protected key storage:

**KMU Architecture:**

```
┌─────────────────────────────────────────────────────────┐
│                    Key Management Unit                    │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  OTP Key Bank (One-Time Programmable)                │ │
│  │  ├── Device Root Key (DRK): 256 bits                 │ │
│  │  ├── Manufacturing Hash: 256 bits                    │ │
│  │  ├── Device Unique ID: 128 bits                      │ │
│  │  └── Anti-Rollback Counter: 32 bits                  │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Volatile Key Registers (SRAM-backed)                │ │
│  │  ├── Session Key Slot 0: 128 bits                    │ │
│  │  ├── Session Key Slot 1: 128 bits                    │ │
│  │  ├── HMAC Key Slot: 128 bits                         │ │
│  │  ├── ECDH Private Key Slot: 256 bits                 │ │
│  │  └── Temp Key Slot: 256 bits                         │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Access Control Logic                                │ │
│  │  ├── OTP Bank: Read-only (all), Write (manufacturing only)│
│  │  ├── Volatile: CPU write (masked), Crypto read/write │ │
│  │  └── Debug: Disabled in production                    │ │
│  └─────────────────────────────────────────────────────┘ │
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  Tamper Response                                     │ │
│  │  ├── Voltage: < 1.6V → zeroize volatile keys        │ │
│  │  ├── Temperature: > 85°C → zeroize volatile keys    │ │
│  │  ├── Light: Photodiode detection → zeroize          │ │
│  │  ├── Physical: Mesh integrity → zeroize              │ │
│  │  └── Timing: Clock glitch → zeroize                  │ │
│  └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 3.3 Hardware Security Engine (HSE)

The HSE provides cryptographic acceleration with security guarantees:

| Feature | Specification |
|---------|--------------|
| AES-128/256 | ECB, CBC, CTR, GCM, CCM |
| SHA-256/384 | Hash, HMAC, CMAC |
| ECDSA | P-256, P-384 |
| ECDH | P-256, P-384 |
| True Random | NIST SP 800-90B compliant |
| Key Storage | 8 key slots (volatile) |
| Tamper | Voltage, temperature, physical |

## 4. Chain of Trust

### 4.1 Trust Chain Architecture

The iPACE-CHIP implements a hierarchical chain of trust:

```
Level 0: Hardware Root of Trust
  │  Source: Mask ROM + OTP keys
  │  Trust basis: Physics (cannot be modified)
  │  Capabilities: Verify, derive keys, attest identity
  │
  ├──→ Level 1: Secure Boot Loader (SBL)
  │      Source: Protected flash (signed by manufacturer)
  │      Trust basis: Verified by Level 0
  │      Capabilities: Verify Level 2, update Level 2
  │
  ├──→ Level 2: Application Boot Loader (ABL)
  │      Source: Protected flash (signed by manufacturer)
  │      Trust basis: Verified by Level 1
  │      Capabilities: Verify Level 3, manage firmware updates
  │
  └──→ Level 3: Application Firmware
         Source: Application flash (signed by manufacturer)
         Trust basis: Verified by Level 2
         Capabilities: Medical device operation
```

### 4.2 Trust Verification at Each Level

```
Verification Chain:

Level 0 (Boot ROM):
  Self-verification: POST tests validate hardware integrity
  Key derivation: DRK → verify_key = HKDF(DRK, "verify")
  Identity: Device_ID loaded from OTP

Level 1 (SBL):
  Stored hash: SHA-256(SBL_code) in Level 0 code (hardcoded)
  Signature: ECDSA-verify(Manufacturer_pubkey, hash, signature)
  Version: SBL_version > Anti-rollback_counter (stored in OTP)
  Hash location: Embedded in SBL header at fixed offset

Level 2 (ABL):
  Stored hash: SHA-256(ABL_code) in SBL flash area
  Signature: ECDSA-verify(Manufacturer_pubkey, hash, signature)
  Version: ABL_version > stored_rollback_counter
  Hash location: SBL-protected flash sector

Level 3 (Application):
  Stored hash: Merkle tree root in ABL-protected flash
  Signature: ECDSA-verify(Manufacturer_pubkey, image_hash, signature)
  Version: FW_version > stored_rollback_counter
  Integrity: Full image signature + per-segment Merkle verification
```

### 4.3 Secure Boot Timing

| Level | Verification | Time | Energy |
|-------|-------------|------|--------|
| Level 0 (POST) | Hardware self-test | 2 ms | 36 μJ |
| Level 0 (Key derivation) | HKDF | 0.1 ms | 1.8 μJ |
| Level 1 (SBL verify) | SHA-256 + ECDSA | 1.2 ms | 21.6 μJ |
| Level 2 (ABL verify) | SHA-256 + ECDSA | 1.2 ms | 21.6 μJ |
| Level 3 (FW verify) | Merkle tree (1KB) | 3.8 ms | 68.4 μJ |
| **Total boot time** | — | **8.3 ms** | **149.4 μJ** |

## 5. Device Identity

### 5.1 Unique Device Identifier (UDI)

Each iPACE-CHIP has a globally unique device identifier:

```
UDI Structure (128 bits):
  [Manufacturer ID: 16 bits]
  [Product Code: 16 bits]
  [Serial Number: 64 bits]
  [Manufacturing Date: 16 bits]
  [Reserved: 16 bits]

  CRC-32: appended for error detection (not security)
```

The UDI is burned into OTP memory during manufacturing and is read-only
after fabrication. It serves as the device's identity throughout its lifetime.

### 5.2 Device Certificate

The iPACE-CHIP device certificate binds the device identity to its
cryptographic keys:

```
Certificate Structure (DER-encoded X.509 v3):
  Version: 3
  Serial Number: UDI (128 bits)
  Signature Algorithm: ECDSA-SHA256
  Issuer: iPACE-CHIP Manufacturer CA
  Validity:
    Not Before: Manufacturing date
    Not After: Manufacturing date + 15 years
  Subject: iPACE-CHIP UDI:XX-XXXX-XXXX-XXXX
  Subject Public Key Info:
    Algorithm: ECDSA P-256
    Public Key: 64 bytes (uncompressed point)
  Extensions:
    Key Usage: digitalSignature, keyAgreement
    Extended Key Usage: anyExtendedKeyUsage
    Subject Key Identifier: SHA-1(Public Key)
    Medical Device Identifier: UDI (OID: 2.16.840.1.113883.3.xxx)
```

### 5.3 Certificate Storage

| Location | Content | Protection |
|----------|---------|-----------|
| OTP | UDI | Read-only, tamper-resistant |
| Flash (read-only) | Device Certificate (DER) | Signed, integrity-protected |
| Flash (read-only) | Manufacturer CA Certificate | Signed, integrity-protected |

## 6. Hardware Attestation

### 6.1 Attestation Protocol

The iPACE-CHIP can prove its identity and state to a remote verifier:

```
Attestation Protocol:

Verifier → Implant:
  Challenge(nonce_V: 32 bytes)

Implant → Verifier:
  Attestation_Report {
    Nonce_V (echoed from verifier)
    Device_UDI (128 bits)
    Firmware_Version (32 bits)
    Security_State (8 bits):
      bit 0: tamper_detected
      bit 1: debug_enabled
      bit 2: keys_zeroized
      bit 3: safe_mode
    Boot_Counter (32 bits)
    Certificate (DER, variable)
    Signature: ECDSA-SHA256(d_attest, report_data)
  }

Verifier:
  1. Verify Certificate chain to manufacturer CA
  2. Verify Signature using Certificate public key
  3. Check Nonce_V matches challenge
  4. Validate Firmware_Version against known versions
  5. Check Security_State for anomalies
  6. Verify Boot_Counter > last_known_counter
```

### 6.2 Attestation Key

The attestation key is derived from the Device Root Key:

```
attest_key_context = "iPACE-CHIP attestation v1"
attest_priv_key = HKDF-SHA256(
  IKM = DRK,
  salt = UDI,
  info = attest_key_context
)[0:256]

attest_pub_key = ECDSA-ScalarMultiply(G, attest_priv_key)
```

The attestation private key never leaves the KMU. All signing operations
occur within the hardware security boundary.

### 6.3 Attestation Properties

| Property | Value |
|----------|-------|
| Freshness | Nonce-based, single-use challenges |
| Binding | Key derived from hardware-rooted DRK |
| Completeness | Report includes all security-relevant state |
| Unforgeability | ECDSA signature with hardware-protected key |
| Replay protection | Nonce prevents reuse |

## 7. Anti-Rollback Protection

### 7.1 Monotonic Counter

The iPACE-CHIP implements a hardware monotonic counter to prevent firmware
downgrade attacks:

```
Counter Storage:
  Location: OTP memory (one-time programmable)
  Width: 32 bits
  Maximum value: 2^32 - 1 (4,294,967,295)
  Increment: One-time programmable fuses

Counter Update Process:
  1. New firmware version available
  2. Verify new version > current counter value
  3. Program additional OTP fuses to represent new value
  4. Verify counter reads correctly
  5. If verification fails: device enters safe mode

  Note: Each increment permanently programs OTP fuses
        No way to decrement or reset the counter
```

### 7.2 Anti-Rollback Enforcement

```
Boot-Time Check:
  1. Read current firmware version from image header
  2. Read anti-rollback counter from OTP
  3. If FW_version < counter_value:
     → Reject firmware
     → Enter safe mode
     → Log rollback attempt
  4. If FW_version ≥ counter_value:
     → Accept firmware
     → If FW_version > counter_value:
        → Update counter (program additional OTP fuses)

  Counter Storage Efficiency:
    Each OTP fuse represents one version increment
    32 fuses = 32 firmware versions
    For 10-year device lifetime: ~3 versions/year average
```

### 7.3 Rollback Attack Prevention

| Attack | Countermeasure |
|--------|---------------|
| Firmware downgrade | Anti-rollback counter in OTP |
| SBL downgrade | SBL version in anti-rollback counter |
| ABL downgrade | ABL version in anti-rollback counter |
| Config downgrade | Configuration version counter (NVM) |
| Key downgrade | Key version in certificate extension |

## 8. Boot Security Analysis

### 8.1 Threat Analysis

| Threat | Attack Vector | Countermeasure |
|--------|--------------|----------------|
| Boot ROM modification | Physical chip alteration | Mask ROM, active mesh |
| Key extraction | Side-channel analysis | Constant-time, masking |
| Firmware substitution | Flash manipulation | ECDSA signature verification |
| Rollback attack | Firmware downgrade | Hardware monotonic counter |
| Boot-time DoS | Interrupted boot | Watchdog timer, timeout |
| Post-boot compromise | Runtime attack | Runtime integrity monitoring |

### 8.2 Boot ROM Protection

The Boot ROM is protected through multiple physical mechanisms:

**Active Shield Mesh:**

```
┌─────────────────────────────────────────┐
│  ┌─── Active Metal Mesh ───────────┐   │
│  │  ┌─────────────────────────────┐ │   │
│  │  │                             │ │   │
│  │  │      Boot ROM Core          │ │   │
│  │  │                             │ │   │
│  │  └─────────────────────────────┘ │   │
│  └──────────────────────────────────┘   │
│                                          │
│  Monitoring:                             │
│  - Mesh resistance: 100 Ω nominal       │
│  - Tamper threshold: ±20% deviation     │
│  - Response time: < 100 ns              │
│  - Action: Zeroize all keys, halt       │
└─────────────────────────────────────────┘
```

### 8.3 Fault Injection Resistance

| Fault Type | Detection Method | Response |
|-----------|-----------------|----------|
| Voltage glitch | Voltage supervisor (±5%) | Zeroize + halt |
| Clock glitch | Clock monitor (frequency) | Zeroize + halt |
| Laser fault | Light sensor array | Zeroize + halt |
| EM fault | EM field sensor | Zeroize + halt |
| Temperature fault | Thermal sensor | Safe mode |

## 9. Manufacturing Security

### 9.1 Secure Manufacturing Process

```
Manufacturing Flow:

Wafer Fabrication
  → Individual chip test
  → TRNG characterization
  → OTP programming:
      1. Generate DRK from TRNG
      2. Generate Device UDI
      3. Program Boot ROM (mask programming)
      4. Program anti-rollback counter = 0
      5. Program manufacturer certificate hash
  → Post-programming verification
  → Packaging
  → Final test

Secure Manufacturing Requirements:
  - Clean room with access control
  - All OTP programming logged and audited
  - TRNG characterization data recorded per device
  - DRK never exposed (generated and stored in-chip)
  - Manufacturing equipment tamper-evident
```

### 9.2 Key Generation at Manufacturing

```
DRK Generation:
  1. TRNG generates 512 bits of entropy
  2. Health test: verify entropy quality (NIST SP 800-90B)
  3. KDF: DRK = HKDF-SHA256(TRNG_entropy, salt=wafer_id, info="DRK")
  4. Program DRK into OTP (write-once)
  5. Verify OTP readback matches DRK
  6. Erase all intermediate values
  7. DRK never exposed to test equipment

  Security: DRK is known only to the chip itself
  The manufacturer stores only the UDI, not the DRK
```

### 9.3 Supply Chain Integrity

| Measure | Implementation |
|---------|---------------|
| Chip authentication | ECDSA attestation with DRK-derived key |
| Tamper-evident packaging | Physical seals, X-ray verification |
| Chain of custody | Logged at each manufacturing step |
| Clone detection | Unique DRK per device, verified by RoT |
| counterfeit prevention | UDI + attestation + certificate chain |

## 10. Runtime Integrity Monitoring

### 10.1 Periodic Integrity Checks

The iPACE-CHIP performs periodic integrity verification during operation:

```
Runtime Integrity:
  Check interval: Every 60 seconds
  Method: SHA-256 hash of critical code regions
  Regions monitored:
    - Boot ROM: 2 KB (fixed, known-good)
    - SBL: 16 KB (verified at boot)
    - ABL: 32 KB (verified at boot)
    - Critical application code: 64 KB

  If integrity check fails:
    1. Log integrity failure with timestamp
    2. If Boot ROM check fails: halt (hardware fault)
    3. If SBL/ABL check fails: reboot and re-verify
    4. If application check fails: reboot into safe mode
```

### 10.2 Watchdog Timer

The hardware watchdog timer ensures the system cannot be hung or disabled:

```
Watchdog Configuration:
  Timeout: 4 seconds
  Feed requirement: Write specific value to specific register
  Clock source: Independent 32 kHz oscillator
  Reset behavior: Full system reset → re-boot → re-verify

  If watchdog triggers:
    1. System reset
    2. Full secure boot sequence
    3. Integrity verification
    4. Resume or enter safe mode
```

## 11. Testing and Validation

### 11.1 Root of Trust Verification Tests

| Test | Method | Pass Criteria |
|------|--------|--------------|
| Boot ROM integrity | Checksum verification | SHA-256 matches expected |
| OTP key storage | Read-back verification | DRK reads correctly |
| Secure boot | Signature verification | All signatures valid |
| Anti-rollback | Version comparison | Version ≥ counter |
| TRNG quality | NIST SP 800-90B | All health tests pass |
| Tamper response | Fault injection test | Keys zeroized within 100 ns |

### 11.2 Penetration Testing

The root of trust undergoes independent penetration testing:

- Physical attacks: Decapsulation, microprobing, laser fault injection
- Side-channel attacks: Power analysis, EM emanation, timing analysis
- Fault injection attacks: Voltage glitching, clock manipulation
- Software attacks: Exploit boot vulnerabilities, firmware manipulation

### 11.3 Formal Verification

The secure boot controller's hash comparison logic has been formally verified:

```
Verified Properties:
  ✅ Hash comparison is correct for all inputs
  ✅ Verification cannot be bypassed
  ✅ Anti-rollback counter cannot be decremented
  ✅ Keys cannot be read through CPU interface
  ✅ Tamper response activates within 100 ns
```

## 12. Summary

The iPACE-CHIP root of trust provides a hardware-anchored security foundation
from which all other security mechanisms derive. The immutable Boot ROM ensures
that the initial code cannot be tampered with. The Key Management Unit protects
device secrets against both software and physical attacks. The chain of trust
extends from hardware through multiple firmware layers using cryptographic
verification. Hardware attestation proves device identity to remote verifiers.
Anti-rollback protection prevents firmware downgrade attacks. The comprehensive
design, validated through penetration testing and formal verification, ensures
that the iPACE-CHIP's security architecture rests on an unassailable foundation.
