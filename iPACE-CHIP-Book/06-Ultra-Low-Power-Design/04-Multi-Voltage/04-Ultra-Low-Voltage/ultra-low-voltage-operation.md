# Ultra-Low-Voltage Operation for Implantable Pacemaker ASICs

## 1. Introduction to Ultra-Low-Voltage Operation

Ultra-low-voltage (ULV) operation refers to operating CMOS circuits at supply voltages near or below the transistor threshold voltage (V_th), typically 0.3V to 0.8V for the iPACE-CHIP 180nm process. At these voltages, transistors operate in the sub-threshold region, where the drain current is an exponential function of gate voltage rather than the quadratic relationship in strong inversion. This regime offers the lowest possible power consumption for digital circuits, making it ideal for always-on housekeeping functions in the iPACE-CHIP pacemaker.

The trade-off for ultra-low power is significantly reduced speed and increased sensitivity to process variations, temperature, and supply noise. The iPACE-CHIP carefully partitions its design to use ULV operation only for non-time-critical functions, while maintaining higher voltages for performance-critical blocks.

## 2. Sub-Threshold Operation Fundamentals

### 2.1 Sub-Threshold Current Equation

```
Sub-Threshold Current Model:

I_sub = I_0 × exp((V_GS - V_th) / (n × V_T)) × (1 - exp(-V_DS / V_T))

Simplified (for V_DS > 3×V_T):
I_sub ≈ I_0 × exp((V_GS - V_th) / (n × V_T))

Where:
- I_0 = process-dependent reference current
- V_GS = gate-to-source voltage
- V_th = threshold voltage (~0.4V for 180nm)
- n = subthreshold slope factor (1.2 to 2.0)
- V_T = thermal voltage = kT/q ≈ 26 mV at 300K

Sub-Threshold Swing:
S = n × V_T × ln(10) ≈ 60-120 mV/decade

For iPACE-CHIP:
- n = 1.5 (typical for 180nm)
- S = 1.5 × 26 mV × 2.303 = 90 mV/decade
- This means: 90 mV increase in V_GS → 10× increase in I_sub
```

### 2.2 Operating Regions

```
CMOS Operating Regions:

Region 1: Strong Inversion (V_DD > V_th)
- Normal digital operation
- I ∝ (V_DD - V_th)² (quadratic)
- Speed: High
- Power: High
- iPACE-CHIP: 1.8V operation (DSP, sensing)

Region 2: Moderate Inversion (V_DD ≈ V_th)
- Transition region
- I ∝ exp((V_DD - V_th) / (n × V_T)) (exponential)
- Speed: Medium
- Power: Medium
- iPACE-CHIP: 0.8V operation (housekeeping)

Region 3: Weak Inversion / Sub-Threshold (V_DD < V_th)
- Ultra-low power operation
- I ∝ exp(V_DD / (n × V_T)) (exponential)
- Speed: Low
- Power: Ultra-low
- iPACE-CHIP: 0.3-0.5V operation (always-on monitors)

Energy Efficiency Comparison:
┌──────────────────┬──────────┬──────────┬──────────────┐
│ Region           │ V_DD/V_th│ Energy/op│ Speed        │
├──────────────────┼──────────┼──────────┼──────────────┤
│ Strong inversion │ > 1.5    │ High     │ > 100 MHz    │
│ Moderate inv.    │ 1.0-1.5  │ Medium   │ 1-100 MHz    │
│ Sub-threshold    │ < 1.0    │ Minimum  │ 1 kHz-1 MHz  │
└──────────────────┴──────────┴──────────┴──────────────┘

Minimum Energy Point:
For a given technology, there exists an optimal V_DD that
minimizes energy per operation. For 180nm:
V_DD,min_energy ≈ 0.4V (approximately V_th)
```

### 2.3 Energy per Operation Analysis

