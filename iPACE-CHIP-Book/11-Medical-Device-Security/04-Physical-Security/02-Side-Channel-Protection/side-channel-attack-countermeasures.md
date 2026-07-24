# Side-Channel Attack Countermeasures for iPACE-CHIP

## Overview

Side-channel attacks exploit physical information leaked during cryptographic
operations — timing variations, power consumption patterns, electromagnetic
emanation, and even acoustic signals — to extract secret keys without breaking
the mathematical strength of the algorithm. For an implantable pacemaker like
the iPACE-CHIP, side-channel resistance is critical because the device operates
continuously in a potentially hostile environment. This chapter covers the
specific side-channel threats, countermeasure implementations, and evaluation
methodologies for the iPACE-CHIP security architecture.

## 1. Side-Channel Threat Landscape

### 1.1 Attack Types

| Attack Type | Information Source | Required Access | Difficulty |
|------------|-------------------|-----------------|------------|
| Simple Power Analysis (SPA) | Power trace shape | Power measurement | Low |
| Differential Power Analysis (DPA) | Power-data correlation | Statistical analysis | Medium |
| Correlation Power Analysis (CPA) | Power correlation | Statistical analysis | Medium |
| Electromagnetic Analysis (EMA) | EM emanation | EM probe | Medium |
| Differential EMA (DEMA) | EM correlation | Statistical analysis | Medium |
| Timing Analysis | Execution time | Precise timer | Low |
| Cache Timing | Cache hit/miss patterns | Shared cache | High (not applicable) |
| Acoustic Analysis | Sound emanation | Microphone | High (not applicable) |

### 1.2 Applicability to iPACE-CHIP

| Attack | Applicability | Risk Level | Primary Countermeasure |
|--------|--------------|------------|----------------------|
| SPA | Direct measurement of implant | High | Masking + shuffling |
| DPA | Requires many traces | High | Boolean masking |
| CPA | Requires many traces | High | Boolean masking |
| EMA | EM probe near patient | Medium | Shielding + masking |
| Timing | Remote measurement possible | High | Constant-time implementation |
| Cache | Not applicable (no cache) | N/A | N/A |
| Acoustic | Not applicable (no sound) | N/A | N/A |

### 1.3 Measurement Setup

Side-channel measurements against the iPACE-CHIP would typically involve:

Power Analysis Setup:
- Shunt resistor: 1 ohm, in series with battery
- Oscilloscope: 1 GHz bandwidth, 5 GS/s
- Probe: Differential voltage probe
- Trigger: RF trigger from programmer
- Number of traces: 10,000 to 1,000,000

EM Analysis Setup:
- EM probe: Near-field, 100 kHz to 6 GHz
- Amplifier: Low-noise, 40 dB gain
- Oscilloscope: Same as power analysis
- Positioning: Near die surface (requires package thinning)

Timing Analysis Setup:
- Measurement: RF signal strength indicator
- Method: Measure time between known trigger and response
- Precision: 100 nanoseconds (sufficient for AES round counting)
- Non-contact: Can be performed without physical access

## 2. Power Analysis Countermeasures

### 2.1 First-Order Boolean Masking

Boolean masking randomizes intermediate values during computation, decorrelating
power consumption from secret data:

Masking Principle:
For an operation f(x, k) where k is secret:
1. Generate random mask m
2. Compute x' = x XOR m
3. Compute f'(x', k') = f(x, k) XOR m (where k' is masked key)
4. Output = f'(x', k') XOR m = f(x, k)

The attacker sees f' operating on masked values, which are uncorrelated with
the actual intermediate values.

AES S-Box Masking:
```
Unmasked: output = Sbox[input XOR key]
Masked:
  1. Generate random mask r (8 bits)
  2. Compute masked_input = input XOR key XOR r
  3. Compute masked_output = Sbox[masked_input] (using precomputed masked table)
  4. Apply linear correction to remove mask
  5. Final output = Sbox[input XOR key]
```

