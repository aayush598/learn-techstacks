# Current Steering DAC for Pacing Applications

## Overview

The Current Steering DAC (CS-DAC) is the core digital-to-analog converter architecture used in the iPACE-CHIP pacing output stage. Unlike voltage-mode DACs that generate a voltage output, the CS-DAC directly produces a programmed current that flows through the pacing lead into cardiac tissue. This approach provides inherent current regulation independent of load impedance variations, making it ideal for implantable pacemakers where lead impedance can change over time.

## Operating Principle

### Basic Current Steering Concept

```
Current Steering DAC Operation:

  Iref ────┬────┬────┬────
           │    │    │
        ┌──┴─┐┌─┴──┐┌─┴──┐
        │ I0 ││ I1 ││ I2 │  ← Unit current sources
        └──┬─┘└─┬──┘└─┬──┘
           │    │    │
        ┌──┴──┐┌┴──┐┌─┴──┐
        │ SW0 ││SW1││SW2│  ← Steering switches
        └──┬──┘└┬──┘└─┬──┘
           │    │    │
           ▼    │    ▼
         Iout   │   Iout_bar
                │
              (to load)

  When SW0=1: I0 → Iout
  When SW0=0: I0 → Iout_bar
  
  Total Iout = Σ (SWi × Ii)
```

### Thermometer vs Binary Coding

```
Thermometer Coding (preferred for linearity):

  3-bit example: 7 unit elements
  
  Code 0: ○○○○○○○  → Iout = 0
  Code 1: ●○○○○○○  → Iout = I
  Code 2: ●●○○○○○  → Iout = 2I
  Code 3: ●●●○○○○  → Iout = 3I
  Code 4: ●●●●○○○  → Iout = 4I
  Code 5: ●●●●●○○  → Iout = 5I
  Code 6: ●●●●●●○  → Iout = 6I
  Code 7: ●●●●●●●  → Iout = 7I

Binary Coding (smaller area):

  3-bit example: 3 weighted elements
  
  Code 0: 000  → Iout = 0
  Code 1: 001  → Iout = I (LSB)
  Code 2: 010  → Iout = 2I
  Code 3: 011  → Iout = 3I
  Code 4: 100  → Iout = 4I (MSB = 4× LSB)
  Code 5: 101  → Iout = 5I
  Code 6: 110  → Iout = 6I
  Code 7: 111  → Iout = 7I

For iPACE-CHIP: Segmented architecture
  - Upper 4 bits: Thermometer (15 elements)
  - Lower 4 bits: Binary (4 weighted elements)
  - Total: 8-bit resolution
```

## Circuit Implementation

### Unit Current Source

```
PMOS Current Source with Cascode:

       VDD
        │
   ┌────┴────┐
   │         │
   │   M1    │  ← Main current source
   │ (W/L=4/2)│    VGS set by bias voltage
   │         │
   ├─────────┤
   │         │
   │   M2    │  ← Cascode transistor
   │ (W/L=2/1)│    Increases output impedance
   │         │
   └────┬────┘
        │
        └──── Iout (to switch)

Output impedance:
  R_out = g_m2 × r_o2 × r_o1 ≈ (g_m × r_o)² × r_o1
  
  For 180nm: g_m × r_o ≈ 50
  R_out ≈ 50² × 1 MΩ = 2.5 GΩ (ideal)
  Actual: ~100 MΩ (with parasitics)
  
  This ensures > 60 dB variation over 100-1000 Ω load
```

### Steering Switch

```
Current Steering Switch (Differential):

         Isrc (from current source)
          │
     ┌────┴────┐
     │         │
  ┌──┴──┐   ┌──┴──┐
  │ M3  │   │ M4  │  ← PMOS steering pair
  │     │   │     │
  └──┬──┘   └──┬──┘
     │         │
     ▼         ▼
   Iout      Iout_bar
     │
     └──→ To output stage

Control signals:
  SW_P ────┤M3├──→ Iout
  SW_N ────┤M4├──→ Iout_bar

Switch timing (critical for glitch-free output):
  
  SW_P:  ───┐  ┌─────────────
            └──┘
  SW_N:  ───────────┐  ┌────
                    └──┘
  
  Make-before-break: Both switches on briefly
  Duration: < 1 ns (minimize feedthrough)
```