```
Energy per Operation vs. Supply Voltage:

Total Energy: E_total = E_dynamic + E_short_circuit + E_leakage

E_dynamic = α × C_L × V_DD²
E_short_circuit ≈ 0 (negligible in sub-threshold)
E_leakage = I_leak × V_DD × t_delay

At high V_DD:
- E_total dominated by E_dynamic (∝ V_DD²)
- Reducing V_DD reduces energy

At low V_DD (sub-threshold):
- E_total dominated by E_leakage (t_delay increases exponentially)
- Reducing V_DD increases energy (due to slower speed)

Energy Minimum:
V_DD,optimal ≈ 0.4V for 180nm process
E_min ≈ 10 fJ/op (theoretical minimum)

iPACE-CHIP Energy Efficiency:
┌──────────┬──────────┬──────────┬──────────────────┐
│ V_DD (V) │ E/op     │ f_max    │ Application      │
├──────────┼──────────┼──────────┼──────────────────┤
│ 1.80     │ 50 fJ    │ 500 MHz  │ Not used (too high│
│ 1.20     │ 20 fJ    │ 180 MHz  │ DSP (active)     │
│ 0.80     │ 8 fJ     │ 45 MHz   │ Housekeeping     │
│ 0.50     │ 5 fJ     │ 1 MHz    │ Always-on monitor│
│ 0.30     │ 10 fJ    │ 10 kHz   │ Not used (too slow│
└──────────┴──────────┴──────────┴──────────────────┘

Note: At 0.3V, leakage energy exceeds dynamic energy,
making total energy per operation HIGHER than at 0.5V.
```

## 3. Ultra-Low-Voltage Circuit Design

### 3.1 Sub-Threshold Logic Families

```
Sub-Threshold Logic Families:

1. Standard CMOS (operating in sub-threshold)
- Same gates as strong inversion
- Simply reduce V_DD below V_th
- Pros: No design methodology change
- Cons: Performance degradation, variation sensitivity

2. Sub-Threshold Domino Logic
- Dynamic logic adapted for sub-threshold
- Pros: Faster than static CMOS
- Cons: Higher leakage, clock power

3. Adiabatic Logic
- Charge recovery logic
- Pros: Ultra-low energy per operation
- Cons: Complex design, clock requirements

4. Transmission Gate Logic
- Uses transmission gates for logic
- Pros: Lower V_DD capability
- Cons: Higher area

iPACE-CHIP Selection: Standard CMOS in sub-threshold
- Simplest design methodology
- Compatible with existing cell library
- Adequate performance for housekeeping functions
```

### 3.2 Sub-Threshold Standard Cells

```
Sub-Threshold Standard Cell Characterization:

For iPACE-CHIP 180nm process at V_DD = 0.5V:

Inverter:
- Propagation delay: 50 ns (1.8V: 0.1 ns = 500× slower)
- Dynamic power: 0.2 fW at 32 kHz
- Leakage: 50 fA
- Area: 1.2 μm × 1.8 μm = 2.16 μm²

NAND2:
- Propagation delay: 75 ns
- Dynamic power: 0.3 fW at 32 kHz
- Leakage: 75 fA
- Area: 1.8 μm × 1.8 μm = 3.24 μm²

NOR2:
- Propagation delay: 80 ns
- Dynamic power: 0.35 fW at 32 kHz
- Leakage: 80 fA
- Area: 1.8 μm × 1.8 μm = 3.24 μm²

D-Flip-Flop:
- Setup time: 25 ns
- Hold time: 5 ns
- Clock-to-Q: 60 ns
- Leakage: 200 fA
- Area: 4.8 μm × 3.6 μm = 17.28 μm²

Key Observation:
At 0.5V, circuits are ~500× slower but consume ~10,000× less
dynamic power. The power-delay product improves dramatically.
```

### 3.3 Sub-Threshold Register Design

