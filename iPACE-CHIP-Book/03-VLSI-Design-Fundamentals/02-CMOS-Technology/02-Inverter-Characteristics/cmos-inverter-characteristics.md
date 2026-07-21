# CMOS Inverter Characteristics

## 1. Introduction to CMOS Inverter

The CMOS inverter is the fundamental building block of all digital circuits. It consists of one PMOS and one NMOS transistor connected in series, with their gates tied together as input and their drains tied together as output.

### 1.1 CMOS Inverter Structure

```
CMOS Inverter Schematic:

      V_DD
       │
    ┌──┴──┐
    │ PMOS │ ← Gate = Input A
    └──┬──┘
       │
       ├──── Output Y
       │
    ┌──┴──┐
    │ NMOS │ ← Gate = Input A
    └──┬──┘
       │
      GND

Physical Layout:
┌─────────────────────────┐
│  V_DD Metal             │
│     │                   │
│  ┌──┴──┐               │
│  │ PMOS │ Active        │
│  │ W_p  │               │
│  └──┬──┘               │
│     │                   │
│  ┌──┴──┐               │
│  │ NMOS │ Active        │
│  │ W_n  │               │
│  └──┬──┘               │
│     │                   │
│  GND Metal              │
└─────────────────────────┘
     Input A (poly gate)
```

### 1.2 Truth Table

```
Input-Output Relationship:
A | Y = A'
--|-----
0 |  1
1 |  0

Boolean Function: Y = NOT(A) = Ā = A'

Gate Symbol:
A ────|>o──── Y
      NOT
```

## 2. Voltage Transfer Characteristic (VTC)

### 2.1 VTC Curve Definition

```
Voltage Transfer Characteristic:
Plot of V_out vs V_in for CMOS inverter

V_out
  │
V_DD ──────────────────┐
  │                    │
  │   Region A:        │
  │   NMOS=OFF         │
  │   PMOS=Linear      │
  │                    │
V_M ───────────────────┼─── Switching Threshold
  │                    │   (V_in = V_out)
  │   Region B:        │
  │   Transition       │
  │   Region           │
  │                    │
  └────────────────────┘──── V_in
  0          V_DD/2    V_DD

Key Regions:
Region A (V_in < V_THN): NMOS OFF, PMOS Linear → V_out = V_DD
Region B (Transition): Both transistors conducting → Sharp transition
Region C (V_in > V_DD - |V_THP|): NMOS Linear, PMOS OFF → V_out = 0
```

### 2.2 VTC Regions of Operation

```
V_in       | NMOS          | PMOS          | V_out
-----------|---------------|---------------|--------
0-V_THN    | Cutoff        | Linear        | V_DD
V_THN-V_M  | Linear        | Linear        | ~V_DD
V_M        | Saturation    | Saturation    | V_M
V_M-V_DD+|V_THP| | Linear    | Saturation    | ~0
V_DD-|V_THP|-V_DD | Saturation    | Cutoff        | 0

V_M = Switching Threshold:
For symmetric inverter (W_p/W_n = μ_n/μ_p):
V_M = V_DD/2
```

### 2.3 Switching Threshold Calculation

```
At V_M, V_in = V_out = V_M, and both transistors are in saturation:

I_DN = I_DP

(1/2) × μ_n × C_ox × (W/L)_n × (V_M - V_THN)² = (1/2) × μ_p × C_ox × (W/L)_p × (V_DD - V_M - |V_THP|)²

Assuming V_THN = |V_THP| = V_TH (symmetric):
(W/L)_p/(W/L)_n = μ_n/μ_p = r (mobility ratio)

V_M = V_DD / (1 + √r) + V_TH × (√r - 1)/(1 + √r)

For r = μ_n/μ_p = 2.5 (typical):
V_M = V_DD / (1 + 1.58) + V_TH × (1.58 - 1)/(1 + 1.58)
V_M = 0.39 × V_DD + 0.22 × V_TH

If W_p/W_n = r (matched):
V_M = V_DD/2 (ideal symmetric inverter)
```

### 2.4 VTC Slope and Gain

