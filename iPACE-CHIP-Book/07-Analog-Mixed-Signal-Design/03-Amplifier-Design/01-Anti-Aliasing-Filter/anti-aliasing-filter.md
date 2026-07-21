# Anti-Aliasing Filter Design for Bio-Potential ADC

## Overview

The anti-aliasing filter (AAF) is a critical analog signal conditioning block placed before the ADC in the iPACE-CHIP signal chain. It attenuates high-frequency noise and interference above the Nyquist frequency to prevent aliasing—where out-of-band signals fold back into the desired band during sampling. For bio-potential acquisition, the AAF must provide sufficient rejection while maintaining low noise and low power consumption.

## Aliasing Theory

### What is Aliasing?

```
Aliasing occurs when a signal at frequency f_in is sampled at f_s:

  f_alias = |f_in - n × f_s|  (for integer n)

If f_alias falls within the signal band (0 to f_BW), it cannot
be distinguished from a legitimate signal.

Example:
  f_s = 2 kHz (sampling rate)
  f_BW = 250 Hz (signal bandwidth)
  f_Nyquist = f_s / 2 = 1 kHz
  
  Interference at 1.5 kHz aliases to: |1500 - 2000| = 500 Hz
  500 Hz is within the 250 Hz band? No → not a problem
  
  Interference at 750 Hz aliases to: |750 - 0| = 750 Hz
  750 Hz is within the 250 Hz band? No → not a problem
  
  Interference at 2750 Hz aliases to: |2750 - 2×2000| = 750 Hz
  Still outside band → not a problem
  
  Interference at 1125 Hz aliases to: |1125 - 2000| = 875 Hz
  Outside band → not a problem
  
  Critical case: Interference at 2000 + 250 = 2250 Hz
  Aliases to: |2250 - 2000| = 250 Hz (at band edge!)
  
  More generally: Any frequency within f_s ± f_BW aliases into band
```

### Required Attenuation

```
Anti-alias filter rejection requirement:

  Minimum rejection at f_alias = N_alias dB
  
  N_alias = Number of alias-free bits × 6.02 + 1.76
  
  For 12-bit ADC:
  N_alias = 12 × 6.02 + 1.76 = 74 dB
  
  This means the filter must provide > 74 dB rejection
  at the worst-case aliasing frequency.
  
  For 2 kHz sampling:
  Worst case: f_alias = 1750 Hz (2000 - 250)
  Filter must attenuate 1750 Hz by > 74 dB
  
  For 1st order filter (-20 dB/decade):
  Need f_stop / f_pass = 10^(74/20) = 5012
  f_stop = 5012 × 250 Hz = 1.25 MHz
  
  This is impractical for on-chip filter!
  
  Solution: Use higher-order filter + oversampling
```

### Oversampling Advantage

```
With 4× oversampling (f_s = 2 kHz, f_BW = 250 Hz):

  f_Nyquist = 1 kHz
  f_alias_min = f_s - f_BW = 1750 Hz
  
  Required rejection at 1750 Hz:
  For 12-bit: 74 dB
  
  With 2nd-order filter (-40 dB/decade):
  f_stop = f_pass × 10^(74/40) = 250 × 70.8 = 17.7 kHz
  
  This is achievable on-chip! ✓
  
  With 3rd-order filter (-60 dB/decade):
  f_stop = 250 × 10^(74/60) = 250 × 15.1 = 3.78 kHz
  
  Even more relaxed specification ✓
```

## Filter Architecture

### Sallen-Key Low-Pass Filter

```
2nd-order Sallen-Key topology:

           R1          R2
Vin ──┤/\/\/├──┬──┤/\/\/├──┬── Vout
                │           │
                │           │
               ═══ C1      ═══ C2
                │           │
                │           │
               GND         │
                           │
                    ┌──────┴──────┐
                    │   Op-Amp    │
                    │   (unity    │
                    │    gain)    │
                    └─────────────┘

Transfer function:
  H(s) = 1 / (s² × R1 × R2 × C1 × C2 + 
               s × (R1 × C2 + R2 × C2) + 1)

For Butterworth response (Q = 0.707):
  R1 = R2 = R
  C1 = 2 × C2
  
  f_c = 1 / (2π × R × √(C1 × C2))
  f_c = 1 / (2π × R × C2 × √2)
```

### Multiple Feedback (MFB) Filter

```
2nd-order MFB topology:

                R2
           ┌──┤/\/\/├──┐
           │            │
Vin ──R1──┤           ═══ C2
           │            │
          ═══ C1        ├── Vout
           │            │
          GND      ┌────┴────┐
                   │  Op-Amp  │
                   │  (inverting)│
                   └──────────┘

Transfer function:
  H(s) = -R2/(R1) / (s² × R1 × R2 × C1 × C2 +
                       s × R2 × (C1 + C2) + 1)

Advantages over Sallen-Key:
  - Inverting gain available
  - Better high-frequency rejection
  - Less sensitive to component spread
```

