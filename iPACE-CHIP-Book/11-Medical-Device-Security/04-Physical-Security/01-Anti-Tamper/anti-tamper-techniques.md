# Anti-Tamper Techniques for iPACE-CHIP

## Overview

Anti-tamper techniques complement tamper detection by actively preventing or
deterring physical attacks on the iPACE-CHIP implantable pacemaker. While tamper
detection identifies intrusion attempts, anti-tamper measures make successful
intrusion more difficult, time-consuming, and expensive. This chapter covers
physical hardening, packaging security, environmental monitoring, and the layered
defense strategy that protects the device against physical compromise.

## 1. Anti-Tamper Strategy

### 1.1 Defense-in-Depth Layers

The iPACE-CHIP implements six concentric layers of physical protection:

Layer 1: Outer Package
- Titanium hermetic enclosure
- Medical-grade biocompatible coating
- Laser-welded seams
- Serial number engraving (tamper-evident)

Layer 2: Internal Potting
- Medical-grade epoxy encapsulation
- Opacious to visible and IR light
- Thermally conductive
- Chemically resistant

Layer 3: Active Shield Mesh
- Dual-layer conductive mesh (top and bottom metal)
- Continuous AC monitoring
- 16 independent segments
- Covers 98.5% of die area

Layer 4: Die-Level Protection
- Guard rings around sensitive circuits
- Tamper sensors (light, EM, temperature)
- Redundant logic for critical functions
- Bus encryption for internal data paths

Layer 5: Logical Protection
- Memory Protection Unit (MPU)
- Secure boot and runtime integrity
- Key zeroization on tamper
- Debug port fuse protection

Layer 6: Cryptographic Protection
- Encrypted key storage
- Hardware security module
- Side-channel resistant implementations
- Constant-time algorithms

### 1.2 Anti-Tamper Design Principles

Principle 1: Deterrence
Make the device visibly difficult to attack, discouraging opportunistic attempts.

Principle 2: Delay
Increase the time required for successful attack, allowing detection and response.

Principle 3: Detection
Identify attack attempts through multiple independent sensor mechanisms.

Principle 4: Response
React proportionally to detected attacks, from logging to key destruction.

Principle 5: Denial
Ensure that even successful physical access does not yield useful information.

## 2. Physical Package Security

### 2.1 Titanium Enclosure

The iPACE-CHIP uses a Grade 23 titanium alloy (Ti-6Al-4V ELI) enclosure:

Enclosure Specifications:
- Wall thickness: 0.4 millimeters
- Dimensions: 42 millimeters x 36 millimeters x 6 millimeters
- Weight: 18 grams (including electronics)
- Surface finish: Electropolished (Ra less than 0.2 micrometers)
- Hermeticity: Helium leak rate less than 10^-9 atmospheres per cubic centimeter per second

Tamper Resistance Properties:
- Hardness: 340 HV (Vickers) - resists scratching and drilling
- Melting point: 1660 degrees Celsius - resists thermal attacks
- Chemical resistance: Immune to body fluids, common solvents
- Weld integrity: Laser-welded seams, X-ray verifiable

Tamper-Evident Features:
- Laser engraving: Serial number,UDI, manufacturer mark
- Micro-engraving: 50-micrometer features visible only under microscope
- Weld inspection: Each weld bead photographed and stored
- Any physical modification visible under routine inspection

### 2.2 Medical-Grade Encapsulation

Internal encapsulation provides additional physical protection:

Encapsulation Material:
- Type: Medical-grade silicone epoxy (USP Class VI)
- Thermal conductivity: 1.5 W/(m*K)
- Dielectric constant: 3.5 at 1 MHz
- Operating range: -40 to +85 degrees Celsius
- Biocompatibility: ISO 10993 compliant

Protection Properties:
- Opacious: Blocks visible, UV, and near-IR light
- Chemical resistant: Protects against solvents and acids
- Mechanically rigid: Prevents microprobing needle access
- Thermally conductive: Distributes heat from external sources

Tamper Indicators:
- Encapsulant discoloration under UV exposure (attacks visible)
- Crack propagation patterns indicate force application
- Moisture ingress changes dielectric properties (detectable)

### 2.3 Feedthrough Security

Electrical feedthroughs for the pacing leads are potential attack vectors:

