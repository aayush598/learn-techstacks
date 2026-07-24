# AES Encryption for Medical Device Data Protection

## Overview

The Advanced Encryption Standard (AES) serves as the cornerstone symmetric encryption
algorithm for the iPACE-CHIP implantable pacemaker ecosystem. Medical devices demand
encryption that is both computationally efficient for resource-constrained hardware
and robust enough to protect life-critical patient data against sophisticated adversaries.

## 1. AES Algorithm Fundamentals

### 1.1 Mathematical Foundation

AES operates on a fixed 128-bit (16-byte) block of data, organized as a 4×4 matrix
of bytes called the State matrix. The algorithm applies a series of transformations
over multiple rounds depending on the key size:

| Key Size | Rounds | Block Size | Key Length (bits) |
|----------|--------|------------|-------------------|
| AES-128 | 10 | 128 | 128 |
| AES-192 | 12 | 128 | 192 |
| AES-256 | 14 | 128 | 256 |

The iPACE-CHIP uses AES-128 as its primary encryption mode due to the balance between
security margin and computational overhead on the implant's microcontroller.

### 1.2 Round Transformations

Each AES round consists of four transformations applied sequentially:

**SubBytes** — A non-linear byte substitution using a predefined S-box lookup table.
Each byte of the State is replaced with its multiplicative inverse in GF(2^8),
followed by an affine transformation over GF(2). This step provides confusion,
ensuring that the relationship between the plaintext and ciphertext is as complex
as possible.

**ShiftRows** — The rows of the State matrix are cyclically shifted left by
increasing offsets (0, 1, 2, 3 bytes). Row 0 is not shifted, row 1 shifts by 1,
row 2 by 2, and row 3 by 3. This provides diffusion across columns.

**MixColumns** — Each column of the State is multiplied by a fixed polynomial
{03}x^3 + {01}x^2 + {01}x + {02} in GF(2^8). This transformation ensures that
each output byte depends on all four input bytes of the column.

**AddRoundKey** — The State is XORed with a subkey derived from the original key
through a key expansion schedule. This is the only operation that directly involves
the secret key.

### 1.3 Key Expansion Schedule

The AES key expansion algorithm generates (N+1) × 4 words (where N is the number
of rounds) from the original key. Each word is derived by XORing the previous word
with the word located N positions earlier, with a rotational SubBytes transformation
applied when the word position is a multiple of N.

```
Key Expansion Process:
  w[i] = w[i-N] XOR SubWord(RotWord(w[i-1])) XOR Rcon[i/N]  (if i mod N == 0)
  w[i] = w[i-N] XOR w[i-1]                                    (otherwise)
```

The round constants (Rcon) are powers of x in GF(2^8), preventing symmetry in
the key schedule that could be exploited by algebraic attacks.

## 2. AES Modes of Operation for iPACE-CHIP

### 2.1 Counter Mode (CTR)

AES-CTR transforms a block cipher into a stream cipher by encrypting a sequential
counter and XORing the result with the plaintext. This mode is preferred for
iPACE-CHIP telemetry streams because it supports parallelizable encryption and
decryption, and any bit-flip in the ciphertext affects only the corresponding
bit in the plaintext.

**Counter Block Construction:**

```
Counter block = [Nonce (64 bits) || Counter (64 bits)]
```

The nonce must never repeat under the same key. The iPACE-CHIP generates nonces
using a monotonic hardware counter seeded from a true random number source at
power-up.

**Security Properties for Medical Telemetry:**

- Deterministic encryption enables random access to encrypted telemetry records
- No padding required, minimizing data overhead on bandwidth-constrained RF links
- Decryption can be performed in parallel, critical for emergency data retrieval
- Authentication is provided when combined with a separate MAC (Encrypt-then-MAC)

### 2.2 Galois/Counter Mode (GCM)

AES-GCM provides both confidentiality and authenticity in a single pass, making it
ideal for the iPACE-CHIP wireless communication channel. GCM combines CTR-mode
encryption with GHASH authentication.

**GHASH Authentication:**

GHASH computes a polynomial hash over the authenticated data and ciphertext:

```
GHASH(X) = (X1 · H^(n+1)) ⊕ (X2 · H^n) ⊕ ... ⊕ (Xn · H) ⊕ L · H
```

where H is the hash subkey (encryption of all-zero block) and L is the length block.

**GCM Tag Generation:**

```
Tag = GHASH(AAD || ciphertext || length(AAD) || length(ciphertext)) ⊕ J0
```

The 128-bit GCM tag provides authentication strength equivalent to 128-bit symmetric
security, sufficient for protecting against message forgery in medical device contexts.

**Performance on ARM Cortex-M (typical iPACE-CHIP processor):**

| Operation | AES-CTR | AES-GCM | Overhead |
|-----------|---------|---------|----------|
| Encrypt 128B | 42 μs | 48 μs | +14% |
| Decrypt 128B | 42 μs | 51 μs | +21% |
| Energy (3V) | 0.8 μJ | 0.95 μJ | +19% |

