# Analog Layout Techniques for Implantable ICs

## Overview

Analog layout is the physical implementation of analog circuit designs in silicon, where the arrangement, sizing, and routing of transistors, resistors, capacitors, and interconnects directly determine circuit performance. For the iPACE-CHIP implantable pacemaker, analog layout must achieve excellent matching, minimize parasitic effects, provide robust noise isolation, and meet strict reliability requirements. This chapter covers the essential analog layout techniques used in the iPACE-CHIP design.

## Layout Principles

### Matching Techniques

```
Matching hierarchy (best to worst):

1. Common-centroid: Best matching
   - Elements arranged symmetrically around a center point
   - Cancels linear gradient errors
   - Used for: differential pairs, current mirrors
   
   Example (4-element common-centroid):
   
   +----+----+----+----+
   | 1  | 3  | 2  | 4  |  <- Element placement
   +----+----+----+----+
   
   Order: 1,3,2,4 (not 1,2,3,4)
   Gradient: +1,+2,+3,+4 cancels in pairs

2. Interdigitated: Good matching
   - Alternating fingers of two elements
   - Reduces systematic errors
   
   Example (interdigitated pair):
   
   M1: |===|   |===|   |===|
   M2:    |===|   |===|   |===|
   
   Common in current mirrors and differential pairs

3. Dummy devices: Baseline matching
   - Dummy elements at array edges
   - Absorbs edge effects
   - Must be same size as active elements

4. Orientation: All elements same orientation
   - Prevents systematic offset from crystal effects
   - Minimum 90-degree rotation increment
```

### Common-Centroid Layout

```
Common-centroid for differential pair:

  M1 and M2 (differential pair):
  
  Simple:           Common-centroid:
  +------+          +------+------+
  |  M1  |          |  M1  |  M2  |
  +------+          +------+------+
  |  M2  |          |  M2  |  M1  |
  +------+          +------+------+
  
  Matching improvement: 2-5x (reduces gradient error)

Common-centroid for current mirror array:

  M1 and M2 (1:1 current mirror, 4 elements each):
  
  +----+----+----+----+
  | M1 | M2 | M1 | M2 |  <- Interleaved
  +----+----+----+----+
  | M2 | M1 | M2 | M1 |
  +----+----+----+----+
  
  Both M1 and M2 see average gradient
```

### Interdigitated Layout

```
Interdigitated differential pair:

  Finger arrangement (2 fingers per device):
  
  M1: |=====|   |=====|
          |         |
  M2:    |=====|   |=====|
  
  Wiring:
  
  M1_drain --+--+  M2_drain --+--+
             |  |             |  |
            [M1a][M1b]       [M2a][M2b]
             |  |             |  |
  M1_source--+--+  M2_source--+--+

  Benefits:
  - Reduces offset from process gradients
  - Equal parasitic capacitance on both sides
  - Used in all matched pairs in iPACE-CHIP
```

## Transistor Layout

### MOSFET Layout Rules

```
MOSFET layout considerations:

1. Gate orientation:
   - All transistors in same direction
   - Prefer horizontal gates (for process uniformity)
   - Minimum rotation: 90 degrees (if needed)
   
2. Finger width:
   - W_finger < 20 um (for good matching)
   - If W_total > 20 um, use multi-finger
   
   Example: W/L = 100/1
   Use 10 fingers x 10 um/1 um each
   
3. Gate poly extension:
   - Overhang: 0.2 um minimum
   - Prevents source/drain at gate edge
   
4. Source/drain contacts:
   - Minimum 2 contacts per S/D region
   - Contact-to-gate spacing: 0.1 um minimum
   - Stacked contacts for low resistance
```

### Cascode Transistor Layout

```
Cascode pair layout (M1 + M2):

  M1 (input)          M2 (cascode)
  +----------+        +----------+
  |          |        |          |
  |   Gate   |        |   Gate   |
  |   =====  |        |   =====  |
  |          |        |          |
  |  Drain   +--------+  Source  |
  |          | shared |          |
  +----------+ metal  +----------+
  
  Shared drain/source reduces parasitic capacitance
  
  Parasitic reduction:
  - Without sharing: C_drain1 + C_source2 = 2 x C_par
  - With sharing: C_drain1_source2 = C_par (50% reduction)
  
  Benefits:
  - Reduced parasitic capacitance at intermediate node
  - Improved high-frequency performance
  - Smaller area
```

