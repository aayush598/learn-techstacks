# Resistor Ladder DAC for Pacing Voltage Generation

## Overview

The Resistor Ladder DAC (R-2R or string DAC) generates precise analog voltages from digital codes through a network of resistors. In the iPACE-CHIP, the resistor ladder DAC serves as the voltage reference generator for pacing pulse amplitude control. While current steering DACs are preferred for high-current output, resistor ladder DACs provide excellent linearity for voltage-mode pacing and serve as the internal reference generation for the entire analog front-end.

## Architecture Types

### String DAC (Segmented Resistor Ladder)

```
String DAC Architecture:

  Vref_hi ──┤R├──┬──┤R├──┬──┤R├──┬──┤R├──┬── Vref_lo
             │    │    │    │    │    │    │
             │    │    │    │    │    │    │
            ┌┴┐  ┌┴┐  ┌┴┐  ┌┴┐  ┌┴┐  ┌┴┐  ┌┴┐
            │S0│ │S1│ │S2│ │S3│ │S4│ │S5│ │S6│  ← Switches
            └┬┘  └┬┘  └┬┘  └┬┘  └┬┘  └┬┘  └┬┘
             │    │    │    │    │    │    │
             └────┴────┴────┴────┴────┴────┘
                              │
                             Vout

  Number of resistors: 2^N (for N-bit DAC)
  Number of switches: 2^N
  
  For 8-bit: 256 resistors, 256 switches
  
  Advantages:
  + Inherently monotonic
  + No missing codes
  + Simple design
  
  Disadvantages:
  - Large area (2^N elements)
  - High parasitic capacitance
  - Slow settling for large N
```

### R-2R Ladder DAC

```
R-2R Ladder Architecture:

                    Vref
                     │
                     R
                     │
          ┌──────────┤
          │          │
         R         ┌─┴─┐
          │        │S7 │  ← MSB switch
          │        └─┬─┘
          │          │
          │          ├──── Vout
          │          │
          │         R
          │          │
          │     ┌────┤
          │     │    │
          │    R   ┌─┴─┐
          │     │  │S6 │
          │     │  └─┬─┘
          │     │    │
          │     │    ├──── Vout
          │     │    │
          │     │   R
          │     │    │
          │     └────┤
          │          │
         ...       ...
          │          │
         R         ┌─┴─┐
          │        │S0 │  ← LSB switch
          │        └─┬─┘
          │          │
          └──────────┘
                     │
                    GND

  Number of resistors: 3 × N (for N-bit DAC)
  Number of switches: N
  
  For 8-bit: 24 resistors, 8 switches
  
  Advantages:
  + Small area (3N elements vs 2^N)
  + Fast settling
  + Low parasitic capacitance
  
  Disadvantages:
  - Resistor matching critical at LSB end
  - Not inherently monotonic without trimming
```

## R-2R Ladder Analysis

### Ladder Theory

```
R-2R Ladder Voltage Division:

At each node, the resistance looking left is 2R, looking right is 2R.
The divider ratio at each node is exactly 1/2.

  Vref ──R──┬──R──┬──R──┬──R── GND
            │     │     │     │
           2R    2R    2R    2R
            │     │     │     │
           GND   GND   GND   GND

Each bit contributes:
  Vout = Vref × Σ(Bi × 2^i / 2^N)

Where Bi is the bit value (0 or 1).

Example (4-bit):
  B3=1, B2=0, B1=1, B0=0
  Vout = Vref × (8/16 + 0/16 + 2/16 + 0/16)
  Vout = Vref × 10/16 = 0.625 × Vref
```

### Output Impedance

```
R-2R Ladder Output Impedance:

The Thevenin equivalent resistance of the ladder:
  R_out = R (for ideal R-2R network)

For all digital codes, the output impedance is constant:
  R_out = R = 10 kΩ (design value)

This is a key advantage over string DACs:
  String DAC: R_out varies from 0 to R × 2^N / 2
  R-2R DAC:   R_out = R (constant)

Constant output impedance simplifies:
  - Buffer amplifier design
  - Settling time analysis
  - Load regulation
```

### Ladder Resistor Sizing

```
Resistor value selection:

  R = 10 kΩ (chosen for: power, area, noise trade-off)
  2R = 20 kΩ

Power per element:
  P_element = V² / R_element
  For Vref = 1V, R = 10 kΩ:
  P_element = 1 / 10000 = 100 µW per branch

Total ladder power (8-bit):
  8 branches active (in parallel)
  P_ladder = 8 × 100 µW = 800 µW
  
  This is too high for implantable device!
  
  Solution: Use higher R values
  R = 100 kΩ → P_ladder = 80 µW ✓
  R = 1 MΩ → P_ladder = 8 µW (but slower settling)
```

