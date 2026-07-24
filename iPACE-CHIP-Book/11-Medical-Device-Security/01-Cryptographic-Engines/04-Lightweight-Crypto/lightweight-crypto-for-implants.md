# Lightweight Cryptography for Implantable Medical Devices

## Overview

Implantable pacemakers like the iPACE-CHIP operate under severe resource constraints
that challenge conventional cryptographic implementations. With microcontrollers
running at 24 MHz, limited RAM (8-32 KB), and a battery that must last 10-15 years,
every microjoule of energy and every gate of silicon area must be justified. Lightweight
cryptography addresses these constraints by providing security guarantees with
drastically reduced computational, memory, and energy overhead.

## 1. The Lightweight Cryptography Landscape

### 1.1 Why Standard Crypto Is Sometimes Insufficient

While AES and SHA-256 are efficient, certain iPACE-CHIP subsystems operate under
constraints even more severe than the main processor:

**Sub-Microcontroller Security Processor:** A dedicated coprocessor for continuous
physiological monitoring operates at 4 MHz with 2 KB RAM and 16 KB flash. This
processor performs real-time data authentication on every cardiac cycle sample
(500 Hz = 2 ms intervals), leaving only microseconds for cryptographic operations.

**Batteryless NFC Interface:** The near-field communication interface harvests
energy from the reader's RF field and must perform mutual authentication before
establishing a secure channel, all within the brief energy-harvesting window
(~10 ms).

**Inter-Device Communication:** Communication between the iPACE-CHIP and auxiliary
sensors (e.g., accelerometers, pressure sensors) uses ultra-low-power protocols
where standard AES-GCM overhead is prohibitive.

### 1.2 NIST Lightweight Cryptography Standardization

In 2023, NIST selected ASCON as the standard for lightweight authenticated
encryption and hashing. The iPACE-CHIP incorporates ASCON alongside conventional
algorithms for constrained subsystems.

**NIST LWC Competition Finalists:**

| Algorithm | Type | Block Size | Key Size | State Size |
|-----------|------|-----------|----------|------------|
| ASCON | AEAD + Hash | 320/160 bits | 128 bits | 320 bits |
| Elephant | AEAD | 128 bits | 128 bits | 256 bits |
| Grøstl | Hash | 512/1024 bits | — | 512/1024 bits |
| PHOTON-Beetle | AEAD + Hash | 256 bits | 128/256 bits | 256 bits |
| Xoodyak | AEAD + Hash | 160 bits | 128 bits | 384 bits |

### 1.3 Lightweight Cipher Comparison

| Metric | ASCON-128 | AES-128-GCM | Grain-128a | PHOTON-Beetle |
|--------|-----------|-------------|------------|---------------|
| Security (bits) | 128 | 128 | 128 | 128 |
| State size (bits) | 320 | 128 | 128 | 256 |
| Key size (bits) | 128 | 128 | 128 | 128 |
| Gates (GE) | 2,450 | 12,400 | 3,200 | 1,800 |
| Energy (nJ/byte) | 2.8 | 5.1 | 3.4 | 2.1 |
| Throughput (Mbps) | 4.2 | 96 | 3.8 | 2.9 |
| RAM (bytes) | 40 | 208 | 24 | 32 |

## 2. ASCON: Primary Lightweight Primitive

### 2.1 ASCON Algorithm Architecture

ASCON is a sponge-based authenticated encryption algorithm built on a 320-bit
permutation operating over GF(2) with 12 rounds.

**Sponge Construction:**

The sponge construction absorbs input data into the state (rate portion) and
provides output from the state (capacity portion):

```
State = [rate (64 bits) | capacity (256 bits)]

Absorb: state[rate] ← state[rate] ⊕ message_block
        state ← ASCON_permutation(state)

Squeeze: output ← state[rate]
         state ← ASCON_permutation(state)
```

**ASCON Permutation (Single Round):**

```
x ← x ⊕ round_constant
x ← x ⊕ (x >> 19) ⊕ (x >> 28)   (linear layer: addition of diagonals)
x ← x & (x >> 1) ^ (x << 63) & (x >> 61) ^ (x << 45) & (x >> 39)  (nonlinear: AND)
```