Feedthrough Protection:
- Hermetic ceramic-to-metal seals
- Individual lead isolation (no shared ground path)
- Series resistance: 10 kilohms per lead (limits probe current)
- ESD protection: 15 kilovolt rating
- Filtering: 100 kilohertz low-pass (rejects RF injection)

Lead Monitoring:
- Impedance measurement: continuous (detects probe insertion)
- Current monitoring: detects unauthorized current injection
- Voltage monitoring: detects voltage injection attacks
- Differential measurement: rejects common-mode interference

## 3. Die-Level Anti-Tamper

### 3.1 Guard Rings

Sensitive circuit blocks are surrounded by protective guard rings:

Guard Ring Specifications:
- Material: N+ diffusion ring connected to VDD
- Width: 5 micrometers
- Spacing: 2 micrometers from protected circuitry
- Purpose: Collects substrate currents from probing attempts

Protected Regions:
- Key Management Unit: full guard ring enclosure
- True Random Number Generator: full guard ring enclosure
- Crypto accelerator: full guard ring enclosure
- OTP memory: full guard ring enclosure
- Boot ROM: full guard ring enclosure

### 3.2 Bus Encryption

Internal data buses between sensitive blocks are encrypted:

Bus Encryption Parameters:
- Algorithm: Lightweight stream cipher (ASCON-128)
- Key: Derived from DRK, refreshed every 64 kilobytes
- Overhead: 2 cycles latency per bus transaction
- Coverage: All buses connecting KMU, crypto engine, OTP

Benefits:
- Bus snooping yields encrypted data
- Microprobe on bus captures ciphertext only
- Key for bus encryption never on bus
- Physical access to bus does not compromise keys

### 3.3 Logic Hardening

Critical logic blocks are hardened against reverse engineering:

Obfuscation Techniques:
- Redundant logic gates: decoy circuits with no function
- Camouflaged gates: identical layout for different functions
- Delay insertion: random delays prevent timing analysis
- Clock domain crossing: multiple independent clock domains

Randomization Techniques:
- Random placement: sensitive blocks randomly placed per chip
- Random routing: critical signal routes randomized
- Dummy metal fills: prevent SEM-based layout extraction
- Fill patterns: non-functional metal patterns obscure real layout

### 3.4 Redundant Logic for Safety-Critical Functions

Safety-critical functions use redundant logic with voter circuits:

Triple Modular Redundancy (TMR):
- Three independent copies of safety-critical logic
- Majority voter determines output
- Any single fault tolerated
- Used for: therapy control, safety monitor, watchdog

Dual Modular Redundancy (DMR):
- Two independent copies with comparison
- Mismatch triggers safe state
- Used for: timer, voltage monitor, communication controller

## 4. Environmental Monitoring

### 4.1 Comprehensive Sensor Array

The iPACE-CHIP includes a comprehensive environmental monitoring system:

Sensor Summary:
- Temperature: 2 sensors (die center, periphery)
- Voltage: 4 rails monitored
- Current: 1 supply current sensor
- Light: 8 photodiodes
- EM field: 1 pickup coil
- Pressure: 1 MEMS pressure sensor (package internal)
- Humidity: 1 capacitive humidity sensor
- Acceleration: 3-axis MEMS accelerometer
- Active mesh: 16 impedance channels
- Total: 37 sensor channels

### 4.2 Environmental Baseline

During manufacturing, each iPACE-CHIP records its environmental baseline:

Baseline Parameters:
- Normal temperature range: 35 to 40 degrees Celsius (in body)
- Normal voltage range: 2.8 to 3.4 volts (battery)
- Normal current: 50 to 200 microamps
- Normal pressure: 760 mmHg (atmospheric)
- Normal humidity: 0% (hermetic package)
- Normal acceleration: less than 0.5g (stationary)

Any deviation from baseline that cannot be explained by normal operation
triggers investigation.

### 4.3 Attack Environment Detection

Certain environmental conditions indicate attack attempts:

Attack Indicators:
- Temperature outside body range: device outside patient
- Pressure below 600 mmHg: partial vacuum (lab environment)
- Humidity above 0%: hermetic seal breach
- Acceleration above 10g: device being handled roughly
- Light detected: package opened or thinned
- EM field anomaly: probe or coil nearby
- Voltage outside battery range: external power applied
- Current above 5 milliamps: external current injection