### Filter Order Selection

```
Filter order vs. rejection:

Order │ Slope    │ Rejection at 1750 Hz │ Component Count
──────┼──────────┼──────────────────────┼────────────────
1     │ -20 dB/dec│ -14.9 dB            │ R + C
2     │ -40 dB/dec│ -29.8 dB            │ 2R + 2C + OA
3     │ -60 dB/dec│ -44.7 dB            │ 3R + 3C + 2OA
4     │ -80 dB/dec│ -59.6 dB            │ 4R + 4C + 2OA

For 12-bit ADC (74 dB rejection needed):
  4th-order filter: 59.6 dB (insufficient alone)
  4th-order + oversampling: sufficient ✓
  
Design choice: 3rd-order filter (balance of rejection, power, area)
  + 4× oversampling provides additional digital filtering margin
```

## Design for Bio-Potential Signals

### Signal Bandwidth

```
Bio-potential signal bandwidths:

Channel      │ f_low  │ f_high │ Bandwidth │ Required f_c
─────────────┼────────┼────────┼───────────┼─────────────
Atrial       │ 40 Hz  │ 250 Hz │ 210 Hz    │ 300 Hz
Ventricular  │ 40 Hz  │ 250 Hz │ 210 Hz    │ 300 Hz
EMG          │ 20 Hz  │ 500 Hz │ 480 Hz    │ 700 Hz
EEG          │ 0.5 Hz │ 100 Hz │ 99.5 Hz   │ 150 Hz

Design choice:
  f_c = 300 Hz (for cardiac channels)
  f_stop = 1750 Hz (Nyquist consideration)
  
  Transition band: 300 Hz to 1750 Hz (ratio = 5.83)
```

### Interference Rejection

```
Common interference sources:

1. Power line interference:
   - 50/60 Hz fundamental
   - Harmonics up to 1 kHz
   - Amplitude: up to 100 mV (much larger than bio-signal)
   
   AAF rejection at 60 Hz: 0 dB (in-band, cannot filter)
   → Must use notch filter or blanking circuit
   
2. Electrode-skin impedance mismatch:
   - Creates common-mode to differential conversion
   - Frequency dependent (capacitive)
   
   AAF helps by reducing differential noise at high frequency
   
3. RF interference (100 kHz - 100 MHz):
   - From MRI, communication devices
   - Rectified by electrode nonlinearity
   
   AAF provides significant rejection:
   At 1 MHz: 3rd-order filter → -60 dB rejection ✓
```

## Circuit Implementation

### 3rd-Order Butterworth Filter

```
Cascaded 1st-order + 2nd-order stages:

  Stage 1: 1st-order RC
  ─────────────────────
           R1
  Vin ──┤/\/\/├──┬── V1
               ═══ C1
                │
               GND
  
  f_c1 = 1 / (2π × R1 × C1) = 300 Hz
  R1 = 1 MΩ, C1 = 530 pF

  Stage 2: 2nd-order Sallen-Key
  ─────────────────────
           R2          R3
  V1 ──┤/\/\/├──┬──┤/\/\/├──┬── Vout
                │           │
               ═══ C2      ═══ C3
                │           │
               GND         │
                    ┌──────┴──────┐
                    │  Op-Amp    │
                    │  (unity)   │
                    └─────────────┘
  
  f_c2 = 300 Hz (same as stage 1)
  Q = 0.707 (Butterworth)
  
  R2 = R3 = 1 MΩ
  C2 = 2 × C3 = 471 pF (C3 = 235 pF)
```

### Component Values

```
Filter component summary (3rd-order, f_c = 300 Hz):

Stage 1 (1st-order):
  R1 = 1 MΩ
  C1 = 530 pF
  
Stage 2 (2nd-order Sallen-Key):
  R2 = 1 MΩ
  R3 = 1 MΩ
  C2 = 471 pF
  C3 = 235 pF

Component spread:
  R_max / R_min = 1 (all 1 MΩ) ✓
  C_max / C_min = 530 / 235 = 2.26 ✓ (acceptable)
  
Total passive components: 3R + 3C = 6
Active components: 1 op-amp (stage 2)
```

### Op-Amp Design

```
Op-amp for anti-alias filter:

Specifications:
  - GBW > 10 × f_c = 3 kHz (minimum)
  - DC gain > 60 dB
  - Output swing: rail-to-rail
  - Power: < 5 µW
  - Input noise: < 10 nV/√Hz

Implementation (2-stage Miller-compensated):

       VDD
        │
   ┌────┴────┐
   │         │
   │  M1 M2  │  ← Differential pair (PMOS)
   │         │
   └────┬────┘
        │
   ┌────┴────┐
   │  M3 M4  │  ← Current mirror load
   └────┬────┘
        │
   ┌────┴────┐
   │  M5     │  ← Second stage (common source)
   └────┬────┘
        │
       VSS

Design parameters:
  Bias current: 1 µA (first stage)
  Second stage: 5 µA
  Compensation: 1 pF Miller cap
  
  GBW = g_m1 / C_c = 10 µS / 1 pF = 10 MHz ✓
  Phase margin: > 60° (for Butterworth Q accuracy)
```

