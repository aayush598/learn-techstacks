# Hash Functions for Integrity in iPACE-CHIP

## Overview

Cryptographic hash functions provide the integrity and authenticity primitives
essential for the iPACE-CHIP implantable pacemaker. From firmware verification at
boot to real-time telemetry authentication, hash functions underpin virtually
every security mechanism in the device. This chapter covers the specific hash
algorithms deployed, their hardware implementations, and their integration into
the iPACE-CHIP security architecture.

## 1. Cryptographic Hash Function Properties

### 1.1 Required Security Properties

A cryptographic hash function H maps an arbitrary-length input to a fixed-length
output (digest) and must satisfy:

**Preimage Resistance:** Given a hash value h, it is computationally infeasible
to find any message m such that H(m) = h. This property prevents an attacker
from recovering the original data from its hash.

**Second Preimage Resistance:** Given an input m1, it is computationally infeasible
to find a different input m2 such that H(m1) = H(m2). This prevents an attacker
from substituting a malicious document that hashes to the same value as a legitimate
one.

**Collision Resistance:** It is computationally infeasible to find any two distinct
inputs m1 ≠ m2 such that H(m1) = H(m2). Birthday attacks reduce collision
resistance to n/2 bits for an n-bit hash, so SHA-256 provides 128-bit collision
resistance.

### 1.2 Security Levels Required

| Property | Minimum Bits | iPACE-CHIP Target | Algorithm |
|----------|-------------|-------------------|-----------|
| Preimage | 128 | 256 | SHA-256 |
| Second Preimage | 128 | 256 | SHA-256 |
| Collision | 64 | 128 | SHA-256 |
| Truncated (for CMAC) | 32-64 | 32-128 | SHA-256, SHA-384 |

## 2. Hash Algorithms Deployed in iPACE-CHIP

### 2.1 SHA-256 (Primary Algorithm)

SHA-256 produces a 256-bit digest and is the primary hash function for all
iPACE-CHIP integrity operations.

**Algorithm Structure:**

SHA-256 processes 512-bit message blocks through 64 rounds of compression.
Each round applies a message schedule-derived value and six logical functions
to the working variables:

```
Working variables: a, b, c, d, e, f, g, h (32 bits each)
Round function:
  T1 = h + Σ1(e) + Ch(e,f,g) + K[i] + W[i]
  T2 = Σ0(a) + Maj(a,b,c)
  h = g, g = f, f = e, e = d + T1
  d = c, c = b, b = a, a = T1 + T2
```

Where:
- Ch(x,y,z) = (x AND y) XOR (NOT x AND z)
- Maj(x,y,z) = (x AND y) XOR (x AND z) XOR (y AND z)
- Σ0(x) = ROTR²(x) XOR ROTR¹³(x) XOR ROTR²²(x)
- Σ1(x) = ROTR⁶(x) XOR ROTR¹¹(x) XOR ROTR²⁵(x)

**Message Schedule:**

```
W[i] = σ1(W[i-2]) + W[i-7] + σ0(W[i-15]) + W[i-16]  (for 16 ≤ i ≤ 63)
W[i] = M[i]                                              (for 0 ≤ i ≤ 15)
```

**Initial Hash Values:**

Derived from the fractional parts of the square roots of the first eight primes,
providing nothing-up-my-sleeve initialization.

### 2.2 SHA-384 (Firmware Signing)

SHA-384, a variant of SHA-512 with a truncated output, is used exclusively for
firmware image authentication. The 384-bit output provides 192-bit collision
resistance, exceeding the 128-bit requirement with substantial margin.

SHA-384 operates on 1024-bit blocks with 80 rounds, using 64-bit arithmetic
that is efficient on 32-bit processors through double-precision operations.

### 2.3 SHA-3 / SHAKE (Future-Proofing)

The iPACE-CHIP firmware includes a SHA-3 (Keccak) implementation prepared for
future use. SHA-3 provides an alternative construction (sponge) to Merkle-Damgård,
eliminating length extension vulnerabilities inherent in SHA-2.

**SHAKE128/256 (Extendable-Output Functions):**

SHAKE is provisioned for variable-length output requirements:
- SHAKE128 for lightweight keyed hashing (MAC applications)
- SHAKE256 for key derivation (replacing HKDF-SHA256 if required)

### 2.4 BLAKE2s (Lightweight Alternative)

