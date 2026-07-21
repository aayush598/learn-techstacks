# SAR ADC for Bio-Signal Acquisition

## Overview

The Successive Approximation Register (SAR) ADC is the workhorse converter in the iPACE-CHIP analog front-end. It converts the amplified bio-potential signals—atrial and ventricular electrograms—into digital representations suitable for the pacing decision engine. The SAR topology is chosen for its excellent balance of speed, power, and area, making it ideal for implantable medical devices where every nanojoule counts.

## Architecture Fundamentals

### Operating Principle

The SAR ADC performs binary search to determine the digital code corresponding to the input voltage. Starting from the most significant bit (MSB), each clock cycle resolves one bit by comparing the input against a DAC-generated reference voltage.

```
Vin+ ──────┐
           │    ┌──────────────┐
Vin- ──────┼────│  Sample &    │
           │    │  Hold (S/H)  │
           └────│              │
                └──────┬───────┘
                       │ Vsh
                ┌──────┴───────┐
                │              │
                │  Comparator  │─── Bcomp
                │              │
                └──────┬───────┘
                       │
                ┌──────┴───────┐
                │              │
                │  SAR Logic   │◄── Clock
                │              │
                └──────┬───────┘
                       │ Dout[11:0]
                       │
                ┌──────┴───────┐
                │              │
                │  DAC Array   │─── Vdac
                │              │
                └──────────────┘
```

### Key Components

| Component | Function | Design Target |
|-----------|----------|---------------|
| Sample-and-Hold | Captures input during conversion | < 0.5 LSB droop |
| Comparator | Resolves bit decisions | Offset < 0.25 LSB |
| SAR Logic | Controls binary search FSM | 12-bit in 12 cycles |
| DAC Array | Generates comparison voltages | INL < 0.5 LSB |
| Timing Controller | Sequences conversion phases | 1 MHz clock |

## Design for Bio-Potential Signals

### Signal Characteristics

Bio-potential signals from cardiac electrodes present unique challenges:

| Parameter | Atrial Signal | Ventricular Signal |
|-----------|---------------|---------------------|
| Amplitude | 0.5 – 5 mV | 2 – 20 mV |
| Bandwidth | 40 – 250 Hz | 40 – 250 Hz |
| DC Offset | Up to ±300 mV | Up to ±300 mV |
| Slew Rate | 0.1 – 1 V/s | 0.5 – 5 V/s |
| Required Resolution | 10 – 12 bits | 10 – 12 bits |

### Resolution Requirement Calculation

The minimum resolution is determined by the smallest signal that must be detected divided by the full-scale range:

```
N_bits = ceil(log2(FSR / V_signal_min))

For atrial channel:
  FSR = 10 mV (after PGA, referred to input)
  V_signal_min = 0.5 mV
  N_bits = ceil(log2(10 / 0.5)) = ceil(log2(20)) = 5 bits minimum
  
With margin for noise and DC offset variation:
  N_bits = 10 bits (design target: 12 bits)
```

### Sampling Rate Selection

Per the Nyquist theorem and pacing requirements:

```
f_s = 2 × f_max + margin
f_s = 2 × 250 Hz + 500 Hz = 1000 Hz minimum

Design choice: f_s = 2 kHz per channel
  - Provides 4× oversampling of fundamental cardiac signal
  - Allows digital filtering without aliasing artifacts
  - Compatible with pacing decision timing (detect within 50 ms)
```

## Circuit-Level Design

### Comparator Design

The comparator is the most critical analog block. For bio-signal SAR ADCs, an auto-zeroed comparator eliminates offset:

```
Phase 1 (Auto-zero):
  ┌─────────────────────────┐
  │  CLK = 0                │
  │                         │
  │  Vin+ ──┤M1├──┬──┤M3├──┤── Voutp
  │          │    │   │    │
  │  Vin- ──┤M2├──┘  │    │
  │               │   │    │
  │          ┌────┘   └────┘
  │          │  Caz   Caz
  │          │         │
  │          └─────────┘
  │                         │
  │  Offset stored on Caz   │
  └─────────────────────────┘

Phase 2 (Comparison):
  ┌─────────────────────────┐
  │  CLK = 1                │
  │                         │
  │  Input applied to       │
  │  auto-zeroed comparator │
  │                         │
  │  Result latched at      │
  │  rising edge of CLK     │
  └─────────────────────────┘
```

### Comparator Specifications

| Parameter | Specification | Rationale |
|-----------|---------------|-----------|
| Input-referred offset | < 0.5 mV | < 0.5 LSB at 12-bit, 10 mV FSR |
| Noise (RMS) | < 50 µV | < 0.5 LSB at 12-bit, 10 mV FSR |
| Power consumption | < 100 nW | Budget allocation for ADC |
| Propagation delay | < 500 ns | Within 1 MHz clock period |
| Kickback noise | < 0.2 LSB | Minimal disturbance to DAC |

### Capacitive DAC Array

The charge-redistribution DAC uses binary-weighted capacitors:

```
Vref ──┬───┤ C ├──────┬── Vdac
       │   │MSB│      │
       │   ├───┤      │
       │   │   │      │
       │   ├───┤      │
       │   │   │      │
       │   ├───┤      │
       │   │   │      │
       │   ├───┤      │
       │   │LSB│      │
       │   ├───┤      │
       │   │Cdummy│   │
       │   └───┘      │
       │              │
       └──────────────┘
            Vcm
```

### Capacitor Sizing

The unit capacitor is sized based on kT/C noise requirement:

```
Noise_power = kT / C_total

For 12-bit, 10 mV FSR:
  LSB = 10 mV / 4096 = 2.44 µV
  Required: σ_noise < 0.5 LSB = 1.22 µV
  
  C_total > kT / σ²_noise
  C_total > (1.38e-23 × 310) / (1.22e-6)²
  C_total > 2.87 fF / 1.49e-12
  C_total > 1.93 pF

Design choice: C_unit = 50 fF, C_total = 2048 × 50 fF ≈ 100 pF
```

### Mismatch Considerations

Capacitor mismatch degrades DNL and INL:

```
σ(ΔC/C) = A_c / √W × L

Where A_c is the matching coefficient:
  - Metal-Metal: A_c ≈ 0.1 – 0.5 %·µm
  - MIM Capacitor: A_c ≈ 0.05 – 0.2 %·µm

For 12-bit (INL < 0.5 LSB):
  Worst-case mismatch at MSB transition:
  σ(ΔC/C) < 0.5 LSB / √2^N
  
  Using MIM caps with A_c = 0.1 %·µm:
  W × L > (A_c / σ)² = (0.001 / 0.000244)² ≈ 16.8 µm²
  Minimum cap size: 5 µm × 5 µm = 25 µm²  ✓
```

## Calibration Techniques

### Foreground Calibration

At power-up or during idle periods, the SAR ADC performs self-calibration:

```
Calibration Sequence:
  1. Reset all DAC capacitors to known state
  2. Apply Vref/2 to comparator input
  3. Sweep each capacitor, measure comparator response
  4. Store correction codes in SRAM/Latch array
  5. Apply corrections during normal conversion

Storage requirement:
  12 bits × 12 capacitors × 1 correction = 144 bits
  Implementable with standard-cell latches
```

### Background Calibration

Continuous tracking of drift during operation:

```
┌─────────────────────────────────────────┐
│        Background Calibration FSM       │
│                                         │
│  ┌─────┐    ┌─────┐    ┌─────┐         │
│  │Idle │───►│Sample│───►│ Convert │    │
│  │     │    │Normal│    │  Normal  │    │
│  └──┬──┘    └─────┘    └─────┘      │
│     │                                  │
│     │◄── every 1024 conversions        │
│     │                                  │
│     ▼                                  │
│  ┌──────────┐                          │
│  │Calibrate │  Measure one cap pair    │
│  │One Stage │  per background cycle    │
│  └──────────┘                          │
│                                         │
│  Full recalibration: 12 × 1024 = 12K   │
│  conversions ≈ 6 seconds at 2 kHz      │
└─────────────────────────────────────────┘
```

## Power Budget Analysis

### ADC Power Allocation

```
Total iPACE-CHIP power budget: 10 µW (target)
ADC allocation: 2 µW (20% of total)

Breakdown:
  Comparator:        800 nW  (40%)
  DAC switching:     500 nW  (25%)
  SAR logic:         400 nW  (20%)
  S/H circuit:       200 nW  (10%)
  Bias/reference:    100 nW  ( 5%)
  ─────────────────────────────
  Total:           2000 nW  (100%)
```

### Energy per Conversion

```
E_conv = P_ADC × T_conversion
E_conv = 2 µW × (12 cycles / 1 MHz)
E_conv = 2 µW × 12 µs
E_conv = 24 pJ per conversion

For two channels at 2 kHz:
  E_total = 24 pJ × 2 × 2000 = 96 nW continuous
  
  Well within 2 µW budget  ✓
```

### Duty Cycling

Since bio-signals are slow compared to ADC capability, duty cycling saves power:

```
Active time per conversion: 12 µs
Sampling rate: 2 kHz (period = 500 µs)

Duty cycle = 12 µs / 500 µs = 2.4%

Effective power = Peak power × Duty cycle
Effective power = 2 µW × 0.024 = 48 nW average

This leaves margin for always-on bias circuits
```

## Noise Analysis

### Thermal Noise

```
Noise contributors (input-referred):

1. Sampling switch noise:
   en²_sw = kT / C_sampling
   C_sampling = 100 pF
   en_sw = √(4 × 1.38e-23 × 310 / 100e-12) = 12.9 µV RMS

2. Comparator noise:
   en_comp = 30 µV RMS (from transistor sizing)

3. DAC noise:
   en_dac = √(kT × R_on × BW)
   R_on = 1 kΩ (switch resistance)
   en_dac = √(4 × 1.38e-23 × 310 × 1e3 × 250) = 6.6 µV RMS

Total input-referred noise:
   en_total = √(12.9² + 30² + 6.6²) = 33.5 µV RMS
   
   SNR = 20 × log10(10 mV / (2 × 33.5 µV))
   SNR = 20 × log10(149.3) = 43.5 dB
   
   Effective number of bits:
   ENOB = (SNR - 1.76) / 6.02 = (43.5 - 1.76) / 6.02 = 6.9 bits
   
   Adequate for bio-signal detection  ✓
   (Signal of interest is 0.5–20 mV, not full scale)
```

