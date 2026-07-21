# Wireless Telemetry Link

## 2.4.1 MICS Band, ISM Band, Antenna Design, and Body Propagation

The wireless telemetry link provides bidirectional communication between the
implanted pacemaker and external programming/monitoring equipment. This
chapter covers the MICS (Medical Implant Communication Service) and ISM
(Industrial, Scientific, and Medical) frequency bands, antenna design for
implanted devices, RF propagation through body tissue, and specific
absorption rate (SAR) considerations.

---

## 2.13.1 Telemetry Requirements

### Functional Requirements

| Parameter | Requirement | Unit |
|-----------|------------|------|
| Bidirectional communication | Yes | — |
| Data rate | 8-500 | kbps |
| Range (in body) | ≥ 2 | m |
| Range (through body) | ≥ 1 | m |
| Latency | < 100 | ms |
| BER (bit error rate) | ≤ 10⁻⁶ | — |
| Encryption | Optional (AES-128) | — |
| Power consumption (TX) | ≤ 5 | mA |
| Power consumption (RX) | ≤ 2 | mA |
| Wake-up time | < 50 | ms |
| Antenna size | < 10 × 10 × 2 | mm |

### Regulatory Requirements

| Band | Frequency | Bandwidth | Max Power | Regulation |
|------|-----------|-----------|-----------|-----------|
| MICS | 402-405 MHz | 300 kHz | 25 µW (−16 dBm) | FCC Part 95, EN 302 268 |
| MedRadio | 401-402 MHz | 100 kHz | 25 µW | ETSI EN 303 287 |
| ISM 402-405 MHz | 402-405 MHz | 300 kHz | 25 µW | MICS band |
| ISM 2.4 GHz | 2400-2483.5 MHz | 83.5 MHz | 10 mW | FCC Part 15 |
| ISM 433 MHz | 433.05-434.79 MHz | 1.74 MHz | 10 mW | ETSI EN 300 220 |

---

## 2.13.2 MICS Band (402-405 MHz)

### Band Characteristics

The MICS band is specifically allocated for medical implant communication
and offers several advantages for pacemaker telemetry:

```
  MICS Band Allocation:
  
  402 MHz ─────────────────────────────────────── 405 MHz
  │←──────────── 3 MHz total bandwidth ─────────────→│
  │                                                    │
  │  Channel 1: 402.000-402.300 MHz (300 kHz)         │
  │  Channel 2: 402.300-402.600 MHz (300 kHz)         │
  │  Channel 3: 402.600-402.900 MHz (300 kHz)         │
  │  Channel 4: 402.900-403.200 MHz (300 kHz)         │
  │  Channel 5: 403.200-403.500 MHz (300 kHz)         │
  │  Channel 6: 403.500-403.800 MHz (300 kHz)         │
  │  Channel 7: 403.800-404.100 MHz (300 kHz)         │
  │  Channel 8: 404.100-404.400 MHz (300 kHz)         │
  │  Channel 9: 404.400-404.700 MHz (300 kHz)         │
  │  Channel 10: 404.700-405.000 MHz (300 kHz)        │
  │                                                    │
  │  10 channels × 300 kHz = 3 MHz total               │
```

### Advantages of MICS Band

1. **Dedicated medical band**: No interference from consumer electronics
2. **Good body penetration**: 400 MHz penetrates tissue well
3. **Low SAR**: Lower frequency means lower specific absorption rate
4. **Small antenna**: λ/4 at 400 MHz ≈ 18.75 cm (can be reduced with
   loading techniques)
5. **Regulatory clarity**: Well-defined power limits and channelization

### Disadvantages

1. **Limited bandwidth**: 3 MHz total limits data rate
2. **Antenna size**: λ/4 is still relatively large for implant
3. **Requires licensing**: MICS band requires coordinated use
4. **Limited external equipment**: Fewer off-the-shelf MICS transceivers

---

## 2.13.3 ISM 2.4 GHz Band

### Band Characteristics

The ISM 2.4 GHz band offers higher data rates and smaller antennas:

```
  ISM 2.4 GHz Band:
  
  2400 MHz ──────────────────────────────────── 2483.5 MHz
  │←────────────── 83.5 MHz bandwidth ──────────────→│
  │                                                    │
  │  Overlaps with:                                    │
  │  - Wi-Fi (802.11b/g/n): 2401-2473 MHz             │
  │  - Bluetooth: 2402-2480 MHz                        │
  │  - ZigBee: 2405-2480 MHz                           │
  │  - Microwave ovens: 2450 MHz                       │
  │                                                    │
  │  14 channels × 20 MHz = 280 MHz (Wi-Fi)           │
  │  79 channels × 1 MHz = 79 MHz (Bluetooth)          │
```