BLAKE2s is included as a high-performance alternative for operations where speed
and code size are critical:

| Algorithm | Throughput (ARM M4) | Code Size | RAM |
|-----------|--------------------:|----------:|----:|
| SHA-256 | 15.2 cycles/byte | 2.1 KB | 100 B |
| SHA-384 | 10.8 cycles/byte | 3.4 KB | 200 B |
| BLAKE2s | 7.3 cycles/byte | 2.8 KB | 176 B |
| SHA-3-256 | 12.1 cycles/byte | 4.2 KB | 352 B |

BLAKE2s is used for high-throughput telemetry authentication where energy
consumption must be minimized.

## 3. Hash-Based Constructions in iPACE-CHIP

### 3.1 HMAC-SHA256 (Message Authentication)

HMAC (Hash-based Message Authentication Code) provides symmetric message
authentication using a hash function and a secret key:

```
HMAC(K, m) = H((K' ⊕ opad) || H((K' ⊕ ipad) || m))
```

where K' is the key padded or hashed to the block size, ipad = 0x36 repeated,
and opad = 0x5c repeated.

**iPACE-CHIP Usage:**

- Real-time telemetry stream authentication (HMAC-SHA256-128, truncated to 128 bits)
- Stored data integrity verification
- Key derivation input authentication
- Command authentication between programmer and implant

**Security Analysis:**

HMAC-SHA256 security is bounded by min(n, |K|/2, l) where n is the hash output
length, |K| is the key length, and l is the block length. With 128-bit session
keys and 256-bit output, the effective security is 128 bits.

### 3.2 CMAC-AES (Cipher-Based MAC)

CMAC provides authentication using a block cipher instead of a hash function:

```
CMAC(K, m) = AES(K, C1 ⊕ AES(K, C2 ⊕ ... ⊕ AES(K, Cn ⊕ Kn)))
```

where Ki are subkeys derived from the block cipher.

**iPACE-CHIP Usage:**

- Fast integrity verification during boot (truncated to 32 bits)
- Message authentication for low-latency commands
- Key confirmation during key establishment protocols

### 3.3 SHAKE-based MAC (KMAC)

KMAC (Keccak MAC) is prepared for future use:

```
KMAC_XOF(K, m, L) = Keccak-MAC-XOF(K, m, L)
```

KMAC provides an alternative with different security assumptions than HMAC,
useful as a defense-in-depth measure.

### 3.4 Hash-Based Key Derivation

**HKDF (HMAC-based Key Derivation Function):**

HKDF-SHA256 is the primary key derivation function for the iPACE-CHIP:

```
Step 1: Extract
  PRK = HMAC-SHA256(salt, IKM)

Step 2: Expand
  T(0) = empty
  T(i) = HMAC-SHA256(PRK, T(i-1) || info || i)
  OKM = T(1) || T(2) || ... || T(N)
```

**Applications:**

| Derivation | Input Key Material | Context Info | Output |
|------------|-------------------|--------------|--------|
| Session key | DRK | session_id, nonce | 128-bit AES key |
| HMAC key | Session key | "telemetry_mac" | 128-bit HMAC key |
| IV seed | Session key | "iv_seed", counter | 96-bit nonce |
| Firmware key | DRK | "fw_verify", version | 256-bit ECDSA verification key |

### 3.5 Hash Tree (Merkle Tree) for Firmware

The iPACE-CHIP firmware image is organized as a Merkle tree for efficient
segment verification:

```
        Root Hash (stored in OTP)
       /                    \
   H(S1||S2)              H(S3||S4)
   /      \                /      \
H(S1)    H(S2)         H(S3)    H(S4)
 |        |             |        |
Seg1     Seg2          Seg3     Seg4
```

**Verification Process:**

1. Compute hash of the segment being verified
2. Retrieve the sibling hash from the Merkle tree (stored in firmware header)
3. Compute parent hash up the tree
4. Compare computed root with the stored root in OTP memory
5. Accept only if the root hash matches exactly

**Efficiency:** Verification of any single 256-byte segment requires only
log2(N) hash computations plus retrieval of log2(N) sibling hashes, where N is
the number of segments.

## 4. Hardware Hash Accelerator

### 4.1 SHA-256 Hardware Engine

The iPACE-CHIP integrates a dedicated SHA-256 acceleration unit:

**Architecture:**

