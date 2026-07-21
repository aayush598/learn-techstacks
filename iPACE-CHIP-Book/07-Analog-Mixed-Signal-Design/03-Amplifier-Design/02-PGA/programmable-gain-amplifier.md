# Programmable Gain Amplifier (PGA) for Bio-Potential Signals

## Overview

The Programmable Gain Amplifier (PGA) is the variable-gain stage in the iPACE-CHIP analog front-end that amplifies weak bio-potential signals to the optimal input range of the ADC. Cardiac signals vary dramatically—from 0.5 mV P-waves to 20 mV R-waves—and the PGA must adjust gain dynamically to maximize dynamic range without saturation. The PGA design must deliver low noise, precise gain steps, and minimal distortion across all gain settings.

## System Requirements

### Gain Range

```
Bio-potential signal amplitudes (after electrode):

Signal Type     │ Min      │ Typical  │ Max      │ Required Gain
────────────────┼──────────┼──────────┼──────────┼──────────────
P-wave (atrial) │ 0.5 mV   │ 2 mV     │ 5 mV     │ 4 – 20×
R-wave (vent.)  │ 2 mV     │ 10 mV    │ 20 mV    │ 1 – 4×
T-wave          │ 0.3 mV   │ 1 mV     │ 3 mV     │ 4 – 20×
Noise floor     │ 10 µV    │ 30 µV    │ 100 µV   │ -

ADC input range: ±5 mV (differential)

Gain calculation:
  Gain_min = ADC_range_max / Signal_max = 5 mV / 20 mV = 0.25×
  Gain_max = ADC_range_max / Signal_min = 5 mV / 0.5 mV = 10×

Design choice: Gain range = 1× to 16× (with 0.5× option)
```

### Gain Step Resolution

```
Gain settings for iPACE-CHIP:

Setting │ Gain  │ Application
────────┼───────┼─────────────────────
0       │ 0.5×  │ Large R-wave (noisy environment)
1       │ 1×    │ Normal R-wave
2       │ 2×    │ Small R-wave
4       │ 4×    │ Large P-wave
8       │ 8×    │ Normal P-wave
16      │ 16×   │ Small P-wave (high sensitivity)

Binary-weighted gain steps for digital control:
  3-bit gain selector (8 settings available)
  
  Gain = 2^(gain_code/2) × base_gain
  Where gain_code = 0 to 5, base_gain = 0.5×
```

## Architecture

### Closed-Loop PGA (Non-Inverting)

```
Non-inverting PGA with switched feedback:

         Rf
    ┌──┤/\/\/├──┐
    │           │
Vin(+)──┤      │
    │           │
    │   ┌───────┴───────┐
    │   │               │
    │   │    Op-Amp     │──── Vout
    │   │               │
    │   └───────┬───────┘
    │           │
    │          ═══ Rg
    │           │
    └───┤Sw├───┘
        │
       GND

Gain = 1 + Rf/Rg

For Rf = 100 kΩ:
  Rg = 100 kΩ → Gain = 2×
  Rg = 50 kΩ  → Gain = 3×
  Rg = 33 kΩ  → Gain = 4×
  Rg = 12.5 kΩ → Gain = 9×
  
Switched Rg values provide discrete gain steps.
```

### Digital Gain Control

```
Gain switching network:

         Rf (fixed)
    ┌──┤/\/\/├──┐
    │           │
Vin ─┤          │
    │           │
    │   ┌───────┴───────┐
    │   │               │
    │   │    Op-Amp     │──── Vout
    │   │               │
    │   └───────┬───────┘
    │           │
    │    ┌──────┴──────┐
    │    │  Rg Switch  │
    │    │  Network    │
    │    └──────┬──────┘
    │           │
   GND     Gain_code[2:0]

Switch network (3-bit control):

  Gain_code │ Active Rg    │ Gain
  ──────────┼──────────────┼──────
  000       │ 100 kΩ       │ 2×
  001       │ 50 kΩ        │ 3×
  010       │ 33 kΩ        │ 4×
  011       │ 20 kΩ        │ 6×
  100       │ 12.5 kΩ      │ 9×
  101       │ 6.7 kΩ       │ 16×
  110       │ 3.3 kΩ       │ 31× (reserved)
  111       │ Bypass        │ 1×
```

### Fully Differential PGA

```
For differential bio-potential signals:

Vin+ ──R1──┬──┤        ├──┬── Vout+
            │  │        │  │
            │  │ Op-Amp │  │
Vin- ──R2──┘  │(diff.)  │  └── Vout-
               │        │
               └──Rf1───┘
               │
               └──Rf2───┘

Differential gain:
  Ad = Rf / R1 = Rf / R2 (for matched resistors)

CMRR requirement:
  CMRR > 60 dB (to reject 60 Hz common-mode)
  
  CMRR = 20 × log10(Ad / Acm)
  Where Acm = common-mode gain
  
  For matched resistors (0.1% matching):
  CMRR ≈ 20 × log10(1/0.001) = 60 dB ✓
```

