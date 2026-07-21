# CMOS Logic Families

## 1. Introduction to Logic Families

Logic families are groups of digital circuits that share similar voltage levels, power characteristics, and performance properties. Understanding different logic families is essential for selecting the right technology for specific applications.

### 1.1 Classification of Logic Families

```
Logic Family Classification:
├── Bipolar Logic
│   ├── TTL (Transistor-Transistor Logic)
│   ├── ECL (Emitter-Coupled Logic)
│   └── IIL (Integrated Injection Logic)
└── MOS Logic
    ├── PMOS Logic (obsolete)
    ├── NMOS Logic (mostly obsolete)
    ├── CMOS Logic (dominant)
    │   ├── Standard CMOS
    │   ├── High-Speed CMOS (HCMOS)
    │   ├── Low-Power CMOS (LVCMOS)
    │   └── Advanced CMOS
    └── BiCMOS Logic
```

### 1.2 Comparison Overview

| Family | Speed | Power | Noise Margin | Fanout | Voltage |
|--------|-------|-------|--------------|--------|---------|
| TTL | Medium | Medium | Good | 10 | 5V |
| ECL | Very High | Very High | Poor | 25 | -5.2V |
| CMOS | Medium | Very Low | Excellent | ∞ | 1.2-5V |
| LVCMOS | High | Low | Good | ∞ | 1.2-3.3V |
| BiCMOS | High | Medium | Good | 20 | 3.3-5V |

## 2. Standard CMOS Logic

### 2.1 Basic CMOS Gates

```
Standard CMOS Characteristics:
- Supply voltage: 5V (original), 3.3V, 2.5V, 1.8V
- Logic levels: Rail-to-rail (0V to V_DD)
- Static power: Near zero (only leakage)
- Dynamic power: αCV²f
- Fanout: Theoretically infinite (capacitive loading only)

CMOS Inverter:
PMOS: W/L = 3:1 (typical)
NMOS: W/L = 1:1 (reference)
Rise/Fall symmetry: W_p/W_n = μ_n/μ_p ≈ 2.5-3

Advantages:
- Ultra-low static power
- High noise margins
- Wide operating voltage
- Simple design rules
- Scalable to deep sub-micron
```

### 2.2 CMOS Logic Levels

```
Logic Level Definitions (3.3V LVCMOS):

Parameter     | Symbol | Min  | Typical | Max  | Units
--------------|--------|------|---------|------|-------
V_DD          | V_DD   | 3.0  | 3.3     | 3.6  | V
V_OH (I_OH=0)| V_OH   | 2.4  | 3.3     | -    | V
V_OL (I_OL=0)| V_OL   | -    | 0       | 0.4  | V
V_IH          | V_IH   | 2.0  | 2.2     | -    | V
V_IL          | V_IL   | -    | 0.8     | 1.0  | V
I_OH (max)    | I_OH   | -    | -       | -4   | mA
I_OL (max)    | I_OL   | -    | -       | 4    | mA
t_pd          | t_pd   | -    | 3       | 10   | ns
C_load        | C_L    | -    | 10      | 50   | pF
```

### 2.3 Power Consumption

```
Static Power:
P_static = V_DD × I_leak

For 3.3V CMOS:
I_leak ≈ 1-10 nA per gate (typical)
P_static ≈ 3-30 nW per gate

Dynamic Power:
P_dynamic = α × C_L × V_DD² × f

Example (3.3V, 100 MHz):
C_L = 10 pF
α = 0.15
P_dynamic = 0.15 × 10e-12 × 3.3² × 100e6
          = 0.15 × 10e-12 × 10.89 × 100e6
          = 16.3 mW per gate (with load!)

Power Comparison:
Logic Family | P_static | P_dynamic @ 100MHz
-------------|----------|-------------------
TTL          | 10 mW    | 15 mW
ECL          | 25 mW    | 30 mW
CMOS         | 10 nW    | 16 mW
```

## 3. High-Speed CMOS (HCMOS)

### 3.1 74HCT Series

