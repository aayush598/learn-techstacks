# Fault Attack Protection for iPACE-CHIP

## Overview

Fault attacks manipulate the physical operating conditions of an integrated
circuit — voltage, clock frequency, temperature, or electromagnetic fields —
to induce computational errors that can reveal secret information or bypass
security checks. For the iPACE-CHIP implantable pacemaker, fault attacks pose
a serious threat because an induced error during cryptographic operations could
expose patient data or therapy parameters, or bypass authentication to allow
unauthorized device control. This chapter covers the fault threat model,
detection mechanisms, and protective countermeasures.

## 1. Fault Attack Taxonomy

### 1.1 Fault Injection Methods

| Method | Mechanism | Equipment Required | Precision |
|--------|-----------|-------------------|-----------|
| Voltage glitching | Brief voltage deviation | Pulse generator | Nanoseconds |
| Clock glitching | Extra/missing clock pulse | External oscillator | Nanoseconds |
| Laser fault injection | Photon-induced current | Pulsed laser (532nm) | Micrometers |
| EM fault injection | Induced eddy currents | EM pulse coil | Millimeters |
| Thermal fault | Localized heating | Focused laser/heat | Micrometers |
| Body bias manipulation | Substrate voltage change | Probe station | Nanometers |

### 1.2 Fault Types

| Fault Type | Effect | Detection Difficulty |
|-----------|--------|---------------------|
| Stuck-at-0 | Bit permanently 0 | Medium |
| Stuck-at-1 | Bit permanently 1 | Medium |
| Bit flip | Single bit transition | Medium |
| Byte skip | Operation skipped entirely | High |
| Delay fault | Slow transition | High |
| Multiple bit flip | Multiple bits affected | Medium |

### 1.3 Fault Targets in iPACE-CHIP

| Target | Attack Goal | Potential Impact |
|--------|-----------|-----------------|
| AES S-Box | Recover key bits | Key compromise |
| AES MixColumns | Bypass diffusion | Simplified cryptanalysis |
| ECDSA scalar multiplication | Recover private key | Signature forgery |
| RSA exponentiation | CRT fault attack | Private key recovery |
| Hash function | Collision creation | Integrity bypass |
| Secure boot check | Skip verification | Firmware substitution |
| Authentication check | Bypass authentication | Unauthorized access |
| Tamper response | Prevent zeroization | Key preservation |

## 2. Voltage Glitching Protection

### 2.1 Voltage Glitch Threat

Voltage glitching involves briefly changing the supply voltage to cause
computational errors:

Attack Mechanism:
1. Monitor power consumption for crypto operation start
2. Inject voltage glitch (typically 10-30% deviation, 1-10 nanoseconds)
3. Glitch causes specific instruction to produce wrong result
4. Analyze output to extract key information

Common Targets:
- Comparison operations (e.g., MAC verification → always pass)
- Conditional branches (e.g., if-else → always take one path)
- Modular reduction (e.g., r = x mod n → force r = 0)

### 2.2 Voltage Supervisor Protection

The iPACE-CHIP includes a dedicated voltage supervisor:

Voltage Supervisor Specifications:
- Monitoring: VDD_CORE (1.0V), VDD_IO (1.8V), VBAT (2.0-3.6V)
- Detection threshold: plus or minus 5% of nominal
- Response time: less than 10 nanoseconds
- Glitch detection: transient greater than 10% in less than 10 nanoseconds
- Response: immediate tamper alarm, zeroize volatile keys

### 2.3 Redundant Computation

Critical security operations use redundant computation to detect faults:

Dual Computation:
```
Operation: result = f(input)

Protected Operation:
  result_1 = f(input)
  result_2 = f(input)
  if result_1 != result_2:
    → fault detected
    → abort operation
    → log fault event
  else:
    → result = result_1
```

Triple Modular Redundancy (TMR):
```
Protected Operation:
  result_1 = f(input)
  result_2 = f(input)
  result_3 = f(input)
  if majority agree:
    → result = majority value
  else:
    → fault detected, abort
```

Applied Operations:
- AES round computation: TMR
- ECDSA point multiplication: dual computation
- Signature verification: dual computation
- Boot hash verification: triple computation
- MAC verification: dual computation

### 2.4 Voltage Glitch Detection Timing

Detection latency analysis:

| Glitch Duration | Detection | Key Protected |
|-----------------|-----------|---------------|
| Greater than 10 ns | Detected by supervisor | Yes |
| 5-10 ns | Detected by redundancy | Yes |
| 1-5 ns | Detected by redundancy | Yes |
| Less than 1 ns | Too small to affect logic | N/A |

