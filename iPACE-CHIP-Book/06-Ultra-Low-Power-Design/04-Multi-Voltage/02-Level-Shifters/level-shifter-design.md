# Level Shifter Design for Implantable Pacemaker ASICs

## 1. Introduction to Level Shifters

Level shifters are essential circuit elements in multi-voltage designs that translate digital signals between different voltage domains. For the iPACE-CHIP pacemaker ASIC, level shifters enable communication between blocks operating at different supply voltages (0.8V, 1.2V, 1.5V, and 1.8V), ensuring reliable signal integrity while minimizing power consumption and propagation delay.

In implantable medical devices, level shifters must meet stringent requirements: ultra-low leakage when passing static signals, minimal propagation delay for timing-critical paths, guaranteed glitch-free operation, and radiation tolerance for the implant environment. The iPACE-CHIP employs specialized level shifter designs optimized for each voltage translation pair and application requirement.

## 2. Level Shifter Architectures

### 2.1 Low-to-High Level Shifter

```
Low-to-High (LH) Level Shifter:

Translates signals from low voltage domain to high voltage domain.

V_DD_high (1.8V)
    │
    ├─────────────────────────────────────┐
    │                                     │
    │  ┌──────────────┐   ┌──────────────┐│
    │  │              │   │              ││
    │  │   PMOS M1    │   │   PMOS M3    ││
    │  │   (cross-    │   │   (cross-    ││
    │  │    coupled)  │   │    coupled)  ││
    │  └──────┬───────┘   └──────┬───────┘│
    │         │                  │         │
    │    ┌────┴────┐        ┌────┴────┐    │
    │    │         │        │         │    │
IN ──────┤  NMOS   ├────────┤  NMOS   │    │
(1.2V)   │  M2     │        │  M4     │    │
    │    │  (input)│        │  (input)│    │
    │    └────┬────┘        └────┬────┘    │
    │         │                  │         │
    │    ┌────┴────┐        ┌────┴────┐    │
    │    │  PMOS   │        │  PMOS   │    │
    │    │  M5     │        │  M6     │    │
    │    │(V_DD_low│        │(V_DD_low│    │
    │    │ feedbck)│        │ feedbck)│    │
    │    └────┬────┘        └────┬────┘    │
    │         │                  │         │
    │    ┌────┴────┐        ┌────┴────┐    │
    │    │  NMOS   │        │  NMOS   │    │
    │    │  M7     │        │  M8     │    │
    │    │(V_DD_low│        │(V_DD_low│    │
    │    │ feedbck)│        │ feedbck)│    │
    │    └────┬────┘        └────┬────┘    │
    │         │                  │         │
    │         ├──────────────────┤         │
    │         │                  │         │
    │    ┌────┴────┐        ┌────┴────┐    │
    │    │ Output  │        │ Output  │    │
    │    │ Node A  │        │ Node B  │    │
    │    └────┬────┘        └────┬────┘    │
    │         │                  │         │
    │         └──────────┬───────┘         │
    │                    │                 │
    │              ┌─────┴─────┐           │
    │              │           │           │
    │              │  OUT      │           │
    │              │ (1.8V)    │           │
    │              └───────────┘           │
    │                                      │
    └──────────────────────────────────────┘
                    │
               GND (0V)

Operation:
- IN = 0V (GND): M2 OFF, M4 OFF
  M1 ON (via M5/M7 feedback), M3 ON (via M6/M8 feedback)
  OUT = V_DD_high (1.8V)

- IN = 1.2V: M2 ON, M4 ON
  M1 OFF (pulled down by M2), M3 OFF (pulled down by M4)
  OUT = 0V (GND)

Specifications:
- Input voltage: 0V to 1.2V
- Output voltage: 0V to 1.8V
- Propagation delay: 0.2 ns (typical)
- Static power: 100 pA (leakage only)
- Dynamic power: 2 fF × (1.8V)² × f
- Area: 3.6 μm × 2.4 μm = 8.64 μm²
```

### 2.2 High-to-Low Level Shifter