```
74HCT Series Characteristics:
- Drop-in replacement for TTL
- TTL-compatible input levels
- CMOS output levels
- Supply voltage: 4.5-5.5V

TTL Compatibility:
V_IH (HCT) = 2.0V (same as TTL V_OH min)
V_IL (HCT) = 0.8V (same as TTL V_OL max)

This allows direct interface between TTL and HCT

Speed-Power Product:
SPP = t_pd × P_dissipated

74HCT00 (NAND):
t_pd ≈ 10 ns
P ≈ 2.5 mW (at 50% duty cycle)
SPP ≈ 25 pJ

Comparison:
Series   | t_pd (ns) | P (mW) | SPP (pJ)
---------|-----------|--------|---------
74HC     | 10        | 2.5    | 25
74HCT    | 10        | 2.5    | 25
74ALS    | 4         | 10     | 40
74AS     | 1.5       | 20     | 30
```

### 3.2 74HC Series

```
74HC Series Characteristics:
- Pure CMOS input levels
- Rail-to-rail output
- Supply voltage: 2-6V (wide range)
- Low power consumption

Operating Voltage Range:
V_DD = 2V to 6V

Delay vs Voltage:
V_DD (V) | t_pd (ns)
---------|----------
  2.0    | 50
  3.0    | 20
  4.5    | 10
  6.0    | 7

Power vs Voltage:
V_DD (V) | P_dynamic (mW)
---------|----------------
  2.0    | 0.5
  3.0    | 1.5
  4.5    | 2.5
  6.0    | 4.0

Application:
- Battery-operated devices
- Low-power portable electronics
- Wide supply voltage tolerance
```

## 4. Low-Voltage CMOS (LVCMOS)

### 4.1 LVCMOS Standards

```
LVCMOS Families:
┌──────────────┬───────────┬─────────┬──────────┐
│ Standard     │ V_DD (V)  │ V_OH    │ V_OL     │
├──────────────┼───────────┼─────────┼──────────┤
│ LVCMOS 5V    │ 5.0       │ 3.8     │ 0.4      │
│ LVCMOS 3.3V  │ 3.3       │ 2.4     │ 0.4      │
│ LVCMOS 2.5V  │ 2.5       │ 1.9     │ 0.4      │
│ LVCMOS 1.8V  │ 1.8       │ 1.35    │ 0.35     │
│ LVCMOS 1.5V  │ 1.5       │ 1.1     │ 0.3      │
│ LVCMOS 1.2V  │ 1.2       │ 0.9     │ 0.25     │
│ LVCMOS 1.0V  │ 1.0       │ 0.75    │ 0.2      │
└──────────────┴───────────┴─────────┴──────────┘

Speed vs Voltage Trade-off:
Lower voltage → Lower power but slower
V_DD reduction by 2× → Power reduction by 4×
V_DD reduction by 2× → Delay increase by 2-3×
```

### 4.2 Sub-1V CMOS

```
Sub-Threshold CMOS Operation:
- Operate below V_TH
- Ultra-low power (μW range)
- Very slow (MHz range)

Near-Threshold CMOS:
- V_DD ≈ V_TH + 100-200 mV
- Optimal energy efficiency
- 5-10× slower than super-threshold

Example (65nm technology):
Super-threshold: V_DD = 1.0V, P = 100 mW, f = 2 GHz
Near-threshold:  V_DD = 0.5V, P = 5 mW, f = 200 MHz
Sub-threshold:   V_DD = 0.3V, P = 50 μW, f = 1 MHz

Energy Efficiency (Energy/Operation):
Super-threshold: 50 pJ
Near-threshold:  25 pJ (optimal!)
Sub-threshold:   50 pJ (worse due to leakage)
```

### 4.3 Multi-Voltage Design

```
Multi-Voltage Domain Design:

┌─────────────────┐     ┌─────────────────┐
│  1.0V Domain    │     │  0.6V Domain    │
│  (High Speed)   │────│  (Low Power)    │
│                 │Level│                 │
│  Critical Path  │Shift│  Non-Critical   │
└─────────────────┘     └─────────────────┘

Level Shifter:
- Translates signals between voltage domains
- Prevents excessive current flow
- Adds 1-2 gate delays

Power Management:
- Dynamic Voltage and Frequency Scaling (DVFS)
- Multiple V_DD islands
- Adaptive body biasing

Benefits:
- 30-50% power reduction
- Maintains performance where needed
- Complex design flow
```