Total protection: all glitches that could cause logical errors are detected.

## 3. Clock Glitching Protection

### 3.1 Clock Glitch Threat

Clock glitching involves inserting extra clock pulses or removing expected
pulses:

Attack Mechanism:
1. Synchronize external clock with device clock
2. Insert extra rising edge during critical operation
3. Extra edge causes register to capture wrong value
4. Or: remove clock edge to skip operation

Common Targets:
- Counter increment (skip increment → repeat loop)
- Memory write (skip write → prevent zeroization)
- Conditional check (skip check → take wrong branch)

### 3.2 Clock Monitoring

The iPACE-CHIP implements continuous clock monitoring:

Clock Monitor Features:
- Primary clock: 24 MHz crystal oscillator
- Monitoring clock: independent 32.768 kHz oscillator
- Frequency measurement: count primary cycles per monitoring cycle
- Expected count: 24,000,000 / 32,768 = 732.42 per monitoring period
- Tolerance: plus or minus 1 clock cycle

Detection:
- Missing clock cycle: count less than expected
- Extra clock cycle: count greater than expected
- Clock frequency deviation: count outside tolerance
- Response: immediate tamper alarm

### 3.3 Dual Clock Domain

Critical operations use two independent clock domains:

Dual Clock Architecture:
- Domain A: Primary 24 MHz oscillator
- Domain B: Secondary 16 MHz ring oscillator
- Cross-check: both domains execute same operation
- Result comparison: must agree within 1 cycle

Benefits:
- Clock glitch on Domain A: Domain B detects (correct result)
- Clock glitch on Domain B: Domain A detects (correct result)
- Both domains glitched simultaneously: extremely difficult
- Frequency difference prevents synchronized attacks

### 3.4 Clock Glitch Detection Latency

| Glitch Type | Detection Time | Method |
|-------------|---------------|--------|
| Missing pulse | 1 clock cycle (42 ns) | Counter comparison |
| Extra pulse | 1 clock cycle (42 ns) | Counter comparison |
| Frequency shift | 1 monitoring period (31 us) | Frequency measurement |
| Complete halt | 2 clock cycles (84 ns) | Watchdog timeout |

## 4. Laser Fault Injection Protection

### 4.1 Laser Fault Threat

Laser fault injection uses focused laser beams to induce current in silicon:

Attack Mechanism:
1. Remove package (decapsulation) to expose die
2. Focus pulsed laser (532 nm typical) on target transistor
3. Laser pulse generates electron-hole pairs
4. Induced current flips bit in memory cell or register
5. Repeat with controlled timing to extract keys

Laser Parameters:
- Wavelength: 532 nm (green) or 1064 nm (IR)
- Pulse energy: 0.1 to 10 nanojoules
- Pulse duration: 1 to 100 nanoseconds
- Spot size: 0.5 to 5 micrometers
- Repetition rate: 1 to 100 kHz

### 4.2 Light Sensor Detection

The iPACE-CHIP photodiode array detects laser attacks:

Detection Mechanism:
- 8 photodiodes across die surface
- Sensitivity: 1 microwatt per square centimeter
- Response time: less than 10 nanoseconds
- Laser wavelength: 400-1100 nm (covers common laser wavelengths)

Detection Process:
1. Laser pulse generates photon flux
2. Photodiode generates photocurrent
3. Comparator detects current above threshold
4. Tamper signal asserted within 10 nanoseconds
5. Key zeroization begins immediately

### 4.3 Redundant Logic Protection

Even if a laser flips a bit, redundant logic prevents exploitation:

TMR for Critical Registers:
- 3 copies of each critical register
- Majority voter on read
- Bit flip in 1 register: corrected by majority
- Bit flip in 2 registers: detected (no majority)
- Bit flip in 3 registers: extremely unlikely (different physical locations)

Spatial Separation:
- Register copies placed at different die locations (greater than 50 micrometers apart)
- Single laser spot (5 micrometers) cannot hit 2 copies simultaneously
- Requires multiple precisely-targeted laser shots (increasingly difficult)

### 4.4 Laser Fault Countermeasure Effectiveness

| Attack Scenario | Countermeasure | Protection Level |
|----------------|----------------|-----------------|
| Single bit flip in AES | Masking + redundancy | Complete |
| Single bit flip in ECDSA | Redundant computation | Complete |
| Byte skip in operation | Dual computation + timing | Complete |
| Multiple bit flips | TMR + light detection | Complete |
| Targeted register flip | Spatial separation + TMR | Complete |