## Capacitor Layout

### MIM Capacitor Layout

```
Metal-Insulator-Metal (MIM) capacitor:

  Top plate (M5)
  +=========================+
  |                         |
  |    Dielectric (SiN)     |
  |                         |
  +=========================+
  Bottom plate (M4)
  
  Layout rules:
  - Minimum size: 5 um x 5 um
  - Aspect ratio: 1:1 to 2:1 (avoid long, thin caps)
  - Guard ring: P+ around capacitor
  - Spacing to other caps: > 2 um (reduce coupling)
  
  Matching:
  σ(C1/C2) = A_C / sqrt(W x L)
  A_C = 0.05-0.2 %·um (for MIM)
  
  For W x L = 10 x 10 um:
  σ = 0.1 / sqrt(100) = 0.01% = 0.04 LSB (8-bit) ✓
```

### Capacitor Matching

```
Capacitor matching layout techniques:

1. Same orientation:
   All MIM caps oriented the same way
   Prevents systematic gradient errors
   
2. Dummy capacitors:
   Place dummy caps at array edges
   Same size as active caps
   Absorbs edge effects
   
   Array: [C][C][C][C][C][D]  <- D is dummy
           [C][C][C][C][C][D]
   
3. Common-centroid for capacitor DAC:
   
   12-bit SAR ADC capacitor array:
   
   +--+--+--+--+--+--+--+--+
   |C1|C2|C3|C4|C5|C6|C7|C8|  <- Top plate
   +--+--+--+--+--+--+--+--+
   |C8|C7|C6|C5|C4|C3|C2|C1|  <- Bottom plate
   +--+--+--+--+--+--+--+--+
   
   Symmetric arrangement cancels linear gradients

4. Matching target:
   For 12-bit ADC: σ < 0.1% per capacitor
   Using MIM: A_C = 0.1 %·um, W x L = 25 um^2
   σ = 0.1 / sqrt(25) = 0.02% ✓ (2x margin)
```

## Resistor Layout

### Poly Resistor Layout

```
Polysilicon resistor:

  +----------------------------------+
  | Poly resistor body               |
  | (R_sheet = 100-800 ohm/sq)      |
  +----------------------------------+
  
  Layout rules:
  - Width: > 1 um (for matching)
  - Length: > 10 x width (for edge effects)
  - Contacts at both ends
  - Dummy resistors at array edges
  
  Matching:
  σ(R1/R2) = A_R / sqrt(W x L)
  A_R = 0.05-0.2 %·um (for poly)
  
  For W x L = 2 x 20 um:
  σ = 0.1 / sqrt(40) = 0.016% ✓
```

### Resistor Matching

```
Resistor matching layout:

1. Same width and length:
   All resistors in a matched array must have identical W/L
   Differences cause systematic mismatch
   
2. Orientation:
   All resistors same orientation
   Prefer horizontal for process uniformity
   
3. Common-centroid for DAC resistors:
   
   R-2R DAC (for reference):
   
   +----+----+----+----+----+
   | R  | 2R | R  | 2R | R  |
   +----+----+----+----+----+
   | 2R | R  | 2R | R  | 2R |
   +----+----+----+----+----+
   
   R and 2R elements interleaved

4. Temperature coefficient:
   Same type of resistor for all matched elements
   TC matching: < 10 ppm/°C difference
   
   Poly TC: 100-500 ppm/°C (process dependent)
   For matched elements: TC difference < 10 ppm/°C ✓
```

## Guard Rings

### Guard Ring Types