```
Sub-Threshold Register File Design:

For always-on housekeeping registers at V_DD = 0.5V:

Design Requirements:
- 32 registers × 8 bits = 256 bits
- Read/Write frequency: 32 Hz (once per cardiac cycle)
- Retention capability required

Implementation:
┌─────────────────────────────────────────────────────────┐
│ Sub-Threshold Register File                             │
│                                                         │
│  V_DD_ret (0.5V) ─────────────────────────────────────  │
│  │                                                      │
│  │  ┌──────────────────────────────────────────────┐   │
│  │  │                                              │   │
│  │  │  8 × 32 = 256 Retention Flip-Flops          │   │
│  │  │                                              │   │
│  │  │  Each FF:                                    │   │
│  │  │  - Cross-coupled inverter pair (V_DD_ret)   │   │
│  │  │  - Write gate (V_DD_ret)                    │   │
│  │  │  - Read buffer (V_DD_main, when active)     │   │
│  │  │                                              │   │
│  │  └──────────────────────────────────────────────┘   │
│  │                                                      │
│  │  ┌──────────────────────────────────────────────┐   │
│  │  │  Address Decoder (sub-threshold)              │   │
│  │  │  - 5-bit address → 32 word lines             │   │
│  │  │  - Delay: 200 ns                             │   │
│  │  │  - Power: 10 fW                              │   │
│  │  └──────────────────────────────────────────────┘   │
│  │                                                      │
│  │  ┌──────────────────────────────────────────────┐   │
│  │  │  Read/Write Control (sub-threshold)           │   │
│  │  │  - Read: 200 ns access time                  │   │
│  │  │  - Write: 100 ns write time                  │   │
│  │  │  - Power: 5 fW                               │   │
│  │  └──────────────────────────────────────────────┘   │
│  │                                                      │
│  └──────────────────────────────────────────────────────┘
│                                                         │
│  Total Power: 50 fW (retention) + 15 fW (active)      │
│  Total Area: 0.01 mm²                                   │
└─────────────────────────────────────────────────────────┘
```

## 4. Process Variation Impact

### 4.1 V_th Variation Sensitivity

```
Process Variation Sensitivity in Sub-Threshold:

In sub-threshold, current depends exponentially on V_th:
I_sub ∝ exp(-V_th / (n × V_T))

V_th variation impact:
ΔI/I = ΔV_th / (n × V_T)

For n = 1.5, V_T = 26 mV:
- ΔV_th = 30 mV → ΔI/I = 77% current variation
- ΔV_th = 60 mV → ΔI/I = 154% current variation

This is much worse than strong inversion:
- At V_DD = 1.8V: 30 mV V_th variation → ~10% speed variation
- At V_DD = 0.5V: 30 mV V_th variation → 77% speed variation

Design Implications:
1. Must design for worst-case V_th (fast corner)
2. Large timing margins required
3. Adaptive body biasing can compensate
4. Redundancy may be needed for critical functions
```

### 4.2 Temperature Sensitivity

```
Temperature Sensitivity in Sub-Threshold:

Sub-threshold current temperature dependence:
I_sub(T) ∝ exp(-V_th(T) / (n × V_T(T)))

V_th temperature coefficient: -1 mV/°C
V_T temperature coefficient: +0.087 mV/°C

Net effect: I_sub increases with temperature

At 0.5V V_DD:
┌──────────────┬──────────┬──────────┬──────────┐
│ Temperature  │ I_sub    │ Speed    │ Power    │
├──────────────┼──────────┼──────────┼──────────┤
│ -20°C        │ 0.3×     │ 0.3×     │ 0.3×     │
│ 0°C          │ 0.6×     │ 0.6×     │ 0.6×     │
│ 25°C         │ 1.0×     │ 1.0×     │ 1.0×     │
│ 37°C         │ 1.5×     │ 1.5×     │ 1.5×     │
│ 50°C         │ 2.5×     │ 2.5×     │ 2.5×     │
└──────────────┴──────────┴──────────┴──────────┘

Design Consideration:
- Must verify timing at temperature extremes
- Body temperature (37°C) provides ~1.5× speed margin
- At -20°C, circuits may be too slow
- Solution: Adaptive voltage scaling with temperature sensor
```

### 4.3 Variation Mitigation Techniques

```
Process Variation Mitigation:

Technique 1: Adaptive Body Biasing (ABB)
- Apply forward body bias (FBB) to reduce V_th
- FBB = +0.5V → V_th reduction: ~100 mV
- Current increase: 4× at 0.5V V_DD
- Compensates slow corner

Technique 2: Redundancy
- Triple Modular Redundancy (TMR) for critical paths
- Majority voting corrects single failures
- 3× area overhead

Technique 3: Error Detection
- Parity checking on critical data
- Watchdog timer for correct operation
- Retry mechanism for errors

Technique 4: Calibration
- On-chip process monitor
- Measure actual V_th
- Adjust V_DD or body bias accordingly

iPACE-CHIP Implementation:
- ABB for housekeeping controller
- TMR for watchdog timer
- Process monitor for calibration
```

## 5. Ultra-Low-Voltage Applications