## Circuit Design

### Op-Amp Design

```
PGA op-amp specifications:

Parameter          │ Target      │ Rationale
───────────────────┼─────────────┼────────────────────
DC gain            │ > 80 dB     │ Gain accuracy
GBW                │ > 1 MHz     │ Settling for switching
Output swing       │ Rail-to-rail│ Maximize dynamic range
Input noise        │ < 5 nV/√Hz │ Minimize total noise
Input offset       │ < 100 µV    │ < 0.5 LSB at 12-bit
Slew rate          │ > 1 V/µs    │ Fast settling
Power              │ < 5 µW      │ Budget allocation
Load drive         │ > 10 pF     │ Drive anti-alias filter
```

### Two-Stage Miller-Compensated Op-Amp

```
              VDD
               │
          ┌────┴────┐
          │  M5     │  ← Tail current source
          │  (1µA)  │
          └────┬────┘
               │
         ┌─────┴─────┐
         │           │
    ┌────┴──┐   ┌───┴────┐
    │  M1   │   │  M2    │  ← Differential pair (PMOS)
    │(W/L=  │   │(W/L=  │
    │10/1)  │   │10/1)   │
    └───┬───┘   └───┬────┘
        │           │
    ┌───┴───┐   ┌───┴────┐
    │  M3   │   │  M4    │  ← Current mirror load (NMOS)
    │(W/L=  │   │(W/L=  │
    │5/1)   │   │5/1)    │
    └───┬───┘   └───┬────┘
        │           │
        └─────┬─────┘
              │
         ┌────┴────┐
         │  M6     │  ← Second stage (common source)
         │(W/L=    │
         │20/1)    │
         └────┬────┘
              │
         ┌────┴────┐
         │  M7     │  ← Active load
         │(W/L=    │
         │10/1)    │
         └────┬────┘
              │
             VSS

Compensation:
  Cc = 1 pF (Miller capacitor between stages)
  Rc = 1 kΩ (zero-nulling resistor)
```

### Op-Amp Performance

```
Simulated op-amp performance:

Parameter          │ Value       │ Target
───────────────────┼─────────────┼────────
DC gain            │ 85 dB       │ > 80 dB ✓
Unity-gain BW      │ 2.5 MHz     │ > 1 MHz ✓
Phase margin       │ 65°         │ > 60° ✓
Slew rate          │ 1.5 V/µs   │ > 1 V/µs ✓
Input noise        │ 4.2 nV/√Hz │ < 5 nV/√Hz ✓
Input offset       │ 80 µV       │ < 100 µV ✓
Output swing       │ 0.05-1.75V  │ Rail-to-rail ✓
CMRR               │ 80 dB       │ > 60 dB ✓
PSRR               │ 75 dB       │ > 60 dB ✓
Power              │ 3.6 µW      │ < 5 µW ✓
```

## Noise Analysis

### Total Input-Referred Noise

```
Noise contributors in PGA:

1. PGA op-amp noise:
   en_OA = 4.2 nV/√Hz
   Gain = G (PGA gain)
   Referred to input: en_OA / G

2. Feedback resistor noise:
   en_Rf = √(4kT × Rf × BW)
   Rf = 100 kΩ, BW = 250 Hz
   en_Rf = √(4 × 1.38e-23 × 310 × 100e3 × 250)
   en_Rf = 0.66 µV RMS
   
   Referred to input: en_Rf / G

3. Source impedance noise (from LNA):
   en_src = √(4kT × Rsrc × BW)
   Rsrc = 10 kΩ (typical electrode impedance)
   en_src = √(4 × 1.38e-23 × 310 × 10e3 × 250)
   en_src = 0.21 µV RMS

Total input-referred noise:
  en_total = √(en_OA²/G² + en_Rf²/G² + en_src²)
  
For G = 1×:
  en_total = √((4.2e-9 × √250)² + (0.66e-6)² + (0.21e-6)²)
  en_total = √(2.76e-16 + 4.36e-13 + 4.41e-14)
  en_total = 0.70 µV RMS

For G = 16×:
  en_total = √((4.2e-9 × √250 / 16)² + (0.66e-6 / 16)² + (0.21e-6)²)
  en_total = √(1.08e-18 + 1.70e-15 + 4.41e-14)
  en_total = 0.22 µV RMS (dominated by source impedance)
```

### SNR vs Gain

```
SNR at different PGA gains:

Gain │ Input Range │ Signal (10mV) │ Noise    │ SNR
─────┼─────────────┼───────────────┼──────────┼───────
1×   │ ±20 mV      │ 10 mV         │ 0.70 µV  │ 83 dB
2×   │ ±10 mV      │ 10 mV         │ 0.45 µV  │ 87 dB
4×   │ ±5 mV       │ 10 mV         │ 0.31 µV  │ 90 dB
8×   │ ±2.5 mV     │ 2.5 mV        │ 0.25 µV  │ 80 dB
16×  │ ±1.25 mV    │ 1.25 mV       │ 0.22 µV  │ 75 dB

Note: Higher gain improves SNR for small signals
      but reduces input range (risk of clipping)
      
Optimal gain selection:
  Signal > 5 mV → use 1× or 2×
  Signal 1-5 mV → use 4× or 8×
  Signal < 1 mV → use 16×
```