## String DAC Implementation

### 8-Bit String DAC

```
Full string DAC with 256 resistors:

  Vref_hi ──┤R├──┤R├──┤R├──...──┤R├── Vref_lo
             │    │    │         │
            ┌┴┐  ┌┴┐  ┌┴┐      ┌┴┐
            │S0│ │S1│ │S2│ ... │S255│
            └┬┘  └┬┘  └┬┘      └┬┘
             │    │    │         │
             └────┴────┴─────────┘
                       │
                      Vout

  Element matching requirement:
  σ(ΔR/R) < 0.5 LSB / √(2^N) at worst case
  
  For 8-bit: σ(ΔR/R) < 0.5 / 16 = 3.1%
  
  Using poly resistor:
  A_R = 0.1 %·µm (matching coefficient)
  
  R_min = (A_R / σ)² = (0.1 / 3.1)² = 0.001 µm²
  This is very relaxed → area dominated by switch size
  
  Design choice: R = 50 kΩ per element
  Total resistance: 256 × 50 kΩ = 12.8 MΩ
  Total area: 256 × 2 µm × 10 µm = 51,200 µm² = 0.05 mm²
```

### Switch Implementation

```
CMOS Transmission Gate Switch:

         Vout (from resistor node)
          │
     ┌────┴────┐
     │         │
  ┌──┴──┐   ┌──┴──┐
  │ NMOS│   │ PMOS│  ← Transmission gate
  │     │   │     │
  └──┬──┘   └──┬──┘
     │         │
     └────┬────┘
          │
         DAC_out

Control:
  NMOS gate: EN (active high)
  PMOS gate: ENB (active low, inverted EN)

Switch resistance:
  R_sw = R_nmos || R_pmos ≈ 50 Ω (typical)
  
  Effect on output:
  V_error = I_out × R_sw
  For I_out = 10 µA: V_error = 0.5 mV (0.05% of 1V FSR)
  
  This is < 0.5 LSB at 8-bit → acceptable ✓
```

## Matching and Calibration

### Resistor Matching Analysis

```
Random mismatch (sigma):

  σ(ΔR/R) = A_R / √(W × L)

For poly resistor in 180nm:
  A_R = 0.1 %·µm (typical)
  
  W × L = 2 µm × 10 µm = 20 µm²
  σ = 0.1 / √20 = 0.022%

  For string DAC with 256 elements:
  Worst case mismatch: √(256) × 0.022% = 0.35%
  In LSB: 0.35% × 256 = 0.9 LSB
  
  This exceeds 0.5 LSB requirement → trimming needed!

Systematic mismatch (gradient):

  ΔR = G × Δx (linear gradient)
  G = 0.01% per µm (typical)
  
  For 100 µm resistor chain length:
  ΔR_max = 0.01% × 100 = 1%
  In LSB: 1% × 256 = 2.56 LSB
  
  Mitigation: Common-centroid layout
```

### Digital Calibration

```
Calibration approach for string DAC:

1. Measure actual code transitions:
   - Apply precision voltage reference
   - Sweep DAC code, measure output
   - Record transition voltages
   
2. Build lookup table:
   Code → Actual voltage mapping
   Stored in 256 × 12-bit table = 3072 bits
   
3. Apply correction:
   Desired code → Lookup corrected code
   Use corrected code for output

Implementation:
  - 3 Kbit SRAM for calibration table
  - Digital correction logic (comparator + mux)
  - Power: < 1 µW (digital only)
  - Area: ~0.01 mm² (SRAM)
```

### Analog Trimming

```
Laser trimming of resistor values:

Process:
  1. Fabricate with wider-than-normal resistors
  2. Measure resistance of each element
  3. Laser cut trim taps to adjust value
  4. Achieve < 0.1% matching

Trim tap implementation:
  ────┤R├────┤R├────
       │      │
       ├──────┤  ← Trim tap (can be shorted)
       │      │
       └──────┘
       
  Shorting trim tap reduces R by fixed amount
  
Advantages:
  - No digital overhead
  - Permanent correction
  - No calibration time
  
Disadvantages:
  - Requires laser equipment
  - Adds test time/cost
  - Not reconfigurable
```

## Output Buffer

### Voltage Follower

