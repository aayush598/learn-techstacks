# Power Switch Design for Implantable Pacemaker ASICs

## 1. Introduction to Power Switches

Power switches are the fundamental building blocks of power gating, enabling complete shutdown of circuit blocks by disconnecting them from the power supply or ground. For the iPACE-CHIP pacemaker ASIC, power switches must achieve ultra-low leakage in the off state while providing adequate current drive in the on state, all within the constraints of an implantable medical device.

The design of power switches for implantable pacemakers presents unique challenges: the switches must be radiation-tolerant, reliable over 10 years of continuous operation, and capable of millions of power cycling events without degradation. Additionally, the switches must minimize both on-state resistance (to avoid voltage droop) and off-state leakage (to maximize power savings).

## 2. Power Switch Architectures

### 2.1 Header Switch (PMOS)

```
PMOS Header Power Switch Architecture:

V_DD ─────────────────────────┐
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    │    PMOS Header      │
                    │    Power Switch     │
                    │                     │
                    │    W/L = 10μm/0.18μm│
                    │                     │
                    └──────────┬──────────┘
                               │
                    V_DD_switched (clean power domain)
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    │    Power Domain     │
                    │    (logic block)    │
                    │                     │
                    └──────────┬──────────┘
                               │
GND ───────────────────────────┘

Operating Modes:
- ON:  V_G = GND, V_GS = -V_DD, R_on ≈ 50 Ω
- OFF: V_G = V_DD, V_GS = 0V, I_leak ≈ 50 pA

Control Signal: active-high PWR_EN_n (active-low)
```

### 2.2 Footer Switch (NMOS)

```
NMOS Footer Power Switch Architecture:

V_DD ─────────────────────────┐
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    │    Power Domain     │
                    │    (logic block)    │
                    │                     │
                    └──────────┬──────────┘
                               │
                    V_DD_footer (virtual ground)
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    │    NMOS Footer      │
                    │    Power Switch     │
                    │                     │
                    │    W/L = 8μm/0.18μm │
                    │                     │
                    └──────────┬──────────┘
                               │
GND ───────────────────────────┘

Operating Modes:
- ON:  V_G = V_DD, V_GS = V_DD, R_on ≈ 60 Ω
- OFF: V_G = GND, V_GS = 0V, I_leak ≈ 30 pA

Note: NMOS footer has body effect that increases R_on
when V_DD is applied. Larger width needed vs. PMOS header.
```

### 2.3 Comparison of Header vs. Footer

```
Header vs. Footer Switch Comparison:

┌──────────────────────┬──────────────┬──────────────┐
│ Parameter            │ PMOS Header  │ NMOS Footer  │
├──────────────────────┼──────────────┼──────────────┤
│ ON resistance        │ 50 Ω         │ 60 Ω         │
│ OFF leakage          │ 50 pA        │ 30 pA        │
│ Area                 │ 21.3 μm²    │ 17.1 μm²    │
│ Body effect          │ None         │ Significant  │
│ Gate control         │ Active-low   │ Active-high  │
│ Virtual supply       │ V_DD_switched│ V_DD_footer  │
│ Noise immunity       │ High         │ Medium       │
│ Process sensitivity  │ Low          │ Medium       │
├──────────────────────┼──────────────┼──────────────┤
│ iPACE-CHIP Choice    │ PRIMARY      │ SECONDARY    │
└──────────────────────┴──────────────┴──────────────┘

Recommendation: Use PMOS header as primary power switch
for iPACE-CHIP due to better noise immunity and no body effect.
```

## 3. Transistor-Level Design

### 3.1 PMOS Header Switch Design

```
PMOS Header Switch Transistor Schematic:

V_DD ──────────────────────────┐
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    │      PMOS M1        │
                    │      W = 10 μm      │
                    │      L = 0.18 μm    │
                    │      V_th = -0.4V   │
                    │                     │
                    └──────────┬──────────┘
                               │
                    V_DD_switched
                               │
                    ┌──────────┴──────────┐
                    │   Parasitic Caps    │
                    │   C_db = 50 fF      │
                    │   C_sb = 0 fF       │
                    │   (source = V_DD)   │
                    └─────────────────────┘

Gate Control Circuit:
                    ┌─────────────────────┐
V_DD ───────────────┤                     │
                    │   Level Shifter     │
PWR_EN_n ──────────┤   (V_DD to V_DD)    ├─── V_G
                    │                     │
GND ───────────────┤                     │
                    └─────────────────────┘

Design Parameters:
- On-resistance: R_on = 1/(μ_p × C_ox × (W/L) × (V_GS - V_th))
- R_on ≈ 50 Ω at V_GS = -1.8V
- Maximum current: I_max = (V_DD - V_DD_switched) / R_on
- For 10 μA load: V_drop = 10 μA × 50 Ω = 0.5 mV (negligible)
```