### Advantages

1. **High data rate**: Up to 1 Mbps (Bluetooth) or 54 Mbps (Wi-Fi)
2. **Small antenna**: λ/4 at 2.4 GHz ≈ 3.125 cm
3. **Low cost**: Abundant off-the-shelf transceivers
4. **High integration**: Single-chip solutions available

### Disadvantages

1. **Heavy interference**: Wi-Fi, Bluetooth, microwave ovens
2. **Higher SAR**: 2.4 GHz has higher specific absorption rate than 400 MHz
3. **Poorer body penetration**: Higher frequency attenuates more in tissue
4. **Not dedicated medical**: Shared band with consumer devices
5. **Higher power**: May require more power for reliable communication

---

## 2.13.4 Antenna Design for Implanted Devices

### Antenna Types

| Type | Size | Gain | Bandwidth | Application |
|------|------|------|-----------|------------|
| Monopole (λ/4) | Large | 2-5 dBi | Wide | External programmer |
| Loop (small) | Small | -20 to -10 dBi | Narrow | Implanted device |
| Patch | Medium | 3-7 dBi | Narrow | External programmer |
| Helix | Medium | 5-10 dBi | Narrow | External programmer |
| Meandered | Small | -15 to -5 dBi | Narrow | Implanted device |
| PIFA | Small | 0-3 dBi | Medium | Implanted device |

### Implanted Antenna Design

The implanted antenna must be:
1. **Small**: < 10 × 10 × 2 mm (for cosmetic reasons)
2. **Efficient**: Despite small size, must achieve adequate link budget
3. **Biocompatible**: Encapsulated in biocompatible material
4. **Hermetically sealed**: Protected from body fluids
5. **Low SAR**: Must meet SAR limits for tissue heating

### Loop Antenna Design

The loop antenna is the most common type for implanted devices:

```
                    LOOP ANTENNA (Top View)

         ┌────────────────────────────┐
         │                            │
         │    ┌──────────────────┐    │
         │    │                  │    │
         │    │    Loop Area     │    │
         │    │    (A = 5×5 mm²) │    │
         │    │                  │    │
         │    └──────────────────┘    │
         │                            │
         │    Feed point ──┐          │
         │                │          │
         └────────────────┼──────────┘
                          │
                    Matching network
                          │
                    To RF transceiver

  Loop parameters:
    Area: 5 × 5 = 25 mm²
    Turns: 1-5
    Wire width: 0.1-0.5 mm
    Resonant frequency: 402-405 MHz (MICS) or 2.4 GHz (ISM)
```

### Loop Antenna Radiation Pattern

```
                    LOOP ANTENNA RADIATION PATTERN

  E-plane (vertical):
  
                    0°
                    │
            90° ────┼──── 270°
                    │
                   180°

  H-plane (horizontal):
  
                    0°
                    │
            90° ────●──── 270°
                    │
                   180°

  Pattern: Doughnut-shaped (toroidal)
  Maximum radiation: In the plane of the loop
  Minimum radiation: Along the axis of the loop
```

### Antenna Matching Network

The antenna must be matched to the RF transceiver input impedance (typically
50 Ω) for maximum power transfer:

```
                    ANTENNA MATCHING NETWORK

  Antenna ────────┬─────────────────────── To RF Transceiver
                  │
                  ▼
             ┌────────┐
             │  L1    │ (Series inductor)
             └───┬────┘
                 │
                 ├─── C1 ────┐ (Shunt capacitor)
                 │           │
                 ▼           │
             ┌────────┐      │
             │  L2    │      │
             └───┬────┘      │
                 │           │
                 ▼           │
             ┌────────┐      │
             │  C2    │      │
             └───┬────┘      │
                 │           │
                GND          GND

  Matching network: L-type or π-type
  Component values: Calculated for 402-405 MHz
  Typical values: L = 10-100 nH, C = 0.5-5 pF
  Matching bandwidth: > 3 MHz (for 10-channel MICS)
```

---

## 2.13.5 RF Propagation Through Body Tissue

### Tissue Properties

| Tissue | Permittivity (εr) | Conductivity (σ) | Density (kg/m³) |
|--------|------------------|-----------------|----------------|
| Muscle | 52.7 | 1.74 | 1041 |
| Fat | 5.56 | 0.04 | 911 |
| Blood | 58.3 | 1.54 | 1060 |
| Bone | 12.5 | 0.24 | 1042 |
| Skin | 38.0 | 1.46 | 1100 |
| Lung | 20.8 | 0.73 | 400 |
| Liver | 43.0 | 1.69 | 1060 |
| Heart | 54.4 | 1.82 | 1050 |