```
High-to-Low (HL) Level Shifter:

Translates signals from high voltage domain to low voltage domain.

V_DD_high (1.8V)
    │
    ├─────────────────────────────────────┐
    │                                     │
    │  ┌──────────────┐   ┌──────────────┐│
    │  │              │   │              ││
    │  │   PMOS M1    │   │   PMOS M3    ││
    │  │   (cross-    │   │   (cross-    ││
    │  │    coupled)  │   │    coupled)  ││
    │  └──────┬───────┘   └──────┬───────┘│
    │         │                  │         │
    │    ┌────┴────┐        ┌────┴────┐    │
    │    │         │        │         │    │
IN ──────┤  NMOS   ├────────┤  NMOS   │    │
(1.8V)   │  M2     │        │  M4     │    │
    │    │  (input)│        │  (input)│    │
    │    └────┬────┘        └────┬────┘    │
    │         │                  │         │
    │    ┌────┴────┐        ┌────┴────┐    │
    │    │  NMOS   │        │  NMOS   │    │
    │    │  M5     │        │  M6     │    │
    │    │(V_DD_low│        │(V_DD_low│    │
    │    │ feedbck)│        │ feedbck)│    │
    │    └────┬────┘        └────┬────┘    │
    │         │                  │         │
    │    ┌────┴────┐        ┌────┴────┐    │
    │    │ Output  │        │ Output  │    │
    │    │ Node A  │        │ Node B  │    │
    │    └────┬────┘        └────┬────┘    │
    │         │                  │         │
    │         └──────────┬───────┘         │
    │                    │                 │
    └────────────────────┼─────────────────┘
                         │
                    ┌────┴────┐
                    │         │
                    │  OUT    │
                    │(1.2V)   │
                    └─────────┘
                         │
                    V_DD_low (1.2V)

Operation:
- IN = 0V (GND): M2 OFF, M4 OFF
  M1 ON, M3 ON (cross-coupled feedback)
  OUT = V_DD_low (1.2V)

- IN = 1.8V: M2 ON, M4 ON
  M1 OFF, M3 OFF
  OUT = 0V (GND)

Specifications:
- Input voltage: 0V to 1.8V
- Output voltage: 0V to 1.2V
- Propagation delay: 0.15 ns (typical)
- Static power: 50 pA (leakage only)
- Dynamic power: 1.5 fF × (1.2V)² × f
- Area: 3.0 μm × 2.0 μm = 6.0 μm²
```

### 2.3 Ultra-Low-Voltage Level Shifter

```
Ultra-Low-Voltage Level Shifter (0.8V to 1.8V):

Special design for translating from ultra-low voltage domain:

V_DD_high (1.8V)
    │
    ├─────────────────────────────────────┐
    │                                     │
    │  ┌──────────────┐   ┌──────────────┐│
    │  │   PMOS M1    │   │   PMOS M3    ││
    │  └──────┬───────┘   └──────┬───────┘│
    │         │                  │         │
    │    ┌────┴────┐        ┌────┴────┐    │
    │    │  NMOS   │        │  NMOS   │    │
    │    │  M2     │        │  M4     │    │
    │    │(V_DD_ultra│      │(V_DD_ultra│  │
    │    │ 0.8V)   │        │ 0.8V)   │    │
    │    └────┬────┘        └────┬────┘    │
    │         │                  │         │
    │    ┌────┴────┐        ┌────┴────┐    │
    │    │  PMOS   │        │  PMOS   │    │
    │    │  M5     │        │  M6     │    │
    │    │(V_DD_ultra│      │(V_DD_ultra│  │
    │    │ 0.8V)   │        │ 0.8V)   │    │
    │    └────┬────┘        └────┬────┘    │
    │         │                  │         │
    │    ┌────┴────┐        ┌────┴────┐    │
    │    │ Output  │        │ Output  │    │
    │    │ Node    │        │ Node    │    │
    │    └────┬────┘        └────┬────┘    │
    │         │                  │         │
    │         └──────────┬───────┘         │
    │                    │                 │
    │              ┌─────┴─────┐           │
    │              │  OUT      │           │
    │              │ (1.8V)    │           │
    │              └───────────┘           │
    │                                      │
    └──────────────────────────────────────┘
                    │
               GND (0V)

Design Considerations:
- Input swing: 0V to 0.8V (very low)
- Must overcome threshold voltage issues
- Use minimum-length transistors for speed
- Larger widths for adequate current drive
- Metastability protection critical at low voltage

Specifications:
- Input voltage: 0V to 0.8V
- Output voltage: 0V to 1.8V
- Propagation delay: 0.4 ns (typical, slower due to low input)
- Static power: 200 pA (higher due to low V_th)
- Dynamic power: 3 fF × (1.8V)² × f
- Area: 4.8 μm × 3.0 μm = 14.4 μm²
```

## 3. Transistor Sizing

### 3.1 Input Stage Sizing