### Switch Driver

```
Switch Driver Circuit:

  Digital ──┬──► Inverter ──┬──► SW_P (PMOS gate)
  Code      │              │
            └──► Inverter ──┴──► SW_N (NMOS gate)
                   │
                   └── Delay (matching)
  
  Purpose:
  1. Generate differential control signals
  2. Match timing between P and N paths
  3. Provide sufficient drive strength
  4. Level shift if needed (1.8V → 5V for output stage)
```

## Segmented Architecture

### 8-Bit Segmented CS-DAC

```
Segmentation: 4-bit thermometer + 4-bit binary

  ┌──────────────────────────────────────────────────┐
  │                                                  │
  │  MSB Segment (4-bit thermometer, 15 elements)   │
  │  ┌─────────────────────────────────────────┐    │
  │  │  U1  U2  U3  U4  U5  U6  U7  U8  ...   │    │
  │  │  ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐ ┌─┐      │    │
  │  │  │I│ │I│ │I│ │I│ │I│ │I│ │I│ │I│ × 15  │    │
  │  │  └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘ └─┘      │    │
  │  └──────────────────────┬──────────────────┘    │
  │                         │ I_msb                  │
  │  LSB Segment (4-bit binary, 4 elements)        │
  │  ┌─────────────────────────────────────────┐    │
  │  │  W1    W2     W4     W8                  │    │
  │  │  ┌─┐  ┌──┐  ┌───┐  ┌────┐              │    │
  │  │  │I│  │2I│  │4I │  │8I  │              │    │
  │  │  └─┘  └──┘  └───┘  └────┘              │    │
  │  └──────────────────────┬──────────────────┘    │
  │                         │ I_lsb                  │
  │                         ▼                        │
  │                      Iout = I_msb + I_lsb        │
  └──────────────────────────────────────────────────┘

  Total elements: 15 (thermometer) + 4 (binary) = 19
  vs. pure thermometer: 255 elements
  
  Area savings: ~93%
  DNL penalty: < 0.3 LSB (with proper matching)
```

### Segment Transition Matching

```
At major segment boundary (code 0x0F → 0x10):

  Code 0x0F: 15 MSB elements ON, all LSB OFF
             Iout = 15 × I_unit
             
  Code 0x10: 16th MSB element ON, all LSB OFF
             Iout = 16 × I_unit
  
  Mismatch concern:
  - MSB element 16 vs sum of 15 LSB elements
  - Requirement: Element 16 = Sum of W1+W2+W4+W8 = 15 × I_unit
  - Matching target: < 0.5 LSB (at 8-bit level)
  
  Mitigation:
  - Size MSB elements 2× larger than needed
  - Trim MSB element to match LSB segment sum
  - Use calibration to correct any residual error
```

## Noise Analysis

### Current Source Noise

```
Thermal noise of current source transistor:

  In² = 4kT × g_m × BW

For M1 (main current source):
  g_m = 2 × I_D / V_ov
  For I_D = 62.5 µA (8-bit, 10 mA full scale / 16 × MSB_factor):
  V_ov = 0.2V
  g_m = 2 × 62.5 µA / 0.2V = 625 µS
  
  In = √(4 × 1.38e-23 × 310 × 625e-6 × 250)
  In = √(2.68e-17) = 164 pA/√Hz
  
  Total noise in 250 Hz band:
  In_total = 164 × √250 = 2.6 nA RMS
  
  In percentage of full scale (10 mA):
  In/Ifull = 2.6 nA / 10 mA = 0.000026% ✓
  (Negligible for 8-bit application)
```

### Flicker Noise