```
DC Voltage Gain:
A_v = dV_out/dV_in (at V_M)

For ideal CMOS inverter:
|A_v| → ∞ (infinite gain at V_M)

In reality:
|A_v| ≈ 10-30 (typical)

Gain calculation:
A_v = -(g_mn + g_mp) × (r_on || r_op)

Where:
g_mn, g_mp = Transconductances of NMOS and PMOS
r_on, r_op = Output resistances

Higher gain → sharper transition → better noise margins
```

## 3. Noise Margins

### 3.1 Definition of Noise Margins

```
Noise Margin Parameters:

V_OH (Output High): Maximum output voltage when input is low
  - Ideal: V_OH = V_DD
  - Practical: V_OH = V_DD (CMOS has rail-to-rail output)

V_OL (Output Low): Minimum output voltage when input is high
  - Ideal: V_OL = 0
  - Practical: V_OL = 0 (CMOS has rail-to-rail output)

V_IH (Input High): Minimum input voltage recognized as logic high
  - Defined as VTC point where slope = -1 (V_in > V_M)

V_IL (Input Low): Maximum input voltage recognized as logic low
  - Defined as VTC point where slope = -1 (V_in < V_M)

Noise Margins:
NM_H (High-level noise margin) = V_OH - V_IH = V_DD - V_IH
NM_L (Low-level noise margin) = V_IL - V_OL = V_IL - 0 = V_IL

For ideal symmetric inverter:
NM_H = NM_L = V_DD/2
```

### 3.2 Noise Margin Calculation

```
Finding V_IH and V_IL from VTC:

Method 1: Graphical
- Plot VTC curve
- Find points where dV_out/dV_in = -1
- V_IH is at higher V_in, V_IL at lower V_in

Method 2: Analytical
For V_in > V_M (V_IH region):
NMOS in saturation, PMOS in linear

Solving dV_out/dV_in = -1:
V_IH = (2 × V_out - V_DD + V_THP) / (1 - 1/r)

Where r = (W/L)_p/(W/L)_n × (μ_p/μ_n)

For V_in < V_M (V_IL region):
NMOS in linear, PMOS in saturation

V_IL = (2 × V_out - V_THN) / (1 - r)

Typical Values (V_DD = 1.2V):
V_OH = 1.2 V
V_OL = 0 V
V_IH ≈ 0.72 V (60% of V_DD)
V_IL ≈ 0.48 V (40% of V_DD)

NM_H = 1.2 - 0.72 = 0.48 V
NM_L = 0.48 V
```

### 3.3 Factors Affecting Noise Margins

```
1. Supply Voltage (V_DD):
   - Higher V_DD → larger noise margins
   - NM ∝ V_DD
   - Power ∝ V_DD² (trade-off!)

2. Transistor Sizing (W_p/W_n):
   - Affects V_M and VTC symmetry
   - Equal rise/fall → symmetric noise margins

3. Threshold Voltage (V_TH):
   - Lower V_TH → V_M moves toward V_DD/2
   - But increases leakage current

4. Temperature:
   - Higher T → V_TH decreases → V_M shifts
   - Can reduce noise margins by 5-10%

5. Process Variation:
   - V_TH variation affects V_M
   - W/L variation affects drive strength
   - Can reduce noise margins by 10-20%

Design Rule of Thumb:
NM ≥ V_DD/4 for reliable operation
```

## 4. Power Dissipation

### 4.1 Dynamic Power

```
Dynamic Power Dissipation:
P_dynamic = α × C_L × V_DD² × f

Where:
α = Activity factor (probability of switching)
C_L = Load capacitance (gate + wire + diffusion)
V_DD = Supply voltage
f = Clock frequency

Components:
C_L = C_gate + C_wire + C_diffusion

C_gate = C_gn + C_gp (input capacitance)
C_wire = Wire capacitance (interconnect)
C_diffusion = Drain junction capacitances

Example (65nm):
C_L = 50 fF (typical)
V_DD = 1.2 V
f = 1 GHz
α = 0.15 (typical activity factor)

P_dynamic = 0.15 × 50e-15 × 1.2² × 1e9
          = 0.15 × 50e-15 × 1.44 × 1e9
          = 10.8 μW per gate
```

### 4.2 Static Power

