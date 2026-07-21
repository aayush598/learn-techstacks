# Pacing Pulse DAC Design

## Overview

The Pacing Pulse DAC converts the digital pacing parameters into analog voltage or current waveforms that drive the cardiac tissue through the pacing electrodes. In the iPACE-CHIP, this DAC must generate precisely controlled pulses with adjustable amplitude, pulse width, and shape to ensure safe and effective cardiac stimulation. The DAC design must balance accuracy, power efficiency, and patient safety.

## Pacing Pulse Requirements

### Clinical Parameters

| Parameter | Range | Resolution | Unit |
|-----------|-------|------------|------|
| Amplitude | 0.5 – 7.5 | 0.1 | V |
| Pulse width | 0.05 – 1.5 | 0.01 | ms |
| Polarity | Biphasic / Monophasic | 1 bit | - |
| Slew rate | > 10 | - | V/µs |
| Output impedance | < 100 | - | Ω |

### Pulse Waveforms

```
Monophasic Pacing Pulse:

  Voltage
  (V)
  5.0 ┤    ┌──────────────────┐
      │    │                  │
  2.5 ┤    │                  │
      │    │                  │
  0.0 ┼────┘                  └────
      │
      └──────────────────────────
        0    0.5    1.0    1.5  ms


Biphasic Pacing Pulse:

  Voltage
  (V)
  5.0 ┤    ┌──────────┐
      │    │          │
  2.5 ┤    │          │
      │    │          │
  0.0 ┼────┘          └────
      │                   │
 -2.5 ┤                   │
      │                   │
 -5.0 ┤                   └────
      └──────────────────────────
        0    0.5    1.0    1.5  ms

  Phase 1: Stimulation (cathodal)
  Phase 2: Charge recovery (anodal)
```

## Architecture Selection

### Current-Mode vs Voltage-Mode

```
Voltage-Mode DAC:
  ┌──────────┐
  │  Digital  │──►┌──────┐──► Vout ──► R_lead ──► Tissue
  │  Control  │   │ V-DAC│         │
  └──────────┘   └──────┘         │
                                  └──► Vreturn

  Advantages:
  + Simple architecture
  + Low quiescent power
  + Easy voltage scaling
  
  Disadvantages:
  - Current limited by output impedance
  - Tissue impedance variation affects current
  - Pacemaker output depends on lead impedance

Current-Mode DAC:
  ┌──────────┐
  │  Digital  │──►┌──────┐──► Iout ──► R_lead ──► Tissue
  │  Control  │   │ I-DAC│         │
  └──────────┘   └──────┘         │
                                  └──► Vreturn

  Advantages:
  + Constant current regardless of lead impedance
  + Predictable stimulation energy
  + Better tissue response control
  
  Disadvantages:
  - Requires voltage compliance headroom
  - More complex output stage
  - Higher power for high-current modes

Design choice: Current-mode DAC (preferred for pacing)
  Additional voltage-mode: backup for low-energy modes
```

## Current-Mode DAC Architecture

### Binary-Weighted Current Steering

```
                    VDD
                     │
               ┌─────┴─────┐
               │  Bias      │
               │  Generator │
               └─────┬─────┘
                     │ Iref
        ┌────────────┼────────────┐
        │            │            │
   ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
   │ 2^0 × I │  │ 2^1 × I │  │ 2^7 × I │
   │  SW[0]  │  │  SW[1]  │  │  SW[7]  │
   └────┬────┘  └────┬────┘  └────┬────┘
        │            │            │
        └────────────┼────────────┘
                     │
               ┌─────┴─────┐
               │  Cascode   │
               │  Stage     │
               └─────┬─────┘
                     │ Iout
                     ▼
               To Output Stage
```

### Unit Element Array

For improved matching, use thermometer-coded unit elements:

```
8-bit DAC with 255 unit current sources:

  ┌───┬───┬───┬───┬───┬───┬───┬───┐
  │U01│U02│U03│...│U253│U254│U255│
  └─┬─┴─┬─┴─┬─┴───┴──┬─┴──┬─┴─┬─┘
    │   │   │        │    │   │
    └───┴───┴────────┴────┴───┘
                   │
                  Iout

  Thermometer coding:
  Code 0:   000000000000000 (all off)
  Code 1:   100000000000000 (U01 on)
  Code 128: 111111111111111 (all on)
  
  Binary to thermometer conversion in digital
```