```
1/f noise of current source:

  In²_flicker = Kf / (Cox × W × L × f) × I_D²

For 180nm PMOS:
  Kf = 5e-24 V²·C/Cm²
  W/L = 4 µm / 2 µm
  Cox = 8.5 fF/µm²
  
  At f = 1 Hz:
  In_flicker = I_D × √(Kf / (Cox × W × L × f))
  In_flicker = 62.5e-6 × √(5e-24 / (8.5e-3 × 8 × 1))
  In_flicker = 62.5e-6 × √(7.35e-20)
  In_flicker = 62.5e-6 × 2.71e-10 = 17 pA/√Hz
  
  Flicker corner frequency:
  f_c = In²_flicker / In²_thermal = (17/164)² = 0.011
  f_c = 1 Hz / 0.011 ≈ 91 Hz
  
  In-band flicker noise (40-250 Hz):
  In_f = 17 × √(250 - 40) = 246 pA RMS
  
  Negligible compared to thermal noise ✓
```

## Glitch Energy Minimization

### Source of Glitches

```
Glitch sources during code transitions:

1. Switch timing mismatch:
   - Different propagation delays in SW_P and SW_N
   - Causes momentary overlap or gap
   
2. Code-dependent delay:
   - Different code paths have different delays
   - MSB transitions have more switching activity
   
3. Charge injection:
   - Switch gate charge couples to output
   - Proportional to switch size

Glitch energy metric:
  E_glitch = ∫|ΔI(t)| dt (in A·s)
  
  Target: E_glitch < 0.5 LSB × T_clock
  For 8-bit, 10 mA, 10 µs clock:
  E_glitch < 0.039 mA × 10 µs = 0.39 nA·s
```

### Mitigation Techniques

```
1. Return-to-zero coding:
   - Insert zero-code between all transitions
   - Glitch occurs at zero level (no output disturbance)
   
   Code sequence: N → 0 → M (instead of N → M)
   
2. Synchronized switching:
   - All switches driven by same clock edge
   - Eliminates timing skew between elements
   
3. Dummy switches:
   - Add complementary charge injection
   - Cancel output charge disturbance
   
4. Current source cascoding:
   - High output impedance limits voltage glitch
   - V_glitch = E_glitch / C_parasitic
```

## Dynamic Performance

### Settling Time

```
Output settling after code change:

  Iout(t) = I_final × (1 - exp(-t/τ_settle))

Where τ_settle = R_load × C_parasitic

For R_load = 500 Ω, C_parasitic = 1 pF:
  τ_settle = 500 × 1e-12 = 500 ps
  
  Settling to 0.5 LSB (8-bit):
  t_settle = τ_settle × ln(2^8) = 500 ps × 5.55 = 2.77 ns
  
  This is << clock period (10 µs) ✓
```

### SFDR Performance

```
Spurious-Free Dynamic Range of CS-DAC:

Major spurs from:
1. Current source mismatch → harmonic distortion
2. Switch nonlinearity → even harmonics
3. Clock feedthrough → spurs at clock-related frequencies

Expected SFDR for 8-bit CS-DAC:
  SFDR ≈ 6.02 × N + 1.76 - mismatch_error
  SFDR ≈ 50 dB - 3 dB (mismatch) = 47 dBc
  
  For 10 mA full scale:
  Largest spur amplitude = 10 mA / 10^(47/20) = 22.5 µA
  
  This corresponds to 0.22 LSB → acceptable ✓
```

## Power Optimization

### Current Mode Operation

```
CS-DAC power dissipation:

  P_total = P_current_sources + P_switches + P_bias + P_digital

  Current sources (always on during pacing):
    P_sources = V_supply × I_total
    For 5V supply, 10 mA output + overhead:
    P_sources = 5V × 12 mA = 60 mW (peak)
    
  Switches (dynamic):
    P_switches = C_load × V² × f_code
    For 1 pF, 5V, 10 kHz switching:
    P_switches = 1e-12 × 25 × 1e4 = 250 nW (negligible)
    
  Bias:
    P_bias = 5V × 50 µA = 250 µW
    
  Digital:
    P_digital = 1.8V × 10 µA = 18 µW
    
  Total peak: 60.3 mW (dominated by current sources)
```

