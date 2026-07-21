# RF Link Budget Analysis

## 2.4.4 Transmitter/Receiver Design, Path Loss, Antenna Efficiency, and Regulatory Compliance

The RF link budget analysis quantifies the maximum achievable communication
range and reliability of the telemetry link between the implanted pacemaker
and the external programmer. This chapter covers transmitter and receiver
design, path loss models, antenna efficiency, tissue impedance effects,
and regulatory compliance requirements.

---

## 2.16.1 Link Budget Fundamentals

### Link Budget Equation

```
  Link Budget (dB) = P_TX + G_TX + G_RX - L_path - L_body - L_misc - S_RX

  where:
    P_TX    = Transmitter output power (dBm)
    G_TX    = Transmitter antenna gain (dBi)
    G_RX    = Receiver antenna gain (dBi)
    L_path  = Free-space path loss (dB)
    L_body  = Body tissue absorption loss (dB)
    L_misc  = Miscellaneous losses (dB)
    S_RX    = Receiver sensitivity (dBm)

  Link Margin = Link Budget (dB)
  Required: Link Margin ≥ 10 dB for reliable communication
```

### Free-Space Path Loss

```
  L_fs = 20 × log₁₀(4π × d / λ)

  where:
    d = distance between antennas (m)
    λ = wavelength (m) = c / f
    c = speed of light (3 × 10⁸ m/s)
    f = frequency (Hz)

  At 400 MHz (λ = 0.75 m):
    d = 0.1 m: L_fs = 20 × log₁₀(4π × 0.1 / 0.75) = -1.5 dB
    d = 0.3 m: L_fs = 20 × log₁₀(4π × 0.3 / 0.75) = 8.0 dB
    d = 0.5 m: L_fs = 20 × log₁₀(4π × 0.5 / 0.75) = 12.5 dB
    d = 1.0 m: L_fs = 20 × log₁₀(4π × 1.0 / 0.75) = 22.5 dB

  At 2.4 GHz (λ = 0.125 m):
    d = 0.1 m: L_fs = 20 × log₁₀(4π × 0.1 / 0.125) = 10.1 dB
    d = 0.3 m: L_fs = 20 × log₁₀(4π × 0.3 / 0.125) = 27.7 dB
    d = 0.5 m: L_fs = 20 × log₁₀(4π × 0.5 / 0.125) = 32.1 dB
    d = 1.0 m: L_fs = 20 × log₁₀(4π × 1.0 / 0.125) = 40.1 dB
```

---

## 2.16.2 Transmitter Design

### MICS Transmitter Specifications

| Parameter | Specification | Unit |
|-----------|--------------|------|
| Output power | -16 to 0 | dBm |
| Frequency range | 402-405 | MHz |
| Channel bandwidth | 300 | kHz |
| Modulation | GFSK (BT=0.5) | — |
| Frequency deviation | ±50-100 | kHz |
| Phase noise | < -100 | dBc/Hz @ 100 kHz |
| Harmonic emissions | < -40 | dBc |
| Spurious emissions | < -40 | dBm |
| Power amplifier efficiency | > 30 | % |
| Supply voltage | 1.8-2.8 | V |
| Current consumption | 1-5 | mA |

### Power Amplifier (PA) Design

```
                    CLASS-E POWER AMPLIFIER

  V_DD ────────────────┬────────────────────────────
                       │
                       ▼
                  ┌─────────┐
                  │  L_choke│ (RF choke)
                  └────┬────┘
                       │
                       ├──────────────────────┐
                       │                      │
                       ▼                      ▼
                  ┌─────────┐           ┌─────────┐
                  │  C_shunt │           │  L_series│
                  └────┬────┘           └────┬────┘
                       │                     │
                       │                     ▼
                       │                ┌─────────┐
                       │                │  C_series│
                       │                └────┬────┘
                       │                     │
                       │                     ▼
                  ┌────┴────┐           ┌─────────┐
                  │  Q1     │           │  Antenna │
                  │ (NMOS)  │           │  Match   │
                  └────┬────┘           └─────────┘
                       │
                      GND

  Class-E PA characteristics:
  - High efficiency: 60-80%
  - Simple topology: Single transistor
  - Low harmonic content: With output filtering
  - Suitable for GFSK modulation
  - Supply voltage: 1.8-2.8V
  - Output power: -16 to 0 dBm
```

### PA Efficiency vs. Output Power