```
Guard ring types:

1. P+ guard ring (substrate):
   - Connected to analog ground
   - Collects minority carriers in substrate
   - Width: 2-5 um
   - Contacts: every 10 um
   
   +--P+--P+--P+--P+--P+--+
   |                       |
   |    Analog circuit     |
   |                       |
   +--P+--P+--P+--P+--P+--+
           |
          GND

2. N+ guard ring (in P-substrate):
   - Connected to VDD
   - Provides isolation from substrate noise
   - Width: 2-5 um
   
   +--N+--N+--N+--N+--N+--+
   |                       |
   |    Digital circuit     |
   |                       |
   +--N+--N+--N+--N+--N+--+
           |
          VDD

3. Combined guard ring:
   P+ ring (ground) + N+ ring (VDD) = best isolation
   
   +--P+--P+--P+--P+--P+--+
   +--N+--N+--N+--N+--N+--+
   |                       |
   |    Sensitive analog   |
   |    circuit            |
   |                       |
   +--N+--N+--N+--N+--N+--+
   +--P+--P+--P+--P+--P+--+
```

### Guard Ring Sizing

```
Guard ring sizing guidelines:

Width:
  - Minimum: 2 um (for process rules)
  - Recommended: 5 um (for isolation)
  - Maximum: 10 um (diminishing returns)
  
Contact density:
  - Minimum: 1 contact per 20 um length
  - Recommended: 1 contact per 10 um length
  - Via arrays for connections to upper metals
  
Placement:
  - Distance from circuit: 5-10 um
  - Must be continuous (no gaps)
  - Must contact substrate frequently
  
Effectiveness:
  2 um wide guard ring: 20-30 dB isolation
  5 um wide guard ring: 30-40 dB isolation
  10 um wide guard ring: 35-45 dB isolation
```

## Routing

### Analog Routing Rules

```
Analog routing guidelines:

1. Metal selection:
   - M1, M2: Sensitive analog signals
   - M3, M4: Digital signals (avoid over analog)
   - M5: Power routing (VDD, GND)
   
2. Trace width:
   - Minimum: 0.5 um (for weak signals)
   - Recommended: 1-2 um (for matched traces)
   - Power: 5-10 um (for low resistance)
   
3. Spacing:
   - Signal to signal: > 1 um
   - Signal to power: > 2 um
   - Sensitive to digital: > 5 um
   
4. Shielding:
   - Sensitive traces flanked by ground lines
   
   GND --- Signal --- GND
   
   Reduces coupling by 10-20 dB
   
5. Symmetry:
   - Differential pairs: matched length and width
   - Reference traces: matched to signal traces
   - No crossovers on matched paths
```

### Power Routing

```
Power routing strategy:

  VDD (analog)                GND (analog)
    |                            |
    +----[wide]----+----[wide]---+
                   |              |
            +------+------+      |
            |             |      |
            v             v      v
         [block]      [block]  [block]
         
  Rules:
  - Use top metal for power (low resistance)
  - Width > 5 um for analog power
  - Via arrays at connections
  - Decoupling caps near power pins
  
  IR drop target: < 1% of VDD
  For VDD = 1.8V: IR < 18 mV
  
  For I = 100 uA, R = 100 ohm:
  IR = 10 mV ✓
```

## Floor Planning

### iPACE-CHIP Floor Plan

```
Complete floor plan:

+--------------------------------------------------+
|                                                  |
|  +-----------+  +-----------+  +-----------+     |
|  | Digital   |  | Telemetry |  | Clock Gen |     |
|  | Controller|  | Interface |  | & PLL     |     |
|  +-----------+  +-----------+  +-----------+     |
|                                                  |
|  +-----------------------------------------+    |
|  |          Guard Ring (5 um)              |    |
|  |  +---------+  +---------+  +---------+ |    |
|  |  |   LNA   |  |   PGA   |  |   AAF   | |    |
|  |  +---------+  +---------+  +---------+ |    |
|  |                                         |    |
|  |  +---------+  +---------+  +---------+ |    |
|  |  |   ADC   |  |   DAC   |  |  Bias   | |    |
|  |  +---------+  +---------+  +---------+ |    |
|  |                                         |    |
|  +-----------------------------------------+    |
|                                                  |
|  +-----------------------------------------+    |
|  |          Guard Ring (5 um)              |    |
|  |  +-----------------------------------+  |    |
|  |  |     Pacing Output Stage           |  |    |
|  |  |     (high-current path)           |  |    |
|  |  +-----------------------------------+  |    |
|  |                                         |    |
|  |  +---------+  +---------+              |    |
|  |  | Charge  |  | Safety  |              |    |
|  |  | Pump    |  | Limiter |              |    |
|  |  +---------+  +---------+              |    |
|  +-----------------------------------------+    |
|                                                  |
|  +--+  +--+  +--+  +--+  +--+  +--+  +--+     |
|  |IO|  |IO|  |IO|  |IO|  |IO|  |IO|  |IO|     |
|  +--+  +--+  +--+  +--+  +--+  +--+  +--+     |
+--------------------------------------------------+

Area allocation:
  Digital: 0.3 mm^2 (20%)
  Analog front-end: 0.5 mm^2 (33%)
  Pacing output: 0.4 mm^2 (27%)
  I/O pads: 0.2 mm^2 (13%)
  Guard rings: 0.1 mm^2 (7%)
  Total: 1.5 mm^2
```