Masking in Hardware:
The iPACE-CHIP AES accelerator uses first-order Boolean masking with:
- 8-bit random masks refreshed every operation
- Masked S-Box lookup using dual-rail logic
- Masked GF(2^8) multiplication for MixColumns
- Computation in both original and masked domains simultaneously

### 2.2 Higher-Order Masking

First-order masking protects against first-order attacks but may be vulnerable
to second-order DPA. The iPACE-CHIP implements second-order masking for
high-security operations:

Second-Order Masking:
- Two independent masks per intermediate value
- Requires combining two separate power measurements
- Increases attacker complexity from O(N) to O(N^2) traces
- Applied to: ECDSA signing, ECDH key exchange

### 2.3 Shuffling Countermeasure

Shuffling randomizes the order of independent operations:

AES Round Shuffling:
```
Standard order: SubBytes, ShiftRows, MixColumns, AddRoundKey
Shuffled order: Permutation of {0,1,2,3} for column processing
  - 4! = 24 possible orderings
  - Random permutation selected per round
  - Prevents SPA from identifying round structure
```

Point Multiplication Shuffling (ECC):
```
Randomized addition chain:
  k = sum of {2^i * k_i} where k_i in {0,1}
  Shuffle: randomize order of point additions
  - Multiple valid addition orders for same scalar
  - Prevents simple power analysis of scalar bits
```

### 2.4 Dual-Rail Logic

Dual-rail logic ensures constant power consumption regardless of data:

WDDL (Wave Dynamic Differential Logic):
- Each signal has complementary pair (P, N)
- Exactly one transitions per clock cycle
- Power consumption: constant (data-independent)
- Area overhead: 2x single-rail

iPACE-CHIP Implementation:
- Applied to: S-Box, GF multiplier, key schedule
- Coverage: All crypto engine datapath
- Power variation: less than 5% (measured)
- Area overhead: 1.8x for masked blocks

## 3. Timing Attack Countermeasures

### 3.1 Constant-Time Implementation

All cryptographic operations on the iPACE-CHIP execute in constant time:

AES Implementation:
- 10 rounds always executed (AES-128)
- No early termination based on data
- S-Box lookup: constant-time combinational logic (no ROM indexing)
- MixColumns: constant-time GF multiplication
- Key schedule: precomputed, no runtime branching

ECDSA Implementation:
- Scalar multiplication: Montgomery ladder (constant-time)
- Modular inversion: Fermat's little theorem (constant-time)
- Point validation: constant-time comparison
- Signature generation: no conditional branches on secret data

### 3.2 Montgomery Ladder for ECC

The Montgomery ladder provides constant-time scalar multiplication:

Standard Scalar Multiplication (VULNERABLE):
```
for i from msb to lsb of k:
  Q = 2 * Q
  if k[i] == 1:
    Q = Q + P    // BRANCH: leaks k[i] via timing
```

Montgomery Ladder (CONSTANT-TIME):
```
R0 = O, R1 = P
for i from msb to lsb of k:
  if k[i] == 0:
    R1 = R0 + R1
    R0 = 2 * R0
  else:
    R0 = R0 + R1
    R1 = 2 * R1
  // No branch: both cases execute same operations
// Result: R0 = k * P
```

Properties:
- Same number of operations regardless of scalar value
- Same memory access pattern regardless of scalar value
- Same power consumption profile regardless of scalar value
- Timing variation: less than 0.1% (measurement noise)

### 3.3 Constant-Time Comparison

All authentication checks use constant-time comparison:

```
Constant-Time Compare(a, b, length):
  result = 0
  for i from 0 to length-1:
    result = result OR (a[i] XOR b[i])
  return (result == 0)

// No early exit: always compares all bytes
// Timing: identical for all inputs
```

## 4. Electromagnetic Countermeasures

### 4.1 EM Shielding

The iPACE-CHIP includes electromagnetic shielding:

Shielding Layers:
- Titanium enclosure: provides 20-40 dB attenuation (1-100 MHz)
- Internal copper foil: additional 20 dB attenuation
- Guard ring grounding: substrate current containment
- Decoupling capacitors: reduce high-frequency emissions

Shielding Effectiveness:
| Frequency | Titanium Only | Titanium + Copper | Total |
|-----------|---------------|-------------------|-------|
| 1 MHz | 20 dB | 40 dB | 40 dB |
| 10 MHz | 30 dB | 50 dB | 50 dB |
| 100 MHz | 40 dB | 60 dB | 60 dB |
| 1 GHz | 20 dB | 40 dB | 40 dB |

### 4.2 EM Noise Generation

An active noise generator creates EM masking:

Noise Generator:
- Type: On-chip ring oscillator array (8 independent)
- Frequency: 10-100 MHz (randomly selected)
- Amplitude: 10 mV at 1 cm distance
- Purpose: Decorrelate EM emanation from computation

Noise Generator Operation:
- Active during all cryptographic operations
- Frequency randomly varied per operation
- Adds approximately 15 dB of EM noise floor
- Requires attacker to average more traces

### 4.3 EM Countermeasure Effectiveness

| Scenario | Traces Required (unprotected) | Traces Required (with countermeasures) |
|----------|-------------------------------|----------------------------------------|
| AES-128 DPA | 10,000 | 1,000,000+ |
| AES-128 CPA | 5,000 | 500,000+ |
| ECDSA scalar recovery | 1,000 | 100,000+ |
| ECDH key recovery | 1,000 | 100,000+ |

## 5. Implementation Details

### 5.1 Masked AES S-Box Hardware

The iPACE-CHIP uses a masked S-Box implemented in hardware:

S-Box Architecture:
- Input: 8-bit masked value + 8-bit mask
- Processing: 4 parallel masked sub-layers
- Output: 8-bit masked output + mask propagation
- Latency: 2 cycles (pipelined)
- Area: 2,400 GE (masked) vs. 800 GE (unmasked)

Mask Refresh:
- New mask generated by TRNG at start of each AES operation
- Mask value never reused across operations
- Mask stored in dedicated register (not accessible to CPU)

### 5.2 Constant-Time ECDSA

ECDSA signing implementation avoids all data-dependent branches:

```
Constant-Time ECDSA Sign(message, private_key):
  1. e = SHA-384(message)
  2. k = deterministic_nonce(private_key, e)  // RFC 6979
  3. (x1, y1) = scalar_multiply(k, G)        // Montgomery ladder
  4. r = x1 mod n                              // Constant-time mod
  5. s = modular_inverse(k) * (e + r * d) mod n // Fermat + constant-time ops
  6. Return (r, s)

  All operations: constant-time, no branches on secret data
  Memory access: sequential, no indexed access with secret data
```

### 5.3 Key Schedule Hardening

The AES key schedule is hardened against side-channel attacks:

Key Schedule Countermeasures:
- Precomputed: all subkeys derived at key setup time
- Encrypted storage: subkeys stored encrypted with random mask
- On-the-fly decryption: subkeys decrypted only when needed
- Zeroization: subkey registers zeroized after use

Timing:
- Key setup: 120 cycles (one-time cost)
- Per-round subkey access: 2 cycles (decryption from masked storage)

## 6. Evaluation and Testing

### 6.1 Side-Channel Evaluation Methodology

The iPACE-CHIP undergoes comprehensive side-channel evaluation:

Evaluation Protocol:
1. Setup: Connect measurement equipment to sample device
2. Capture: Record power/EM traces for 10,000+ operations
3. Analysis: Apply SPA, DPA, CPA, and template attacks
4. Assessment: Determine if key recovery is feasible
5. Iteration: If vulnerable, apply countermeasure and re-evaluate

Evaluation Equipment:
- Oscilloscope: Keysight DSOX6004A (6 GHz, 20 GS/s)
- EM probe: Langer EMV-TECH NI-090
- Power probe: Picotest J2100A
- Analysis software: Custom + ChipWhisperer, ELMO