## 5. Emitter-Coupled Logic (ECL)

### 5.1 ECL Basics

```
ECL (Emitter-Coupled Logic):
- Current-mode logic (CML)
- Non-saturating transistors
- Very high speed
- High power consumption

ECL Inverter Structure:
       V_EE (-5.2V)
          │
       ┌──┴──┐
       │  Re  │ (Emitter resistor)
       └──┬──┘
          │
       ┌──┴──┐
       │ Q1  │ ← Input A
       └──┬──┘
          │
       ┌──┴──┐
       │ Q2  │ ← Reference (V_BB)
       └──┬──┘
          │
     ┌────┴────┐
     │         │
  ┌──┴──┐   ┌──┴──┐
  │ Rc1 │   │ Rc2 │
  └──┬──┘   └──┬──┘
     │         │
   V_CC       V_CC
    (0V)       (0V)

Operating Principle:
- Differential pair
- Current steers between Q1 and Q2
- Non-saturating operation (fast switching)
```

### 5.2 ECL Characteristics

```
ECL Parameters:
- Supply voltage: V_CC = 0V, V_EE = -5.2V
- Logic levels: V_OH = -0.9V, V_OL = -1.7V
- Swing: 0.8V (small → fast)
- Propagation delay: 0.3-1 ns
- Power per gate: 2-5 mW
- Fanout: 25+

ECL Logic Levels:
      0V
       │
-0.9V ──── V_OH (Logic 1)
       │
       │ 0.8V swing
       │
-1.7V ──── V_OL (Logic 0)
       │
-5.2V ──── V_EE

Advantages:
- Fastest logic family (sub-nanosecond)
- Low noise (constant current draw)
- Good for high-frequency applications

Disadvantages:
- High power consumption
- Negative supply voltage
- Requires termination resistors
- Complex PCB layout
```

### 5.3 ECL vs CMOS Comparison

```
Performance Comparison:
Parameter     | ECL          | CMOS (0.18μm)
-------------|--------------|----------------
t_pd         | 0.3-1 ns     | 10-50 ns
Power/gate   | 2-5 mW       | 1-10 μW (dynamic)
V_DD         | -5.2V/0V     | 1.8V
Noise Margin | 0.2V         | 0.4V
Fanout       | 25           | ∞ (capacitive)
Integration  | Low (<10K)   | High (>1M)

When to Use ECL:
- Ultra-high-speed applications (>10 GHz)
- Clock generation
- High-speed serial links
- When CMOS is too slow

When to Use CMOS:
- High integration density
- Low power required
- Cost-sensitive applications
- Most digital logic
```

## 6. BiCMOS Logic

### 6.1 BiCMOS Concept

```
BiCMOS combines Bipolar and CMOS:
- Bipolar transistors for high-speed driving
- CMOS transistors for logic functions
- Best of both worlds

BiCMOS Inverter:
      V_DD
       │
    ┌──┴──┐
    │ PMOS │ ← Gate = A
    └──┬──┘
       │
    ┌──┴──┐
    │ BJT  │ ← Collector to output
    │ (NPN)│
    └──┬──┘
       │
       ├──── Output Y
       │
    ┌──┴──┐
    │ NMOS │ ← Gate = A
    └──┬──┘
       │
      GND

Operation:
- PMOS/NMOS provide logic function
- BJT provides high-current drive
- Fast charging/discharging of load capacitance
```

### 6.2 BiCMOS Characteristics

```
BiCMOS Parameters:
- Supply voltage: 3.3-5V
- Propagation delay: 0.5-2 ns
- Power per gate: 0.1-1 mW
- Fanout: 20+
- Drive strength: High (good for buses)

BiCMOS vs CMOS:
Parameter     | BiCMOS      | CMOS
-------------|-------------|--------
t_pd         | 0.5-2 ns    | 5-20 ns
Drive        | High        | Medium
Power        | Medium      | Low
Area         | Medium      | Small
Cost         | Higher      | Lower

Applications:
- High-speed bus drivers
- Memory output drivers
- Clock distribution
- I/O interfaces
```