```
Static Power Dissipation:
P_static = V_DD × I_leak

Leakage Current Components:
1. Subthreshold leakage (I_sub):
   I_sub = I_0 × exp((V_GS - V_TH)/(n × V_T)) × (1 - exp(-V_DS/V_T))

2. Gate tunneling leakage (I_gate):
   I_gate = A × (V_DD/T_ox)² × exp(-B × T_ox/V_DD)

3. Junction leakage (I_junc):
   - Reverse-biased diode leakage
   - Typically small compared to subthreshold

Total Leakage:
I_leak = I_sub + I_gate + I_junc

Static Power (65nm):
V_DD = 1.2 V
I_leak = 10 nA per transistor
1M transistors on chip:
P_static = 1.2 × 10e-9 × 1e6 = 12 mW

This can be 30-50% of total power in modern chips!
```

### 4.3 Short-Circuit Power

```
Short-Circuit Power:
During switching, both NMOS and PMOS conduct simultaneously

P_sc = V_DD × I_sc × t_sc × f

Where:
I_sc = Short-circuit current (peak)
t_sc = Overlap time (when both transistors ON)
f = Switching frequency

For CMOS inverter:
- Both transistors ON when V_THN < V_in < V_DD - |V_THP|
- Overlap time ≈ 10-20% of rise/fall time
- Typically 10-20% of dynamic power

Example:
I_sc = 50 μA (peak)
t_sc = 100 ps
f = 1 GHz
P_sc = 1.2 × 50e-6 × 100e-12 × 1e9 = 6 μW
```

### 4.4 Power Breakdown

```
Typical Power Budget (65nm, V_DD=1.2V, 1GHz):

Component      | Percentage | Value (1W chip)
---------------|------------|----------------
Dynamic        | 60-70%     | 600-700 mW
  - Switching  | 50-60%     | 500-600 mW
  - Short-circuit | 10-20%  | 100-200 mW
Static         | 30-40%     | 300-400 mW
  - Subthreshold | 20-30%   | 200-300 mW
  - Gate tunneling | 10%    | 100 mW

Power Reduction Techniques:
1. Voltage scaling: P ∝ V² (most effective)
2. Frequency scaling: P ∝ f
3. Clock gating: Reduce effective α
4. Power gating: Eliminate static power
5. Multi-V_th: Balance speed and leakage
```

## 5. Propagation Delay

### 5.1 Delay Definitions

```
Propagation Delay (CMOS Inverter):

t_pHL (High-to-Low): Time for output to fall from V_DD to V_DD/2
  - When input rises from 0 to V_DD
  - NMOS pulls output low

t_pLH (Low-to-High): Time for output to rise from 0 to V_DD/2
  - When input falls from V_DD to 0
  - PMOS pulls output high

t_p (Average propagation delay):
  t_p = (t_pHL + t_pLH) / 2

Timing Diagram:
V_in:  _____|‾‾‾‾‾‾‾‾‾‾‾‾|_____
              ↑
V_out: |‾‾‾‾‾‾|___________
         ↑   ↓
         t_pHL
         (output falls)

V_in:  |‾‾‾‾‾‾|___________
              ↓
V_out: _____|‾‾‾‾‾‾‾‾‾‾‾‾|_____
         ↑   ↓
         t_pLH
         (output rises)
```

### 5.2 Delay Calculation

```
RC Model for Delay:

t_pHL = 0.69 × R_eqn × C_L

Where:
R_eqn = Equivalent NMOS resistance in linear region
      = 1 / (μ_n × C_ox × (W/L)_n × (V_DD - V_THN - V_DSAT/2))

C_L = Total load capacitance

For t_pLH:
t_pLH = 0.69 × R_eqp × C_L

Where:
R_eqp = Equivalent PMOS resistance
      = 1 / (μ_p × C_ox × (W/L)_p × (V_DD - |V_THP| - V_DSAT/2))

Simplified Delay Model:
t_p = 0.69 × R_eq × C_L

For matched inverter (equal rise/fall):
R_eqn = R_eqp → t_pHL = t_pLH

Typical Values (65nm):
R_eq ≈ 5-20 kΩ (minimum size)
C_L ≈ 10-100 fF
t_p ≈ 10-100 ps
```

### 5.3 Fanout Effect