### 3.2 Multi-Finger Layout

```
Power Switch Layout Strategy:

Multi-Finger PMOS Layout:

┌─────────────────────────────────────────────────────────┐
│                    PMOS Header Switch                    │
│                                                         │
│  V_DD (metal4) ───────────────────────────────────────  │
│  │     │     │     │     │     │     │     │     │     │
│  ┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐    │
│  │ F1  ││ F2  ││ F3  ││ F4  ││ F5  ││ F6  ││ F7  │    │
│  │     ││     ││     ││     ││     ││     ││     │    │
│  └──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘    │
│     │      │      │      │      │      │      │        │
│  V_DD_switched (metal4) ─────────────────────────────   │
│                                                         │
│  Gate (poly) ───────────────────────────────────────    │
│  │     │     │     │     │     │     │     │     │     │
│  └─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘     │
│                                                         │
│  Dimensions:                                             │
│  - Total W = 10 μm (7 fingers × 1.43 μm each)          │
│  - L = 0.18 μm (minimum)                                │
│  - Finger pitch: 0.5 μm                                 │
│  - Total area: 4.2 μm × 2.1 μm = 8.8 μm²              │
│  - Diffusion area: 6.0 μm² (for capacitance)            │
└─────────────────────────────────────────────────────────┘

Layout Benefits:
- Multi-finger reduces gate resistance
- Shared diffusion reduces area
- Symmetric layout for uniform current density
- Guard rings for latch-up prevention
```

### 3.3 Guard Ring Implementation

```
Power Switch Guard Ring Design:

┌─────────────────────────────────────────────────────────┐
│                    Guard Ring Structure                  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ N+ Guard Ring (connected to V_DD)                │   │
│  │                                                 │   │
│  │  ┌─────────────────────────────────────────┐    │   │
│  │  │ P+ Guard Ring (connected to GND)         │    │   │
│  │  │                                         │    │   │
│  │  │  ┌─────────────────────────────────┐    │    │   │
│  │  │  │                                 │    │    │   │
│  │  │  │     PMOS Power Switch           │    │    │   │
│  │  │  │     (active region)             │    │    │   │
│  │  │  │                                 │    │    │   │
│  │  │  └─────────────────────────────────┘    │    │   │
│  │  │                                         │    │   │
│  │  └─────────────────────────────────────────┘    │   │
│  │                                                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Guard Ring Specifications:                             │
│  - N+ ring width: 0.36 μm (2× minimum)                 │
│  - P+ ring width: 0.36 μm (2× minimum)                 │
│  - Contact spacing: 0.5 μm                             │
│  - Number of contacts per side: 5                      │
│  - Latch-up immunity: > 100 mA                         │
└─────────────────────────────────────────────────────────┘

Purpose:
- Prevents latch-up between power switch and substrate
- Provides low-impedance path for substrate current
- Required for medical device reliability
```

## 4. Switch Sizing

### 4.1 On-Resistance Sizing

```
Power Switch Sizing Methodology:

Step 1: Determine Maximum Current
- Active mode current: I_active = 10 μA
- Stimulation pulse current: I_stim = 50 μA
- Transient current: I_transient = 100 μA (startup)

Step 2: Calculate Maximum Allowable IR Drop
- Acceptable droop: < 5% of V_DD = 90 mV
- R_on,max = V_drop / I_max = 90 mV / 100 μA = 900 Ω

Step 3: Calculate Minimum Transistor Width
- R_on ∝ 1/W (inversely proportional to width)
- R_on = R_on,unit × (L/W) where R_on,unit ≈ 10 kΩ·μm
- For R_on = 900 Ω: W = 10 kΩ·μm / 900 Ω = 11.1 μm

Step 4: Apply Process Margin
- Account for process variation (±30%)
- W_margin = 11.1 μm × 1.3 = 14.4 μm
- Round to practical value: W = 15 μm

Step 5: Verify Leakage
- I_leak ∝ W (proportional to width)
- I_leak at W = 15 μm: 75 pA (acceptable)
```