### Current Source Transistor Sizing

```
Unit current source matching:

  σ(ΔI/I) = A_ISD / √(W × L)

Where:
  A_ISD = current source matching coefficient
  For 180nm CMOS: A_ISD ≈ 1-2 %·µm

For 8-bit DAC (DNL < 0.5 LSB):
  σ(ΔI/I) < 0.5 LSB / √(2^8) = 0.5 / 16 = 3.1%
  
  Using A_ISD = 1.5 %·µm:
  W × L > (A_ISD / σ)² = (1.5 / 3.1)² = 0.23 µm²
  Minimum: W = 1 µm, L = 1 µm (conservative)
  
  Design choice: W = 2 µm, L = 2 µm (safety margin)
  Matching: σ = 1.5 / √4 = 0.75% ✓
```

## Output Stage Design

### Current Compliance Stage

```
                    VDD (5V)
                     │
               ┌─────┴─────┐
               │           │
  Iout ───────┤  PMOS     │
  (from DAC)  │  Pass     │
               │  Transistor│
               └─────┬─────┘
                     │
                     ├──── Vout (to lead)
                     │
               ┌─────┴─────┐
               │  Current   │
               │  Sense     │
               │  (R_sense) │
               └─────┬─────┘
                     │
                    VSS (0V)

Output voltage compliance:
  Vout_max = VDD - Vdsat_pass - Iout × R_sense
  
  For VDD = 5V, Vdsat = 0.3V, R_sense = 10 Ω:
  Vout_max = 5 - 0.3 - Iout × 10
  
  At 10 mA: Vout_max = 5 - 0.3 - 0.1 = 4.6V ✓
  At 20 mA: Vout_max = 5 - 0.3 - 0.2 = 4.5V ✓
```

### Shutdown and Discharge

```
Pulse termination circuit:

  During pacing: Normal current flow
  After pulse:   Active discharge of output
  
  Discharge switch:
  Vout ────┤S├──── GND
  
  Timing:
  ┌──────────────────────────────────────────┐
  │ Pacing    │ Discharge  │ Recovery        │
  │ Active    │ Active     │ Complete        │
  ├───────────┼────────────┼─────────────────┤
  │ 0-1 ms    │ 1-2 ms     │ > 2 ms          │
  │ Iout > 0  │ Vout → 0   │ Vout = 0        │
  └───────────┴────────────┴─────────────────┘
  
  Discharge time constant:
  τ_discharge = R_on × C_parasitic
  For R_on = 100 Ω, C_parasitic = 10 pF:
  τ_discharge = 1 ns (instantaneous)
```

## Pulse Generation Timing

### Timing State Machine

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  ┌──────┐   ┌────────┐   ┌─────────┐   ┌────────┐  │
│  │ IDLE │──►│ PHASE1 │──►│PHASE1_RE│──►│PHASE2  │  │
│  │      │   │        │   │ (ramp)  │   │        │  │
│  └──┬───┘   └────────┘   └─────────┘   └───┬────┘  │
│     │                                       │       │
│     │◄──────────────────────────────────────┘       │
│                                                      │
│  States:                                             │
│  IDLE:    No pacing, DAC output high-Z              │
│  PHASE1:  Cathodal stimulation (constant current)   │
│  PHASE1_RE: Controlled ramp-down (optional)        │
│  PHASE2:  Anodal charge recovery (biphasic)         │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Timer Implementation

```
Pulse width counter:

  PW_counter[15:0] ← Digital register (programmed value)
  
  Resolution: 10 µs per count
  Range: 10 µs to 655.35 ms
  
  Example: 1.0 ms pulse width
    PW_counter = 1.0 ms / 10 µs = 100 counts
    
  Timing accuracy:
    Clock accuracy: ±1% (RC oscillator)
    PW accuracy: ±1 µs (1 LSB at 10 µs resolution)
    
  For pacing: ±10 µs is acceptable (0.01 ms resolution)
```