Multi-Sensor Correlation:
Multiple simultaneous anomalies increase confidence in tamper assessment.
For example, low pressure AND humidity above 0% strongly indicates
package breach (decapsulation attempt).

## 5. Anti-Reverse Engineering

### 5.1 Layout Obfuscation

The iPACE-CHIP layout incorporates multiple obfuscation techniques:

Standard Cell Obfuscation:
- Camouflaged standard cells: same physical layout for different functions
- Example: NAND, NOR, AND gates share identical layout
- Function determined by buried contact (not visible in SEM)
- Reverse engineering requires cross-sectioning (destructive)

Metal Layer Obfuscation:
- Dummy vias: non-connected via structures
- Redundant metal: overlapping metal layers
- Non-functional fills: random patterns between functional wires
- Grid-aligned fills: prevent pattern-based extraction

### 5.2 Design Obfuscation

RTL-level obfuscation complicates logical reverse engineering:

Techniques Applied:
- State machine obfuscation: unreachable states added
- Signal renaming: internal signals use non-descriptive names
- Module flattening: hierarchy removed in synthesis
- Logic locking: additional gates controlled by key input

Design Flow:
1. Original RTL written with descriptive names
2. Obfuscation tool applies transformations
3. Physical design with obfuscation
4. Manufacturing with obfuscated layout
5. De-obfuscation key stored in OTP (not accessible externally)

### 5.3 Anti-Decapsulation Measures

The iPACE-CHIP includes features that resist decapsulation:

Chemical Resistance:
- Encapsulant resistant to fuming nitric acid (standard decap chemical)
- Requires hot sulfuric acid at 300 degrees Celsius (more aggressive)
- Titanium package requires mechanical removal first

Laser-Based Decap Countermeasures:
- Opaque encapsulant blocks UV and visible laser wavelengths
- Thermal dissipation prevents localized melting
- Mesh monitoring detects laser beam presence

Mechanical Decap Countermeasures:
- Hardened package resists grinding and milling
- Titanium shell requires specialized cutting tools
- Any package modification visible under inspection

## 6. Tamper-Evident Packaging

### 6.1 Tamper-Evident Seals

The iPACE-CHIP packaging includes multiple tamper-evident features:

External Tamper Evidence:
- Weld bead continuity: visible breaks indicate re-welding
- Surface finish: any grinding/polishing alters electropolish
- Laser engraving depth: modification changes engraving profile
- Serial number location: unique per-unit positioning

Internal Tamper Evidence:
- Encapsulant flow patterns: unique per unit (like a fingerprint)
- Wire bond routing: slight variations detect rework
- Die placement: precise location recorded during manufacturing
- Marking alignment: laser marks on die and package

### 6.2 Manufacturing Records

Each iPACE-CHIP has a complete manufacturing record:

Recorded Parameters:
- Die photograph (multiple angles, multiple wavelengths)
- Package dimensions (measured to micrometer precision)
- Weld bead profile (3D scan)
- Encapsulant flow pattern (X-ray)
- Wire bond routing (X-ray)
- Electrical test results (all parameters)
- Tamper sensor baselines (all 37 channels)

Storage:
- Encrypted and signed by manufacturer
- Stored in manufacturer database (15-year retention)
- Hash of record stored in device OTP
- Retrieval for forensic comparison after suspected tamper

### 6.3 Authentication of Packaging

Programmers can verify packaging integrity at each session:

Packaging Verification:
1. NFC-based measurement of package resonant frequency
2. Comparison with stored baseline (in device firmware)
3. Deviation indicates physical modification
4. Warning if deviation exceeds threshold
5. Tamper response if deviation indicates attack

Limitations:
- Requires programmer (not continuous monitoring)
- Cannot detect all modifications
- Provides evidence, not prevention

## 7. Secure Manufacturing

### 7.1 Foundry Security

The iPACE-CHIP is manufactured in a secure foundry:

Foundry Requirements:
- Trusted foundry certification (e.g., DMEA-accredited)
- Personnel vetting (background checks, access control)
- Clean room access: biometric + badge
- Camera monitoring: all fabrication areas
- Material tracking: lot-level traceability
- Waste management: all silicon waste destroyed