### 4.2 Leakage Sizing

```
Leakage-Conscious Sizing:

Trade-off: Larger W reduces R_on but increases I_leak

┌──────────┬──────────┬──────────┬──────────────────┐
│ W (μm)   │ R_on (Ω) │ I_leak   │ Application      │
├──────────┼──────────┼──────────┼──────────────────┤
│ 2        │ 450      │ 10 pA    │ Low-power domain │
│ 5        │ 180      │ 25 pA    │ Medium power     │
│ 10       │ 90       │ 50 pA    │ High-power domain│
│ 15       │ 60       │ 75 pA    │ iPACE-CHIP       │
│ 20       │ 45       │ 100 pA   │ Ultra-fast wake-up│
│ 50       │ 18       │ 250 pA   │ Not recommended  │
└──────────┴──────────┴──────────┴──────────────────┘

iPACE-CHIP Selection: W = 15 μm
- R_on = 60 Ω (provides 6× margin over requirement)
- I_leak = 75 pA (within 100 pA budget)
- Area = 32 μm² (acceptable overhead)
```

### 4.3 Multi-Stage Sizing for Deep Shutdown

```
Multi-Stage Power Switch Sizing:

For deep shutdown modes, cascaded switches reduce leakage:

Stage 1: Main Switch (W = 15 μm)
- R_on = 60 Ω
- I_leak = 75 pA
- Purpose: Normal power gating

Stage 2: Deep Sleep Switch (W = 5 μm)
- R_on = 180 Ω
- I_leak = 25 pA
- Purpose: Ultra-low leakage

Combined (series):
- R_on,total = 60 + 180 = 240 Ω
- I_leak,total = 75 × 25 / (75 + 25) = 18.75 pA (parallel)
  Actually for series: I_leak ≈ min(I_leak1, I_leak2) ≈ 25 pA

Area Overhead:
- Stage 1: 32 μm²
- Stage 2: 10.7 μm²
- Total: 42.7 μm² (2× single switch)

Benefit:
- Leakage: 25 pA vs. 75 pA (3× reduction)
- Justified for always-off blocks
```

## 5. Power Switch Array Design

### 5.1 Array Architecture

```
Power Switch Array for iPACE-CHIP:

┌─────────────────────────────────────────────────────────┐
│                    Power Switch Array                    │
│                                                         │
│  V_DD ────────────────────────────────────────────────  │
│  │     │     │     │     │     │     │     │     │     │
│  ┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐    │
│  │ S1  ││ S2  ││ S3  ││ S4  ││ S5  ││ S6  ││ S7  │    │
│  └──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘└──┬──┘    │
│     │      │      │      │      │      │      │        │
│  ┌──┴──────┴──────┴──────┴──────┴──────┴──────┴──┐      │
│  │              V_DD_switched                    │      │
│  │              (Power Rail)                     │      │
│  └───────────────────────────────────────────────┘      │
│                                                         │
│  Control: PWR_EN_n ──┐                                  │
│                      │                                  │
│              ┌───────┴───────┐                          │
│              │  Delay Chain  │                          │
│              │  (100 ns)     │                          │
│              └───────┬───────┘                          │
│                      │                                  │
│         ┌────────────┼────────────┐                     │
│         │            │            │                     │
│    ┌────┴────┐  ┌────┴────┐  ┌────┴────┐               │
│    │ Buffer  │  │ Buffer  │  │ Buffer  │               │
│    │ (S1-S2) │  │ (S3-S5) │  │ (S6-S7) │               │
│    └─────────┘  └─────────┘  └─────────┘               │
│                                                         │
│  Array Parameters:                                      │
│  - Number of switches: 7                                │
│  - Total W: 7 × 15 μm = 105 μm                         │
│  - Total R_on: 60 Ω / 7 = 8.6 Ω                       │
│  - Total I_leak: 7 × 75 pA = 525 pA                    │
│  - Total area: 7 × 32 μm² = 224 μm²                    │
└─────────────────────────────────────────────────────────┘
```