## Power Analysis

### Power During Pacing

```
Power = Vsupply × Isupply

Isupply components:
  - DAC current source: Iout = 5 mA (typical)
  - Bias circuits: 10 µA
  - Digital control: 5 µA
  - Output stage: 20 µA
  
  Total supply current: 5.035 mA
  
  Power at 5V supply:
  P_pacing = 5V × 5.035 mA = 25.2 mW (during pulse)
  
  Pulse energy:
  E_pulse = P × t_pulse
  E_pulse = 25.2 mW × 1 ms = 25.2 µJ per pulse
```

### Average Power (Duty Cycling)

```
Pacing scenario: 70 bpm, 1 ms pulse width

Duty cycle = (70/60) × 1 ms / 1 s = 0.117%

Average power:
  P_avg = P_pacing × duty_cycle + P_idle × (1 - duty_cycle)
  P_avg = 25.2 mW × 0.00117 + 1 µW × 0.999
  P_avg = 29.5 µW + 1.0 µW = 30.5 µW
  
  Well within 100 µW pacing power budget ✓
```

### Battery Life Impact

```
Battery capacity: 1.0 Ah (lithium primary)
Nominal voltage: 3.0V
Energy: 3.0 Wh = 10800 J

Pacing power consumption:
  30.5 µW average
  
  Battery life (pacing only):
  T_battery = 10800 J / 30.5e-6 W = 3.54 × 10^8 seconds
  T_battery = 11.2 years ✓
  
  With total chip power (10 µW digital + 30.5 µW pacing):
  T_battery = 10800 / 40.5e-6 = 8.7 years
  (Still within 10-year target with margin)
```

## Safety Considerations

### Output Current Limiting

```
Hardware current limiter:

  Maximum output current: 20 mA (safety limit)
  
  Implementation:
  ┌─────────────────────────────┐
  │                             │
  │  Iout ──┤M1├──┬──┤M2├──── │
  │          │    │   │    │    │
  │          │    │   │    │    │
  │     R_sense  │   │    │    │
  │          │    │   │    │    │
  │          └────┘   └────┘    │
  │                             │
  │  When Iout × R_sense > Vth  │
  │  M2 turns off → limits Iout │
  └─────────────────────────────┘
  
  R_sense = Vth / I_max = 0.5V / 20 mA = 25 Ω
```

### Open-Circuit Protection

```
Lead impedance monitoring:

  Continuous measurement during pacing attempt:
  
  Vout = Iout × R_lead + V_tissue
  
  If Vout > V_compliance (5V):
    Lead impedance too high → fault condition
    
  Threshold: R_lead > 2000 Ω (lead fracture detected)
  
  Response:
    1. Abort pacing attempt
    2. Set fault flag
    3. Retry with reduced current (if appropriate)
    4. Notify digital controller
```

### Charge Balancing

```
For biphasic pacing, net charge must be zero:

  Q_net = ∫(I_phase1)dt + ∫(I_phase2)dt = 0

Implementation:
  Phase 1: I_stim × t_phase1 (cathodal)
  Phase 2: I_recovery × t_phase2 (anodal)
  
  Where: I_stim × t_phase1 = I_recovery × t_phase2
  
  Typical: I_recovery = I_stim / 10
           t_phase2 = 10 × t_phase1
           
  This ensures charge neutrality while:
  - Delivering therapeutic stimulus
  - Preventing tissue damage from DC current
  - Avoiding electrode polarization
```

## Digital Interface

### Control Register Map

```
Register Name    │ Address │ Bits │ Description
─────────────────┼─────────┼──────┼─────────────────────
DAC_CTRL         │ 0x100   │ 8    │ Enable, mode, polarity
DAC_AMPLITUDE    │ 0x101   │ 8    │ Output amplitude (0-255)
DAC_PULSE_WIDTH  │ 0x102   │ 16   │ Pulse width (10 µs steps)
DAC_SHAPE        │ 0x103   │ 8    │ Waveform shape control
DAC_STATUS       │ 0x104   │ 8    │ Output current, voltage
DAC_FAULT        │ 0x105   │ 8    │ Fault flags
DAC_TIMING       │ 0x106   │ 16   │ Inter-pulse delay
DAC_POLARITY     │ 0x107   │ 8    │ Phase 2 settings
```