Each round applies the substitution-linear-substitution pattern across the five
64-bit words of the 320-bit state.

### 2.2 ASCON-128 Authenticated Encryption

ASCON-128 provides authenticated encryption with associated data (AEAD):

```
Initialization:
  IV = 0x80400c0600000000
  state = IV || key (128 bits) || 0...0 (to fill 320 bits)
  state ← ASCON_permutation(state)
  state[64:128] = state[64:128] ⊕ key

Process associated data (AD):
  For each AD block:
    state[0:64] ← state[0:64] ⊕ AD_block
    state ← ASCON_permutation(state)
  state[319] ← state[319] ⊕ 1 (domain separation)

Process plaintext:
  For each plaintext block (except last):
    state[0:64] ← state[0:64] ⊕ plaintext_block
    ciphertext_block = state[0:64]
    state ← ASCON_permutation(state)
  Final block:
    state[0:64] ← state[0:64] ⊕ last_plaintext_block
    ciphertext_last = state[0:64]
    state[64:128] = state[64:128] ⊕ key

Tag = state[128:256]
```

### 2.3 ASCON-Hash256

ASCON-Hash256 provides hash functionality for constrained subsystems:

```
Initialization:
  state = IV_hash || 0...0
  state ← ASCON_permutation(state)

Absorb:
  For each message block:
    state[0:rate] ← state[0:rate] ⊕ msg_block
    state ← ASCON_permutation(state)

Finalize:
  state[319] ← state[319] ⊕ 1
  tag = squeeze 256 bits from state
```

### 2.4 ASCON Performance on iPACE-CHIP Subsystems

**Benchmarks on 4 MHz Coprocessor:**

| Operation | Cycles | Time | Energy (1.8V) |
|-----------|--------|------|---------------|
| ASCON-128 Init | 320 | 80 μs | 14.4 nJ |
| ASCON-128 Absorb (8B) | 160 | 40 μs | 7.2 nJ |
| ASCON-128 Finalize | 480 | 120 μs | 21.6 nJ |
| ASCON-128 (128B total) | 3,840 | 960 μs | 172.8 nJ |
| ASCON-Hash (128B) | 3,200 | 800 μs | 144.0 nJ |
| ASCON-Hash (1 KB) | 22,400 | 5.6 ms | 1,008 nJ |

## 3. Lightweight Hash Functions

### 3.1 ASCON-Hash

ASCON-Hash provides 256-bit hash output using the ASCON permutation with
rate = 256 bits (faster absorption than the AEAD mode):

- No key required
- 12-round permutation
- Output: 256 bits (can be truncated)
- Security: 128-bit collision resistance, 256-bit preimage resistance

### 3.2 PHOTON-Beetle Hash

PHOTON-Beetle uses a smaller 256-bit state with aAES-like construction:

- 256-bit permutation over GF(2^8)
- Variable output (up to 256 bits)
- Extremely small gate count: 1,800 GE
- Suitable for the most constrained subsystems

### 3.3 Light-Hash Construction

For the most constrained applications, the iPACE-CHIP uses a light-hash
construction:

```
Light-Hash(K, M) = AES-CMAC(K, pad(M)) truncated to 32 bits
```

This provides 32-bit authentication strength suitable for:
- Telemetry packet sequence validation
- Wake-up word authentication
- Low-security integrity checks on auxiliary sensor data

## 4. Lightweight Authenticated Encryption

### 4.1 ASCON-128a (Higher Throughput)

For subsystems requiring higher throughput, ASCON-128a doubles the rate
(128 bits vs 64 bits) at the cost of slightly reduced security margin:

| Parameter | ASCON-128 | ASCON-128a |
|-----------|-----------|------------|
| Rate | 64 bits | 128 bits |
| Rounds (init/final) | 12/8 | 12/8 |
| Rounds (process) | 6/8 | 8/8 |
| Throughput (4 MHz) | 0.53 MB/s | 1.06 MB/s |
| Security margin | Higher | Adequate |

### 4.2 Xoodyak (Cyclist Mode)

Xoodyak operates in "cyclist" mode, alternating between absorbing and squeezing
phases with a 384-bit state:

```
Cyclist:
  Absorb(key || nonce || plaintext)
  Squeeze → ciphertext || tag
  Rate: 160 bits
  Rounds: 12
```

**Advantages for iPACE-CHIP:**

- Flexible rate selection (160 bits for encryption, 320 bits for hashing)
- Built-in duplex mode for continuous authentication
- Efficient for variable-length messages common in telemetry

### 4.3 Ketje (Keyed Duplex)

Ketje provides a keyed duplex mode ideal for the iPACE-CHIP's continuous
bidirectional communication:

```
Setup:  state ← ASCON_permutation(key || nonce)
Send:   state[rate] ← state[rate] ⊕ plaintext; output = state[rate]
Receive: plaintext = state[rate] ⊕ output; state[rate] ← state[rate] ⊕ output
```

This enables simultaneous encryption/decryption and authentication without
separate setup phases, reducing latency for time-critical cardiac data.

## 5. Hardware Implementation of Lightweight Crypto

### 5.1 Area-Efficient ASCON Core

The iPACE-CHIP coprocessor implements ASCON as a serialized architecture:

```
┌─────────────────────────────────────────────┐
│           ASCON Lightweight Core            │
│                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Round    │  │ State    │  │ Linear   │  │
│  │ Function │→ │ Register │→ │ Layer    │  │
│  │ (AND)    │← │ (320b)   │→ │ (XOR/    │  │
│  └──────────┘  └──────────┘  │  ROT)    │  │
│                              └──────────┘  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Round    │  │ Key/Nonce│  │ Tag      │  │
│  │ Constant │  │ XOR Unit │  │ Output   │  │
│  │ Counter  │  │          │  │ Register │  │
│  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────┘
```

**Resource Usage:**

| Resource | Amount |
|----------|--------|
| Gate count | 2,450 GE |
| SRAM | 40 bytes |
| Max frequency | 8 MHz |
| Throughput (serialized) | 0.53 MB/s |
| Power (1.8V, 4 MHz) | 8.2 μW |

### 5.2 Pipelined ASCON for Higher Performance

For the main iPACE-CHIP processor (24 MHz ARM Cortex-M4), a pipelined
implementation provides higher throughput:

**Pipeline Stages:**

1. Input XOR (1 cycle)
2. Substitution layer rounds 1-4 (4 cycles)
3. Linear layer rounds 1-4 (4 cycles)
4. Substitution layer rounds 5-8 (4 cycles)
5. Linear layer rounds 5-8 (4 cycles)
6. Substitution layer rounds 9-12 (4 cycles)
7. Linear layer rounds 9-12 (4 cycles)
8. Output extraction (1 cycle)

**Pipelined Performance:**

| Parameter | Value |
|-----------|-------|
| Cycles per permutation | 22 |
| Throughput (24 MHz) | 8.7 Mbps |
| Gate count | 5,800 GE |
| Power (1.8V, 24 MHz) | 42 μW |

### 5.3 Composite Hardware Module

The iPACE-CHIP integrates a unified lightweight crypto module supporting
ASCON, PHOTON-Beetle, and Xoodyak through a shared permutation core:

```
┌─────────────────────────────────────────────────────┐
│         Unified Lightweight Crypto Module            │
│                                                     │
│  ┌─────────────────────────────────────────────┐    │
│  │  Configurable Permutation Core              │    │
│  │  - 256/320/384-bit state (configurable)     │    │
│  │  - 8/12/20 rounds (configurable)            │    │
│  │  - GF(2)/GF(2^8) arithmetic (selectable)    │    │
│  └─────────────────────────────────────────────┘    │
│                                                     │
│  Mode Selection:                                    │
│  [00] = ASCON-128   [01] = ASCON-128a              │
│  [10] = Xoodyak     [11] = PHOTON-Beetle           │
│                                                     │
│  Resource Sharing:                                  │
│  - State register shared across modes               │
│  - Round function multiplexed                        │
│  - Key scheduling unified                            │
└─────────────────────────────────────────────────────┘
```

**Combined Resource Usage:**

