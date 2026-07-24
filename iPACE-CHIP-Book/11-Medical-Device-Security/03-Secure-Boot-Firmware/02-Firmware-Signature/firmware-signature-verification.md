# Firmware Signature Verification for iPACE-CHIP

## Overview

Firmware signature verification ensures that only authentic, unmodified firmware
runs on the iPACE-CHIP implantable pacemaker. A compromised firmware image could
alter therapy parameters, disable safety features, or exfiltrate patient data.
Digital signatures provide cryptographic proof that firmware was created by the
authorized manufacturer and has not been tampered with since creation. This chapter
covers the signature scheme, verification process, and the complete firmware
authentication infrastructure.

## 1. Firmware Signature Architecture

### 1.1 Signature Scheme Selection

The iPACE-CHIP uses ECDSA with SHA-384 (ECDSA-P384) for firmware signing:

| Criterion | ECDSA-P384 | RSA-2048 | Ed25519 |
|-----------|-----------|---------|---------|
| Security level | 192 bits | 112 bits | 128 bits |
| Signature size | 96 bytes | 256 bytes | 64 bytes |
| Public key size | 96 bytes | 256 bytes | 32 bytes |
| Verification time | 95 ms | 12 ms | 18 ms |
| Verification energy | 1.71 mJ | 0.22 mJ | 0.32 mJ |
| Quantum resistance | 96 bits | 56 bits | 64 bits |

ECDSA-P384 provides the highest security margin (192-bit classical, 96-bit
quantum) with acceptable verification overhead. The 96-bit quantum security
margin is critical for firmware that must remain valid for the device's 10-15
year lifetime.

### 1.2 Trust Chain for Firmware

```
Manufacturer Root CA (offline, ECDSA-P521)
  │
  └── Firmware Signing CA (ECDSA-P384)
        │
        ├── Firmware Release Key v1 (ECDSA-P384)
        ├── Firmware Release Key v2 (ECDSA-P384)
        └── Emergency Patch Key (ECDSA-P384)
```

### 1.3 Signing Infrastructure

```
┌─────────────────────────────────────────────────────────────┐
│              Firmware Signing Infrastructure                 │
│                                                             │
│  ┌──────────────┐     ┌──────────────┐                     │
│  │ Build Server │────→│ Signing      │                     │
│  │ (compiles FW)│     │ HSM          │                     │
│  └──────────────┘     │ (Thales)     │                     │
│                       │              │                     │
│  Role:                │ - Key never  │                     │
│  - Source code        │   leaves HSM │                     │
│  - Build scripts      │ - M-of-N     │                     │
│  - Test results       │   approval   │                     │
│                       │ - Audit log  │                     │
│                       └──────┬───────┘                     │
│                              │                             │
│                       ┌──────┴───────┐                     │
│                       │ Signed FW    │                     │
│                       │ Image        │                     │
│                       │ (.ispg)      │                     │
│                       └──────────────┘                     │
└─────────────────────────────────────────────────────────────┘
```

## 2. Firmware Image Format

### 2.1 Image Structure

```
iPACE-CHIP Firmware Image Format (.ispg):

┌──────────────────────────────────────────────┐
│ Header (256 bytes)                           │
│   Magic: "iPACE" (4 bytes)                  │
│   Version: Major.Minor.Patch (4 bytes)      │
│   Image Size: bytes (4 bytes)               │
│   Header Size: bytes (2 bytes)              │
│   Number of Segments: (2 bytes)             │
│   Hash Algorithm: SHA-384 (2 bytes)         │
│   Signature Algorithm: ECDSA-P384 (2 bytes) │
│   Flags: (4 bytes)                          │
│   Timestamp: Unix UTC (8 bytes)             │
│   Build ID: 16 bytes                        │
│   Target Hardware: 4 bytes                  │
│   Reserved: 48 bytes                        │
├──────────────────────────────────────────────┤
│ Signature Block (192 bytes)                  │
│   Image Hash: SHA-384 (48 bytes)            │
│   Signature: ECDSA-P384 (96 bytes)          │
│   Signer Certificate: ECDSA-P384 (96 bytes) │
├──────────────────────────────────────────────┤
│ Segment 0 (variable)                        │
│   Segment Header (32 bytes)                 │
│     Load Address: 4 bytes                   │
│     Segment Size: 4 bytes                   │
│     Segment Hash: SHA-256 (32 bytes)        │
│   Segment Data: variable                    │
├──────────────────────────────────────────────┤
│ Segment 1 (variable)                        │
│   ...                                       │
├──────────────────────────────────────────────┤
│ ...                                         │
├──────────────────────────────────────────────┤
│ Merkle Tree (variable)                      │
│   Root Hash: 48 bytes (SHA-384)             │
│   Tree Nodes: variable                      │
└──────────────────────────────────────────────┘
```