```
Fanout = C_load / C_in (load capacitance / input capacitance)

Delay with fanout:
t_p = 0.69 × R_eq × C_in × fanout

Or using logical effort:
t_p = t_p0 × (1 + fanout/h_opt)

Where:
t_p0 = Intrinsic delay
h_opt = Optimal fanout = √(p/g) ≈ 3-5

Example:
C_in = 10 fF
C_load = 50 fF
Fanout = 5
R_eq = 10 kΩ

t_p = 0.69 × 10e3 × 50e-15 = 345 ps

Optimal design: fanout ≈ 4
t_p increases linearly with fanout
```

### 5.4 Asymmetric Delay

```
When PMOS and NMOS are not matched:

t_pHL = 0.69 × R_eqn × C_L
t_pLH = 0.69 × R_eqp × C_L

If W_p = W_n (same size):
Since μ_n ≈ 2.5 × μ_p:
R_eqp ≈ 2.5 × R_eqn
t_pLH ≈ 2.5 × t_pHL

Asymmetry ratio: t_pLH/t_pHL = W_n/W_p × μ_n/μ_p

For matched delays:
W_p/W_n = μ_n/μ_p ≈ 2.5-3

Impact on Circuit:
- Asymmetric delays cause duty cycle distortion
- Affects clock generation
- Reduces maximum frequency
- Requires careful sizing for clock paths
```

## 6. CMOS Inverter Design

### 6.1 Design Parameters

```
Given Specifications:
- V_DD = 1.2 V
- V_THN = 0.4 V, |V_THP| = 0.4 V
- t_p ≤ 100 ps
- C_L = 50 fF
- Power budget: < 10 μW

Step 1: Calculate Required R_eq
t_p = 0.69 × R_eq × C_L
100e-12 = 0.69 × R_eq × 50e-15
R_eq = 100e-12 / (0.69 × 50e-15) = 2.9 kΩ

Step 2: Size NMOS for Required R_eq
R_eqn = 1 / (μ_n × C_ox × (W/L)_n × (V_DD - V_THN - V_DSAT/2))

Assuming V_DSAT = 0.3 V:
2.9e3 = 1 / (400 × 28.5e-15 × (W/L)_n × (1.2 - 0.4 - 0.15))
(W/L)_n = 1 / (2.9e3 × 400 × 28.5e-15 × 0.65)
(W/L)_n ≈ 48

Step 3: Size PMOS for Symmetry
(W/L)_p = (W/L)_n × μ_n/μ_p = 48 × 2.5 = 120

Final Design:
NMOS: W/L = 48 (e.g., W = 480 nm, L = 10 nm)
PMOS: W/L = 120 (e.g., W = 1.2 μm, L = 10 nm)
```

### 6.2 Inverter Sizing Guide

```
Sizing for Different Requirements:

1. Minimum Area:
   Use minimum L (technology limit)
   W_n = W_min, W_p = 2.5 × W_min
   Trade-off: Slower, higher resistance

2. Minimum Delay:
   Increase W (reduces R_eq)
   But increases C_L (more capacitance)
   Optimal: W ∝ √C_L

3. Minimum Power:
   Reduce W (less leakage)
   But increases delay
   Optimal: Balance delay vs leakage

4. Balanced Rise/Fall:
   W_p/W_n = μ_n/μ_p ≈ 2.5-3
   Ensures symmetric VTC

Sizing Table:
Requirement      | W_n    | W_p     | t_p   | Power
-----------------|--------|---------|-------|--------
Minimum area     | W_min  | 2.5W_min| Slow  | Low
Balanced         | W_min  | 3W_min  | Medium| Medium
High speed       | 2W_min | 6W_min  | Fast  | High
Low power        | W_min  | W_min   | Slow  | Very low
```

### 6.3 Layout Considerations

```
CMOS Inverter Layout Rules:

1. Gate Alignment:
   - PMOS and NMOS gates must align vertically
   - Shared polysilicon gate reduces area

2. Active Region Spacing:
   - Minimum spacing between n+ and p+ active
   - N-well boundary considerations

3. Contact Placement:
   - Source/drain contacts at minimum size
   - Multiple contacts for low resistance

4. Metal Routing:
   - V_DD and GND rails in metal 1
   - Input/output in metal 2 or higher

Layout Area Estimation:
Area ≈ (W_p + W_n + spacing) × (L + active_overlap)

For W_p = 1.2 μm, W_n = 0.48 μm:
Area ≈ (1.2 + 0.48 + 0.1) × (0.01 + 0.04) ≈ 84 nm²
```

## 7. Performance Metrics

