# Session Key Management for iPACE-CHIP

## Overview

Session key management governs the lifecycle of cryptographic keys used during
active communication sessions between the iPACE-CHIP implantable pacemaker and
external devices. Proper key management is critical: a leaked session key
exposes all data encrypted under it, while a stale or improperly derived key
can cause authentication failures with life-threatening consequences. This
chapter covers key generation, distribution, storage, rotation, revocation,
and destruction.

## 1. Key Lifecycle Overview

### 1.1 Key States

Every key in the iPACE-CHIP system exists in one of six states:

```
┌─────────┐    ┌──────────┐    ┌─────────┐    ┌─────────┐
│ Created │───→│ Active   │───→│ Rotating│───→│ Expired │
└─────────┘    └──────────┘    └─────────┘    └─────────┘
                    │               │               │
                    │               │               ▼
                    ▼               ▼          ┌─────────┐
              ┌──────────┐  ┌──────────┐      │Destroyed│
              │ Suspended│  │ Comprom. │      └─────────┘
              └──────────┘  └──────────┘
```

### 1.2 Key Types and Roles

| Key Type | Purpose | Lifetime | Storage |
|----------|---------|----------|---------|
| Device Root Key (DRK) | Key derivation root | Device lifetime | OTP NVM |
| Pairing Key | Device pairing | Until re-pairing | Protected NVM |
| Session Key | Active session encryption | 1 hour max | Volatile (KMU) |
| Telemetry Key | Telemetry stream auth | 1 session | Volatile (KMU) |
| Command Key | Command authentication | 1 session | Volatile (KMU) |
| Hop Key | Frequency hop sequence | 1 session | Volatile (KMU) |
| Firmware Key | FW verification | Firmware version | Protected NVM |

## 2. Key Generation

### 2.1 True Random Number Generator (TRNG)

All cryptographic key material is generated from the iPACE-CHIP's hardware TRNG:

**TRNG Architecture:**

```
┌──────────────────────────────────────────────────┐
│                 TRNG Subsystem                    │
│                                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐    │
│  │ Ring     │   │ Von Neumann│   │ Health   │    │
│  │ Oscillator│→ │ Debiaser  │→ │ Monitor  │    │
│  │ (RO)     │   │           │   │          │    │
│  └──────────┘   └──────────┘   └──────────┘    │
│       │              │              │            │
│  Entropy Source   Conditioning   Quality Check  │
│  (~50 Mbps raw)   (Whitening)   (NIST SP800-90B)│
│       │              │              │            │
│       └──────────────┼──────────────┘            │
│                      ▼                           │
│              ┌──────────────┐                    │
│              │  TRNG Output │                    │
│              │  (1 Mbps)    │                    │
│              └──────────────┘                    │
└──────────────────────────────────────────────────┘
```

**Health Test Suite (NIST SP 800-90B):**

| Test | Threshold | Response on Failure |
|------|-----------|-------------------|
| Repetition count | 1 bit ≤ 34 identical | Switch to backup RO |
| Adaptive proportion | Proportion > 20% of 512 samples | Halt and alert |
| Running average | Drift > 5% from 0.5 | Recalibrate |
| Autocorrelation | Lag-1 correlation > 0.01 | Reseed entropy pool |

### 2.2 Key Derivation Functions

**HKDF-SHA256 for Session Keys:**

The primary key derivation uses HKDF (HMAC-based Key Derivation Function):

```
Step 1: Extract
  PRK = HMAC-SHA256(salt, input_key_material)
  - salt: 128-bit random value (from TRNG)
  - IKM: shared_secret from ECDH key exchange

Step 2: Expand
  T(0) = empty string
  T(1) = HMAC-SHA256(PRK, T(0) || info || 0x01)
  output_key_material = T(1)[0:requested_length]
```

**Derivation Parameters per Key Type:**