```
┌─────────────────────────────────────────────┐
│              SHA-256 Accelerator            │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Message   │  │ Round    │  │ Hash     │  │
│  │ Schedule  │→ │ Function │→ │ State    │  │
│  │ Unit      │  │ (64 RND) │  │ Register │  │
│  └──────────┘  └──────────┘  └──────────┘  │
│       ↑              ↑              ↓       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ DMA      │  │ Round    │  │ Digest   │  │
│  │ Interface│  │ Constant │  │ Output   │  │
│  │          │  │ ROM      │  │ Buffer   │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────┘
```

**Performance Characteristics:**

| Parameter | Value |
|-----------|-------|
| Clock frequency | 24 MHz |
| Throughput | 120 Mbps |
| Latency (512-bit block) | 64 cycles (2.67 μs) |
| Latency (full SHA-256 of 1 KB) | 1.07 ms |
| Latency (full SHA-256 of 64 KB) | 68 ms |
| Power consumption | 15 μW |
| Gate count | 12.4K GE |

**DMA Integration:**

The SHA-256 accelerator supports scatter-gather DMA for processing non-contiguous
memory buffers. A descriptor chain specifies source addresses and lengths, enabling
hash computation over fragmented firmware segments without reassembly.

### 4.2 Dual-Hash Engine

The iPACE-CHIP includes two independent hash engines:

1. **SHA-256 Engine:** Primary engine for telemetry authentication and key
   derivation
2. **SHA-384 Engine:** Dedicated engine for firmware verification, active only
   during boot and update procedures

Having two engines allows simultaneous hash computation:
- SHA-256 engine processes incoming telemetry data
- SHA-384 engine verifies firmware segments during background integrity checks

### 4.3 Constant-Time Operation

All hash operations execute in constant time to prevent timing side channels:

- **Number of rounds is fixed:** SHA-256 always executes exactly 64 rounds
- **Message padding is deterministic:** Input length extension follows a fixed
  pattern
- **No data-dependent branches:** The round function uses arithmetic operations
  rather than conditional branches
- **No data-dependent memory access:** All operations occur on registers, not
  indexed memory

## 5. Hash Function Security Analysis

### 5.1 Length Extension Attacks