### 7.1 Power-Delay Product (PDP)

```
Power-Delay Product:
PDP = P × t_p

Units: Joules (energy per switching event)

PDP = α × C_L × V_DD² × t_p

For minimum PDP:
- Reduce V_DD (most effective)
- Reduce C_L (smaller transistors)
- Optimize t_p (sizing)

Typical Values (65nm):
PDP ≈ 0.1-1 fJ per gate

Example:
P = 10 μW, t_p = 100 ps
PDP = 10e-6 × 100e-12 = 1 fJ

Energy Efficiency:
Energy/bit = PDP / bits_processed
           = 1 fJ / 1 bit = 1 fJ/bit
```

### 7.2 Energy-Delay Product (EDP)

```
Energy-Delay Product:
EDP = PDP × t_p = P × t_p²

Units: J·s

EDP is used to compare circuits with different speed-power trade-offs

Lower EDP = Better overall efficiency

For CMOS inverter:
EDP ∝ V_DD² × C_L × t_p²

Minimizing EDP requires optimizing both power and delay

Typical Values (65nm):
EDP ≈ 0.01-0.1 fJ·ps

Example:
PDP = 1 fJ, t_p = 100 ps
EDP = 1e-15 × 100e-12 = 100 e-27 = 0.1 fJ·ps
```

### 7.3 Figure of Merit (FoM)

```
Common Figures of Merit:

1. Speed: f_max = 1/(2 × t_p)
2. Power Efficiency: Energy/bit = PDP/bits
3. Area Efficiency: Gate density = 1/area
4. Power Density: P/area (W/mm²)
5. Performance/Watt: Operations per watt

Technology Comparison:
Technology | f_max  | PDP   | Area   | Power Density
-----------|--------|-------|--------|---------------
180nm      | 1 GHz  | 10 fJ | 1 μm²  | 10 W/mm²
65nm       | 3 GHz  | 1 fJ  | 0.1 μm²| 50 W/mm²
28nm       | 5 GHz  | 0.1fJ | 0.02μm²| 100 W/mm²
16nm       | 8 GHz  | 0.05fJ| 0.01μm²| 200 W/mm²
```

## 8. Advanced Inverter Configurations

### 8.1 Transmission Gate Inverter

```
Uses transmission gates instead of single transistors:

Structure:
V_DD
 |
[TG1] ← A' (A inverted)
 |
 Y --- Output
 |
[TG2] ← A
 |
GND

TG1 = PMOS (gate = A') + NMOS (gate = A)
TG2 = NMOS (gate = A) + PMOS (gate = A')

Advantages:
- Full voltage swing (0 to V_DD)
- Lower output resistance
- Better noise margins

Disadvantages:
- More transistors (6 vs 2)
- More capacitance
- Higher power
```

### 8.2 Pseudo-NMOS Inverter

```
Uses PMOS as active load:

      V_DD
       │
    ┌──┴──┐
    │ PMOS │ ← Gate = GND (always ON)
    └──┬──┘
       │
       ├──── Output Y
       │
    ┌──┴──┐
    │ NMOS │ ← Gate = Input A
    └──┬──┘
       │
      GND

Characteristics:
- Static power consumption (PMOS always conducts)
- Faster than CMOS (PMOS acts as pull-up resistor)
- Used in specialized applications

VTC is asymmetric:
- Output high: V_DD - I_D × R_on (not rail-to-rail)
- Output low: 0 V
```

### 8.3 Dynamic CMOS Inverter

```
Uses clock to precharge output:

      V_DD
       │
    ┌──┴──┐
    │ PMOS │ ← CLK
    └──┬──┘
       │
       ├──── Output Y
       │
    ┌──┴──┐
    │ NMOS │ ← CLK
    └──┬──┘
       │
      GND

Operation:
- Precharge phase (CLK=0): Output precharged to V_DD
- Evaluate phase (CLK=1): Output evaluates to logic value

Advantages:
- Higher speed (less capacitance)
- Lower power (no static current)

Disadvantages:
- Requires clock distribution
- Charge sharing issues
- More complex design
```

### 8.4 Comparison