### 2.3 CBC Mode for Legacy Storage

Cipher Block Chaining (CBC) is retained in the iPACE-CHIP firmware for encrypting
non-volatile storage of historical telemetry data. While slower than CTR/GCM for
streaming data, CBC provides acceptable security for static data-at-rest scenarios.

**Padding Oracle Consideration:**

CBC mode requires padding (PKCS#7), which introduces padding oracle attack
vulnerability. The iPACE-CHIP mitigates this by always authenticating before
decrypting (Encrypt-then-MAC) and by using a constant-time comparison for MAC
verification to prevent timing-based oracle attacks.

### 2.4 SIV Mode for Rekeying Operations

Synthetic Initialization Vector (SIV) mode is used specifically for rekeying
operations between the implant and external programmer. SIV provides deterministic
encryption — the same plaintext and associated data always produce the same
ciphertext — which is essential for key derivation protocols where replay detection
relies on nonce comparison.

## 3. Hardware AES Implementation on iPACE-CHIP

### 3.1 Crypto Accelerator Architecture

The iPACE-CHIP integrates a dedicated AES hardware accelerator as a memory-mapped
peripheral. The accelerator operates independently from the main CPU core, allowing
encryption to proceed without stalling firmware execution.

**Register Map:**

| Address Offset | Register Name | Description |
|---------------|---------------|-------------|
| 0x00 | AES_CTRL | Control register (start, mode, key size) |
| 0x04 | AES_STATUS | Status register (busy, done, error) |
| 0x08-0x18 | AES_KEY[0-3] | 128-bit key storage (write-only) |
| 0x1C-0x2C | AES_IV[0-3] | 128-bit IV/nonce storage |
| 0x30-0x3C | AES_DATA_IN[0-3] | 128-bit input data block |
| 0x40-0x4C | AES_DATA_OUT[0-3] | 128-bit output data block |
| 0x50 | AES_GCM_H | GHASH subkey (read-only, computed internally) |
| 0x54 | AES_GCM_TAG | Authentication tag output |

**DMA Integration:**

The AES accelerator connects to the DMA controller for bulk encryption of telemetry
buffers. A transfer descriptor specifies source address, destination address, block
count, and cryptographic parameters. This enables encryption of an entire 4 KB
telemetry page without CPU intervention.

**Latency Characteristics:**

| Parameter | Value |
|-----------|-------|
| Single block latency | 32 clock cycles |
| Throughput (24 MHz) | 96 Mbps |
| DMA burst latency | 35 cycles/block |
| Key setup time | 12 cycles |

### 3.2 Constant-Time Implementation Requirements

All AES operations on the iPACE-CHIP must execute in constant time to prevent
timing side-channel attacks. This is enforced through:

**Hardware S-Box:** The SubBytes lookup table is implemented as combinational
logic rather than ROM-based lookup, eliminating cache timing variations.

**Uniform Round Processing:** All rounds execute identically regardless of the
data or key values. The hardware pipeline processes exactly 32 cycles per block
under all input conditions.

**Branch-Free Key Expansion:** The key expansion schedule uses arithmetic
conditionals rather than branch instructions, preventing branch prediction
side channels.

**Memory Access Pattern:** The key material resides in a dedicated register file
separate from general-purpose SRAM, eliminating memory bus contention that could
leak information through electromagnetic emanation patterns.

### 3.3 Power Analysis Resistance

**Masked S-Box Design:** The hardware S-Box employs first-order Boolean masking,
randomizing the intermediate values during SubBytes computation. The mask bits
are refreshed at the start of each new encryption operation using the on-chip
true random number generator (TRNG).

**Shuffling Countermeasure:** The order of SubBytes operations across the four
columns of the State matrix is randomized using a permutation derived from the
TRNG, preventing Simple Power Analysis (SPA) from identifying round boundaries.

**Balanced CMOS Logic:** All datapath elements use complementary logic gates
with equal rise and fall times, minimizing the correlation between switching
activity and data values.

## 4. Key Management for AES in iPACE-CHIP

### 4.1 Key Hierarchy

The iPACE-CHIP implements a three-tier key hierarchy:

**Device Root Key (DRK):** A 256-bit key burned into one-time-programmable (OTP)
memory during manufacturing. The DRK never leaves the device and is used solely
to derive operational keys. The DRK is derived from the device serial number
concatenated with a manufacturer-specific secret, processed through HKDF.

**Session Keys:** Derived from the DRK using HKDF-SHA256 with context-specific
information (session identifier, timestamp, device role). Session keys have a
configurable lifetime (default: 1 hour for active telemetry sessions).

**Message Keys:** Derived from session keys using a counter-based key derivation
function. Each telemetry message uses a unique message key, providing
key-compromise resistance for individual messages.

### 4.2 Key Derivation Protocol

```
Session Key = HKDF-SHA256(
    IKM = DRK,
    salt = nonce_programmer || nonce_implant,
    info = "iPACE-CHIP session" || session_id || expiration_time
)

Message Key = HKDF-SHA256(
    IKM = Session Key,
    salt = "",
    info = "msg_key" || message_counter
)
```

### 4.3 Secure Key Storage

AES keys in the iPACE-CHIP are stored in a dedicated Key Management Unit (KMU)
that provides:

- **Volatile storage only:** Keys are loaded from protected NVM at boot and
  immediately zeroized from NVM. In the KMU, keys exist only in flip-flop
  storage powered by the battery.
- **Access control:** The KMU enforces that key material can only be read by the
  AES accelerator and the key derivation engine. The CPU can only read status
  registers, not key values.
- **Tamper response:** Upon detection of physical intrusion, the KMU immediately
  zeros all key registers within 100 ns.

## 5. Security Analysis and Threat Mitigation

### 5.1 Brute Force Resistance

With AES-128, the key space is 2^128 operations. Even assuming a specialized
hardware attacker could perform 10^12 operations per second (well beyond current
capabilities for embedded systems), exhausting the key space would require
approximately 10^21 years. AES-256 raises this to 10^30 years.

### 5.2 Known-Attack Resistance

| Attack | Resistance | Mitigation |
|--------|------------|------------|
| Biclique cryptanalysis | 2^126.1 complexity | Still computationally infeasible |
| Square attack | Reduced rounds only | Full rounds always executed |
| Algebraic attacks | Infeasible for full AES | S-box has optimal nonlinearity |
| Related-key attacks | No effect | Key schedule prevents related keys |

### 5.3 Quantum Computing Considerations

Grover's algorithm reduces the effective security of AES-128 to 64 bits and
AES-256 to 128 bits against a quantum adversary. The iPACE-CHIP roadmap includes
a firmware update path to AES-256 encryption for long-term security, triggered
by a cryptographic agility framework that allows algorithm negotiation during the
initial programmer-implant pairing.

### 5.4 Compliance and Certification

The AES implementation in the iPACE-CHIP targets FIPS 197 (AES) certification and
is designed to meet the requirements of:

- IEC 62443-4-1 (Security for industrial automation — secure product development)
- IEC 81001-5-1 (Health software and health IT systems — security)
- FDA Pre-Cybersecurity Guidance for medical devices
- UL 2900-1 (Software cybersecurity for network-connectable products)

## 6. AES Configuration Profiles

### 6.1 Profile: Telemetry Encryption (AES-GCM-128)

Used for real-time telemetry streaming from implant to programmer:

- **Key Size:** 128 bits
- **Mode:** GCM with 96-bit nonce
- **Tag Length:** 128 bits
- **AAD:** Sequence number + device ID + timestamp
- **Rekey Interval:** Every 3,600 seconds or 2^20 messages

### 6.2 Profile: Stored Data Encryption (AES-CBC-MAC-128)

Used for historical telemetry data stored in implant NVM:

- **Key Size:** 128 bits
- **Mode:** CBC with PKCS#7 padding
- **MAC:** HMAC-SHA256 over ciphertext (Encrypt-then-MAC)
- **IV Generation:** Random from TRNG per storage block
- **Rekey:** On each programmer session

### 6.3 Profile: Secure Boot Verification (AES-CMAC)

Used for firmware integrity verification during boot:

- **Key Size:** 128 bits
- **Mode:** CMAC (Cipher-based MAC)
- **Truncated Output:** 32 bits for fast verification
- **Key Source:** Derived from DRK via HKDF

## 7. Implementation Testing and Validation

### 7.1 Known Answer Tests (KAT)

All AES operations are validated against NIST FIPS 197 test vectors at
manufacturing time and during self-test at each power-up. The KAT suite includes:

- 128 known plaintext/ciphertext pairs for each key size
- Variable-text tests for CTR and GCM modes
- GCM test vectors from NIST SP 800-38D including adversarial examples

### 7.2 Power Analysis Evaluation

The AES accelerator undergoes Differential Power Analysis (DPA) evaluation using
a statistical test suite with at least 10,000 traces. The test confirms that the
masked implementation provides sufficient leakage attenuation (target: > 80 dB
Signal-to-Noise ratio degradation compared to unmasked implementation).

### 7.3 Fuzzing and Edge Cases

The firmware AES API is fuzzed with:

- Block-aligned and non-aligned data sizes
- Zero-length inputs and single-byte inputs
- Maximum telemetry buffer sizes (64 KB)
- Concurrent DMA and CPU access patterns
- Interrupt-driven operation with preemption at every cycle boundary

## 8. Summary

AES encryption provides the fundamental data protection mechanism for the iPACE-CHIP
implantable pacemaker. Through careful selection of operating modes (GCM for
authenticated telemetry, CBC for stored data, CMAC for integrity), hardware
acceleration with side-channel countermeasures, and a robust key hierarchy anchored
in a device root key, the system achieves medical-grade confidentiality while
respecting the tight power and computational budget of an implantable device.

The cryptographic agility framework ensures that the iPACE-CHIP can adapt to
evolving threats, including the eventual transition to post-quantum symmetric
primitives as standards emerge.
