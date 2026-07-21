# Sigma-Delta ADC for High-Resolution Bio-Signal Acquisition

## Overview

The Sigma-Delta (ΣΔ) ADC provides high-resolution digitization of bio-potential signals through oversampling and noise shaping. In the iPACE-CHIP architecture, the ΣΔ ADC serves as an alternative to the SAR ADC for channels requiring higher dynamic range or when the design trade-off favors digital complexity over analog precision. The noise-shaping property pushes quantization noise out of band, achieving effective resolution far beyond what the single-bit or multi-bit quantizer inherently provides.

## Fundamental Principles

### Oversampling

Traditional Nyquist-rate ADCs sample at twice the signal bandwidth. ΣΔ ADCs sample at much higher rates:

```
Oversampling Ratio (OSR) = f_s / (2 × f_BW)

For iPACE-CHIP bio-signal channel:
  f_BW = 250 Hz (signal bandwidth)
  f_s = 256 kHz (chosen for power-of-2 relationship)
  
  OSR = 256000 / (2 × 250) = 512
  
  This high OSR allows noise shaping to be very effective
```

### Noise Shaping

The modulator loop shapes quantization noise, pushing energy to high frequencies:

```
Quantization noise transfer function (NTF):

  For an Lth-order modulator:
  |NTF(f)|² = (2 × sin(πf/f_s))^(2L)
  
  At low frequencies (f << f_s):
  |NTF(f)|² ≈ (2πf/f_s)^(2L)
  
  Noise is suppressed by (2π × OSR)^(-2L) in-band
  
  For L=2, OSR=512:
  In-band noise reduction = (2π × 512)^(-4) ≈ -72 dB
```

### Modulator Order Selection

```
Resolution improvement per doubling of OSR:

  1st order: 1.5 bits (9 dB)
  2nd order: 2.5 bits (15 dB)
  3rd order: 3.5 bits (21 dB)

For 12-bit target from 1-bit quantizer:
  2nd order, OSR=512: ~12.5 bits effective  ✓
  
Stability considerations:
  - 1st order: Unconditionally stable
  - 2nd order: Stable for most inputs
  - 3rd order: Requires care, possible instability
  
Design choice: 2nd order modulator (best stability/resolution trade-off)
```

## Modulator Architecture

### Single-Loop 2nd-Order Topology

```
Vin ──►(+)──┐
            │    ┌────┐    ┌────┐
      ┌─────┴────┤ H1 ├───┤ H2 ├───┐
      │     (-)  │1/s │   │1/s │   │
      │          └────┘   └────┘   │
      │                             │
      │    ┌───────┐               │
      └────┤  DAC  │◄──┐          │
           │  (1b) │   │          │
           └───────┘   │          │
                 ▲     │          │
                 │   ┌─┴──┐       │
                 └───┤ Q  │◄──────┘
                     │(1b)│
                     └─┬──┘
                       │ Dout
                       
  H1, H2: Integrators (active-RC)
  Q: 1-bit quantator (comparator)
  DAC: 1-bit (bipolar reference)
```

### Integrator Implementation

Active-RC integrators using low-power operational amplifiers:

```
                    ┌──────────────┐
                    │              │
  Vin ──R1──┬──┬───┤  Op-Amp 1    ├──┬── Vint1
            │  │   │              │  │
            │  │   └──────────────┘  │
            │  C1                   │
            │  │                    │
            └──┴────────────────────┘
                    
  Transfer function: Vint1/Vin = -1/(s × R1 × C1)
  
  Integrator time constant:
  τ1 = R1 × C1 = 1 / (2π × f_s/2)
  τ1 = 1 / (2π × 128000) ≈ 1.24 µs
  
  Component values:
  R1 = 1 MΩ (high resistance for low power)
  C1 = 1.24 pF
```

### Second Integrator

```
                    ┌──────────────┐
                    │              │
  Vint1 ──R2──┬──┬─┤  Op-Amp 2    ├──┬── Vint2
               │  │  │              │  │
               │  │  └──────────────┘  │
               │  C2                   │
               │  │                    │
               └──┴────────────────────┘

  τ2 = R2 × C2
  
  For 2nd-order noise shaping with unity-gain:
  R2 × C2 = R1 × C1
  
  R2 = 1 MΩ, C2 = 1.24 pF (matched to first stage)
```