```
Level Shifter Input Stage Sizing:

For Low-to-High (1.2V to 1.8V):

Input NMOS (M2, M4):
- Must overcome threshold voltage at V_DD_low = 1.2V
- V_GS = 1.2V (at input high)
- V_th = 0.4V (standard Vt)
- Overdrive: V_GS - V_th = 0.8V
- Required current: 10 μA (for fast switching)
- W/L = I / (μ_n × C_ox × (V_GS - V_th)² / 2)
- W/L = 10 μA / (270 × 8.6fF/μm² × (0.8V)² / 2)
- W/L = 10 / (270 × 8.6 × 0.32 / 2) = 10 / 37.2 = 0.27 μm
- Use W = 0.5 μm, L = 0.18 μm (rounded up for margin)

Cross-Coupled PMOS (M1, M3):
- Must be weak enough to be overridden by NMOS
- But strong enough to pull up output
- W/L ratio: PMOS_width / NMOS_width = 0.3 to 0.5
- Use W = 0.2 μm, L = 0.18 μm

Feedback PMOS/NMOS (M5-M8):
- Weak devices for metastability prevention
- W = 0.18 μm, L = 0.18 μm (minimum size)
```

### 3.2 Output Stage Sizing

```
Level Shifter Output Stage Sizing:

Output must drive subsequent logic:
- Load capacitance: 5 fF (typical)
- Required slew rate: 1 V/ns
- I_required = C × dV/dt = 5 fF × 1 V/ns = 5 μA

Output PMOS (M1, M3):
- W/L sized for 5 μA at V_DD_high = 1.8V
- W/L = 5 μA / (60 × 8.6fF/μm² × (1.8V - 0.4V)² / 2)
- W/L = 5 / (60 × 8.6 × 0.98 / 2) = 5 / 252.8 = 0.02 μm
- Minimum W = 0.36 μm (process minimum for output drive)

Output NMOS (M2, M4):
- Must pull down against cross-coupled PMOS
- W = 0.5 μm (input stage sizing already adequate)

Net output drive capability:
- Pull-up: 5 μA (PMOS)
- Pull-down: 10 μA (NMOS)
- Asymmetric but acceptable (pull-down faster)
```

### 3.3 Process Variation Impact

```
Level Shifter Performance vs. Process Corner:

Corner    │ Delay    │ Power    │ Status
──────────┼──────────┼──────────┼────────
FF (fast) │ 0.12 ns  │ 150 pA   │ PASS
TT (typ)  │ 0.20 ns  │ 100 pA   │ PASS
SS (slow) │ 0.35 ns  │ 60 pA    │ PASS
SF        │ 0.18 ns  │ 120 pA   │ PASS
FS        │ 0.22 ns  │ 80 pA    │ PASS

Worst-case delay: 0.35 ns (SS corner)
Timing budget: 1.0 ns (for iPACE-CHIP)
Margin: 0.65 ns (65% margin)
All corners pass timing requirements.
```

## 4. Power Analysis

### 4.1 Static Power

```
Level Shifter Static Power Analysis:

Sources of Static Power:
1. Sub-threshold leakage through OFF transistors
2. Gate oxide tunneling (negligible at 180nm)
3. Junction leakage (negligible)

Per-Cell Leakage (at 37°C):
┌──────────────────────┬──────────┬──────────┐
│ Voltage Pair         │ Leakage  │ Power    │
├──────────────────────┼──────────┼──────────┤
│ 1.2V → 1.8V (LH)    │ 100 pA   │ 180 pW   │
│ 1.8V → 1.2V (HL)    │ 50 pA    │ 60 pW    │
│ 0.8V → 1.8V (ULV)   │ 200 pA   │ 360 pW   │
│ 1.8V → 0.8V (HL-ULV)│ 80 pA    │ 64 pW    │
└──────────────────────┴──────────┴──────────┘

iPACE-CHIP Level Shifter Count:
- 1.2V → 1.8V: 16 cells
- 1.8V → 1.2V: 10 cells
- 0.8V → 1.8V: 8 cells
- 1.8V → 0.8V: 5 cells
- Total: 39 cells

Total Static Power:
P_static = 16×180 + 10×60 + 8×360 + 5×64
         = 2880 + 600 + 2880 + 320 = 6680 pW = 6.68 nW
```

### 4.2 Dynamic Power