### 2.2 Header Fields Detail

| Field | Offset | Size | Description |
|-------|--------|------|-------------|
| Magic | 0x00 | 4 B | "iPACE" (0x6950414345) |
| Version | 0x04 | 4 B | Major.Minor.Patch (16.16.16 bits) |
| Image Size | 0x08 | 4 B | Total image size in bytes |
| Header Size | 0x0C | 2 B | Header + signature block size |
| Num Segments | 0x0E | 2 B | Number of code/data segments |
| Hash Algo | 0x10 | 2 B | 0x01=SHA-384, 0x02=SHA-256 |
| Sig Algo | 0x12 | 2 B | 0x01=ECDSA-P384, 0x02=ECDSA-P256 |
| Flags | 0x14 | 4 B | Compression, encryption flags |
| Timestamp | 0x18 | 8 B | Build timestamp (UTC) |
| Build ID | 0x20 | 16 B | Unique build identifier |
| Target HW | 0x30 | 4 B | Hardware revision compatibility |
| Reserved | 0x34 | 48 B | Future use, must be zero |

### 2.3 Segment Structure

Each firmware segment contains:

```
Segment Header (32 bytes):
  Load Address: 4 bytes (where to load in memory)
  Segment Size: 4 bytes (size of segment data)
  Segment Hash: 32 bytes (SHA-256 of segment data)

Segment Data:
  Code or data to be loaded at Load Address
  Padded to 4-byte alignment

Maximum Segments: 64
Maximum Segment Size: 64 KB
Total Image Size Limit: 2 MB
```

### 2.4 Compression Support

The iPACE-CHIP supports LZ4 compression for firmware images:

```
Compression Flags (in header):
  bit 0: compressed (1=yes, 0=no)
  bit 1: compression algorithm (0=LZ4, 1=reserved)

Decompression:
  - Performed during firmware update, not during boot
  - Decompressed image written to flash
  - Verification performed on decompressed image
  - Decompression buffer: 64 KB (temporary NVM)
```

## 3. Signature Generation Process

### 3.1 Build and Sign Workflow

```
Firmware Release Process:

Step 1: Source Compilation
  - Compile C/Assembly source for ARM Cortex-M4
  - Link with hardware-specific addresses
  - Generate ELF binary

Step 2: Image Assembly
  - Extract code and data sections
  - Organize into segments
  - Generate segment headers with hashes
  - Calculate total image size

Step 3: Image Hashing
  - Compute SHA-384 over (Header + all Segments)
  - Exclude signature block (not yet generated)
  - Store hash in signature block

Step 4: Signing (in HSM)
  - HSM loads signing key (never exposed)
  - Verify image hash matches HSM computation
  - Generate ECDSA-P384 signature
  - Output: signature + signer certificate

Step 5: Package
  - Assemble complete .ispg image
  - Generate Merkle tree for segments
  - Run validation tests on complete image
  - Distribute to update servers
```

### 3.2 Multi-Person Signing Policy

Firmware signing requires M-of-N approval:

```
Signing Quorum:
  M = 3 (minimum signers required)
  N = 5 (total authorized signers)
  Roles: Lead Engineer, Security Lead, Quality Lead,
         Medical Officer, Release Manager

Process:
  1. Build server generates firmware image (unsigned)
  2. Each authorized signer reviews and approves
  3. Each approval is recorded (timestamped, signed)
  4. When M approvals collected: proceed to signing
  5. HSM generates signature (requires M PIN codes)
  6. Signed image released to update infrastructure
```

### 3.3 Emergency Patch Signing

For critical security patches, an expedited process exists:

```
Emergency Patch Process:
  1. Security team identifies critical vulnerability
  2. Patch developed and tested (abbreviated timeline)
  3. Emergency Patch Key used (separate from release key)
  4. M = 2 (reduced quorum for emergency)
  5. Signed image deployed within 24 hours
  6. Full review and re-signing with release key within 7 days
```

## 4. Signature Verification Process

### 4.1 Boot-Time Verification

The iPACE-CHIP verifies firmware signatures during the secure boot sequence:

```
Verification Steps:

Step 1: Read Image Header (256 bytes from flash)
  - Validate magic bytes ("iPACE")
  - Parse version, size, segment count
  - Check hardware compatibility

Step 2: Verify Image Hash (SHA-384)
  - Compute SHA-384 over Header + all Segments
  - Compare with stored hash in signature block
  - If mismatch: REJECT image, enter safe mode

Step 3: Verify ECDSA-P384 Signature
  - Extract signer's certificate from signature block
  - Verify certificate chain to manufacturer root CA
  - Extract public key from certificate
  - Verify ECDSA-SHA384 signature over image hash
  - If verification fails: REJECT image, enter safe mode

Step 4: Verify Anti-Rollback
  - Extract firmware version from header
  - Compare with anti-rollback counter in OTP
  - If version < counter: REJECT, enter safe mode

Step 5: Verify Segments (Merkle Tree)
  - For each segment:
    - Compute SHA-256 of segment data
    - Compare with hash in segment header
    - If mismatch: REJECT segment, enter safe mode
  - Verify Merkle root matches expected value
```

### 4.2 Verification Timing

| Step | Operation | Time | Energy |
|------|-----------|------|--------|
| Header read | Flash read (256 B) | 0.05 ms | 0.9 μJ |
| Image hash | SHA-384 (256 KB) | 12 ms | 216 μJ |
| Certificate parse | DER parse | 0.8 ms | 14.4 μJ |
| Certificate verify | Chain verification | 189 ms | 3.4 mJ |
| Signature verify | ECDSA-P384 | 95 ms | 1.71 mJ |
| Anti-rollback | OTP read + compare | 0.01 ms | 0.2 μJ |
| Segment verify | SHA-256 (256 KB) | 16 ms | 288 μJ |
| **Total** | — | **313 ms** | **5.64 mJ** |

### 4.3 Verification Error Handling

| Error | Response | Recovery |
|-------|----------|----------|
| Invalid magic | Halt boot | N/A (corrupt flash) |
| Image hash mismatch | Reject, safe mode | Re-flash firmware |
| Signature invalid | Reject, safe mode | Re-flash firmware |
| Certificate invalid | Reject, safe mode | Re-flash firmware |
| Version below counter | Reject, safe mode | Cannot downgrade |
| Segment hash mismatch | Reject, safe mode | Re-flash firmware |
| Flash read error | Retry 3×, then safe mode | Hardware check |

## 5. Code Signing Infrastructure

### 5.1 Hardware Security Module (HSM)

The firmware signing key is stored in a Thales Luna Network HSM:

```
HSM Configuration:
  Model: Thales Luna Network HSM 7
  Key Storage: FIPS 140-3 Level 3
  Key Type: ECDSA-P384
  Key Label: "iPACE-FW-SIGN-v1"
  Key Export: Non-exportable
  Access: M-of-N quorum (3-of-5)
  Audit: All operations logged

HSM Network:
  ┌──────────────┐     ┌──────────────┐
  │ Build Server │────→│ HSM Appliance│
  │ (signing     │     │ (in secure   │
  │  request)    │     │  data center)│
  └──────────────┘     └──────────────┘

  - HSM not accessible from internet
  - VPN-only access from build network
  - Physical access requires 2-person rule
```

### 5.2 Key Hierarchy

```
Manufacturer Root CA (ECDSA-P521)
  Location: Offline air-gapped system
  Usage: Sign Firmware Signing CA certificate
  Access: 4-of-6 quorum, physical presence required

Firmware Signing CA (ECDSA-P384)
  Location: HSM in secure data center
  Usage: Sign firmware release certificates
  Access: Automatic (certificate pre-signed)

Firmware Release Keys (ECDSA-P384)
  Location: HSM in secure data center
  Usage: Sign firmware images
  Access: 3-of-5 quorum, logged
  Rotation: Every 12 months or per key compromise
```

### 5.3 Key Rotation Procedure

```
Key Rotation Process:

Pre-Rotation (30 days before):
  1. Generate new ECDSA-P384 key pair in HSM
  2. Create new certificate (signed by Firmware Signing CA)
  3. Distribute new public key to all iPACE-CHIP devices
     (via existing update mechanism)

Rotation Day:
  1. Disable old signing key (HSM policy)
  2. Sign first firmware with new key
  3. Verify new key works on test devices
  4. Monitor for issues

Post-Rotation (30 days):
  1. Keep old key for emergency patch signing only
  2. After 30 days: old key permanently disabled
  3. After 90 days: old key destroyed in HSM
```