### 6.3 BiCMOS Logic Gates

```
BiCMOS NAND Gate:
V_DD
 │
┌┴┐
│P1│ ← A
└┬┘
 │
┌┴┐
│P2│ ← B
└┬┘
 │
 ├──── Output
 │
┌┴┐
│N1│ ← A
└┬┘
 │
┌┴┐
│N2│ ← B
└┬┘
 │
GND

With BJT buffers on output for high drive strength

Performance:
- Similar speed to ECL
- Power closer to CMOS
- Higher drive capability than pure CMOS
```

## 7. Differential Logic Families

### 7.1 Current-Mode Logic (CML)

```
CML (Current-Mode Logic):
- Similar to ECL but with integrated termination
- Differential signaling
- Low voltage swing (200-600 mV)

CML Structure:
     V_DD
      │
   ┌──┴──┐
   │ RL1 │  RL2 │
   └──┬──┘  └──┬┘
      │        │
   ┌──┴────────┴──┐
   │               │
┌──┴──┐         ┌──┴──┐
│ Q1  │         │ Q2  │ ← Differential pair
└──┬──┘         └──┬──┘
   │               │
   └───────┬───────┘
           │
        ┌──┴──┐
        │ Ie  │ (Tail current)
        └──┬──┘
           │
          V_SS

Operation:
- Constant tail current steers between Q1 and Q2
- Small voltage swing at outputs
- Very high speed (30+ GHz)
```

### 7.2 Low-Voltage Differential Signaling (LVDS)

```
LVDS Characteristics:
- Differential signaling standard
- Low voltage swing (350 mV typical)
- High speed (1-3 Gbps)
- Low power

LVDS Parameters:
- V_OD (output differential): 250-450 mV
- V_CM (common mode): 1.125-1.375V
- I_OD (output current): 3.5 mA
- R_load: 100 Ω (differential termination)
- t_rise/t_fall: 0.3-0.5 ns

Applications:
- High-speed data links
- Clock distribution
- FPGA-to-FPGA communication
- Display interfaces (DVI, HDMI)
```

### 7.3 Comparison

| Logic Type | Swing | Speed | Power | Noise Immunity |
|------------|-------|-------|-------|----------------|
| Single-ended CMOS | V_DD | Medium | Low | Good |
| ECL/CML | 0.8V | Very High | High | Poor |
| LVDS | 0.35V | High | Low | Good (differential) |
| CML | 0.2-0.6V | Very High | High | Good (differential) |

## 8. Pass-Transistor Logic

### 8.1 Basic Pass-Transistor

```
NMOS Pass-Transistor:
- Passes strong '0', weak '1'
- V_out = V_in - V_TH (when passing '1')

Structure:
     V_in
      │
    ┌─┴─┐
    │NMOS│ ← Control = 1
    └─┬─┘
      │
     V_out

V_out when passing '1':
V_out = V_DD - V_THN
     = 1.2V - 0.4V = 0.8V (degraded!)

Solution: Use transmission gates (complementary pass transistors)
```

### 8.2 Transmission Gate Logic

```
Transmission Gate (TG):
- Parallel NMOS + PMOS
- Passes both '0' and '1' well
- Full voltage swing

Structure:
     V_in
      │
   ┌──┴──┐
   │ NMOS │ ← Gate = Control
   │      │
   │ PMOS │ ← Gate = Control'
   └──┬──┘
      │
     V_out

TG Characteristics:
- ON resistance: R_NMOS || R_PMSO ≈ R/2
- Better than single transistor
- Used in MUX, latches, flip-flops
```

### 8.3 CPL (Complementary Pass-Transistor Logic)

```
CPL Structure:
- Differential pass-transistor network
- Cross-coupled latch for level restoration
- High speed, low power

CPL NAND Gate:
Inputs: A, B
Outputs: Y, Y'

Pass network implements:
Y = A'B' + A'B + AB' + AB (with appropriate connections)

Cross-coupled inverter restores levels

Advantages:
- Fewer transistors than static CMOS
- Lower capacitance
- Higher speed

Disadvantages:
- More complex design
- Level restoration needed
- Not truly ratio-free
```