```
Level Shifter Dynamic Power Analysis:

Dynamic Power per Cell:
P_dynamic = C_load × V_DD² × f × α

Where:
- C_load: Input capacitance of level shifter
- V_DD: Supply voltage of receiving domain
- f: Switching frequency
- α: Switching activity factor

Per-Cell Dynamic Power (at 32 kHz, α = 0.5):
┌──────────────────────┬──────────┬──────────┬──────────┐
│ Voltage Pair         │ C_load   │ V_DD²    │ P_dyn    │
├──────────────────────┼──────────┼──────────┼──────────┤
│ 1.2V → 1.8V (LH)    │ 3 fF     │ 3.24     │ 0.155 nW │
│ 1.8V → 1.2V (HL)    │ 2.5 fF   │ 1.44     │ 0.058 nW │
│ 0.8V → 1.8V (ULV)   │ 4 fF     │ 3.24     │ 0.207 nW │
│ 1.8V → 0.8V (HL-ULV)│ 3 fF     │ 0.64     │ 0.031 nW │
└──────────────────────┴──────────┴──────────┴──────────┘

Total Dynamic Power (39 cells):
P_dynamic = 16×0.155 + 10×0.058 + 8×0.207 + 5×0.031
         = 2.48 + 0.58 + 1.656 + 0.155 = 4.87 nW

Total Level Shifter Power: 6.68 + 4.87 = 11.55 nW

Percentage of Total iPACE-CHIP Power: 11.55 / 3300 = 0.35%
Level shifter power is negligible.
```

### 4.3 Power Optimization

```
Level Shifter Power Optimization Techniques:

Technique 1: Clock Gating on Level Shifters
- Gate clock to level shifters during idle periods
- Savings: 50% of dynamic power (2.44 nW)
- Implementation: AND gate before level shifter input

Technique 2: Minimum-Size Transistors
- Use minimum-length transistors where timing allows
- Savings: 20% of area (and capacitance)
- Risk: Slower switching at process corners

Technique 3: Body Biasing
- Apply reverse body bias to reduce leakage
- Savings: 50% of static power (3.34 nW)
- Implementation: Separate body contact per level shifter

Technique 4: Power Gating
- Power off level shifters when not needed
- Savings: 100% of power when off
- Risk: Glitches during power-on

Total Potential Savings: 5.78 nW (50% reduction)
Optimized Level Shifter Power: 5.77 nW
```

## 5. Metastability Protection

### 5.1 Metastability Analysis

```
Level Shifter Metastability Risk:

Risk Scenario: Input changes during internal regenerative transition

When the input to a cross-coupled level shifter changes at
the same time as the internal nodes are regenerating,
metastability can occur.

Metastability Window:
- Setup time: 0.1 ns
- Hold time: 0.05 ns
- Window: 0.15 ns

Probability of Metastability:
P_meta = f_CLK × t_window × f_input
P_meta = 32 kHz × 0.15 ns × 1 kHz = 4.8 × 10⁻⁹ per second

For 10-year operation:
Expected metastable events: 4.8 × 10⁻⁹ × 3.15 × 10⁸ = 1.5 events

This is marginal for a medical device.
Metastability protection is required.
```

### 5.2 Metastability Hardened Design

```
Metastability-Hardened Level Shifter:

Add redundant regenerative feedback:

V_DD_high (1.8V)
    │
    ├─────────────────────────────────────┐
    │                                     │
    │  ┌──────────────┐   ┌──────────────┐│
    │  │   PMOS M1    │   │   PMOS M3    ││
    │  └──────┬───────┘   └──────┬───────┘│
    │         │                  │         │
    │    ┌────┴────┐        ┌────┴────┐    │
    │    │  NMOS   │        │  NMOS   │    │
    │    │  M2     │        │  M4     │    │
    │    └────┬────┘        └────┬────┘    │
    │         │                  │         │
    │    ┌────┴────┐        ┌────┴────┐    │
    │    │  PMOS   │        │  PMOS   │    │
    │    │  M5     │        │  M6     │    │
    │    └────┬────┘        └────┬────┘    │
    │         │                  │         │
    │    ┌────┴────┐        ┌────┴────┐    │
    │    │  NMOS   │        │  NMOS   │    │
    │    │  M7     │        │  M8     │    │
    │    └────┬────┘        └────┬────┘    │
    │         │                  │         │
    │    ┌────┴────┐        ┌────┴────┐    │
    │    │ Master  │        │ Master  │    │
    │    │ Output  │        │ Output  │    │
    │    └────┬────┘        └────┬────┘    │
    │         │                  │         │
    │         │    ┌─────────────┤         │
    │         │    │             │         │
    │    ┌────▼────▼─┐   ┌──────▼──────┐  │
    │    │  Voter    │   │  Voter      │  │
    │    │  (TMR)    │   │  (TMR)      │  │
    │    └─────┬─────┘   └──────┬──────┘  │
    │          │                │          │
    │          └────────┬───────┘          │
    │                   │                  │
    │              ┌────┴────┐             │
    │              │  OUT    │             │
    │              │ (1.8V)  │             │
    │              └─────────┘             │
    │                                      │
    └──────────────────────────────────────┘
                    │
               GND (0V)

Features:
- Triple Modular Redundancy (TMR) on output stage
- Majority voter ensures correct output
- Metastability MTBF: > 10¹² years
- Area overhead: 3× (from 8.64 μm² to 25.9 μm²)
- Power overhead: 3× (from 0.18 nW to 0.54 nW)
```