### Quantization Noise

```
For N-bit ADC with FSR = Vref:
  q = Vref / 2^N
  
  Quantization noise power = q² / 12
  
  For 12-bit, 10 mV FSR:
    q = 10 mV / 4096 = 2.44 µV
    Noise_rms = 2.44 µV / √12 = 0.705 µV
    
  SNR_q = 6.02 × N + 1.76 = 6.02 × 12 + 1.76 = 74 dB
  
  Thermal noise dominates → quantization noise negligible ✓
```

## Layout Considerations

### Floor Plan

```
┌─────────────────────────────────────────┐
│              SAR ADC Top                │
│                                         │
│  ┌──────────┐  ┌──────────────────┐    │
│  │  Bias &  │  │   SAR Logic +    │    │
│  │ Reference │  │   Registers     │    │
│  │          │  │                  │    │
│  └──────────┘  └──────────────────┘    │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │     Capacitor DAC Array          │  │
│  │     (common-centroid layout)     │  │
│  └──────────────────────────────────┘  │
│                                         │
│  ┌──────────┐  ┌──────────────────┐    │
│  │Comparator│  │   Sample/Hold    │    │
│  │(shielded)│  │                  │    │
│  └──────────┘  └──────────────────┘  │
│                                         │
│  ▓▓▓ Guard ring (substrate isolation)  │
└─────────────────────────────────────────┘
```

### Matching Strategies

1. **Common-centroid layout** for DAC capacitor array
2. **Interdigitation** of unit capacitors
3. **Dummy devices** at array edges
4. **Symmetry** in signal routing
5. **Shielding** of sensitive nodes

### Parasitic Management

```
Critical parasitics:
  C_parasitic < C_unit / 100 = 0.5 fF
  
  Layout rules:
  - Minimum spacing between DAC nodes: 2 µm
  - Shielding of high-impedance nodes
  - Guard rings around comparator
  - Separate analog/digital routing channels
```

## Simulation Verification

### Performance Metrics to Verify

| Metric | Target | Simulation Method |
|--------|--------|-------------------|
| ENOB | > 10 bits | SINAD test with sine wave |
| DNL | < ±0.5 LSB | Code density test |
| INL | < ±0.5 LSB | Endpoint fit |
| Power | < 2 µW | Transient power measurement |
| Conversion time | < 12 µs | Timing simulation |
| SFDR | > 65 dB | FFT analysis |

### Corner Simulation Matrix

```
Process corners: TT, FF, SS, SF, FS
Temperature: -40°C, 25°C, 60°C (body temperature)
Supply: 1.8V ± 10%

Total simulation cases: 5 × 3 × 3 = 45 corners

Key results to track:
  - ENOB vs corner (must maintain > 10 bits)
  - Power vs temperature (must stay < 2 µW)
  - Offset vs corner (must stay < 0.5 LSB)
```

## Integration with iPACE-CHIP

### Signal Path

```
Electrode → LNA → PGA → Anti-Alias → S/H → SAR ADC → Digital
                                                   │
                                              ┌────┴────┐
                                              │ Ch 1: Atr│
                                              │ Ch 2: Ven│
                                              └─────────┘
```

### Interface to Digital Domain

```
ADC Output Interface:
  - 12-bit parallel bus (or SPI for area savings)
  - Conversion-ready interrupt signal
  - Channel select mux output
  
  Timing:
    CLK rising edge: Start conversion
    CLK cycles 1-12: Bit decisions
    CLK cycle 13: Conversion complete, data valid
    Data valid for: 1 clock cycle (sampled by digital)
```

### Calibration Data Storage

```
Calibration coefficients stored in:
  - 12 × 8-bit correction values = 96 bits
  - Stored in shadow registers
  - Loaded at power-up from eFuse or SRAM
  - Updated by background calibration FSM
```

## Summary

The SAR ADC in the iPACE-CHIP is designed with the following key parameters:

| Parameter | Value |
|-----------|-------|
| Resolution | 12 bits |
| Sampling rate | 2 kHz per channel |
| Number of channels | 2 (atrial + ventricular) |
| Power consumption | < 2 µW |
| ENOB | > 10 bits |
| DNL/INL | < ±0.5 LSB |
| Input range | ±5 mV (after PGA) |
| Technology | 180 nm CMOS |
| Active area | 0.15 mm² |

The SAR architecture provides the optimal trade-off for bio-potential acquisition in an implantable pacemaker, combining moderate resolution with low power and small area. The calibration system ensures accuracy over process, temperature, and aging variations encountered over the device lifetime.