```
  Efficiency
  (%)
    │
   80├──────────────────────────────────────
    │
   70├──────────────────────────────────────
    │
   60├────────╲    ╱────────────────────────
    │          ╲  ╱
   50├──────────╲╱──────────────────────────
    │
   40├──────────╱╲──────────────────────────
    │         ╱  ╲
   30├────────╱    ╲────────────────────────
    │       ╱      ╲
   20├──────╱        ╲──────────────────────
    │     ╱
   10├────╱─────────────────────────────────
    │
    0├────┬────┬────┬────┬────┬────
    -20  -16  -10  -5   0   +5
              Output Power (dBm)

    Peak efficiency: ~70% at -5 dBm
    MICS limit: -16 dBm (25 µW)
```

---

## 2.16.3 Receiver Design

### MICS Receiver Specifications

| Parameter | Specification | Unit |
|-----------|--------------|------|
| Sensitivity | ≤ -100 | dBm |
| Dynamic range | > 60 | dB |
| Frequency range | 402-405 | MHz |
| Channel bandwidth | 300 | kHz |
| Noise figure | < 3 | dB |
| Image rejection | > 30 | dB |
| IIP3 | > -20 | dBm |
| Current consumption | 1-2 | mA |
| Supply voltage | 1.8-2.8 | V |

### Receiver Architecture

```
                    DIRECT-CONVERSION RECEIVER

  Antenna ────┬────────────────────────────────────
              │
              ▼
         ┌─────────┐
         │  LNA    │ (Low-noise amplifier)
         │  NF=2dB │
         └────┬────┘
              │
              ▼
         ┌─────────┐
         │  BPF    │ (Band-pass filter, 402-405 MHz)
         └────┬────┘
              │
              ▼
         ┌─────────┐     ┌─────────┐
         │  Mixer  │◀────│  LO     │ (Local oscillator)
         │         │     │  (PLL)  │
         └────┬────┘     └─────────┘
              │
              ▼
         ┌─────────┐
         │  LPF    │ (Low-pass filter, 150 kHz)
         └────┬────┘
              │
              ▼
         ┌─────────┐     ┌─────────┐
         │  VGA    │     │  AGC    │ (Automatic gain control)
         │  (0-60dB)│◀───│         │
         └────┬────┘     └─────────┘
              │
              ▼
         ┌─────────┐
         │  ADC    │ (10-12 bit, 1 MSPS)
         └────┬────┘
              │
              ▼
         ┌─────────┐
         │  Digital│ (Demodulator, filter, clock recovery)
         │  Base-  │
         │  band   │
         └────┬────┘
              │
              ▼
         Received Data
```

### Receiver Sensitivity

```
  Sensitivity = kTB + NF + SNR_min

  where:
    k = Boltzmann constant (1.38 × 10⁻²³ J/K)
    T = temperature (290 K)
    B = bandwidth (300 kHz)
    NF = noise figure (3 dB)
    SNR_min = minimum SNR for demodulation (10 dB for GFSK)

  Sensitivity = 10 × log₁₀(k × T × B) + NF + SNR_min
              = 10 × log₁₀(1.38e-23 × 290 × 300e3) + 3 + 10
              = 10 × log₁₀(1.2e-15) + 13
              = -149.2 + 13
              = -136.2 dBm (theoretical)

  Practical sensitivity: -100 to -110 dBm
  (limited by implementation, phase noise, I/Q imbalance)
```

---

## 2.16.4 Body Tissue Propagation Model

### Tissue Layer Model

```
                    TISSUE LAYER MODEL

  External Programmer
       │
       ▼
  ┌─────────────────────────────────────────────┐
  │  Skin (1-2 mm)                              │  εr = 38, σ = 1.46 S/m
  ├─────────────────────────────────────────────┤
  │  Fat (5-20 mm)                              │  εr = 5.56, σ = 0.04 S/m
  ├─────────────────────────────────────────────┤
  │  Muscle (10-50 mm)                          │  εr = 52.7, σ = 1.74 S/m
  ├─────────────────────────────────────────────┤
  │  Blood/Vessels (variable)                   │  εr = 58.3, σ = 1.54 S/m
  ├─────────────────────────────────────────────┤
  │  Pericardium (1-2 mm)                       │  εr = 40, σ = 1.0 S/m
  ├─────────────────────────────────────────────┤
  │  Myocardium (5-15 mm)                       │  εr = 54.4, σ = 1.82 S/m
  ├─────────────────────────────────────────────┤
  │  Blood (heart chambers)                     │  εr = 58.3, σ = 1.54 S/m
  └─────────────────────────────────────────────┘
       │
       ▼
  Implanted Pacemaker Antenna
```