### 5.3 Synchronizer Approach

```
Level Shifter with Input Synchronizer:

For applications where metastability is critical:

Input ────┬───────┬───────┬──── Level Shifter Input
          │       │       │
     ┌────▼───┐┌──▼───┐┌──▼───┐
     │ FF-1   ││ FF-2 ││ FF-3 │ (3-stage synchronizer)
     │(V_DD_low││      ││      │
     └────┬───┘└──┬───┘└──┬───┘
          │       │       │
          └───────┴───────┘

Benefits:
- Eliminates metastability at level shifter input
- Adds latency: 3 clock cycles (93.75 μs at 32 kHz)
- Only suitable for non-time-critical signals

iPACE-CHIP Application:
- Configuration register writes (non-critical)
- Status flag updates (non-critical)
- NOT for data path or timing-critical signals
```

## 6. Radiation Hardening

### 6.1 SEU Effects on Level Shifters

```
Single Event Upset (SEU) Effects:

Level Shifter SEU Vulnerability:
- Cross-coupled nodes can be flipped by particle strike
- Output can latch incorrect value
- Error persists until next input transition

SEU Rate Estimation:
- LET threshold: 15 MeV·cm²/mg (180nm)
- Cross-section at LET = 30: 10⁻¹² cm²/bit
- Particle flux in body: 1 particle/cm²/year
- SEU rate per level shifter: 10⁻¹² per year

For 39 level shifters:
- Total SEU rate: 3.9 × 10⁻¹¹ per year
- MTBF: 2.6 × 10¹⁰ years

This is adequate for a medical device.
No special radiation hardening required for level shifters.
```

### 6.2 Radiation Hardening Techniques

```
Radiation Hardened Level Shifter (if needed):

Technique 1: Increased Critical Charge
- Use thicker oxide transistors
- Increase node capacitance
- Q_crit increase: 2×

Technique 2: Redundant Storage
- TMR on cross-coupled nodes
- 3× area overhead
- SEU immune (majority voting)

Technique 3: Temporal Redundancy
- Sample input at two different times
- Compare before accepting
- 2× latency overhead

Technique 4: Guard Rings
- Enhanced guard rings for latch-up prevention
- 20% area overhead
- Not needed for SEU (only for SEL)

iPACE-CHIP Recommendation:
- Standard level shifters (no radiation hardening)
- SEU rate acceptable (< 10⁻¹⁰ per year)
- Focus hardening efforts on retention flops instead
```

## 7. Summary

Level shifter design for the iPACE-CHIP pacemaker ASIC implements four voltage translation pairs (1.2V→1.8V, 1.8V→1.2V, 0.8V→1.8V, 1.8V→0.8V) using cross-coupled inverter architectures optimized for each voltage combination. The total level shifter power is 11.55 nW (0.35% of total), with static power dominating at 6.68 nW. Metastability protection through TMR achieves MTBF exceeding 10¹² years. Process variation analysis confirms timing closure across all corners with 65% minimum margin. The level shifters are a critical enabling technology for the iPACE-CHIP's multi-voltage architecture, enabling communication between voltage domains with minimal power and area overhead.

## References

1. Shimizu, K., et al., "A Level Shifter for Multi-Voltage Operating ASICs," IEEE JSSC, 2002.
2. iPACE-CHIP Project Internal Documentation: Level Shifter Design Specification, Rev 1.3.
3. TSMC 0.18μm Mixed-Signal Process Design Manual: Standard Cell Library.
4. Kulkarni, S., et al., "Low-Voltage Level Shifter Design," IEEE ISCAS, 2006.
5. NASA: Radiation Hardening Techniques for Space Electronics, 2018.