| Type | Transistors | Speed | Power | Area | Application |
|------|-------------|-------|-------|------|-------------|
| Standard CMOS | 2 | Medium | Low | Small | General purpose |
| Transmission Gate | 6 | Fast | Medium | Large | High-speed paths |
| Pseudo-NMOS | 2 | Fast | High (static) | Small | Specialty |
| Dynamic | 2 | Very fast | Very low | Small | High-speed logic |

## 9. Cascaded Inverters

### 9.1 Chain of Inverters

```
N-stage Inverter Chain:
A → [INV1] → [INV2] → ... → [INV_N] → Y

For even N: Y = A (non-inverting buffer)
For odd N: Y = A' (inverting buffer)

Propagation Delay:
t_total = N × t_p

Rise/Fall Time:
t_r = t_f = 2.2 × R_eq × C_L (10% to 90%)

For N identical inverters:
t_total = N × 0.69 × R_eq × C_L

Important: Input rise/fall time affects delay!
When input is slow, delay increases by factor:
t_p(slow) = t_p(fast) × (1 + t_r/(2 × t_p0))
```

### 9.2 Tapered Inverter Chain

```
For driving large capacitive loads:

Input → [INV1] → [INV2] → ... → [INV_N] → C_L

Sizing: Each stage larger than previous by factor f
W_1 = W_min, W_2 = f × W_min, ..., W_N = f^(N-1) × W_min

Optimal Tapering Factor:
f_opt = √(p/g) ≈ 3-5 (for minimum delay)

Total Delay:
t_total = N × t_p0 × (f + p/g)

For minimum delay:
N_opt = ln(C_L/C_in) / ln(f_opt)
f_opt = e^(t_p0/t_p0) ≈ 2.7 (ideal)
Practical f_opt = 3-4

Example:
C_in = 10 fF, C_L = 1000 fF (100× load)
f_opt = 4
N = ln(100) / ln(4) ≈ 3.3 → 4 stages

Delay = 4 × t_p0 × (4 + 1) = 20 × t_p0
vs direct drive: 100 × t_p0 (10× slower!)
```

### 9.3 Ring Oscillator

```
Ring Oscillator: Odd number of inverters in a loop

N inverters (odd) in cascade:
INV1 → INV2 → ... → INV_N → back to INV1

Oscillation Frequency:
f_osc = 1/(2 × N × t_p)

For N = 3 (minimum):
f_osc = 1/(6 × t_p)

For N = 5:
f_osc = 1/(10 × t_p)

Example (65nm, t_p = 20 ps):
N = 3: f_osc = 1/(6 × 20e-12) = 8.3 GHz
N = 5: f_osc = 1/(10 × 20e-12) = 5 GHz
N = 7: f_osc = 1/(14 × 20e-12) = 3.6 GHz

Applications:
- Clock generation (PLL)
- Process monitoring
- Random number generation
- Voltage-controlled oscillator (VCO)
```

## 10. Verilog Models

### 10.1 Gate-Level Model

```verilog
// CMOS Inverter - Gate Level
module cmos_inverter_gate (
    input  wire A,
    output wire Y
);

    // Structural instantiation
    // Note: Requires standard cell library
    // INV_X1 inv1 (.A(A), .Y(Y));

    // Alternative: Using primitives (if available)
    not inv1 (Y, A);

endmodule
```

### 10.2 Dataflow Model

```verilog
// CMOS Inverter - Dataflow
module cmos_inverter_df (
    input  wire A,
    output wire Y
);

    assign Y = ~A;

endmodule
```

### 10.3 Behavioral Model with Timing

```verilog
// CMOS Inverter - Behavioral with timing
module cmos_inverter_behavioral (
    input  wire A,
    output reg  Y
);

    // Propagation delay parameters
    parameter t_pHL = 20e-12;  // 20 ps high-to-low
    parameter t_pLH = 20e-12;  // 20 ps low-to-high

    always @(*) begin
        if (A)
            #(t_pHL) Y = 1'b0;  // Fall delay
        else
            #(t_pLH) Y = 1'b1;  // Rise delay
    end

endmodule
```

### 10.4 Transistor-Level Model

```verilog
// CMOS Inverter - Transistor Level (simplified)
module cmos_inverter_transistor (
    input  wire A,
    output wire Y
);

    // PMOS: source=V_DD, drain=Y, gate=A
    // NMOS: source=GND, drain=Y, gate=A

    // In Verilog-A or SPICE, this would be:
    // MP (Y A V_DD V_DD) PMOS W=1.2u L=0.06u
    // MN (Y A GND GND) NMOS W=0.48u L=0.06u

    // Simplified behavioral:
    assign (strong0, pull1) Y = ~A;

endmodule
```