### Tissue Absorption Calculation

```
  L_body = Σ (α_i × d_i)

  where:
    α_i = attenuation coefficient of tissue i (dB/m)
    d_i = thickness of tissue i (m)

  At 400 MHz:
    Skin: α = 30 dB/m, d = 0.002 m → 0.06 dB
    Fat:  α = 5 dB/m,  d = 0.010 m → 0.05 dB
    Muscle: α = 40 dB/m, d = 0.030 m → 1.20 dB
    Blood: α = 35 dB/m, d = 0.020 m → 0.70 dB
    Pericardium: α = 25 dB/m, d = 0.002 m → 0.05 dB
    Myocardium: α = 42 dB/m, d = 0.010 m → 0.42 dB

    Total L_body = 0.06 + 0.05 + 1.20 + 0.70 + 0.05 + 0.42
                 = 2.48 dB

  At 2.4 GHz:
    Skin: α = 200 dB/m, d = 0.002 m → 0.40 dB
    Fat:  α = 30 dB/m,  d = 0.010 m → 0.30 dB
    Muscle: α = 250 dB/m, d = 0.030 m → 7.50 dB
    Blood: α = 200 dB/m, d = 0.020 m → 4.00 dB
    Pericardium: α = 150 dB/m, d = 0.002 m → 0.30 dB
    Myocardium: α = 260 dB/m, d = 0.010 m → 2.60 dB

    Total L_body = 0.40 + 0.30 + 7.50 + 4.00 + 0.30 + 2.60
                 = 15.1 dB
```

### Frequency-Dependent Body Loss

```
  Body Loss
  (dB)
    │
   20├──────────────────────────────────────
    │
   15├──────────────────────────╱───────────
    │                         ╱
   10├───────────────────────╱──────────────
    │                      ╱
    5├─────────────────────╱────────────────
    │                    ╱
    2├──────────────────╱────────────────── 400 MHz
    │                 ╱
    1├───────────────╱──────────────────────
    │              ╱
    0├────────────╱─────────────────────────
    │
    0├────┬────┬────┬────┬────┬────
    100  200  400  800  1500 2400
              Frequency (MHz)

    400 MHz: ~2.5 dB body loss (through chest)
    2.4 GHz: ~15 dB body loss (through chest)
```

---

## 2.16.5 Antenna Efficiency

### Implanted Loop Antenna Efficiency

```
  η_ant = R_rad / (R_rad + R_loss + R_near)

  where:
    R_rad = radiation resistance
    R_loss = ohmic loss resistance
    R_near = near-field loss (tissue absorption)

  For a 5 × 5 mm loop at 400 MHz:
    R_rad ≈ 0.1 Ω (very small loop)
    R_loss ≈ 1 Ω (copper trace resistance)
    R_near ≈ 5 Ω (tissue absorption in near field)

    η_ant = 0.1 / (0.1 + 1 + 5) = 0.1 / 6.1 = 1.6%

  Including matching network loss (0.5 dB):
    η_total = 1.6% × 10^(-0.5/10) = 1.6% × 0.89 = 1.4%

  Antenna gain: G = η × D (directivity)
    D ≈ 1.5 (loop antenna)
    G = 0.014 × 1.5 = 0.021 = -16.8 dBi
```

### External Antenna Efficiency

The external programmer antenna can be larger and more efficient:

```
  Patch antenna (2.4 GHz, 25 × 25 mm):
    η_ant = 70%
    D = 6 dBi
    G = 0.7 × 6 = 4.2 dBi

  Loop antenna (400 MHz, 50 × 50 mm):
    η_ant = 30%
    D = 2 dBi
    G = 0.3 × 2 = 0.6 dBi = -2.2 dBi
```

---

## 2.16.6 Complete Link Budget Analysis

### MICS Band (400 MHz) Link Budget