## 6. Secure Boot Verification Details

### 6.1 Multi-Stage Verification

```
Stage 1: Boot ROM → SBL
  Method: SHA-256 hash comparison + ECDSA-P384 signature
  Hash: Hardcoded in Boot ROM (256 bits)
  Key: Manufacturer public key (derived from DRK)
  Result: SBL verified as authentic

Stage 2: SBL → ABL
  Method: SHA-256 hash + ECDSA-P384 signature
  Hash: Stored in SBL-protected flash region
  Key: Manufacturer public key (from SBL)
  Result: ABL verified as authentic

Stage 3: ABL → Application
  Method: Full ECDSA-P384 image verification + Merkle tree
  Hash: Computed over entire image
  Key: Manufacturer public key (from ABL)
  Result: Application verified as authentic

Each stage's verification key is derived from the previous stage,
creating an unbroken chain of trust from hardware to application.
```

### 6.2 Dual-Bank Verification

The iPACE-CHIP uses dual-bank flash for safe firmware updates:

```
Dual-Bank Flash Layout:
  ┌──────────────────────────────────┐
  │ Bank A (512 KB)                  │
  │   - Current firmware             │
  │   - Verified and running         │
  ├──────────────────────────────────┤
  │ Bank B (512 KB)                  │
  │   - New firmware (during update) │
  │   - Verified before activation   │
  └──────────────────────────────────┘

Update Process:
  1. Download new firmware to inactive bank
  2. Verify signature of new firmware (ECDSA-P384)
  3. Verify all segment hashes
  4. Verify Merkle tree
  5. Test new firmware (boot to test mode)
  6. If test passes: activate new bank
  7. If test fails: revert to old bank
  8. Old bank preserved for rollback (until next update)
```

### 6.3 Partial Update Verification

The Merkle tree enables verification of individual firmware segments:

```
Partial Update:
  1. Determine which segments changed (diff analysis)
  2. Transmit only changed segments
  3. Verify changed segments against Merkle tree
  4. Update only changed segments in flash
  5. Re-verify Merkle root (unchanged)

  Benefit: Reduces update size and time
  Security: Merkle tree ensures all segments verified
  Applicability: Used for minor version updates
```

## 7. Firmware Anti-Tampering

### 7.1 Runtime Integrity Verification

After boot, the firmware periodically verifies its own integrity:

```
Runtime Integrity Check:
  Interval: Every 60 seconds
  Method: SHA-256 of critical code regions
  Regions:
    - Interrupt vector table: 1 KB
    - Critical handlers: 8 KB
    - Crypto functions: 16 KB
    - Safety monitor: 4 KB

  If check fails:
    1. Log integrity failure (signed, tamper-evident)
    2. Halt normal operations
    3. Enter safe mode (minimal therapy only)
    4. Alert clinician
```

### 7.2 Debug Interface Protection

```
Debug Protection:
  JTAG/SWD: Disabled in production
  Lock mechanism: One-time fuse blow
  Recovery: Impossible (by design)
  Verification: Read-lock status register at boot

  Production test: Debug enabled during manufacturing only
  After final test: Debug fuse blown permanently
```

### 7.3 Fault Injection Resistance

The verification process is hardened against fault injection:

```
Countermeasures:
  1. Double verification: Verify signature twice, compare results
  2. Redundant hash computation: Compute hash twice with different algorithms
  3. Checksum comparison: Compare signature check results
  4. Timing verification: Ensure verification completes in expected window
  5. Voltage monitoring: Detect glitch attempts during verification

  If fault detected:
    → Immediate zeroization of all keys
    → Enter safe mode
    → Log fault event
```

## 8. Update Infrastructure

### 8.1 Update Distribution

```
Distribution Architecture:
  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
  │ Build Server │────→│ Update       │────→│ CDN          │
  │ (signs FW)   │     │ Repository   │     │ (distribution│
  └──────────────┘     │ (encrypted)  │     │  servers)    │
                       └──────────────┘     └──────┬───────┘
                                                   │
                              ┌─────────────────────┤
                              │                     │
                       ┌──────┴───────┐     ┌──────┴───────┐
                       │ Programmer   │     │ Patient      │
                       │ (clinical)   │     │ Controller   │
                       └──────┬───────┘     └──────┬───────┘
                              │                     │
                              └──────────┬──────────┘
                                         │
                                   ┌─────┴─────┐
                                   │  Implant   │
                                   │  iPACE-CHIP│
                                   └────────────┘
```