### Duty Cycling Strategy

```
CS-DAC power reduction through duty cycling:

  Pacing pulse: 1 ms duration
  Pacing rate: 70 bpm (0.857 Hz)
  
  Duty cycle: 1 ms × 0.857 Hz = 0.0857%
  
  Average power:
  P_avg = 60.3 mW × 0.000857 + P_idle
  P_avg = 51.7 µW + 268 µW (bias + digital)
  P_avg = 319.7 µW
  
  With power gating between pulses:
  P_avg = 51.7 µW + 50 µW (always-on bias) = 101.7 µW
```

## Calibration Techniques

### Foreground Calibration

```
Power-up calibration sequence:

1. Output current measurement:
   - Route output through precision R_sense
   - Measure voltage across R_sense with ADC
   - Calculate actual current for each code
   
2. Element matching calibration:
   - Compare each element to reference element
   - Store correction in SRAM
   - 8-bit correction per element × 19 elements = 152 bits
   
3. Gain calibration:
   - Set full-scale code (0xFF)
   - Adjust bias current until Iout = target
   - Store gain code in register
```

### Background Calibration

```
Continuous matching improvement:

Algorithm:
  1. During idle periods (no pacing), cycle through elements
  2. Compare each element to running average
  3. Update correction coefficients
  4. Apply correction in real-time
  
Update rate: 1 element per 10 ms
Full calibration: 19 elements × 10 ms = 190 ms
  
Stored data:
  - 19 × 8-bit correction values = 152 bits
  - 1 × 8-bit gain correction = 8 bits
  - Total: 160 bits in shadow registers
```

## Layout Design

### Common-Centroid Current Source Array

```
15-element thermometer array (4-bit MSB):

  Row 1:  [1] [3] [5] [7] [9] [11] [13] [15]
  Row 2:  [2] [4] [6] [8] [10] [12] [14]
  
  Common-centroid pattern:
  
  ┌───┬───┬───┬───┬───┬───┬───┬───┐
  │ 1 │ 8 │ 3 │10 │ 5 │12 │ 7 │14 │
  ├───┼───┼───┼───┼───┼───┼───┼───┤
  │ 9 │ 2 │11 │ 4 │13 │ 6 │15 │   │
  └───┴───┴───┴───┴───┴───┴───┴───┘
  
  Matching: Gradient errors cancel
  Area: 15 × (4µm × 2µm) = 120 µm²
  With spacing: ~200 µm²
```

### Output Routing

```
High-current output path:

  From current sources → Switches → Summing node → Output pad
  
  Requirements:
  - Low resistance (< 1 Ω total)
  - Minimal parasitic capacitance
  - ESD protection
  
  Layout approach:
  ┌────────────────────────────────────┐
  │ Current    │  Switches  │  Output  │
  │ Sources    │  Array     │  Bus     │
  │ ████ ████  │  ▓▓▓▓ ▓▓▓▓ │ ════════ │→ Pad
  │ ████ ████  │  ▓▓▓▓ ▓▓▓▓ │ ════════ │
  └────────────────────────────────────┘
  
  Output bus: 50 µm wide, top metal
  R_bus < 0.5 Ω for 500 µm length
```

## Summary

| Parameter | Value |
|-----------|-------|
| Architecture | Current steering, segmented |
| Resolution | 8 bits |
| Segmentation | 4-bit thermometer + 4-bit binary |
| Full-scale current | 10 mA |
| LSB current | 39.1 µA |
| Output impedance | > 100 MΩ |
| Settling time | < 5 ns |
| SFDR | > 47 dBc |
| DNL | < ±0.5 LSB |
| INL | < ±0.5 LSB |
| Power (peak) | 60 mW |
| Power (average, 70 bpm) | 102 µW |
| Active area | 0.12 mm² |
| Technology | 180 nm CMOS |