| Derived Key | info Parameter | Length | Salt |
|------------|---------------|--------|------|
| Session Key | "iPACE session" \|\| session_id | 128 bits | Nonce_I \|\| Nonce_P |
| Telemetry Key | "telemetry" \|\| session_id | 128 bits | Session Key |
| Command Key | "commands" \|\| session_id | 128 bits | Session Key |
| Hop Key | "freq_hop" \|\| session_id | 128 bits | Session Key |
| Encryption Key | "encrypt" \|\| session_id | 128 bits | Session Key |

### 2.3 Deterministic Key Generation (RFC 6979)

For ECDSA signature operations where the nonce must be deterministic:

```
k = HMAC-SHA256(
  key = private_key,
  message = Hash(message) || additional_random_entropy
)
```

The additional random entropy prevents deterministic nonce reuse in the event of
a PRNG failure, providing defense-in-depth.

### 2.4 Key Generation Timing

| Operation | Time | Energy |
|-----------|------|--------|
| TRNG 128-bit random | 128 μs | 2.3 nJ |
| HKDF extract | 18 μs | 0.32 μJ |
| HKDF expand (128 bits) | 18 μs | 0.32 μJ |
| ECDSA keypair gen | 48 ms | 864 μJ |
| ECDH shared secret | 52 ms | 936 μJ |
| **Full session key derivation** | **52.3 ms** | **937 μJ** |

## 3. Key Distribution

### 3.1 Key Distribution Protocol

The iPACE-CHIP uses a key distribution protocol based on the Station-to-Station
(STS) model with authentication:

```
Phase 1: Ephemeral Key Exchange
  Programmer generates: (d_P_eph, Q_P_eph) — ephemeral ECDH key pair
  Implant generates: (d_I_eph, Q_I_eph) — ephemeral ECDH key pair

Phase 2: Authentication
  Programmer → Implant: Q_P_eph || Sign(d_P_long, Hash(Q_P_eph || Nonce_I))
  Implant → Programmer: Q_I_eph || Sign(d_I_long, Hash(Q_I_eph || Nonce_P))

Phase 3: Key Derivation
  shared_secret = ECDH(d_I_eph, Q_P_eph) = ECDH(d_P_eph, Q_I_eph)
  master_key = HKDF-extract(salt=Nonce_I||Nonce_P, IKM=shared_secret)
  session_key = HKDF-expand(PRK=master_key, info="session", L=128)
  telemetry_key = HKDF-expand(PRK=master_key, info="telemetry", L=128)
  command_key = HKDF-expand(PRK=master_key, info="commands", L=128)
  hop_key = HKDF-expand(PRK=master_key, info="freq_hop", L=128)

Phase 4: Key Confirmation
  Programmer → Implant: MAC(session_key, "key_confirm_P" || Q_I_eph)
  Implant → Programmer: MAC(session_key, "key_confirm_I" || Q_P_eph)
  Both verify MAC, confirming key agreement
```

### 3.2 Forward Secrecy

The use of ephemeral ECDH key pairs provides forward secrecy:

- Ephemeral private keys (d_P_eph, d_I_eph) are generated per session
- After session key derivation, ephemeral private keys are zeroized
- Compromise of long-term keys (d_P_long, d_I_long) does not expose past sessions
- Each session has an independent key with no mathematical relationship to other
  sessions

### 3.3 Key Distribution Over BLE

When key exchange occurs over the BLE channel (patient controller), the protocol
adds additional verification:

```
BLE Key Distribution:
  1. BLE LESC pairing establishes initial encryption
  2. iPACE key exchange runs within encrypted BLE channel
  3. Additional MAC verification binds BLE identity to iPACE identity
  4. BLE link key is independent of iPACE session keys
```

## 4. Key Storage

### 4.1 Key Management Unit (KMU)

The iPACE-CHIP implements a dedicated Key Management Unit for secure key storage:

```
┌─────────────────────────────────────────────────────┐
│                Key Management Unit                   │
│                                                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐          │
│  │ OTP Bank │  │ NVM Bank │  │ Volatile │          │
│  │ (DRK)    │  │ (Pairing)│  │ (Session)│          │
│  │ 256 bits │  │ 512 bits │  │ 768 bits │          │
│  └──────────┘  └──────────┘  └──────────┘          │
│       │              │              │                │
│  ┌──────────────────────────────────────────────┐  │
│  │        Access Control Arbiter                 │  │
│  │  - CPU: read-only (status), no key access    │  │
│  │  - Crypto engine: full key read/write        │  │
│  │  - DMA: no access                            │  │
│  │  - Debug: disabled in production              │  │
│  └──────────────────────────────────────────────┘  │
│       │              │              │                │
│  ┌──────────────────────────────────────────────┐  │
│  │        Tamper Response Unit                   │  │
│  │  - Voltage monitor: < 1.6V → zeroize         │  │
│  │  - Temperature: > 85°C → zeroize             │  │
│  │  - Physical intrusion → zeroize              │  │
│  │  - Debug probe → zeroize                     │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### 4.2 Key Storage Security Properties

| Property | Implementation |
|----------|---------------|
| Confidentiality | Keys in dedicated registers, encrypted NVM |
| Integrity | Parity bits + ECC on NVM keys |
| Access control | Hardware-enforced, no software bypass |
| Zeroization | 3-pass overwrite + voltage drain |
| Tamper response | Immediate zeroize on intrusion detection |
| Power loss safety | Volatile keys lost, NVM keys in encrypted form |

### 4.3 Key Serialization Format

Keys stored in NVM use a serialized format:

```
Stored Key Format:
  [Magic: 4 bytes] [Version: 1 byte] [Key_Type: 1 byte]
  [Key_ID: 4 bytes] [Expiry: 8 bytes] [Key_Data: 16 bytes]
  [HMAC: 32 bytes (over all preceding fields)]
```

The HMAC provides integrity verification before the key is loaded into the KMU.

### 4.4 Memory Layout

| Address Range | Content | Protection |
|--------------|---------|-----------|
| 0x0000_0000 - 0x0000_03FF | OTP (DRK + device ID) | Read-only, tamper-protected |
| 0x0000_1000 - 0x0000_1FFF | Key Storage NVM | Encrypted, HMAC-protected |
| 0x2000_0000 - 0x2000_07FF | KMU Registers | Write-only from CPU |
| 0x2000_1000 - 0x2000_1FFF | Session Key Cache | Volatile, auto-zeroize |

## 5. Key Rotation

### 5.1 Automatic Key Rotation

The iPACE-CHIP implements automatic key rotation based on two triggers:

**Time-Based Rotation:**

```
Rotation Policy:
  Session Key:    every 3,600 seconds (1 hour)
  Telemetry Key:  every 3,600 seconds
  Command Key:    every 3,600 seconds
  Hop Key:        every 1,800 seconds (30 minutes)
  Pairing Key:    every 30 days
```

**Usage-Based Rotation:**

```
Message Counter Thresholds:
  Session Key:    after 2^20 messages (1,048,576)
  Telemetry Key:  after 2^20 messages
  Command Key:    after 2^16 messages (65,536)
```

### 5.2 Key Rotation Protocol

```
Rotation Protocol:
  1. Current key still active
  2. Derive new_key = HKDF(current_key, "rotation", counter)
  3. Both parties compute new_key independently
  4. Send rotation confirmation: MAC(new_key, "rotation_ack")
  5. On mutual confirmation: activate new_key, deactivate old_key
  6. Zeroize old_key from KMU

  Key ID: includes counter value for identification
  Grace period: 60 seconds where both old and new keys accepted
```

### 5.3 Graceful Rotation During Active Therapy

Key rotation during an active telemetry session must not interrupt therapy:

```
Seamless Rotation:
  1. Buffer pending messages during rotation
  2. Complete rotation (steps 1-5 above)
  3. Re-encrypt buffered messages with new key
  4. Transmit buffered messages
  5. Resume normal operation

  Maximum rotation interruption: 200 ms
  Buffer capacity: 32 messages (2 KB)