```
                    MICS LINK BUDGET (400 MHz)

  Transmitter (Implanted):
    Output power:           -16 dBm (25 µW, MICS limit)
    PA efficiency:          30%
    Matching loss:          -0.5 dB
    Cable/trace loss:       -0.5 dB
    Antenna gain:           -16.8 dBi (5×5 mm loop)
    EIRP:                   -16 - 0.5 - 0.5 - 16.8 = -33.8 dBm

  Path Loss:
    Free-space (d=0.3m):    8.0 dB
    Body tissue:            2.5 dB
    Multipath fading:       10 dB (conservative)
    Polarization mismatch:  3 dB
    Total path loss:        23.5 dB

  Receiver (External):
    Antenna gain:           -2.2 dBi (50×50 mm loop)
    Matching loss:          -0.5 dB
    Cable loss:             -0.5 dB
    Noise figure:           3 dB
    Sensitivity:            -100 dBm

  Link Budget:
    Received power = EIRP - L_path + G_RX - L_mismatch
                   = -33.8 - 23.5 + (-2.2) - 1.0
                   = -60.5 dBm

    Link margin = Received power - Sensitivity
                = -60.5 - (-100)
                = 39.5 dB

    Required margin: 10 dB
    Available margin: 39.5 dB → PASS ✓
    Maximum range: ~2 meters (through body)
```

### ISM 2.4 GHz Link Budget

```
                    ISM 2.4 GHz LINK BUDGET

  Transmitter (Implanted):
    Output power:           0 dBm (1 mW, ISM limit)
    PA efficiency:          25%
    Matching loss:          -0.5 dB
    Cable/trace loss:       -0.5 dB
    Antenna gain:           -10 dBi (5×5 mm loop)
    EIRP:                   0 - 0.5 - 0.5 - 10 = -11 dBm

  Path Loss:
    Free-space (d=0.3m):    27.7 dB
    Body tissue:            15.1 dB
    Multipath fading:       10 dB
    Polarization mismatch:  3 dB
    Total path loss:        55.8 dB

  Receiver (External):
    Antenna gain:           3 dBi (patch antenna)
    Matching loss:          -0.5 dB
    Cable loss:             -0.5 dB
    Noise figure:           4 dB
    Sensitivity:            -90 dBm

  Link Budget:
    Received power = EIRP - L_path + G_RX - L_mismatch
                   = -11 - 55.8 + 3 - 1.0
                   = -64.8 dBm

    Link margin = Received power - Sensitivity
                = -64.8 - (-90)
                = 25.2 dB

    Required margin: 10 dB
    Available margin: 25.2 dB → PASS ✓
    Maximum range: ~0.5 meters (through body)
```

---

## 2.16.7 Fading and Multipath

### Multipath Effects

```
                    MULTIPATH PROPAGATION

  Direct path ────────────────────────────────▶
                    │
  Reflected path ───┼───▶ ───▶ ───▶ ──────────▶
  (off chest wall)  │
                    │
  Scattered path ───┼───▶ ──▶ ──▶ ──▶ ────────▶
  (off ribs/organs) │

  Multipath causes:
  1. Constructive/destructive interference
  2. Signal fading (±10-20 dB variation)
  3. Time dispersion (delay spread)
  4. Doppler shift (body movement)
```

### Fading Margin

```
  Fading margin = 10 × log₁₀(1 / P_fade)

  For 99% reliability (P_fade = 0.01):
    Fading margin = 10 × log₁₀(100) = 20 dB

  For 99.9% reliability (P_fade = 0.001):
    Fading margin = 10 × log₁₀(1000) = 30 dB

  Typical design margin: 10-20 dB (for MICS)
```

---

## 2.16.8 Regulatory Compliance

### FCC Part 95 (MICS Band)

| Parameter | Limit | Unit |
|-----------|-------|------|
| Frequency range | 402-405 | MHz |
| Maximum output power | 25 | µW (-16 dBm) |
| Maximum EIRP | 25 | µW (-16 dBm) |
| Bandwidth per channel | 300 | kHz |
| Number of channels | 10 | — |
| Spurious emissions (in-band) | -40 | dBm |
| Spurious emissions (out-of-band) | -40 | dBm |
| Frequency stability | ±100 | kHz |
| Modulation | Any | — |

### EN 302 268 (European MICS)

| Parameter | Limit | Unit |
|-----------|-------|------|
| Frequency range | 402-405 | MHz |
| Maximum output power | 25 | µW |
| Maximum EIRP | 25 | µW |
| Duty cycle | 1 | % (max) |
| Frequency stability | ±100 | kHz |
| Spurious emissions | -40 | dBm |

### FCC Part 15 (ISM 2.4 GHz)