### 5.2 Switch Distribution

```
Power Switch Distribution Across Floorplan:

iPACE-CHIP Floorplan:

┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │  Sensing    │  │    DSP      │  │ Stimulation │     │
│  │  Domain     │  │  Domain     │  │  Domain     │     │
│  │             │  │             │  │             │     │
│  │  3 switches │  │  12 switches│  │  4 switches │     │
│  │  (45 μm)    │  │  (180 μm)   │  │  (60 μm)    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │    Comm     │  │ Housekeep   │  │   Always    │     │
│  │  Domain     │  │  Domain     │  │   On        │     │
│  │             │  │             │  │  Domain     │     │
│  │  2 switches │  │  3 switches │  │  (no gates) │     │
│  │  (30 μm)    │  │  (45 μm)    │  │             │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
│                                                         │
│  Switch Distribution Summary:                           │
│  - Total switches: 24                                   │
│  - Total W: 360 μm                                      │
│  - Total area: 768 μm² (1.5% of die area)              │
│  - Total R_on: 2.5 Ω (array)                           │
│  - Total I_leak: 1.8 nA (all switches off)              │
└─────────────────────────────────────────────────────────┘
```

### 5.3 IR Drop Analysis

```
IR Drop Analysis for Power Switch Array:

Worst-Case Scenario:
- All switches ON simultaneously (startup)
- Maximum current: 100 μA per domain

IR Drop Calculation:
V_drop = I × R_on

Per Domain:
┌─────────────────┬──────────┬──────────┬──────────┐
│ Domain          │ I_max    │ R_on     │ V_drop   │
├─────────────────┼──────────┼──────────┼──────────┤
│ Sensing         │ 20 μA    │ 20 Ω     │ 0.4 mV   │
│ DSP             │ 50 μA    │ 5 Ω      │ 0.25 mV  │
│ Stimulation     │ 100 μA   │ 15 Ω     │ 1.5 mV   │
│ Communication   │ 50 μA    │ 25 Ω     │ 1.25 mV  │
│ Housekeeping    │ 10 μA    │ 20 Ω     │ 0.2 mV   │
├─────────────────┼──────────┼──────────┼──────────┤
│ TOTAL (worst)   │ 230 μA   │ -        │ 1.5 mV   │
└─────────────────┴──────────┴──────────┴──────────┘

Maximum IR Drop: 1.5 mV (0.08% of 1.8V V_DD)
Specification: < 90 mV (5% of V_DD)
Status: WELL WITHIN SPECIFICATION

Note: IR drop is negligible because:
1. Switches are oversized for current requirements
2. Multiple switches in parallel reduce resistance
3. Decoupling capacitors provide transient current
```

## 6. Control Circuitry

### 6.1 Power Switch Controller

```
Power Switch Controller Design:

┌─────────────────────────────────────────────────────────┐
│              Power Switch Controller                     │
│                                                         │
│  Inputs:                                                │
│  - PWR_EN_n (active-low enable)                        │
│  - CLK (timing reference)                              │
│  - RST_n (reset)                                       │
│  - STATUS (power domain ready)                         │
│                                                         │
│  Outputs:                                               │
│  - SW_EN[6:0] (individual switch enables)              │
│  - POWER_GOOD (domain voltage OK)                      │
│  - WAKEUP_ACK (wake-up complete)                       │
│                                                         │
│  State Machine:                                         │
│  ┌──────────┐                                           │
│  │  OFF     │◄──────────── PWR_EN_n = 0                │
│  │  (all    │                                           │
│  │  switches│──── PWR_EN_n = 1 ──►┌──────────┐        │
│  │  off)    │                      │ RAMP_UP  │        │
│  └──────────┘                      │ (stagger │        │
│       ▲                            │  switch  │        │
│       │                            │  on)     │        │
│       │                            └────┬─────┘        │
│       │                                 │              │
│       │         ┌──────────┐            │              │
│       │         │  ON      │◄───────────┘              │
│       └─────────│  (all    │    STATUS = 1             │
│   PWR_EN_n = 0  │  switches│                           │
│                  │  on)     │                           │
│                  └──────────┘                           │
│                                                         │
│  Switch-On Sequence (Staggered):                       │
│  T0:      SW_EN[0] = 1 (first switch)                  │
│  T0+20ns: SW_EN[1] = 1                                 │
│  T0+40ns: SW_EN[2] = 1                                 │
│  ...                                                    │
│  T0+120ns: SW_EN[6] = 1 (last switch)                  │
│  T0+200ns: POWER_GOOD = 1                              │
└─────────────────────────────────────────────────────────┘
```