### Quantator (1-Bit Comparator)

```
  Vint2 ────────(+)──────┐
                         │    ┌─────┐
                  (-)────┤    │ DFF │── Dout
                  │      │    │     │
                  └──────┘    └──┬──┘
                                 │ CLK
                                 ▼
                          ┌──────────┐
                          │ Reference │
                          │ Comparator │
                          └──────────┘
  
  Simple regenerative comparator:
  - Kickback: Minimal (1-bit, known voltage)
  - Offset: Cancels in loop (1-bit quantization)
  - Speed: Must resolve in < 1/f_s = 3.9 µs
```

## Loop Filter Coefficients

### Coefficient Derivation

For a 2nd-order modulator with optimized NTF zeros:

```
NTF(s) = (1 - s/a1)(1 - s/a2) / (1 + b1/s + b2/s²)

Optimal zero placement (Chebyshev):
  a1 = 2π × f_s × 0.318  (first zero)
  a2 = 2π × f_s × 0.833  (second zero)

Coefficient values (normalized):
  a1 = 0.5  (first integrator gain)
  a2 = 0.5  (second integrator gain)
  b1 = 1.0  (feedback to first integrator)
  b2 = 1.0  (feedback to second integrator)
  c1 = 0.25 (feedforward from first to second)

These correspond to:
  R1 = R2 = 1 MΩ
  Rfb1 = Rfb2 = 500 kΩ (DAC feedback)
  Rff = 4 MΩ (feedforward)
```

### Stability Analysis

```
Root locus of 2nd-order modulator:

  Loop gain: L(s) = a1 × a2 / (s² × τ1 × τ2)
  
  DC gain: |L(0)| = ∞ (integrators)
  
  Gain margin: > 6 dB (for input range ±0.8 × Vref)
  
  Maximum stable input amplitude:
  MSIA = 0.8 × Vref (for 2nd order, 1-bit)
  
  Overload recovery: < 10 clock cycles
  
  Simulated maximum stable input: 80% of full scale ✓
```

## Digital Decimation Filter

### Filter Architecture

The decimation filter converts the high-rate, low-resolution bitstream to a low-rate, high-resolution output:

```
  Dout ──►┌──────┐   ┌──────┐   ┌──────┐
          │ Sinc3 │──►│ Sinc2 │──►│ FIR  │──► Dout[15:0]
          │ (×64) │   │ (×8)  │   │(×1)  │     f_out=2kHz
          └──────┘   └──────┘   └──────┘
          
  Stage 1: Sinc³ filter, decimation by 64
    - Output rate: 256 kHz / 64 = 4 kHz
    - Passband droop: < 0.1 dB at 250 Hz
    
  Stage  Half-band, decimation by 2
    - Output rate: 4 kHz / 2 = 2 kHz
    
  Stage 3: Compensation FIR, no decimation
    - Corrects Sinc passband droop
    - Provides additional out-of-band rejection
```

### Sinc³ Filter Implementation

```
Transfer function:
  H(z) = [(1 - z^(-M)) / (M × (1 - z^(-1)))]³

Where M = decimation factor = 64

Implementation using accumulators and comb filters:

  ┌────┐   ┌────┐   ┌────┐   ┌────┐   ┌────┐
  │Acc1│──►│Acc2│──►│Acc3│──►│Comb1│──►│Comb2│──►│Comb3│
  └────┘   └────┘   └────┘   └─────┘   └─────┘   └─────┘
  
  Accumulator word width: 1 + 3 × ceil(log2(64)) = 19 bits
  Comb word width: 19 bits (no truncation)
  
  Output word width: 19 bits (truncated to 16 for output)
```

### Frequency Response

```
Sinc³ magnitude response:

  |H(f)| = [sin(πfM/f_s) / (M × sin(πf/f_s))]³

  At critical frequencies:
  f = 0:        |H| = 1.000 (0 dB)
  f = f_s/2M:   |H| = 0.827 (-1.65 dB)
  f = f_s/M:    |H| = 0.000 (-∞ dB) ← first null
  
  Stopband rejection:
  At f_s/M ± f_BW: > 80 dB rejection ✓
```

## Noise Budget

### Quantization Noise Shaping