```
Buffer amplifier for R-2R output:

         VDD
          │
     ┌────┴────┐
     │         │
  ┌──┴──┐      │
  │ M1  │      │
  │     │      │
  └──┬──┘      │
     │         │
  ┌──┴──┐   ┌──┴──┐
  │ M2  │   │ M3  │
  │     │   │     │
  └──┬──┘   └──┬──┘
     │         │
  Vout ────────┘
     │
     └──► To output stage

  Unity-gain buffer:
  Vout = V_in (from R-2R ladder)
  
  Specifications:
  - Input impedance: > 10 MΩ (FET input)
  - Output impedance: < 100 Ω
  - Bandwidth: > 1 MHz
  - Offset: < 1 mV (with calibration)
  - Power: < 10 µW
```

### Buffer Sizing

```
Op-amp design for buffer:

First stage (differential pair):
  PMOS input: W/L = 20 µm / 1 µm
  Bias current: 5 µA
  
Second stage (gain):
  W/L = 40 µm / 2 µm
  Bias current: 10 µA
  
Output stage (class AB):
  W/L = 50 µm / 1 µm
  Bias current: 20 µA
  
Total buffer power:
  P_buffer = 1.8V × (5 + 10 + 20) µA = 63 µW

Performance:
  DC gain: > 60 dB
  GBW: > 5 MHz
  Slew rate: > 5 V/µs
  Output swing: 0.1V to 1.7V (rail-to-rail)
```

## Power Analysis

### String DAC Power

```
String DAC power components:

1. Resistor ladder:
   P_ladder = V²_ref / R_total
   
   For Vref = 1V, R = 50 kΩ per element:
   Each node draws: V / R = 20 µA (max)
   Total current (all switches open): 0
   Total current (mid-scale): ~5 mA (worst case)
   
   With output buffer (high impedance):
   P_ladder = V²_ref / R_string = 1 / 12.8M = 78 nW
   
2. Switches:
   P_switches = dynamic only ≈ 10 nW
   
3. Buffer:
   P_buffer = 63 µW
   
4. Bias:
   P_bias = 5 µW
   
Total: 68 µW
```

### R-2R DAC Power

```
R-2R DAC power components:

1. R-2R ladder:
   P_ladder = V²_ref / R_equivalent
   R_equivalent = R = 100 kΩ
   P_ladder = 1 / 100000 = 10 µW
   
2. Switches:
   P_switches = dynamic ≈ 5 nW
   
3. Buffer (if needed):
   P_buffer = 63 µW
   
4. Bias:
   P_bias = 5 µW
   
Total (with buffer): 78 µW
Total (without buffer): 15 µW
```

## Comparison with CS-DAC

```
Performance comparison:

Parameter          │ String DAC    │ R-2R DAC      │ CS-DAC
───────────────────┼───────────────┼───────────────┼──────────────
Resolution         │ 8-12 bits     │ 8-12 bits     │ 8 bits
Monotonicity       │ Guaranteed    │ With trimming │ With calibration
Linearity (INL)    │ < 0.5 LSB     │ < 1 LSB       │ < 0.5 LSB
Output type        │ Voltage       │ Voltage       │ Current
Output impedance   │ Variable      │ Constant (R)  │ High (cascoded)
Settling time      │ Fast          │ Fast          │ Very fast
Area               │ Large (2^N)   │ Medium (3N)   │ Small (N)
Power              │ Low (static)  │ Low (static)  │ High (dynamic)
Speed              │ Limited       │ Medium        │ High
Best application   │ Reference gen │ Reference gen │ High-current output
```

## Integration

### DAC in iPACE-CHIP

```
Voltage reference chain:

  Bandgap ──► Reference DAC ──► PGA ──► ADC
     │              │
     │         ┌────┴────┐
     │         │ String  │
     │         │ DAC     │
     │         │ (10-bit)│
     │         └────┬────┘
     │              │
     │         ┌────┴────┐
     │         │ Buffer  │
     │         │ Amp     │
     │         └────┬────┘
     │              │
     └──────────────┤
                    │
               Vref_select (digital control)

  Modes:
  - Fixed reference: 1.0V from bandgap
  - Programmable: 0.5V to 1.5V from DAC
  - Calibrated: Trimmed to ±0.1% accuracy
```

## Summary

| Parameter | String DAC | R-2R DAC |
|-----------|------------|----------|
| Architecture | 2^N resistors | 3N resistors |
| Resolution | 8-12 bits | 8-12 bits |
| Resistor value | 50 kΩ | 100 kΩ (R), 200 kΩ (2R) |
| Matching | < 0.5 LSB (with trim) | < 1 LSB |
| Output impedance | Variable | 100 kΩ |
| Buffer required | Yes | Optional |
| Total power | 68 µW | 15-78 µW |
| Active area | 0.05 mm² | 0.02 mm² |
| Settling time | < 1 µs | < 500 ns |
| Technology | 180 nm CMOS | 180 nm CMOS |