### 6.2 Inrush Current Limiting

```
Inrush Current Control:

Problem: When power switch turns on, large current flows
to charge load capacitance. This can cause:
1. Voltage droop on main V_DD rail
2. Electromagnetic interference
3. Latch-up risk

Solution: Staggered Turn-On

Current Profile Without Staggering:
I (μA)
100 ┤      ╱╲
    │     ╱  ╲
 50 ┤    ╱    ╲
    │   ╱      ╲
  0 ┤──╱────────╲──────────────
    └──┴─────────┴──────────── t
       0        200ns

Current Profile With Staggering:
I (μA)
 20 ┤   ┌──┐
    │  ┌┘  └┐┌──┐
 15 ┤┌─┘    └┘  └┐┌──┐
    ││           └┘  └┐┌──┐
 10 ┤│                └┘  └┐
    ││                     └──────────
  0 ┤┴────────────────────────────────
    └──┴─────────┴──────────── t
       0        200ns

Staggering Parameters:
- Delay between switches: 20 ns
- Total turn-on time: 140 ns (7 switches × 20 ns)
- Peak current per switch: 14 μA
- Total peak current: 14 μA (vs. 100 μA without staggering)
- Inrush reduction: 86%
```

### 6.3 Soft-Start Circuit

```
Power Switch Soft-Start Implementation:

┌─────────────────────────────────────────────────────────┐
│                Soft-Start Circuit                        │
│                                                         │
│  PWR_EN_n ─────┐                                       │
│                │                                        │
│          ┌─────▼─────┐                                  │
│          │  Current  │                                  │
│          │  Limiter  │                                  │
│          └─────┬─────┘                                  │
│                │                                        │
│          ┌─────▼─────┐                                  │
│          │  Ramp      │                                  │
│          │  Generator │                                  │
│          │  (100 ns)  │                                  │
│          └─────┬─────┘                                  │
│                │                                        │
│          ┌─────▼─────┐                                  │
│          │  Switch   │                                  │
│          │  Driver   │                                  │
│          └─────┬─────┘                                  │
│                │                                        │
│          ┌─────▼─────┐                                  │
│          │  Power    │                                  │
│          │  Switch   │──► V_DD_switched                 │
│          └───────────┘                                  │
│                                                         │
│  Operation:                                             │
│  1. PWR_EN_n goes low (enable)                         │
│  2. Current limiter restricts initial current           │
│  3. Ramp generator gradually increases gate drive       │
│  4. V_DD_switched ramps from 0V to V_DD in 100 ns      │
│  5. Full current capability after ramp complete         │
└─────────────────────────────────────────────────────────┘

Soft-Start Parameters:
- Ramp time: 100 ns
- Initial current limit: 10 μA
- Final current capability: 100 μA
- V_DD_switched rise time: 100 ns (0V to 1.8V)
- Slew rate: 18 V/μs
```

## 7. Reliability Considerations

### 7.1 Power Cycling Stress

```
Power Switch Reliability Analysis:

Power Cycling Budget:
- Cycles per heartbeat: 1 (one power-on per detection)
- Heartbeats per minute: 75 (normal sinus rhythm)
- Cycles per day: 108,000
- Cycles per year: 39.4 million
- Cycles per 10 years: 394 million

Reliability Assessment:
- 180nm process: >10⁹ power cycles typical
- iPACE-CHIP requirement: 394 × 10⁶ cycles
- Safety factor: 2.54× (adequate for medical device)

Failure Mechanisms:
1. Gate oxide breakdown (TDDB)
   - Mitigation: Use thick oxide option for switches
   - Voltage stress: V_GS = V_DD = 1.8V (below 3.3V rated)

2. Hot carrier injection (HCI)
   - Mitigation: Operate below maximum V_DS during switching
   - Current density: < 1 mA/μm (within limits)

3. Electromigration
   - Mitigation: Width > 1 μm per finger
   - Current density: < 10 μA/μm (within limits)

4. NBTI (for PMOS)
   - Mitigation: Intermittent stress (switching off)
   - V_th shift: < 20 mV over lifetime
```