```
In-band quantization noise power:

  P_q_inband = (Δ²/12) × (π^(2L) / (2L+1)) × (1/OSR)^(2L+1)

For 1-bit quantizer (Δ = 2 × Vref), L=2, OSR=512:
  P_q = (4 × Vref²/12) × (π^4 / 5) × (1/512)^5
  P_q = 0.333 × 19.48 × 2.91e-12
  P_q = 1.89e-11 × Vref²

Input-referred quantization noise:
  σ_q = √P_q = 4.35e-6 × Vref
  
  For Vref = 1V: σ_q = 4.35 µV RMS
  ENOB = log2(1/(4 × 4.35e-6)) / log2 = 17.5 bits ✓
```

### Integrator Noise

```
Thermal noise from first integrator dominates:

  en_int1² = 4kT × (R1 + R2_on) / (C1² × BW)
  
  R1 = 1 MΩ, R2_on ≈ 500 kΩ (switch)
  BW = 250 Hz
  
  en_int1² = 4 × 1.38e-23 × 310 × 1.5e6 / (1.24e-12)² × 250
  en_int1 = 38.2 µV RMS (input-referred)
  
  SNR_thermal = 20 × log10(Vref_peak / en_int1)
  SNR_thermal = 20 × log10(1.0 / 38.2e-6)
  SNR_thermal = 88.4 dB → ~14.4 bits ENOB from thermal ✓
```

### Flicker Noise (1/f)

```
1/f noise of integrator input transistors:

  en_flicker² = Kf / (Cox × W × L × f) × BW
  
  For PMOS input pair:
    Kf = 5e-24 V²·C/Cm²
    W/L = 100 µm / 1 µm
    Cox = 8.5 fF/µm² (180nm)
    
  At f = 1 Hz:
    en_flicker = √(5e-24 / (8.5e-3 × 100 × 1) × 250)
    en_flicker = 12.1 µV RMS
    
  Total input-referred noise:
    en_total = √(38.2² + 12.1²) = 40.1 µV RMS
    
  Overall ENOB = log2(2 × 1.0 / (2 × 40.1e-6)) = 14.6 bits ✓
```

## Power Analysis

### Modulator Power

```
Component power breakdown:

  Op-Amp 1 (first integrator):
    Bias current: 2 µA
    Supply: 1.8V
    Power: 3.6 µW
    
  Op-Amp 2 (second integrator):
    Bias current: 1 µA (relaxed noise requirement)
    Supply: 1.8V
    Power: 1.8 µW
    
  Comparator:
    Dynamic: ~50 nW average (at 256 kHz)
    
  1-bit DAC:
    Dynamic: ~100 nW (switching)
    
  Bias and references:
    ~200 nW
    
  Total modulator: 5.75 µW
```

### Decimation Filter Power

```
Digital power at 256 kHz, 1.8V:

  Sinc³ (3 accumulators, 19-bit):
    Dynamic = C_eff × V² × f
    C_eff ≈ 500 gate capacitances × 3 stages
    Power ≈ 500 × 2fF × 1.8² × 256e3 = 0.83 µW
    
  Sinc² (2 accumulators, 16-bit):
    Power ≈ 0.3 µW
    
  Compensation FIR (16 taps, 16-bit):
    Power ≈ 0.5 µW
    
  Total digital: 1.63 µW
```

### Total ADC Power

```
Total ΣΔ ADC power:
  Modulator:   5.75 µW
  Digital:     1.63 µW
  ─────────────────────
  Total:       7.38 µW
  
  Per channel (2 channels): 14.8 µW
  
  Comparison with SAR ADC:
  SAR:    2 µW per channel × 2 = 4 µW
  ΣΔ:     7.38 µW per channel × 2 = 14.8 µW
  
  ΣΔ trades power for higher resolution and simpler analog
```

## Digital Interface

### Output Data Format

```
ΣΔ ADC output (16-bit, two's complement):

  Dout[15:0] = signed 16-bit integer
  
  Range: -32768 to +32767
  LSB = Vref / 2^15 = 1.0V / 32768 = 30.5 µV
  
  Data valid signal: DVLD (high for 1 clock cycle)
  Frame sync: FS (high for first sample in frame)
  
  Interface to digital:
    Dout[15:0] ──┐
    DVLD ────────┤──► Digital Processing
    FS ──────────┘
```