### Floor Plan Rules

```
Floor plan guidelines:

1. Block placement:
   - Analog blocks grouped together
   - Digital blocks separated from analog
   - High-current blocks near I/O pads
   - Sensitive blocks away from digital
   
2. Guard ring placement:
   - Continuous around analog block
   - Continuous around pacing output
   - Between analog and digital domains
   
3. Power distribution:
   - Separate VDD/GND for analog and digital
   - Wide metal for high-current paths
   - Decoupling caps distributed evenly
   
4. Signal routing:
   - Analog signals route inside guard ring
   - Digital signals route outside guard ring
   - No crossing of analog/digital boundary
```

## Reliability

### Electromigration

```
Electromigration rules:

  Current density limit:
  J_max = 1e5 A/cm^2 (for aluminum)
  J_max = 3e6 A/cm^2 (for copper)
  
  For M1 (aluminum, 0.5 um thick):
  Width for 1 mA: W = I / (J x t) = 1e-3 / (1e5 x 0.5e-6) = 20 um
  
  For iPACE-CHIP (180nm, aluminum):
  - Signal traces: 1-2 um (low current) ✓
  - Power traces: 5-10 um (moderate current) ✓
  - Output stage: 50 um (high current, 20 mA) ✓
```

### Hot Carrier Injection

```
Hot carrier reliability:

  For 180nm transistors:
  - Maximum VDS: 1.8V (rated)
  - Hot carrier degradation: < 10% over 10 years
  
  Design rules:
  - No transistor operates at maximum VDS continuously
  - Cascode transistors share voltage stress
  - Output stage: voltage clamped by protection circuits
  
  Lifetime estimation:
  t_lifetime = A x exp(B / VDS)
  For VDS = 1.5V: t > 100 years ✓
```

### TDDB (Time-Dependent Dielectric Breakdown)

```
Gate oxide reliability:

  For 180nm, tox = 4 nm:
  - Rated voltage: 1.8V
  - Maximum operating voltage: 2.0V (with margin)
  
  TDDB lifetime:
  t_BD = C x exp(-gamma x E_ox)
  
  For E_ox = 4.5 MV/cm (1.8V / 4 nm):
  t_BD > 100 years ✓
  
  Design rules:
  - No voltage exceeds 2.0V on gate oxide
  - ESD protection on all pads
  - Power sequencing to prevent over-voltage
```

## Summary

| Technique | Purpose | Application in iPACE-CHIP |
|-----------|---------|---------------------------|
| Common-centroid | Gradient cancellation | Diff pairs, current mirrors |
| Interdigitated | Systematic error reduction | Current mirrors, diff pairs |
| Dummy devices | Edge effect absorption | Capacitor arrays, resistor arrays |
| Guard rings | Noise isolation | Analog block, pacing output |
| Symmetry | Matching improvement | All matched components |
| Shielding | Coupling reduction | Sensitive signal routes |
| Kelvin connection | Accurate sensing | Current sense resistor |

These analog layout techniques are essential for achieving the performance specifications of the iPACE-CHIP analog front-end, ensuring reliable cardiac sensing and safe pacing therapy delivery over the 10-year implant lifetime.