## Frequency Response

### Magnitude Response

```
3rd-order Butterworth filter magnitude:

  |H(f)| = 1 / √(1 + (f/f_c)^(2×3))
         = 1 / √(1 + (f/300)⁶)

At key frequencies:
  f = 0 Hz:     |H| = 1.000 (0 dB)
  f = 100 Hz:   |H| = 0.999 (-0.01 dB)
  f = 250 Hz:   |H| = 0.981 (-0.17 dB) ← signal band edge
  f = 300 Hz:   |H| = 0.707 (-3.01 dB) ← cutoff frequency
  f = 500 Hz:   |H| = 0.242 (-12.3 dB)
  f = 1000 Hz:  |H| = 0.031 (-30.1 dB)
  f = 1750 Hz:  |H| = 0.004 (-48.1 dB)
  f = 2000 Hz:  |H| = 0.002 (-54.0 dB)
  f = 5000 Hz:  |H| = 0.0001 (-80.0 dB)
  
  Rejection at alias frequency (1750 Hz): 48.1 dB
  With 4× oversampling: Additional digital filtering provides
  remaining 26 dB → total > 74 dB ✓
```

### Phase Response

```
Phase response of 3rd-order Butterworth:

  φ(f) = -3 × arctan(f/f_c)
       = -3 × arctan(f/300)

At key frequencies:
  f = 0 Hz:    φ = 0°
  f = 100 Hz:  φ = -56.3°
  f = 250 Hz:  φ = -112.6°
  f = 300 Hz:  φ = -135.0° (at cutoff)
  f = 500 Hz:  φ = -171.9°
  f = 1000 Hz: φ = -198.4°
  
  Group delay: τ_g = -dφ/dω
  τ_g at DC: 3 / (2π × f_c) = 1.59 ms
  τ_g at f_c: 0.75 ms
  
  For bio-signals (40-250 Hz):
  Delay variation: ~0.5 ms (acceptable for timing analysis)
```

## Noise Analysis

### Filter Noise Contribution

```
Thermal noise from filter resistors:

  en_R² = 4kT × R × BW

For R1 = 1 MΩ, BW = 250 Hz:
  en_R1 = √(4 × 1.38e-23 × 310 × 1e6 × 250)
  en_R1 = √(4.28e-12) = 2.07 µV RMS

For R2, R3 = 1 MΩ each (in series at low frequency):
  en_R23 = √(2) × 2.07 µV = 2.93 µV RMS

Total filter noise:
  en_filter = √(en_R1² + en_R23²)
  en_filter = √(4.28 + 8.58) × 1e-6
  en_filter = 3.59 µV RMS

Contribution to total ADC noise:
  en_total = √(en_ADC² + en_filter²)
  en_total = √(36.2² + 3.59²) µV
  en_total = 36.4 µV RMS (negligible increase) ✓
```

### Op-Amp Noise

```
Op-amp input-referred noise:

  en_OA = 10 nV/√Hz (specified)
  BW = 250 Hz
  
  en_OA_total = 10 × √250 = 158 nV RMS
  
  This is negligible compared to resistor noise ✓
```

## Power Budget

```
Anti-alias filter power allocation:

  Op-amp: 1 µA × 1.8V = 1.8 µW
  Bias: 0.2 µA × 1.8V = 0.36 µW
  Total: 2.16 µW per filter
  
  Two channels (atrial + ventricular):
  Total AAF power: 4.32 µW
  
  Percentage of analog front-end budget:
  4.32 / 50 µW = 8.6% ✓
```

## Layout Considerations

```
Filter layout guidelines:

1. Component matching:
   - R1, R2, R3: Common-centroid, same orientation
   - C1, C2, C3: MIM caps, matched placement
   
2. Parasitic management:
   - Minimize routing near sensitive nodes
   - Shield high-impedance nodes (R-C junctions)
   - Guard ring around op-amp
   
3. Substrate noise isolation:
   - Separate analog ground from digital
   - Deep n-well isolation for op-amp
   - No digital routing under filter components
   
4. Component placement:
   - Filter close to ADC input
   - Short routing to minimize parasitic C
   - Symmetrical layout for differential paths
```

## Summary

| Parameter | Value |
|-----------|-------|
| Filter type | 3rd-order Butterworth |
| Topology | 1st-order RC + 2nd-order Sallen-Key |
| Cutoff frequency | 300 Hz |
| Passband ripple | < 0.2 dB (Butterworth) |
| Stopband rejection | > 48 dB at 1750 Hz |
| Input-referred noise | 3.59 µV RMS |
| Op-amp power | 1.8 µW |
| Total filter power | 2.16 µW per channel |
| Components | 3 resistors, 3 capacitors, 1 op-amp |
| Active area | 0.02 mm² |
| Technology | 180 nm CMOS |