### Serial Interface

```
SPI interface to digital controller:

  SCLK ──────┐
  MOSI ──────┤    ┌──────────┐
  MISO ◄─────┤    │   DAC    │──► Iout
  CS_n ──────┤    │   Core   │
             │    └──────────┘
             
  Write sequence:
  1. Assert CS_n (low)
  2. Send 16-bit frame: [ADDR(7:0)] [DATA(7:0)]
  3. Deassert CS_n (high)
  4. Data latched on rising edge of CS_n
  
  Clock frequency: up to 10 MHz
  Write time: 1.6 µs per register
  Full setup: 8 writes × 1.6 µs = 12.8 µs
```

## Calibration

### Amplitude Calibration

```
Current source calibration at power-up:

1. Set DAC to mid-scale code (0x80)
2. Enable calibration mode
3. Measure output current through R_sense
4. Compare with target (I_target)
5. Calculate gain correction factor:
   G_corr = I_target / I_measured
6. Store correction in calibration register
7. Apply correction to all output codes

Calibration accuracy:
  Target: ±5% of programmed current
  Achieved: ±2% with calibration ✓
```

### Offset Calibration

```
Offset correction:

1. Set DAC to code 0x00 (zero output)
2. Measure residual output current
3. Store offset value: I_offset
4. During operation: I_out = I_programmed - I_offset

Offset sources:
  - Current source leakage: ~100 nA
  - Switch charge injection: ~10 nA
  - Total offset: ~110 nA
  
  After calibration: < 10 nA ✓
```

## Layout Considerations

### Floor Plan

```
┌───────────────────────────────────────────┐
│           Pacing Pulse DAC                │
│                                           │
│  ┌─────────────────────────────────┐     │
│  │   Current Source Array          │     │
│  │   (thermometer-coded, matched)  │     │
│  │   ██████████████████████████    │     │
│  └─────────────────────────────────┘     │
│                                           │
│  ┌────────────┐  ┌──────────────────┐    │
│  │  Bias      │  │  Output Stage    │    │
│  │  Generator │  │  (high current)  │    │
│  └────────────┘  └──────────────────┘    │
│                                           │
│  ┌────────────┐  ┌──────────────────┐    │
│  │  Digital   │  │  Calibration     │    │
│  │  Control   │  │  Registers       │    │
│  └────────────┘  └──────────────────┘    │
│                                           │
│  ▓▓▓▓▓▓ Guard Ring (high current) ▓▓▓▓▓  │
└───────────────────────────────────────────┘
```

### High-Current Routing

```
Output current path requirements:

  At 20 mA max, metal resistance must be low:
  
  Voltage drop on metal:
  V_drop = I × R_metal
  
  For 20 mA through 100 µm wide metal (R_sheet = 80 mΩ/□):
    If path length = 500 µm, width = 100 µm:
    R_metal = 80 mΩ × 5 = 0.4 Ω
    V_drop = 20 mA × 0.4 Ω = 8 mV
    
  This is acceptable (< 0.2% of 5V output) ✓
  
  Layout rules:
  - Use top metal for high-current paths
  - Width > 50 µm for output routing
  - Via arrays for metal-to-metal connections
  - Thermal relief on output pad
```

## Summary

| Parameter | Value |
|-----------|-------|
| DAC type | Current-mode, 8-bit |
| Output range | 0 – 10 mA |
| Resolution | 0.04 mA (8-bit) |
| Accuracy | ±2% (with calibration) |
| Pulse width range | 0.05 – 1.5 ms |
| Pulse width resolution | 10 µs |
| Maximum output voltage | 4.6V (at 10 mA) |
| Supply voltage | 5V (pacing), 1.8V (digital) |
| Power (during pacing) | 25 mW |
| Power (average, 70 bpm) | 30.5 µW |
| Active area | 0.08 mm² |
| Technology | 180 nm CMOS |