### 6.2 Test Metrics

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| SPA resistance | No key bits visible in single trace | Visual inspection of traces |
| DPA resistance | t-test p-value > 0.01 | Student's t-test on 10,000 traces |
| CPA resistance | Correlation < 0.03 | Pearson correlation on 10,000 traces |
| Timing variance | < 0.1% across all inputs | Statistical timing measurement |
| EM leakage | SNR < -20 dB | EM measurement at 1 cm |

### 6.3 Evaluation Results

AES-128-GCM:
| Attack | Traces Required | Assessment |
|--------|----------------|------------|
| SPA | Not feasible | PASS |
| DPA (1st order) | 1,000,000+ | PASS |
| DPA (2nd order) | 50,000,000+ | PASS |
| CPA | 500,000+ | PASS |
| Timing | Not feasible | PASS |

ECDSA-P256:
| Attack | Traces Required | Assessment |
|--------|----------------|------------|
| SPA | Not feasible | PASS |
| DPA | 100,000+ | PASS |
| CPA | 80,000+ | PASS |
| Timing | Not feasible | PASS |

### 6.4 Continuous Monitoring

Side-channel resistance is monitored during device operation:

Runtime Checks:
- Power consumption self-test at boot
- Timing self-test (measure operation duration)
- EM emanation baseline check
- Mask quality verification (TRNG output)

If self-test fails:
- Log side-channel anomaly
- Switch to backup implementation (if available)
- Alert clinician
- Disable crypto operations until verified

## 7. Advanced Countermeasures

### 7.1 Threshold Implementation

Threshold implementation provides provable security against first-order masking:

Properties:
- Non-completeness: each share depends on fewer inputs than total
- Correctness: reconstruction produces correct result
- Uniformity: intermediate distributions are uniform

Application:
- GF(2^8) multiplication in AES MixColumns
- Point addition in ECDSA/ECDH
- Provides provable security (not just heuristic)

### 7.2 Shuffled Masking

Shuffled masking combines shuffling with masking for enhanced protection:

Concept:
- Compute multiple masked shares in random order
- Shuffle which share is computed at which time
- Requires attacker to guess both the mask values and the shuffle order

Effectiveness:
- Increases traces required by factor of n! (for n shares)
- With 4 shares: 24x improvement over masking alone
- Combined with masking: 24x * masking improvement

### 7.3 Glitch-Resistant Masking

Glitch-resistant masking maintains security even under voltage/clock glitches:

Technique:
- Higher redundancy: 3 or more shares per value
- Refresh rate: masks refreshed every cycle (not just per operation)
- Threshold: 3-of-5 voting for each share
- Glitch detection: voltage monitor triggers mask refresh

## 8. Compliance

| Standard | Requirement | Status |
|----------|-------------|--------|
| FIPS 140-3 Level 2 | Side-channel resistance | Compliant |
| Common Criteria EAL4+ | SPA/DPA resistance | Evaluated |
| ISO 17825 | Side-channel countermeasures | Compliant |
| IEC 62443-4-2 | Cryptographic implementation security | Compliant |
| NIST SP 800-90B | TRNG for mask generation | Compliant |

## 9. Summary

The iPACE-CHIP implements comprehensive side-channel attack countermeasures
covering power analysis, timing analysis, and electromagnetic emanation. First-
and second-order Boolean masking randomizes intermediate values in all crypto
operations. Constant-time implementations using Montgomery ladder and fixed-
operation AES prevent timing attacks. EM shielding and active noise generation
reduce electromagnetic leakage. Hardware-accelerated masked S-Boxes and dual-rail
logic provide provable side-channel resistance. Evaluation against SPA, DPA,
CPA, and timing attacks confirms that key recovery requires more traces than
practically obtainable, meeting the requirements of FIPS 140-3 Level 2 and
Common Criteria EAL4+.