| Parameter | Limit | Unit |
|-----------|-------|------|
| Frequency range | 2400-2483.5 | MHz |
| Maximum output power | 10 | mW (10 dBm) |
| Maximum EIRP | 10 | mW |
| Bandwidth | 83.5 | MHz |
| Modulation | Any | — |
| Spurious emissions | -41.3 | dBm/MHz |

### SAR Compliance

| Standard | Body Region | Limit | Averaging |
|----------|------------|-------|-----------|
| FCC | Head and trunk | 1.6 | W/kg (1g) |
| ICNIRP | Head and trunk | 2.0 | W/kg (10g) |
| ICNIRP | Limbs | 4.0 | W/kg (10g) |
| IEC 62209 | Whole body | 0.4 | W/kg |

---

## 2.16.9 Impedance Effects

### Tissue Impedance Model

```
                    TISSUE IMPEDANCE MODEL

  Z_tissue = R_tissue + jωL_tissue + 1/(jωC_tissue)

  At 400 MHz:
    R_tissue ≈ 50-200 Ω (depends on tissue type)
    L_tissue ≈ 10-50 nH (depends on geometry)
    C_tissue ≈ 1-10 pF (depends on geometry)

  Matching network must account for tissue impedance:
    Z_antenna = Z_tissue conjugate (for maximum power transfer)
```

### Impedance Matching

```
                    IMPEDANCE MATCHING THROUGH TISSUE

  Antenna ────────┬─────────────────────────── To PA/LNA
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
             │  Tissue│      │
             │  Model │      │
             └───┬────┘      │
                 │           │
                 ▼           │
             ┌────────┐      │
             │  C2    │      │
             └───┬────┘      │
                 │           │
                GND          GND

  Matching network:
    - Optimized for 402-405 MHz
    - Accounts for tissue impedance variation
    - Component values: L = 10-100 nH, C = 0.5-5 pF
    - Matching bandwidth: > 3 MHz
    - VSWR: < 2:1 across band
```

---

## 2.16.10 Range Estimation

### Maximum Range Calculation

```
  Maximum range = 10^((P_TX + G_TX + G_RX - L_body - L_misc - S_RX - Margin) / 20) × λ / (4π)

  For MICS (400 MHz):
    P_TX = -16 dBm
    G_TX = -16.8 dBi
    G_RX = -2.2 dBi
    L_body = 2.5 dB
    L_misc = 5 dB (fading + polarization)
    S_RX = -100 dBm
    Margin = 10 dB

    Available path loss = -16 - 16.8 - 2.2 - 2.5 - 5 - (-100) - 10
                        = -16 - 16.8 - 2.2 - 2.5 - 5 + 100 - 10
                        = 47.5 dB

    Maximum range = 10^(47.5/20) × 0.75 / (4π)
                  = 10^2.375 × 0.75 / 12.57
                  = 237.1 × 0.75 / 12.57
                  = 14.1 meters (free space)
                  = ~2 meters (through body, with fading)
```

### Range vs. Frequency Comparison

| Frequency | Max Range (Free Space) | Max Range (Through Body) | Link Margin |
|-----------|----------------------|-------------------------|------------|
| 400 MHz (MICS) | ~14 m | ~2 m | 39.5 dB |
| 2.4 GHz (ISM) | ~3 m | ~0.5 m | 25.2 dB |
| 433 MHz (ISM) | ~12 m | ~1.5 m | 35 dB |

---

## 2.16.11 Summary

The RF link budget analysis demonstrates that:

1. **MICS band (400 MHz) is optimal**: Provides 39.5 dB link margin with
   2-meter through-body range, well above the 10 dB required margin.

2. **Body tissue absorption is manageable**: At 400 MHz, body tissue
   absorption is only ~2.5 dB through the chest, compared to ~15 dB at
   2.4 GHz.

3. **Small antennas are practical**: A 5 × 5 mm loop antenna at 400 MHz
   achieves -16.8 dBi gain, sufficient for 2-meter communication with
   39.5 dB margin.

4. **Regulatory compliance is achievable**: MICS at 25 µW (-16 dBm)
   produces SAR of ~0.25 W/kg, well below the 1.6 W/kg FCC limit.

5. **Fading and multipath must be accounted for**: A 10-20 dB fading
   margin is required for reliable communication in the body environment.

The link budget analysis provides the quantitative foundation for designing
a reliable telemetry link that meets all regulatory requirements while
proventing adequate communication range for clinical use.