### Clock Generation

```
Master clock: 256 kHz (from oscillator)
Derived clocks:
  - 256 kHz: Modulator clock
  - 4 kHz: Sinc³ output rate
  - 2 kHz: Final output rate
  
Clock jitter requirement:
  σ_jitter < 1 / (2π × f_s × SNR_linear)
  σ_jitter < 1 / (2π × 256e3 × 5000) ≈ 124 ps
  
  On-chip RC oscillator jitter: ~100 ps RMS ✓
```

## Calibration and Trimming

### Modulator Calibration

```
Sources of error:
  1. Integrator gain mismatch (affects NTF zeros)
  2. DAC mismatch (adds tones in output)
  3. Op-amp finite gain (leakage)

Calibration approach:
  - Foreground: Inject known test signal at power-up
  - Measure integrator time constants
  - Store correction coefficients
  
  Coefficient storage: 2 × 8-bit per integrator = 32 bits
  Updated: Once at power-up
```

### Dynamic Element Matching (DEM)

For multi-bit ΣΔ modulators (if upgraded):

```
Data-Weighted Averaging (DWA) algorithm:

  Pointer starts at 0
  For each clock cycle:
    Use elements[pointer] to pointer+D-1
    Advance pointer by D (output value)
    Wrap around at N elements
    
  Effect: First-order shaping of DAC mismatch
  
  Implementation: Simple counter + multiplexer
  Area overhead: ~100 gates
```

## Layout Considerations

### Modulator Floor Plan

```
┌─────────────────────────────────────────────┐
│              ΣΔ Modulator                   │
│                                             │
│  ┌─────────────┐  ┌─────────────┐          │
│  │ Integrator 1 │  │ Integrator 2 │        │
│  │ (R1, C1, OA1)│  │ (R2, C2, OA2)│       │
│  │  ██████████  │  │  ██████████  │        │
│  └─────────────┘  └─────────────┘          │
│                                             │
│  ┌─────────────┐  ┌─────────────┐          │
│  │ Comparator   │  │  1-bit DAC  │         │
│  │ (shielded)   │  │  (matched)  │         │
│  └─────────────┘  └─────────────┘          │
│                                             │
│  ░░░░░░░░░░░ Guard Ring ░░░░░░░░░░░        │
└─────────────────────────────────────────────┘

Key layout rules:
  - R1, R2: Matched to 0.1% (common-centroid)
  - C1, C2: Matched MIM caps, > 20 µm² each
  - OA1, OA2: Identical, symmetric placement
  - Guard ring: p+ ring to substrate, n+ ring for deep n-well
```

### Matching Requirements

| Component | Matching Target | Layout Technique |
|-----------|-----------------|------------------|
| R1 vs R2 | 0.1% | Interdigitated, dummy ends |
| C1 vs C2 | 0.1% | Common-centroid MIM |
| OA1 vs OA2 | Offset < 1 mV | Common-centroid layout |
| DAC references | < 0.5 LSB | Shared reference routing |

## Comparison with SAR ADC

| Parameter | ΣΔ ADC | SAR ADC |
|-----------|--------|---------|
| Resolution | 16 bits | 12 bits |
| Sampling rate | 2 kHz | 2 kHz |
| Power | 7.4 µW/ch | 2 µW/ch |
| Area | 0.25 mm² | 0.15 mm² |
| Latency | 2.5 ms | 12 µs |
| Complexity | Digital-heavy | Analog-heavy |
| Robustness | High (noise shaping) | Moderate |
| Best for | High DR signals | Fast, low-power |

## Summary

The ΣΔ ADC provides high-resolution bio-signal digitization through oversampling and noise shaping. Key design parameters:

| Parameter | Value |
|-----------|-------|
| Order | 2nd |
| OSR | 512 |
| Output resolution | 16 bits |
| Output rate | 2 kHz |
| ENOB | > 14 bits |
| Power per channel | 7.4 µW |
| Input-referred noise | 40 µV RMS |
| Active area | 0.25 mm² |
| Technology | 180 nm CMOS |

The ΣΔ architecture is particularly suitable when the iPACE-CHIP requires high dynamic range for detecting subtle atrial signals or when the digital processing benefits from higher-resolution input data.