### Propagation Loss

The propagation loss through body tissue is much higher than in free space:

```
  Path Loss (dB) = Free-space loss + Tissue absorption loss

  Free-space loss:
    L_fs = 20 × log₁₀(4π × d / λ)
    
    At 400 MHz (λ = 0.75 m), d = 0.3 m:
    L_fs = 20 × log₁₀(4π × 0.3 / 0.75) = 20 × log₁₀(5.03) = 14.0 dB

  Tissue absorption loss:
    L_tissue = 8.686 × α × d
    
    where α = attenuation coefficient (dB/m)
    At 400 MHz in muscle: α ≈ 40 dB/m
    For d = 0.3 m: L_tissue = 40 × 0.3 = 12.0 dB

  Total path loss: L_total = 14.0 + 12.0 = 26.0 dB
```

### Frequency-Dependent Attenuation

```
  Attenuation
  (dB/m)
    │
  200├─────────────────────────────────────
    │
  150├─────────────────────────────────────
    │
  100├─────────────────────────────────────
    │
   50├──────╱──────────────────────────────
    │     ╱
   40├────╱──────────────────────────────── 400 MHz
    │   ╱
   30├──╱──────────────────────────────────
    │ ╱
   20├╱────────────────────────────────────
    │
   10├─────────────────────────────────────
    │
    0├────┬────┬────┬────┬────┬────┬────
    100  200  400  600  800  1000 2400
              Frequency (MHz)

    400 MHz: α ≈ 40 dB/m (moderate attenuation)
    2.4 GHz: α ≈ 200 dB/m (high attenuation)
```

---

## 2.13.6 Link Budget Analysis

### Link Budget Equation

```
  Link Budget (dB) = P_TX + G_TX - L_path - L_body + G_RX - S_RX

  where:
    P_TX = transmitter output power (dBm)
    G_TX = transmitter antenna gain (dBi)
    L_path = free-space path loss (dB)
    L_body = body tissue absorption loss (dB)
    G_RX = receiver antenna gain (dBi)
    S_RX = receiver sensitivity (dBm)

  Required: Link Budget ≥ 0 dB for reliable communication
```

### MICS Link Budget

```
  MICS Band (400 MHz) Link Budget:

  Transmitter (Implanted):
    P_TX = -16 dBm (25 µW, MICS limit)
    G_TX = -15 dBi (small loop antenna)
    Cable loss = 0 dB (on-chip)

  Path:
    L_path = 14 dB (free-space, d = 0.3 m)
    L_body = 12 dB (tissue absorption, d = 0.3 m)

  Receiver (External Programmer):
    G_RX = 3 dBi (patch antenna)
    S_RX = -100 dBm (typical MICS receiver)

  Link Budget = (-16) + (-15) - 14 - 12 + 3 - (-100)
              = -16 - 15 - 14 - 12 + 3 + 100
              = 46 dB

  Link margin: 46 dB (adequate for reliable communication)
```

### ISM 2.4 GHz Link Budget

```
  ISM 2.4 GHz Link Budget:

  Transmitter (Implanted):
    P_TX = 0 dBm (1 mW, ISM limit)
    G_TX = -10 dBi (small antenna)
    Cable loss = 0 dB

  Path:
    L_path = 30 dB (free-space, d = 0.3 m)
    L_body = 60 dB (tissue absorption, d = 0.3 m)

  Receiver (External Programmer):
    G_RX = 5 dBi (antenna)
    S_RX = -90 dBm (typical 2.4 GHz receiver)

  Link Budget = 0 + (-10) - 30 - 60 + 5 - (-90)
              = 0 - 10 - 30 - 60 + 5 + 90
              = -5 dB

  Link margin: -5 dB (insufficient!)
  Need to increase TX power or improve antenna gain
```

---

## 2.13.7 Specific Absorption Rate (SAR)

### SAR Definition

SAR (Specific Absorption Rate) is the rate at which RF energy is absorbed
by body tissue:

```
  SAR = σ × |E|² / ρ

  where:
    σ = tissue conductivity (S/m)
    E = electric field strength (V/m)
    ρ = tissue density (kg/m³)

  Units: W/kg
```

### SAR Limits

| Body Region | Limit | Standard |
|------------|-------|----------|
| Head and trunk | 1.6 W/kg (1g average) | FCC |
| Head and trunk | 2.0 W/kg (10g average) | ICNIRP |
| Limbs | 4.0 W/kg (10g average) | ICNIRP |
| Whole body | 0.4 W/kg | FCC |

### SAR Calculation for MICS