## Gain Switching

### Transient Behavior

```
Gain switching transient:

  Gain
  (log)
  16×  ─────┐
             │
  8×         │
             │
  4×         └────────────
             │
  2×         │
             │
  1× ────────┘
             └──────────────
             0    50   100 µs

  Switching time: < 10 µs
  Settling time: < 50 µs (to 0.1%)
  
  During switching:
  - Output may glitch (charge injection)
  - Duration: < 1 µs
  - Amplitude: < 50 mV (input-referred)
  
  Mitigation:
  - Blank ADC sampling during switch settling
  - Use make-before-break switching
  - Pre-charge nodes to expected voltages
```

### Switch Implementation

```
CMOS transmission gate for Rg switching:

              From Rg node
                │
           ┌────┴────┐
           │         │
        ┌──┴──┐   ┌──┴──┐
        │ NMOS│   │ PMOS│
        │     │   │     │
        └──┬──┘   └──┬──┘
           │         │
           └────┬────┘
                │
              To GND

Gate control:
  EN  ─────┤NMOS├
  ENB ─────┤PMOS├ (EN inverted)

Switch resistance:
  R_sw = R_n || R_p ≈ 50 Ω (typical)
  
  Effect on gain:
  Gain = 1 + Rf / (Rg + R_sw)
  
  For Rg = 100 kΩ, R_sw = 50 Ω:
  Gain_error = R_sw / Rg = 0.05% (negligible) ✓
  
  For Rg = 6.7 kΩ, R_sw = 50 Ω:
  Gain_error = 50 / 6700 = 0.75% (acceptable) ✓
```

## Auto-Gain Control

### Signal Level Detection

```
Automatic gain selection algorithm:

1. Sample signal at current gain setting
2. Calculate signal envelope (peak detector)
3. Compare with threshold levels:

  If V_peak < V_thresh_low:
    Decrease gain (if possible)
  If V_peak > V_thresh_high:
    Increase gain (if possible)
  Else:
    Maintain current gain

Threshold levels:
  V_thresh_low = 20% of ADC FSR (optimal at 40-80%)
  V_thresh_high = 80% of ADC FSR (avoid clipping)

Hysteresis:
  10% hysteresis to prevent gain oscillation
```

### Gain Control FSM

```
┌──────────────────────────────────────────────────┐
│              Auto-Gain Control FSM               │
│                                                  │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐    │
│  │ MONITOR  │──►│ DETECT   │──►│ ADJUST   │    │
│  │ (sample) │   │ (compare)│   │ (switch) │    │
│  └──────────┘   └──────────┘   └──────────┘    │
│       ▲                                │        │
│       └────────────────────────────────┘        │
│                                                  │
│  States:                                         │
│  MONITOR: Collect samples, compute envelope     │
│  DETECT: Compare with thresholds                │
│  ADJUST: Switch gain, wait for settling         │
│                                                  │
│  Update rate: Every 100 ms (10 Hz)              │
│  Settling allowance: 50 µs per switch           │
└──────────────────────────────────────────────────┘
```

## Power Budget

```
PGA power allocation:

  Op-amp:     3.6 µW
  Bias:       0.5 µW
  Switches:   0.1 µW (dynamic)
  Control:    0.2 µW (digital)
  ─────────────────────
  Total:      4.4 µW per channel
  
  Two channels: 8.8 µW
  
  Percentage of analog budget:
  8.8 / 50 µW = 17.6% ✓
```

## Layout Considerations

```
PGA layout strategy:

1. Resistor matching:
   - Rf and Rg arrays: common-centroid
   - Dummy resistors at array edges
   - Same orientation for all resistors
   
2. Op-amp layout:
   - Differential pair: common-centroid M1/M2
   - Current mirrors: interdigitated M3/M4
   - Compensation cap: placed near output stage
   
3. Switch network:
   - Symmetrical routing for all gain paths
   - Minimize parasitic resistance mismatch
   - Guard ring around switch network
   
4. Signal routing:
   - Differential paths: matched length/width
   - Shielding of high-impedance nodes
   - Separate analog/digital routing channels
```

## Summary

| Parameter | Value |
|-----------|-------|
| Gain range | 0.5× to 16× |
| Gain steps | 6 (binary-weighted) |
| Gain accuracy | ±1% (with calibration) |
| Gain switching time | < 50 µs |
| Input noise (referred to input) | 0.22 – 0.70 µV RMS |
| Op-amp DC gain | 85 dB |
| Op-amp GBW | 2.5 MHz |
| Output swing | Rail-to-rail (0.05-1.75V) |
| Power per channel | 4.4 µW |
| Active area | 0.03 mm² |
| Technology | 180 nm CMOS |