### 7.2 Mask Security

Photolithography masks are protected:

Mask Protection:
- Stored in secure vault when not in use
- Access logged and audited
- Masks serialized and tracked
- Duplicate detection (unique per mask set)
- End-of-life destruction verified

### 7.3 Supply Chain Integrity

| Stage | Security Measure | Verification |
|-------|-----------------|--------------|
| Wafer fabrication | Clean room access control | Access logs |
| Die testing | Automated test equipment | Test results logged |
| Packaging | Secure facility | Camera monitoring |
| Final test | Parametric verification | Results compared to baseline |
| Programming | Secure OTP station | Audit trail |
| Distribution | Tamper-evident packaging | Seal verification |

## 8. Tamper Response Policy

### 8.1 Response Escalation

```
Escalation Matrix:

Level 1 (Informational):
  Trigger: Single sensor anomaly, explainable
  Action: Log event, continue monitoring
  Example: Temperature spike during exercise

Level 2 (Elevated):
  Trigger: Two sensor anomalies, or single persistent anomaly
  Action: Log event, alert patient controller, increase monitoring
  Example: Acceleration spike with current anomaly

Level 3 (High):
  Trigger: Mesh deviation, light detection, or three sensor anomalies
  Action: Zeroize volatile keys, log tamper, alert clinician
  Example: Package manipulation detected

Level 4 (Critical):
  Trigger: Multiple high-severity detections, or key extraction attempt
  Action: Zeroize ALL keys, halt device, enter safe mode
  Example: Decapsulation attempt detected by mesh + light + pressure
```

### 8.2 Tamper Evidence Preservation

When tamper is detected, evidence is preserved for forensic analysis:

Evidence Collection:
1. Snapshot all sensor values (timestamped)
2. Record tamper event details in tamper-resistant log
3. Compute hash of current device state
4. Sign evidence with device attestation key
5. Store in protected NVM (survives power loss)

Evidence Retrieval:
- Via NFC at next programmer contact
- Signed by device (authenticity guaranteed)
- Timestamped (sequence of events preserved)
- Chain of custody documented

## 9. Testing and Validation

### 9.1 Anti-Tamper Test Categories

| Test | Method | Pass Criteria |
|------|--------|--------------|
| Package integrity | X-ray, CT scan | Matches baseline |
| Weld integrity | Visual, X-ray | No discontinuities |
| Encapsulation | UV inspection | No modifications |
| Mesh integrity | Impedance measurement | Within 10% baseline |
| Sensor calibration | Known stimuli | Response within spec |
| Encapsulant adhesion | Pull test (sample) | Greater than 5 MPa |

### 9.2 Destructive Testing

Production samples undergo destructive testing to validate anti-tamper measures:

Destructive Test Protocol:
1. Select samples per lot (1 per 1000 devices)
2. Attempt decapsulation using standard methods
3. Document resistance at each step
4. Attempt microprobing on exposed die
5. Verify tamper detection activated
6. Document findings for design improvement

### 9.3 Compliance

| Standard | Requirement | Status |
|----------|-------------|--------|
| IEC 62443-4-2 SL3 | Anti-tamper physical protection | Compliant |
| FIPS 140-3 Level 2 | Physical security mechanisms | Compliant |
| ISO 14708-1 | Implantable device mechanical integrity | Compliant |
| IEC 60601-1 | Mechanical protection, biocompatibility | Compliant |
| FDA 21 CFR 820 | Design verification and validation | Compliant |

## 10. Summary

The iPACE-CHIP anti-tamper strategy provides six concentric layers of physical
protection from the titanium outer package through die-level hardening to
cryptographic safeguards. Each layer implements multiple independent countermeasures,
ensuring that compromise of any single layer does not expose the device. Manufacturing
records and tamper-evident packaging enable post-hoc forensic analysis. Environmental
monitoring detects attacks that physical barriers cannot prevent. The combination of
deterrence, delay, detection, response, and denial makes the iPACE-CHIP resistant
to physical attacks up to and including nation-state level adversaries with laboratory
access. All measures are validated through comprehensive destructive and non-destructive
testing, meeting or exceeding the physical security requirements of FIPS 140-3
Level 2, IEC 62443-4-2 SL3, and FDA cybersecurity guidance.