SHA-256, as a Merkle-Damgård construction, is vulnerable to length extension:
given H(m), an attacker can compute H(m || padding || m') without knowing m.

**Mitigation in iPACE-CHIP:**

- HMAC is used instead of plain hash for message authentication (HMAC is
  resistant to length extension)
- SHA-3 (sponge construction) is available for applications requiring natural
  resistance to length extension
- Merkle tree construction includes message length in the leaf hash, preventing
  extension at any level

### 5.2 Second Preimage Attacks on Long Messages

For Merkle-Damgård hashes, second preimage attacks can be more efficient than
birthday attacks for very long messages. The iPACE-CHIP mitigates this by:

- Segmenting all data into fixed-size blocks (max 64 KB)
- Using HMAC rather than plain hash for integrity verification
- Adding a length prefix to the hashed data: H(len(m) || m)

### 5.3 Collision Attack Considerations

While no practical SHA-256 collisions have been found, the theoretical security
margin (2^128 vs. the birthday bound of 2^128) means that any advancement in
collision-finding techniques could be concerning.

**Defense-in-Depth:**

- SHA-384 provides 192-bit collision resistance as an alternative
- Keyed hash functions (HMAC, KMAC) are unaffected by collision attacks on the
  underlying hash
- Merkle tree design limits the scope of any single collision

### 5.4 Quantum Resistance

Grover's algorithm reduces preimage resistance of SHA-256 to 128 bits (from 256)
and collision resistance to 85 bits (from 128). For long-term security:

- SHA-256 remains quantum-resistant at 128-bit preimage security
- SHA-384 provides 192-bit quantum preimage security
- SHAKE256 with 512-bit output provides 256-bit quantum security for critical
  applications

## 6. Practical Applications in iPACE-CHIP

### 6.1 Firmware Integrity Verification

**Boot-Time Verification:**

```
For each firmware segment i:
  1. Read segment from flash
  2. Compute SHA-256(segment)
  3. Compare with stored hash in Merkle tree
  4. Retrieve sibling hashes and compute path to root
  5. Compare computed root with OTP-stored root hash
  6. If mismatch → halt boot, enter safe mode
```

**Time Budget:**

| Firmware Size | Segments | Verification Time | Boot Delay |
|--------------|----------|-------------------|------------|
| 256 KB | 1024 | 270 ms | Acceptable |
| 512 KB | 2048 | 540 ms | Acceptable |
| 1 MB | 4096 | 1.08 s | Within 2s budget |

### 6.2 Telemetry Authentication

Each telemetry packet includes a truncated HMAC-SHA256:

```
Packet format:
  [Sequence# (4B)] [Timestamp (8B)] [Data (variable)] [HMAC-128 (16B)]
```

The HMAC is computed over the concatenation of all fields except the HMAC itself,
using the current message key. Verification is performed before any clinical
decision is made based on the telemetry data.

**Performance Impact:**

- HMAC-SHA256-128 computation: 18 μs per 128-byte packet
- Energy cost: 0.34 μJ per packet
- Throughput overhead: < 5% on the 1 Mbps telemetry link

### 6.3 Secure Boot Chain

The boot chain uses hash functions at multiple levels:

```
Level 0: ROM Bootloader
  Verify: SHA-256(PBL) == stored_hash_in_ROM

Level 1: Primary Bootloader (PBL)
  Verify: SHA-384(SBL_image) == hash_in_certificate
  Certificate: Signed by manufacturer, contains hash

Level 2: Secondary Bootloader (SBL)
  Verify: SHA-256(app_image) via Merkle tree root
  Root: Stored in PBL-protected flash sector

Level 3: Application Firmware
  Runtime: Periodic SHA-256 integrity checks on critical code regions
```

### 6.4 Patient Identifier Binding

The iPACE-CHIP binds cryptographically to a specific patient using a hash-based
protocol:

```
patient_binding = SHA-256(device_serial || patient_ID || pairing_nonce)
```

This binding is stored in protected NVM and verified before each therapy session,
ensuring the device can only be controlled by the authorized programmer for the
correct patient.

### 6.5 Audit Log Integrity

The device maintains a tamper-evident audit log using a hash chain:

```
log_entry[i] = {
  timestamp,
  event_type,
  data,
  previous_hash: SHA-256(log_entry[i-1]),
  entry_hash: SHA-256(timestamp || event_type || data || previous_hash)
}
```

Any modification to a historical log entry will break the hash chain, providing
cryptographic evidence of tampering.

## 7. Hash Function Testing

### 7.1 Known Answer Tests

All hash implementations are validated against NIST test vectors:

**SHA-256 Test Vectors:**

| Input | Expected Digest (truncated) |
|-------|---------------------------|
| "" (empty) | e3b0c44298fc... |
| "abc" | ba7816bf8f01... |
| "abcdbcdecdefdef..." | 248d6a61d206... |

### 7.2 Edge Case Testing

- Zero-length input
- Single-byte input
- Input exactly 55 bytes (maximum padding-free block)
- Input exactly 56 bytes (requires two blocks)
- Input at block boundaries (64, 128, 192 bytes)
- Maximum supported length (64 KB)
- Non-aligned lengths (1, 3, 7, 13 bytes)

### 7.3 Performance Regression Testing

Hash performance is monitored across firmware versions to detect regressions:

```
Benchmark suite:
  SHA-256: 1 KB, 4 KB, 16 KB, 64 KB
  SHA-384: 1 KB, 4 KB, 16 KB, 64 KB
  HMAC-SHA256: 128 B, 1 KB, 4 KB
  CMAC-AES: 16 B, 128 B, 1 KB

Acceptable variance: ± 5% from baseline
```

### 7.4 Implementation Fuzzing

The hash API is fuzzed with:

- Randomized input lengths from 0 to 65535 bytes
- Incremental hashing (partial updates) with random chunk sizes
- Concurrent hashing from multiple tasks
- Hash computation during flash read operations (bus contention)
- Hash computation with interrupts disabled and enabled

## 8. Summary

Hash functions are the foundational building block for integrity, authentication,
and key derivation in the iPACE-CHIP implantable pacemaker. SHA-256 provides the
primary hash capability with hardware acceleration, while SHA-384 serves
firmware verification with enhanced security margin. The comprehensive
implementation covers raw hashing (SHA-2, SHA-3), message authentication
(HMAC, CMAC), key derivation (HKDF), and structural integrity (Merkle trees),
all executed with constant-time guarantees and hardware acceleration to meet
the demanding requirements of a life-critical implantable medical device.