### 8.4 Transmission Gate Logic Examples

```
TG-based 2:1 MUX:
A ──[TG1]──┐
            ├─── Y
B ──[TG2]──┘

TG1 controlled by S'
TG2 controlled by S

Y = S'A + SB

Total: 4 transistors (2 TGs)

TG-based D Latch:
D ──[TG]──┐
           ├─── Q
CLK ──[TG]┘
       │
      CLK'

When CLK=1: TG transparent, Q = D
When CLK=0: TG hold, Q maintains value
```

## 9. Dynamic Logic Families

### 9.1 Domino Logic

```
Domino Logic Structure:
- Precharge phase
- Evaluate phase
- Monotonic evaluation (0→1 only)

Domino AND Gate:
     V_DD
      │
   ┌──┴──┐
   │ PMOS│ ← CLK (precharge)
   └──┬──┘
      │
      ├──── Node X (dynamic node)
      │
   ┌──┴──┐
   │ NMOS│ ← A
   └──┬──┘
      │
   ┌──┴──┐
   │ NMOS│ ← B
   └──┬──┘
      │
   ┌──┴──┐
   │ NMOS│ ← CLK (evaluate)
   └──┬──┘
      │
     GND
      │
   ┌──┴──┐
   │ INV │ ← (static inverter for domino)
   └──┬──┘
      │
     Y (output)

Operation:
CLK=0: Node X precharged to V_DD, Y=0
CLK=1: If A=1 AND B=1, X discharged to 0, Y=1
```

### 9.2 NP-CMOS (Zipper Logic)

```
NP-CMOS Structure:
- Alternating NMOS and PMOS blocks
- Complementary clocks
- Full voltage swing

Structure:
     V_DD
      │
   ┌──┴──┐
   │ PMOS│ ← CLK'
   └──┬──┘
      │
   ┌──┴──┐
   │ PMOS│ ← B'
   └──┬──┘
      │
   ┌──┴──┐
   │ PMOS│ ← A'
   └──┬──┘
      │
      ├──── Node X
      │
   ┌──┴──┐
   │ NMOS│ ← A
   └──┬──┘
      │
   ┌──┴──┐
   │ NMOS│ ← B
   └──┬──┘
      │
   ┌──┴──┐
   │ NMOS│ ← CLK
   └──┬──┘
      │
     GND

Advantages:
- No static inverter needed
- Full swing output
- Faster than domino
```

### 9.3 Dynamic vs Static Logic

| Property | Static CMOS | Domino | NP-CMOS |
|----------|-------------|--------|---------|
| Transistor Count | 2N | N+2 | 2N |
| Speed | Medium | Fast | Very Fast |
| Power | Low | Low | Low |
| Noise Immunity | Good | Poor | Medium |
| Design Complexity | Simple | Complex | Complex |
| Monotonicity | Not required | Required | Required |
| Cascading | Easy | Must add inverter | Not needed |

## 10. Logic Family Selection

### 10.1 Selection Criteria

```
Key Factors for Logic Family Selection:

1. Speed Requirements:
   - f_max < 100 MHz: Standard CMOS
   - f_max = 100-500 MHz: LVCMOS or BiCMOS
   - f_max > 500 MHz: ECL/CML or advanced CMOS

2. Power Budget:
   - Battery-powered: Sub-threshold or near-threshold CMOS
   - Limited power: Standard CMOS
   - Power not critical: ECL or BiCMOS

3. Integration Density:
   - High density (>1M gates): CMOS
   - Medium density (10K-1M): CMOS or BiCMOS
   - Low density (<10K): Any family

4. Voltage Compatibility:
   - Legacy 5V: HCT or LVCMOS 5V
   - 3.3V systems: LVCMOS 3.3V
   - 1.2-1.8V: LVCMOS 1.2-1.8V
   - Mixed voltage: Level shifters needed

5. Environmental:
   - High temperature: SOI CMOS
   - Radiation: Rad-hard CMOS
   - High reliability: Triple redundancy
```

### 10.2 Decision Matrix