## 5. EM Fault Injection Protection

### 5.1 EM Fault Threat

Electromagnetic fault injection uses pulsed EM fields to induce currents:

Attack Mechanism:
1. Position EM coil near die surface
2. Generate high-power EM pulse (10-100 MHz)
3. EM pulse induces eddy currents in on-chip conductors
4. Induced currents cause bit flips or logic errors
5. Can be performed through package (non-invasive)

EM Fault Parameters:
- Frequency: 10-500 MHz
- Pulse duration: 10-100 nanoseconds
- Field strength: 1-10 Tesla at die surface
- Coil-to-die distance: 1-10 millimeters

### 5.2 EM Sensor Detection

The on-chip EM sensor detects fault injection attempts:

Detection:
- Pickup coil: on-chip spiral inductor (10 turns)
- Sensitivity: 1 millivolt per meter
- Frequency range: 1 MHz to 1 GHz
- Response time: less than 50 nanoseconds

Detection Process:
1. EM fault pulse detected by pickup coil
2. Comparator detects field above threshold
3. Tamper signal asserted
4. Key zeroization initiated
5. Operation aborted

### 5.3 EM Shielding

Physical shielding reduces EM fault effectiveness:

Shielding Layers:
- Titanium enclosure: 20-40 dB attenuation (1-100 MHz)
- Internal copper foil: additional 20 dB
- Guard ring: substrate current containment
- Total shielding: 40-60 dB

Effect on EM Fault:
- Required field strength increases by 100-1000x
- Coil must be closer (thinner package)
- Pulse energy must be higher (more detectable)
- Combined with detection: EM faults become impractical

### 5.4 Redundant Computation

Same dual/TMR approach as voltage glitch protection:
- All critical operations use redundant computation
- Results compared before use
- Mismatch triggers tamper response
- Effective against EM faults that affect only one computation

## 6. Software-Based Fault Protection

### 6.1 Infection and Verification

The infection technique delays error propagation to enable detection:

Concept:
1. Execute operation normally
2. Insert deliberate redundant check BEFORE using result
3. If fault detected: result not yet used (safe)
4. If no fault: result can be used

Application to AES:
```
After each round:
  1. Compute expected round output (independent path)
  2. Compare with actual round output
  3. If match: proceed
  4. If mismatch: fault detected, abort
  5. Comparison is constant-time (no timing leak)
```

### 6.2 Random Delay Insertion

Random delays complicate fault timing:

Technique:
- Insert random number of NOP instructions before critical operations
- Random delay: 0 to 255 clock cycles
- Generated from TRNG
- Prevents attacker from knowing exact timing for fault injection

Effectiveness:
- Increases attacker's required shots by factor of 128 (average)
- Does not protect against continuous EM fault (always-on)
- Combined with detection: makes fault injection impractical

### 6.3 Polynomial Checksum

Critical data protected by polynomial checksums:

Technique:
- Compute CRC-32 or polynomial hash over critical data
- After operation, recompute and compare
- Mismatch indicates data corruption (fault or otherwise)
- Applied to: key material, therapy parameters, boot verification data

### 6.4 Sign-Verify Pattern

For digital signatures, the sign-verify pattern catches faults:

```
Sign-Verify Pattern:
  1. Compute signature: (r, s) = Sign(message, key)
  2. Immediately verify: Verify(message, pub_key, (r, s))
  3. If verification fails: fault during signing
  4. Retry signing (with new random nonce)
  5. Maximum retries: 3
  6. If all retries fail: enter safe mode
```

## 7. Countermeasure Integration

### 7.1 Protection Level by Operation

| Operation | Voltage | Clock | Laser | EM | Software |
|-----------|---------|-------|-------|----|----|
| AES encryption | Supervisor + redundancy | Monitor + dual domain | Light + TMR | Sensor + redundancy | Infection |
| AES key schedule | Supervisor + redundancy | Monitor + dual domain | Light + TMR | Sensor + redundancy | Infection |
| ECDSA signing | Supervisor + redundancy | Monitor + dual domain | Light + TMR | Sensor + redundancy | Sign-verify |
| ECDH key exchange | Supervisor + redundancy | Monitor + dual domain | Light + TMR | Sensor + redundancy | Infection |
| Hash computation | Supervisor | Monitor | Light | Sensor | Checksum |
| Boot verification | Supervisor + redundancy | Monitor + dual domain | Light + TMR | Sensor + redundancy | Triple check |
| MAC verification | Supervisor + redundancy | Monitor | Light + TMR | Sensor | Dual check |
| Key zeroization | Supervisor | Monitor | Light | Sensor | Verification |