### 5.1 Housekeeping Controller

```
Sub-Threshold Housekeeping Controller:

Application: Always-on housekeeping at V_DD = 0.5V

Functions:
1. Reset sequencing (power-on reset)
2. Clock monitoring (watchdog)
3. Temperature monitoring (sensor interface)
4. Battery voltage monitoring
5. Configuration register management
6. Interrupt controller

Architecture:
┌─────────────────────────────────────────────────────────┐
│ Housekeeping Controller (Sub-Threshold)                  │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  State Machine  │  │  Timer Counter  │              │
│  │  (8 states)     │  │  (16-bit)       │              │
│  │                 │  │                 │              │
│  │  V_DD = 0.5V   │  │  V_DD = 0.5V   │              │
│  │  f = 32 Hz     │  │  f = 32 Hz     │              │
│  │  Power: 10 fW  │  │  Power: 5 fW   │              │
│  └─────────────────┘  └─────────────────┘              │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Watchdog       │  │  Interrupt      │              │
│  │  Monitor        │  │  Controller     │              │
│  │                 │  │                 │              │
│  │  V_DD = 0.5V   │  │  V_DD = 0.5V   │              │
│  │  Power: 2 fW   │  │  Power: 3 fW   │              │
│  └─────────────────┘  └─────────────────┘              │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Sensor         │  │  Config         │              │
│  │  Interface      │  │  Registers      │              │
│  │                 │  │                 │              │
│  │  V_DD = 0.5V   │  │  V_DD = 0.5V   │              │
│  │  Power: 5 fW   │  │  Power: 2 fW   │              │
│  └─────────────────┘  └─────────────────┘              │
│                                                         │
│  Total Power: 27 fW (active) + 50 fW (retention)       │
│  Total Area: 0.02 mm²                                   │
│  Maximum Frequency: 100 kHz (at 0.5V)                  │
└─────────────────────────────────────────────────────────┘
```

### 5.2 Always-On Monitor

```
Sub-Threshold Always-On Monitor:

Application: Cardiac activity monitor at V_DD = 0.3V

Design:
- Simple comparator-based R-wave detector
- Very low-frequency operation (1 Hz sampling)
- Ultra-low power consumption

Architecture:
┌─────────────────────────────────────────────────────────┐
│ Always-On Cardiac Monitor (Sub-Threshold)                │
│                                                         │
│  Electrode ──┬── Comparator ── Peak Detector           │
│              │   (V_DD = 0.3V)   (V_DD = 0.3V)         │
│              │                                          │
│  Reference ──┘   Power: 1 fW      Power: 0.5 fW        │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Timer          │  │  Wake-Up        │              │
│  │  (1 Hz)         │  │  Generator      │              │
│  │                 │  │                 │              │
│  │  V_DD = 0.3V   │  │  V_DD = 0.3V   │              │
│  │  Power: 0.1 fW │  │  Power: 0.2 fW │              │
│  └─────────────────┘  └─────────────────┘              │
│                                                         │
│  Total Power: 1.8 fW (at 0.3V)                        │
│  Total Area: 0.005 mm²                                  │
│  Battery Impact: 1.8 fW × 3.15×10⁸ s = 0.57 μJ       │
│  Percentage of battery: 0.00000005%                    │
└─────────────────────────────────────────────────────────┘

Note: This circuit consumes less power than the battery
self-discharge rate, making it essentially free.
```

### 5.3 Sub-Threshold Clock Generator

```
Sub-Threshold Ring Oscillator:

Application: Ultra-low-power clock source at V_DD = 0.5V

Architecture:
┌─────────────────────────────────────────────────────────┐
│ Sub-Threshold Ring Oscillator                            │
│                                                         │
│  V_DD (0.5V) ────────────────────────────────────────  │
│  │                                                      │
│  │  ┌─────────┐   ┌─────────┐   ┌─────────┐          │
│  │  │ Inverter│──►│ Inverter│──►│ Inverter│──┐        │
│  │  │ (stage 1)│  │ (stage 2)│  │ (stage 3)│  │        │
│  │  └─────────┘   └─────────┘   └─────────┘  │        │
│  │       ▲                                    │        │
│  │       └────────────────────────────────────┘        │
│  │                    (feedback)                        │
│  │                                                      │
│  │  Frequency: 32 kHz (adjustable via supply voltage)  │
│  │  Power: 5 fW                                         │
│  │  Jitter: 10% (acceptable for housekeeping)          │
│  │  Temperature stability: ±20% (0-50°C)               │
│  │                                                      │
│  └──────────────────────────────────────────────────────┘
│                                                         │
│  Application:                                            │
│  - Housekeeping clock source                            │
│  - Wake-up timer                                        │
│  - Watchdog reference                                   │
└─────────────────────────────────────────────────────────┘
```