```
Application Requirements → Logic Family Choice:

Requirement              | Best Choice
-------------------------|-------------------
High speed (>1 GHz)      | ECL/CML or FinFET CMOS
Ultra-low power          | Sub-threshold CMOS
High integration         | CMOS
TTL compatibility        | HCT or LVCMOS 5V
High drive capability    | BiCMOS or buffer
Low voltage (≤1V)        | Advanced CMOS
Radiation hardened       | Rad-hard CMOS
High temperature         | SOI CMOS
Cost-sensitive           | Standard CMOS
```

### 10.3 Technology Roadmap

```
Logic Family Evolution:

1970s: PMOS → NMOS → CMOS introduction
1980s: CMOS dominates, TTL declines
1990s: CMOS scales (0.5μm → 0.18μm)
2000s: Low-voltage CMOS (1.8V → 1.2V)
2010s: FinFET CMOS (28nm → 7nm)
2020s: Gate-all-around (3nm → 2nm)

Future Trends:
- Continued voltage scaling (<0.5V)
- 3D integration (CFET)
- New materials (2D materials, carbon nanotubes)
- Cryogenic CMOS (for quantum computing)
- Approximate computing
```

## 11. Applications in Medical Implant Design

### 11.1 Logic Family Selection for Implants

```
Medical Implant Requirements:
- Ultra-low power (μW budget)
- High reliability (10+ year lifetime)
- Small size (mm²)
- Radiation tolerance (for some implants)
- Temperature stability (37°C ± 4°C)

Recommended Logic Families:

1. Primary Choice: Standard CMOS
   - Lowest static power
   - Proven reliability
   - Mature technology
   - Wide voltage range

2. For High-Speed Blocks: LVCMOS
   - Higher speed when needed
   - Still low power
   - Compatible with CMOS

3. For Ultra-Low Power: Near-Threshold CMOS
   - Operate near V_TH
   - 5-10× power reduction
   - Acceptable speed for implant functions

4. For Radiation Tolerance: Rad-Hard CMOS
   - SOI technology
   - Guard rings
   - TMR for critical logic
```

### 11.2 Power Optimization Strategy

```
Implant Power Budget Example:
Total power budget: 100 μW

Allocation:
- Sensors: 20 μW
- Analog front-end: 25 μW
- Digital processing: 30 μW
- Communication: 20 μW
- Control logic: 5 μW

Digital Logic Design:
- Use standard CMOS for all logic
- Near-threshold for non-critical paths
- Clock gating for idle blocks
- Power gating for sleep modes

Voltage Strategy:
- Core logic: 0.5V (near-threshold)
- I/O: 1.2V (for external interface)
- Analog: 1.8V (for precision)

Power Estimation:
- 10K gates, 0.5V, 10 MHz
- P_dynamic = 0.15 × 10e-12 × 0.5² × 10e6 = 3.75 μW
- P_static = 0.5V × 10nA × 10K = 50 μW (too high!)
- Solution: Power gating reduces to 5 μW

Total digital power: 3.75 + 5 = 8.75 μW ✓
```

## 12. Summary

| Logic Family | Speed | Power | Voltage | Application |
|--------------|-------|-------|---------|-------------|
| Standard CMOS | Medium | Very Low | 1-5V | General purpose |
| HCT | Medium | Low | 5V | TTL replacement |
| LVCMOS | High | Low | 1-3.3V | Modern digital |
| ECL/CML | Very High | High | -5.2V | High-speed |
| BiCMOS | High | Medium | 3.3-5V | Bus driving |
| Sub-threshold | Very Low | Ultra Low | 0.3-0.5V | Implants |
| Near-threshold | Low | Very Low | 0.4-0.6V | Energy-efficient |

## 13. Exercises

1. Compare power consumption of CMOS vs ECL at 100 MHz and 1 GHz
2. Design a level shifter between 3.3V and 1.8V domains
3. Calculate the propagation delay of a domino logic AND gate
4. Select the appropriate logic family for a 500 MHz clock distribution network
5. Design a near-threshold CMOS inverter for 0.5V operation
6. Compare static CMOS, domino, and NP-CMOS for a 16-bit adder
7. Create a power budget for a medical implant using LVCMOS
8. Design a BiCMOS buffer for driving 50 pF off-chip load