### 10.5 Testbench

```verilog
module tb_cmos_inverter;

    reg A;
    wire Y;

    // Instantiate inverter
    cmos_inverter_df dut (.A(A), .Y(Y));

    // Test stimulus
    initial begin
        $monitor("Time=%0t A=%b Y=%b", $time, A, Y);

        A = 0;
        #10 A = 1;
        #10 A = 0;
        #10 A = 1;
        #10 A = 0;

        // Test with slow input
        #10 A = 0;
        #5 A = 0.2;
        #5 A = 0.4;
        #5 A = 0.6;
        #5 A = 0.8;
        #5 A = 1.0;

        #20 $finish;
    end

    // VCD dump for waveform viewing
    initial begin
        $dumpfile("cmos_inverter.vcd");
        $dumpvars(0, tb_cmos_inverter);
    end

endmodule
```

## 11. Applications in Medical Implant Design

### 11.1 Ultra-Low-Power Inverter Design

```
For implantable devices:

Key Requirements:
- Minimum power consumption
- Reliable operation at low voltage
- Radiation hardness (for some implants)

Design Strategies:

1. Near-Threshold Operation:
   V_DD ≈ V_TH + 100-200 mV
   Example: V_TH = 0.4V, V_DD = 0.5-0.6V
   Power reduction: 5-10×
   Delay increase: 3-5×

2. Multi-Threshold Design:
   - Critical path: Low-V_TH (fast)
   - Non-critical: High-V_TH (low leakage)
   - Best of both worlds

3. Adaptive Body Biasing:
   Forward body bias: Reduce V_TH at runtime
   Reverse body bias: Increase V_TH for low leakage
   Dynamic adjustment based on activity

4. Power Gating:
   Sleep transistors to cut off power
   State retention flip-flops
   Wake-up time: 10-100 ns
```

### 11.2 Radiation Hardening

```
For implants exposed to radiation:

Single-Event Upset (SEU):
- High-energy particle strikes node
- Causes transient voltage glitch
- Can flip stored data

Mitigation:
1. Temporal redundancy: Triple sampling
2. Spatial redundancy: TMR (Triple Modular Redundancy)
3. Guard rings: Prevent charge collection
4. Silicon-on-Insulator (SOI): Reduced charge collection

Hardened Inverter Design:
┌─────────────────────────┐
│    Guard Ring            │
│  ┌─────────────────┐    │
│  │    PMOS          │    │
│  └─────────────────┘    │
│    ┌─────────────────┐  │
│  │    NMOS          │  │
│  └─────────────────┘  │
└─────────────────────────┘

Area overhead: 2-5×
Power overhead: 10-30%
SEU rate reduction: 100-1000×
```

## 12. Summary

| Parameter | Symbol | Typical Value | Impact |
|-----------|--------|---------------|--------|
| Switching Threshold | V_M | V_DD/2 | Noise margins |
| Noise Margin High | NM_H | V_DD/4 | Noise immunity |
| Noise Margin Low | NM_L | V_DD/4 | Noise immunity |
| Propagation Delay | t_p | 10-100 ps | Speed |
| Dynamic Power | P_dyn | αCV²f | Energy consumption |
| Static Power | P_stat | V_DD × I_leak | Battery life |
| Power-Delay Product | PDP | 0.1-1 fJ | Energy efficiency |
| Fanout | h | 3-5 | Delay optimization |

## 13. Exercises

1. Calculate the VTC for a CMOS inverter with W_p/W_n = 3, μ_n/μ_p = 2.5
2. Design a CMOS inverter with t_p ≤ 50 ps for C_L = 20 fF
3. Calculate noise margins for V_DD = 0.8V, V_TH = 0.3V
4. Compare power consumption at V_DD = 1.2V vs V_DD = 0.5V
5. Design a 5-stage ring oscillator and calculate its frequency
6. Analyze the effect of temperature on inverter delay (T = 25°C vs 75°C)
7. Calculate the optimal tapering factor for driving 100× load capacitance
8. Design a low-power inverter for implantable medical device specifications