| Resource | Individual (sum) | Shared | Savings |
|----------|-------------------|--------|---------|
| Gate count | 9,450 GE | 6,200 GE | 34% |
| SRAM | 96 bytes | 48 bytes | 50% |
| Power | 72 μW | 48 μW | 33% |

## 6. Energy Budget Analysis

### 6.1 Cryptographic Energy Budget for iPACE-CHIP

The total daily energy budget for cryptographic operations in the iPACE-CHIP:

**Normal Operation (No Active Telemetry):**

| Operation | Daily Count | Energy/Op | Daily Total |
|-----------|-------------|-----------|-------------|
| Integrity check (boot) | 1 | 2.4 μJ | 2.4 μJ |
| Periodic integrity (1/hr) | 24 | 2.4 μJ | 57.6 μJ |
| Secure time sync (1/hr) | 24 | 18 μJ | 432 μJ |
| Background monitoring | 86,400 | 0.8 μJ | 69.1 mJ |
| **Daily Total** | — | — | **69.6 mJ** |

**Active Telemetry Session (1 hour):**

| Operation | Count | Energy/Op | Total |
|-----------|-------|-----------|-------|
| Session key exchange | 1 | 420 μJ | 420 μJ |
| Telemetry packets (100/s) | 360,000 | 1.2 μJ | 432 mJ |
| Response command auth | 100 | 18 μJ | 1.8 mJ |
| **Session Total** | — | — | **434.2 mJ** |

### 6.2 Energy Comparison: Standard vs. Lightweight

For the coprocessor running at 4 MHz:

| Metric | AES-128-GCM | ASCON-128 | Savings |
|--------|-------------|-----------|---------|
| 128B packet encryption | 218 nJ | 172.8 nJ | 21% |
| 128B packet authentication | 145 nJ | 96 nJ | 34% |
| Combined AEAD (128B) | 363 nJ | 268.8 nJ | 26% |
| Key setup | 85 nJ | 14.4 nJ | 83% |
| **Annual savings (10M packets)** | — | — | **942 mJ** |

### 6.3 Battery Life Impact

The iPACE-CHIP uses a 1.5 Ah (5,400 J) lithium-iodine battery over 10 years:

| Scenario | Crypto Energy (10yr) | Battery % | Impact |
|----------|---------------------|-----------|--------|
| All AES-128-GCM | 1.32 J | 0.024% | Negligible |
| All ASCON-128 | 1.04 J | 0.019% | Negligible |
| Savings with ASCON | 0.28 J | 0.005% | Minimal |

While crypto energy is a small fraction of total battery consumption, the
savings become significant when considering the coprocessor's continuous
operation at 4 MHz where every nanojoule contributes to the thermal budget.

## 7. Security Analysis of Lightweight Primitives

### 7.1 ASCON Security Margins

ASCON provides 128-bit security with the following margin analysis:

| Attack | Complexity | Margin |
|--------|-----------|--------|
| Integral | 2^128.5 | +0.5 bits |
| Substitution-permutation | 2^127 | -1 bit (still adequate) |
| Linear | 2^126.2 | -1.8 bits |
| Collision (生日 attack) | 2^128 | 128 bits |
| State recovery | 2^256 | 128 bits above target |

### 7.2 Comparison with Conventional Algorithms

| Security Property | ASCON-128 | AES-128-GCM | Assessment |
|-------------------|-----------|-------------|------------|
| Confidentiality | 128-bit | 128-bit | Equivalent |
| Authenticity | 128-bit | 128-bit | Equivalent |
| Quantum (Grover) | 64-bit | 64-bit | Equivalent |
| Side-channel margin | Moderate | High | AES preferred for high-security |

### 7.3 Formal Verification

ASCON has undergone extensive formal analysis:

- Proven security in the random permutation model
- Tight security reductions from the ASCON permutation
- No structural weaknesses identified in 5+ years of public analysis
- Selected by NIST after 5-year competition with global cryptanalysis

## 8. Implementation in iPACE-CHIP Firmware

### 8.1 Software Library

The iPACE-CHIP includes an optimized C implementation of ASCON:

```c
// ASCON-128 AEAD interface
int ascon_aead_encrypt(
    uint8_t *c, size_t *clen,
    const uint8_t *m, size_t mlen,
    const uint8_t *ad, size_t adlen,
    const uint8_t *nsec,     // unused (always NULL)
    const uint8_t *npub,     // 128-bit nonce
    const uint8_t *k         // 128-bit key
);

int ascon_aead_decrypt(
    uint8_t *m, size_t *mlen,
    uint8_t *nsec,           // unused
    const uint8_t *c, size_t clen,
    const uint8_t *ad, size_t adlen,
    const uint8_t *npub,
    const uint8_t *k
);
```

**Code Size:**

| Component | Code (bytes) | Data (bytes) |
|-----------|-------------|--------------|
| ASCON-128 AEAD | 1,824 | 40 |
| ASCON-Hash256 | 680 | 40 |
| Xoodyak AEAD | 2,100 | 48 |
| Combined library | 4,200 | 88 |

### 8.2 Assembly Optimization

Critical permutation functions are hand-optimized in ARM Thumb-2 assembly:

```
; ASCON permutation - inner round (ARM Thumb-2)
; Input: r0-r4 = state words W0-W4
; Uses: r5-r8 as temporaries

ascon_round:
    ; Round constant XOR
    eors r0, r0, r9
    ; Substitution (5-way AND-XOR)
    eor  r5, r1, r2
    eor  r6, r3, r4
    and  r5, r5, r0
    eors r1, r1, r5
    eors r2, r2, r5
    and  r6, r6, r7  ; r7 = r0 after rotation
    eors r3, r3, r6
    eors r4, r4, r6
    ; Linear layer (rotation and XOR)
    ... (full implementation: 28 instructions)
```

**Assembly vs. C Performance:**

| Function | C (cycles) | Assembly (cycles) | Speedup |
|----------|-----------|-------------------|---------|
| Single round | 48 | 28 | 1.71× |
| 12-round permutation | 520 | 310 | 1.68× |
| AEAD (128B) | 4,100 | 3,840 | 1.07× |

### 8.3 Usage Policy

The iPACE-CHIP firmware enforces a usage policy for cryptographic primitives:

| Subsystem | Primary Algorithm | Fallback | Justification |
|-----------|------------------|----------|---------------|
| Main processor | AES-128-GCM | ASCON-128 | Hardware acceleration available |
| Coprocessor (4 MHz) | ASCON-128 | — | Too constrained for AES |
| NFC interface | ASCON-128 | — | Batteryless operation |
| Aux sensors | ASCON-128 | ASCON-Hash | Ultra-low power |
| Firmware signing | ECDSA P-384 | — | Requires asymmetric |
| Key exchange | ECDH P-256 | — | Requires asymmetric |

## 9. Future Directions

### 9.1 NIST LWC Standard Adoption

With ASCON standardized by NIST, the iPACE-CHIP roadmap includes:

- **Version 1.x:** ASCON for constrained subsystems (current)
- **Version 2.x:** ASCON as default for all authenticated encryption (planned)
- **Version 3.x:** Full ASCON suite including ASCON-Hash for SHA-256 replacement
  in bandwidth-constrained scenarios

### 9.2 Post-Quantum Lightweight Crypto

Research into lightweight post-quantum primitives:

- **Lattice-based:** Ring-LWE encryption with small key sizes (1 KB)
- **Code-based:** McEliece variants with small matrices for constrained devices
- **Hash-based:** XMSS/LMS signatures with hardware-optimized implementations

### 9.3 Formal Verification Targets

- Machine-checked proofs of ASCON implementation correctness (Coq/Isabelle)
- Side-channel freedom proofs using-masked reference implementation
- Integration with the iPACE-CHIP formal verification framework

## 10. Summary

Lightweight cryptography enables the iPACE-CHIP to maintain robust security
across all subsystems, including those too constrained for conventional algorithms.
ASCON, selected as the NIST standard, provides 128-bit security with significantly
reduced gate count, energy consumption, and memory requirements compared to
AES-GCM. The unified lightweight crypto module in hardware shares resources
across multiple lightweight primitives, maximizing flexibility while minimizing
silicon area. Energy analysis confirms that lightweight crypto reduces the
cryptographic energy budget by 26%, contributing to extended implant battery life
in this life-critical medical device.