```
  SAR = P_TX × SAR_factor / mass

  For MICS (400 MHz, 25 µW):
    SAR_factor ≈ 0.1 W/kg per mW (typical for 400 MHz implant)
    mass ≈ 10 g (1g averaging volume)

    SAR = 0.025 mW × 0.1 / 0.01 kg
        = 0.25 W/kg

  Limit: 1.6 W/kg (FCC) → PASS ✓
  Margin: 1.6 / 0.25 = 6.4× (adequate)
```

---

## 2.13.8 Modulation Schemes

### GFSK (Gaussian Frequency Shift Keying)

GFSK is the most common modulation scheme for MICS telemetry:

```
  GFSK Modulation:

  Data:    1   0   1   1   0   0   1   0
           │   │   │   │   │   │   │   │
           ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼
  f(t):  ┌───┐   ┌───────┐       ┌───┐
         │   │   │       │       │   │
  f₀ + Δf│   │   │       │       │   │
         │   │   │       │       │   │
  f₀ ────┘   └───┘       └───────┘   └───────
         │       │       │       │       │
  f₀ - Δf│       │       │       │       │
         │       └───────┘       └───────┘

  Parameters:
    f₀ = carrier frequency (402-405 MHz)
    Δf = frequency deviation (±50-100 kHz)
    BT = Gaussian filter bandwidth-time product (0.5)
    Data rate: 8-500 kbps
```

### GFSK Advantages

1. **Constant envelope**: Allows efficient Class-C/Class-E power amplifier
2. **Narrow bandwidth**: Gaussian filtering reduces spectral spreading
3. **Good BER performance**: Similar to FSK but with narrower bandwidth
4. **Simple implementation**: Easy to modulate and demodulate

### OOK (On-Off Keying)

OOK is used for simple, low-power wake-up receivers:

```
  OOK Modulation:

  Data:    1   0   1   1   0   0   1   0
           │   │   │   │   │   │   │   │
           ▼   ▼   ▼   ▼   ▼   ▼   ▼   ▼
  Carrier: ────┐       ┌───┐           ┌───
               │       │   │           │
               │       │   │           │
               └───────┘   └───────────┘

  Carrier present = 1
  Carrier absent = 0
```

---

## 2.13.9 Wake-Up Receiver

### Low-Power Wake-Up

The wake-up receiver detects an external programming request without
requiring the full RF transceiver to be powered on:

```
                    WAKE-UP RECEIVER ARCHITECTURE

  Antenna ────────┬────────────────────────────
                  │
                  ▼
             ┌────────┐
             │  BPF   │ (Band-pass filter, 402-405 MHz)
             └───┬────┘
                 │
                 ▼
             ┌────────┐
             │  LNA   │ (Low-noise amplifier, always on)
             │  (1µW) │
             └───┬────┘
                 │
                 ▼
             ┌────────┐
             │  Envelope│ (Envelope detector)
             │  Detector│
             └───┬────┘
                 │
                 ▼
             ┌────────┐
             │  LPF   │ (Low-pass filter, 1-10 kHz)
             └───┬────┘
                 │
                 ▼
             ┌────────┐
             │  Comp. │ (Threshold comparator)
             └───┬────┘
                 │
                 ▼
             ┌────────┐
             │  Digital│ (Pattern decoder)
             │  Decoder│ (Detects wake-up pattern)
             └───┬────┘
                 │
                 ▼
             WAKE-UP INTERRUPT (to main processor)

  Power consumption: 1-5 µW (always on)
  Wake-up time: < 1 ms
  False alarm rate: < 1 per day
```

---

## 2.13.10 Summary

The wireless telemetry link for implantable pacemakers must balance:

1. **Frequency band**: MICS (400 MHz) offers better body penetration and
   lower SAR than ISM 2.4 GHz, making it the preferred choice for
   implanted devices.

2. **Antenna design**: Small loop antennas (< 10 × 10 mm) are practical
   for implants but have low gain (-15 dBi), requiring careful link
   budget analysis.

3. **Body propagation**: Tissue absorption at 400 MHz is ~40 dB/m,
   significantly reducing the available link budget. The link budget
   analysis shows 46 dB margin for MICS at 0.3 m range.

4. **SAR compliance**: MICS at 25 µW produces SAR of ~0.25 W/kg, well
   below the 1.6 W/kg FCC limit.

5. **Power consumption**: The wake-up receiver consumes only 1-5 µW,
   enabling continuous monitoring without significant battery impact.

The MICS band at 402-405 MHz with GFSK modulation provides the optimal
balance of data rate, range, power consumption, and regulatory compliance
for implantable pacemaker telemetry.