```

### 5.4 Emergency Key Rotation

When a key compromise is suspected:

```
Emergency Rotation:
  1. Immediate: invalidate current session
  2. Generate new key pair (ECDH + session keys)
  3. Require full re-authentication (not resumption)
  4. Log security event
  5. Alert clinician (via patient controller)
  6. Force re-pairing on next NFC contact
```

## 6. Key Revocation

### 6.1 Revocation Scenarios

| Scenario | Revocation Scope | Recovery |
|----------|-----------------|----------|
| Controller lost/stolen | Pairing key + all session keys | New NFC pairing |
| Clinician credential revocation | All session keys with that clinician | Re-authentication |
| Compromised firmware | All keys, force re-root | Factory reset |
| Patient deceased | Complete device lockdown | Permanent |

### 6.2 Revocation Protocol

```
Revocation Request:
  Revoking_Entity → Implant: {
    Revocation_Type: [pairing | session | complete]
    Target_Device_ID: 32 bits
    Timestamp: 8 bytes
    Reason_Code: 8 bits
    Signature: Sign(d_revoke, Hash(revocation_data))
  }

Implant Response:
  1. Verify revocation signature
  2. Execute revocation:
     a. Pairing key: zeroize, mark device unpaired
     b. Session keys: zeroize active session
     c. Complete: zeroize all keys except DRK
  3. Log revocation event
  4. Respond: ACK(implant_signature)
  5. If complete: enter safe mode (no therapy changes without re-pairing)
```

### 6.3 Revocation List Management

The iPACE-CHIP maintains a local revocation list:

```
Revocation Entry:
  [Device_ID: 4 bytes] [Revocation_Time: 8 bytes] [Reason: 1 byte]

Maximum entries: 32
Oldest entry eviction: FIFO when full
Storage: Protected NVM (512 bytes reserved)
```

## 7. Key Destruction (Zeroization)

### 7.1 Volatile Key Zeroization

Session keys in volatile memory are zeroized:

```
Zeroization Procedure:
  1. Write all-zero pattern to key register
  2. Write all-one pattern to key register
  3. Write all-zero pattern to key register
  4. Verify read-back is all-zero
  5. Set zeroization complete flag
```

**Timing:**

| Step | Time |
|------|------|
| Triple overwrite | 3 cycles (125 ns) |
| Read-back verify | 1 cycle (42 ns) |
| **Total zeroization** | **167 ns** |

### 7.2 NVM Key Zeroization

Keys in NVM require more careful handling:

```
NVM Zeroization:
  1. Invalidate HMAC (prevents future use)
  2. Overwrite key data with random pattern (3 passes)
  3. Overwrite with zeros
  4. Update NVM metadata to mark slot as empty
  5. Trigger NVM garbage collection
```

### 7.3 Automatic Zeroization Triggers

| Trigger | Response Time | Scope |
|---------|--------------|-------|
| Session timeout | < 100 ms | All session keys |
| Tamper detection | < 100 ns | All keys |
| Low battery (< 2.0V) | < 1 ms | All volatile keys |
| Firmware corruption | < 1 ms | All volatile keys |
| Emergency shutdown | < 100 ns | All keys |

## 8. Key Backup and Recovery

### 8.1 Key Backup Mechanism

For operational continuity, the iPACE-CHIP supports secure key backup:

```
Backup Procedure:
  1. Derive backup_key = HKDF(DRK, "backup", timestamp)
  2. Encrypt current session state with backup_key
  3. Store encrypted backup in protected NVM region
  4. Backup includes:
     - Session parameters (nonces, counters)
     - Encrypted session keys (for recovery)
     - Device state snapshot

  Backup encryption: AES-256-GCM
  Backup integrity: SHA-256 hash stored in separate NVM region