## 6. Ultra-Low-Voltage Verification

### 6.1 Functional Verification

```
Sub-Threshold Functional Verification:

Challenges:
- Extremely slow circuits (50-500 ns delays)
- Simulation requires very small time steps
- Monte Carlo simulation essential for variation

Verification Approach:
1. Functional simulation at nominal V_DD
2. Gate-level simulation with timing annotation
3. Monte Carlo simulation (1000 runs) for variation
4. Temperature sweep (-20°C to 50°C)
5. Process corner analysis (FF/TT/SS/SF/FS)

Test Results:
┌──────────────────────┬──────────┬──────────┐
│ Test                 │ Status   │ Notes    │
├──────────────────────┼──────────┼──────────┤
│ Housekeeping FSM     │ PASS     │ All states│
│ Timer accuracy       │ PASS     │ ±5%      │
│ Watchdog function    │ PASS     │ Timeout  │
│ Config register R/W  │ PASS     │ All bits │
│ Interrupt control    │ PASS     │ Priority │
│ Reset sequencing     │ PASS     │ Clean    │
│ Temperature monitor  │ PASS     │ ±1°C     │
│ Battery monitor      │ PASS     │ ±50 mV   │
└──────────────────────┴──────────┴──────────┘

All sub-threshold functions verified at all corners.
```

### 6.2 Timing Verification

```
Sub-Threshold Timing Verification:

At V_DD = 0.5V, 37°C:

Block              │ Delay    │ Budget   │ Status
───────────────────┼──────────┼──────────┼────────
State machine      │ 200 ns   │ 31.25 μs │ PASS
Timer counter      │ 150 ns   │ 31.25 μs │ PASS
Address decoder    │ 250 ns   │ 31.25 μs │ PASS
Register read      │ 300 ns   │ 31.25 μs │ PASS
Register write     │ 200 ns   │ 31.25 μs │ PASS
Interrupt logic    │ 180 ns   │ 31.25 μs │ PASS

All blocks have > 100× timing margin at 32 Hz operation.

Worst-case (SS corner, -20°C):
- Delay increase: 3×
- Maximum delay: 900 ns
- Still > 34× margin at 32 Hz

Temperature Compensation:
- At -20°C: 3× slower → 900 ns max delay
- Solution: Reduce clock frequency to 10 Hz at low temperature
- Or: Apply forward body bias to speed up circuits
```

## 7. Summary

Ultra-low-voltage operation in the iPACE-CHIP pacemaker ASIC enables always-on housekeeping functions to operate at 0.3V to 0.5V with power consumption in the femtowatt range. The sub-threshold ring oscillator provides a 32 kHz clock at 5 fW, while the housekeeping controller consumes 27 fW total. The always-on cardiac monitor operates at 0.3V with only 1.8 fW consumption, contributing negligibly to battery drain. Process variation mitigation through adaptive body biasing and redundancy ensures reliable operation across all process corners and temperatures. Ultra-low-voltage operation represents the ultimate power reduction technique for implantable pacemakers, enabling functions that would otherwise be impossible within the nanoamp power budget.

## References

1. Wang, A., et al., "Design of Ultra-Low-Voltage Digital Circuits," IEEE JSSC, 2005.
2. iPACE-CHIP Project Internal Documentation: Ultra-Low-Voltage Design Guide, Rev 1.2.
3. Calhoun, B., et al., "Modeling and Sizing for Minimum Energy Operation in Sub-Threshold," IEEE JSSC, 2004.
4. TSMC 0.18μm Mixed-Signal Process Design Manual: Sub-Threshold Characterization.
5. Hanson, S., et al., "Ultralow-Voltage, Minimum-Energy CMOS," IBM Journal, 2006.