### 7.2 Performance Impact

| Countermeasure | Area Overhead | Power Overhead | Timing Overhead |
|---------------|---------------|----------------|-----------------|
| Voltage supervisor | 1.2K GE | 0.5 uW | 0 cycles |
| Clock monitor | 800 GE | 0.3 uW | 0 cycles |
| Light sensor | 600 GE | 0.2 uW | 0 cycles |
| EM sensor | 400 GE | 0.1 uW | 0 cycles |
| Dual computation | 100% per operation | 2x power | 2x time |
| TMR | 200% per operation | 3x power | 3x time |
| Random delays | 200 GE | Negligible | 0-255 cycles |
| Polynomial checksum | 400 GE | Negligible | 2 cycles |
| **Total overhead** | **3.6K GE + redundancy** | **Depends on usage** | **Depends on usage** |

### 7.3 Area Budget

Total fault protection area:
- Sensor circuits: 3.0K GE (1.5% of total die)
- Redundancy for crypto: 8.4K GE (4.2% of total die)
- Checksum circuits: 0.6K GE (0.3% of total die)
- Total: 12.0K GE (6.0% of total die area)

This area overhead is acceptable for a life-critical implant where
fault attack resistance is mandatory.

## 8. Evaluation and Testing

### 8.1 Fault Injection Testing

The iPACE-CHIP undergoes comprehensive fault injection evaluation:

Test Categories:

1. Voltage Glitch Testing:
   - Glitch amplitudes: 5% to 30% of nominal voltage
   - Glitch durations: 1 ns to 100 ns
   - Glitch timing: synchronized to clock edges
   - Target: all security-critical operations

2. Clock Glitch Testing:
   - Extra pulses: 1 to 10
   - Missing pulses: 1 to 10
   - Frequency shifts: plus or minus 10%
   - Target: all security-critical operations

3. Laser Fault Testing:
   - Energy levels: 0.1 to 10 nJ
   - Spot positions: systematic scan across die
   - Wavelengths: 532 nm, 1064 nm
   - Target: KMU, crypto engine, OTP

4. EM Fault Testing:
   - Field strengths: 0.1 to 10 Tesla
   - Frequencies: 10 MHz to 500 MHz
   - Coil positions: multiple angles
   - Target: all security-critical blocks

### 8.2 Evaluation Results

| Fault Method | Attempts | Successful Faults | Key Extracted |
|-------------|----------|-------------------|---------------|
| Voltage glitch | 100,000 | 0 exploitable | No |
| Clock glitch | 100,000 | 0 exploitable | No |
| Laser (532 nm) | 50,000 | 0 (detected by light sensor) | No |
| EM fault | 50,000 | 0 (detected by EM sensor) | No |

Assessment: All tested fault injection methods are prevented by the
combination of detection and redundant computation countermeasures.

### 8.3 Continuous Monitoring

Runtime fault detection provides ongoing protection:

Self-Test Suite:
- Voltage supervisor test: at boot and every 60 seconds
- Clock monitor test: at boot and every 60 seconds
- Light sensor test: at boot (controlled LED)
- Redundancy check: during every crypto operation
- Polynomial check: during every data transfer

If self-test fails:
- Log fault detection anomaly
- Increase monitoring frequency
- Alert clinician if persistent
- Consider device replacement if hardware fault

## 9. Compliance

| Standard | Requirement | Status |
|----------|-------------|--------|
| FIPS 140-3 Level 2 | Fault attack resistance | Compliant |
| Common Criteria EAL4+ | Fault injection protection | Evaluated |
| IEC 62443-4-2 | Physical attack protection | Compliant |
| IEC 60601-1 | Electrical safety (no induced faults) | Compliant |
| FDA Cybersecurity | Physical security measures | Compliant |

## 10. Summary

The iPACE-CHIP implements comprehensive fault attack protection through
multiple independent countermeasures. Voltage supervisors and clock monitors
detect electrical fault injection within nanoseconds. Light and EM sensors
detect laser and electromagnetic fault injection attempts. Redundant computation
(dual and TMR) ensures that even undetected faults produce correct results or
are caught by comparison. Software-based techniques including infection, random
delays, and polynomial checksums provide additional protection layers. Evaluation
with 300,000+ fault injection attempts across all methods confirmed that no
exploitable faults can be induced. The combined protection area overhead of
6% is well within the iPACE-CHIP die budget, and the performance impact is
minimal for the fault-tolerant operations.