```

### 8.2 Key Recovery Protocol

```
Recovery Procedure:
  1. Device powers on after unexpected shutdown
  2. Verify backup integrity (HMAC check)
  3. Derive backup_key = HKDF(DRK, "backup", timestamp)
  4. Decrypt session keys from backup
  5. Validate recovered keys against current nonces
  6. If valid: resume session with recovered keys
  7. If invalid: discard backup, require new session
```

### 8.3 Backup Security Limitations

| Concern | Mitigation |
|---------|-----------|
| Backup exposure | Encrypted with DRK-derived key |
| Backup tampering | HMAC-protected, integrity check |
| Old backup replay | Nonce comparison, expiry check |
| Backup after compromise | Backup invalidated on emergency rotation |

## 9. Key Management API

### 9.1 Firmware API

```c
// Key generation
int km_generate_session_key(uint8_t session_id[16],
                            uint8_t ecdh_shared[32],
                            uint8_t session_key_out[16]);

// Key derivation
int km_derive_key(uint8_t parent_key[16],
                  const char *info,
                  uint8_t derived_key[16]);

// Key storage
int km_store_key(uint8_t key_id, uint8_t key_type,
                 uint8_t key_data[16], uint32_t expiry);

// Key retrieval (crypto engine only)
int km_load_key(uint8_t key_id, uint8_t key_type,
                uint8_t key_out[16]);

// Key destruction
int km_destroy_key(uint8_t key_id, uint8_t key_type);

// Key status
int km_get_key_status(uint8_t key_id, km_status_t *status);
```

### 9.2 Error Handling

| Error Code | Meaning | Recovery |
|-----------|---------|----------|
| KM_ERR_KEY_NOT_FOUND | Key ID not in storage | Generate new key |
| KM_ERR_KEY_EXPIRED | Key past expiry time | Derive new key |
| KM_ERR_TAMPER | Tamper detected | All keys zeroized, enter safe mode |
| KM_ERR_STORAGE_FULL | No room for new key | Evict oldest key |
| KM_ERR_AUTH_FAILED | HMAC verification failed | Key corrupted, destroy and regenerate |

## 10. Security Analysis

### 10.1 Key Compromise Scenarios

| Compromised Key | Impact | Recovery |
|----------------|--------|----------|
| Session Key | Current session exposed | Rotate, establish new session |
| Telemetry Key | Telemetry stream exposed | Rotate, re-derive |
| Command Key | Command injection possible | Rotate, re-authenticate |
| Pairing Key | All sessions with that device | Re-pair with new keys |
| DRK | All derived keys compromised | Factory reset, new DRK |

### 10.2 Key Entropy Requirements

| Key | Minimum Entropy | Source |
|-----|----------------|--------|
| DRK | 256 bits | TRNG at manufacturing |
| Ephemeral ECDH | 256 bits | TRNG per session |
| Session Key | 128 bits | HKDF from ECDH |
| HMAC Key | 128 bits | HKDF from session |
| Nonces | 128 bits | TRNG |

### 10.3 Compliance Requirements

| Standard | Key Management Requirement | iPACE-CHIP Compliance |
|----------|---------------------------|----------------------|
| FIPS 140-3 | Key generation, storage, destruction | Level 2 |
| IEC 62443-4-2 | Key lifecycle management | SL2 |
| ISO 27001 | Cryptographic key management | Annex A.10.1 |

## 11. Summary

The iPACE-CHIP session key management system provides comprehensive lifecycle
control over all cryptographic keys. Hardware-backed key storage in the KMU
ensures confidentiality and tamper resistance. HKDF-based key derivation provides
cryptographic separation between key types. Automatic time and usage-based rotation
limits the impact of potential key compromise. Forward secrecy through ephemeral
ECDH ensures past session security. Immediate zeroization on tamper detection
prevents key extraction. The system meets or exceeds the key management requirements
of FIPS 140-3, IEC 62443-4-2, and ISO 27001.