### 7.2 Redundancy for Safety

```
Redundant Power Switch Configuration:

For safety-critical domains (stimulation), redundant
power switches ensure reliability:

┌─────────────────────────────────────────────────────────┐
│           Redundant Power Switch Configuration           │
│                                                         │
│  V_DD ──────────────┬─────────────────┐                 │
│                     │                 │                 │
│              ┌──────┴──────┐   ┌──────┴──────┐         │
│              │  Primary    │   │  Redundant  │         │
│              │  Switch     │   │  Switch     │         │
│              │  (W=15μm)   │   │  (W=10μm)   │         │
│              └──────┬──────┘   └──────┬──────┘         │
│                     │                 │                 │
│                     └────────┬────────┘                 │
│                              │                          │
│                    V_DD_switched                        │
│                              │                          │
│                    ┌─────────┴─────────┐                │
│                    │  Stimulation      │                │
│                    │  Domain           │                │
│                    └───────────────────┘                │
│                                                         │
│  Control Logic:                                         │
│  - Primary switch: Controlled by normal PWR_EN         │
│  - Redundant switch: Controlled by independent PWR_EN  │
│  - Both must be OFF for domain to power down           │
│  - Either can power domain (OR function)               │
│                                                         │
│  Safety Analysis:                                       │
│  - Primary switch failure: Redundant switch maintains  │
│  - Redundant switch failure: Primary switch maintains  │
│  - Both fail OFF: Device enters safe state             │
│  - Probability of simultaneous failure: 10⁻¹²/year    │
└─────────────────────────────────────────────────────────┘
```

### 7.3 Aging Effects on Switches

```
Power Switch Aging Analysis:

Over 10-year lifetime:

1. NBTI (Negative Bias Temperature Instability):
   - Affects PMOS header when switch is OFF
   - V_th increase: 20-50 mV
   - Impact: Slightly higher R_on when turned ON
   - R_on increase: 5-10%
   - Still within specification

2. HCI (Hot Carrier Injection):
   - Occurs during switching transitions
   - Degrades transistor over time
   - Mitigation: Limited switching frequency
   - iPACE-CHIP: < 100,000 cycles/year (conservative)

3. GOI (Gate Oxide Integrity):
   - Time-dependent dielectric breakdown
   - 180nm process: MTTF > 100 years at 1.8V
   - Not a concern for iPACE-CHIP

4. TDDB (Time-Dependent Dielectric Breakdown):
   - Occurs under voltage stress
   - 180nm at 1.8V: Well below acceleration factor
   - Not a concern for iPACE-CHIP

Overall Aging Impact:
- R_on increase: 10% over 10 years
- I_leak change: < 20% (process dependent)
- No impact on switch functionality
```

## 8. Summary

Power switch design for the iPACE-CHIP pacemaker ASIC employs PMOS header switches with 15 μm total width, achieving 60 Ω on-resistance and 75 pA off-state leakage per switch. The array of 24 switches across 5 power domains provides comprehensive power gating capability with only 1.5% area overhead. Staggered turn-on with 20 ns delay between switches limits inrush current to 14 μA peak, preventing voltage droop on the main supply rail. Redundant switches in the stimulation domain ensure safety-critical reliability. Power cycling analysis confirms 2.54× safety margin for the 394 million cycles expected over the 10-year device lifetime. The combination of careful transistor sizing, array architecture, and control circuitry enables effective power gating while meeting the stringent reliability requirements of an implantable medical device.

## References

1. Keating, M., et al., "Low Power Design Methodology," Springer, 2002.
2. iPACE-CHIP Project Internal Documentation: Power Switch Design Specification, Rev 1.8.
3. TSMC 0.18μm Mixed-Signal Process Design Manual: Power Switch Characterization.
4. Kim, S., et al., "Power Gating Techniques for Medical ASICs," IEEE CICC, 2018.
5. JEDEC Standard JESD78: IC Latch-Up Test for Medical Electronics.