### 8.2 Update Protocol

```
Secure Update Protocol:

Step 1: Notification
  Server → Programmer: UpdateAvailable{version, size, hash, signature}
  Programmer verifies: Server certificate chain
  Programmer verifies: Update signature

Step 2: Download
  Programmer → Server: RequestUpdate{current_version, device_id}
  Server → Programmer: FirmwareImage{encrypted with device-specific key}

Step 3: Pre-Installation
  Programmer:
    1. Verify firmware image signature (ECDSA-P384)
    2. Verify all segment hashes
    3. Verify version > current_version
    4. Verify target hardware compatibility

Step 4: Installation (via NFC or MICS)
  Programmer → Implant: UpdateStart{image_size, num_segments}
  For each segment:
    Programmer → Implant: SegmentData{index, data, hash}
    Implant: Verify segment hash
    Implant: Write to inactive flash bank
  Programmer → Implant: UpdateComplete{image_hash}

Step 5: Verification
  Implant:
    1. Verify full image signature (ECDSA-P384)
    2. Verify Merkle tree
    3. Boot test (in sandbox mode)
    4. If pass: activate new firmware
    5. If fail: revert to previous version

Step 6: Confirmation
  Implant → Programmer: UpdateResult{status, new_version}
  Programmer logs completion
```

### 8.3 Rollback Protection

| Mechanism | Protection | Scope |
|-----------|-----------|-------|
| Anti-rollback counter | Prevents firmware downgrade | OTP (hardware) |
| Version comparison | Rejects older versions | Software (boot loader) |
| Certificate expiry | Limits firmware validity | 15-year certificate |
| Key rotation | Old keys disabled | Newer key only |

## 9. Emergency Firmware Recovery

### 9.1 Recovery Scenarios

| Scenario | Recovery Method | Time |
|----------|----------------|------|
| Failed update | Auto-revert to previous bank | 2 seconds |
| Corrupt firmware | Load from recovery partition | 5 seconds |
| Complete corruption | NFC-based recovery from programmer | 5 minutes |
| Boot loader corruption | Hardware recovery mode (JTAG) | N/A (manufacturing only) |

### 9.2 Recovery Partition

```
Recovery Partition (64 KB):
  Location: Last 64 KB of flash
  Contents: Minimal boot loader + recovery firmware
  Protection: Write-locked after manufacturing
  Signature: Same as main firmware (ECDSA-P384)
  Access: Only on main firmware failure

Recovery Boot Sequence:
  1. Main firmware boot fails (3 attempts)
  2. Boot loader switches to recovery partition
  3. Verify recovery firmware signature
  4. Boot recovery firmware
  5. Recovery firmware: enable NFC programming mode
  6. Patient/clinician: flash new firmware via NFC
```

## 10. Compliance and Certification

### 10.1 Regulatory Requirements

| Standard | Firmware Security Requirement | iPACE-CHIP Compliance |
|----------|-------------------------------|----------------------|
| IEC 62304 | Software update verification | Compliant (ECDSA-P384) |
| IEC 81001-5-1 | Secure update mechanism | Compliant |
| FDA Cybersecurity | Code signing, integrity verification | Compliant |
| UL 2900-1 | Anti-tampering, code authentication | Level 3 |

### 10.2 Testing Requirements

| Test Type | Scope | Frequency |
|-----------|-------|-----------|
| Signature verification | All firmware releases | Per release |
| Rollback protection | Anti-rollback counter | Per release |
| Dual-bank failover | Bank switching | Per release |
| Recovery partition | Recovery boot | Per release |
| Fault injection | Verification process | Annual |
| Penetration testing | Full update process | Annual |

## 11. Summary

Firmware signature verification using ECDSA-P384 provides the cryptographic
assurance that only authentic, manufacturer-approved firmware runs on the
iPACE-CHIP implantable pacemaker. The multi-stage verification chain extends
trust from the immutable Boot ROM through each firmware layer. Anti-rollback
protection prevents downgrade to older, potentially vulnerable versions. The
dual-bank flash architecture enables safe updates with automatic rollback on
failure. A hardware security module protects the signing key with M-of-N
quorum control. The complete infrastructure, from build to distribution to
installation, maintains end-to-end integrity verification ensuring patient
safety throughout the device's lifetime.
