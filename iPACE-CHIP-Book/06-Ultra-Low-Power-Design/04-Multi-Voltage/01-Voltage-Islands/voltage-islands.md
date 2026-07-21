# Voltage Islands for Implantable Pacemaker ASICs

## 1. Introduction to Voltage Islands

Voltage islands are physically contiguous regions of an integrated circuit that operate at a common supply voltage, distinct from neighboring regions. For the iPACE-CHIP pacemaker ASIC, voltage islands enable fine-grained power optimization by assigning different supply voltages to blocks based on their performance requirements and activity patterns. This technique exploits the quadratic relationship between supply voltage and dynamic power, providing significant power savings for blocks that can tolerate lower operating voltages.

The iPACE-CHIP implements multiple voltage islands: a high-performance island for timing-critical blocks, a low-voltage island for the DSP engine during non-peak processing, and an ultra-low-voltage island for housekeeping functions. This strategy, combined with Dynamic Voltage and Frequency Scaling (DVFS), enables the pacemaker to dynamically adjust power consumption based on real-time workload requirements while maintaining the timing precision needed for cardiac therapy.

## 2. Voltage Island Architecture

### 2.1 iPACE-CHIP Voltage Island Definition

```
iPACE-CHIP Voltage Island Architecture:

Island 0: V_DD_High (1.8V)
├── Sensing amplifier (analog, needs high SNR)
├── Reference generator (precision voltage)
├── ADC (high-speed sampling)
├── Stimulation output driver (high current)
├── RF transmitter (high power for telemetry)
└── I/O pads (external interface)

Island 1: V_DD_Medium (1.5V)
├── DSP engine (during high-performance processing)
├── Arrhythmia classifier (when active)
├── Pacing interval calculator (when active)
├── Clock dividers (frequency scalable)
└── Communication encoder (when active)

Island 2: V_DD_Low (1.2V)
├── DSP engine (during low-power processing)
├── Filter coefficients (when not updating)
├── Data path registers (when idle)
└── State machines (at reduced speed)

Island 3: V_DD_Ultra (0.8V)
├── Housekeeping controller
├── Watchdog timer
├── Temperature sensor digital logic
├── Battery monitor
└── Always-on configuration registers

┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │ V_DD_High│  │V_DD_Med  │  │ V_DD_Low │  │V_DD_Ultra│
│  │  1.8V    │  │  1.5V    │  │  1.2V    │  │  0.8V   ││
│  │          │  │          │  │          │  │         ││
│  │ Sensing  │  │ DSP      │  │ DSP      │  │ House-  ││
│  │ Stim     │  │ Classify │  │ Filter   │  │ keeping ││
│  │ Comm     │  │ Calculate│  │ State    │  │ WDT     ││
│  │ I/O      │  │ Encode   │  │ Machine  │  │ Sensors ││
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘│
│                                                         │
│  V_DD_Ret (0.5V): Retention flip-flops (always-on)     │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Voltage Level Assignment

```
Voltage Level Assignment Rationale:

Island 0 (1.8V): High Performance
- Analog circuits require high headroom
- Output drivers need full voltage swing
- I/O pads must meet external interface standards
- No voltage reduction possible

Island 1 (1.5V): Medium Performance
- DSP engine can operate at 83% of max frequency
- Timing slack allows 17% voltage reduction
- Dynamic power savings: 1 - (1.5/1.8)² = 30.6%
- Acceptable performance degradation

Island 2 (1.2V): Low Performance
- DSP engine can operate at 67% of max frequency
- Housekeeping at minimal speed
- Dynamic power savings: 1 - (1.2/1.8)² = 55.6%
- Significant power reduction for non-critical functions

Island 3 (0.8V): Ultra-Low Power
- Housekeeping at minimal speed
- Watchdog timer at low frequency
- Dynamic power savings: 1 - (0.8/1.8)² = 80.2%
- Maximum power reduction for always-on functions
```

### 2.3 Voltage Island Floorplan

```
Voltage Island Floorplan:

┌─────────────────────────────────────────────────────────┐
│                        Pad Ring                          │
│  ┌─────────────────────────────────────────────────┐   │
│  │                                                 │   │
│  │  ┌──────────────┐  ┌──────────────────────┐    │   │
│  │  │              │  │                      │    │   │
│  │  │  V_DD_High   │  │     V_DD_Medium      │    │   │
│  │  │  1.8V        │  │     1.5V             │    │   │
│  │  │  Area: 40%   │  │     Area: 25%        │    │   │
│  │  │              │  │                      │    │   │
│  │  │  ┌────────┐  │  │  ┌────────────────┐  │    │   │
│  │  │  │Sensing │  │  │  │  DSP Engine    │  │    │   │
│  │  │  │Amp     │  │  │  │  (High-Perf)   │  │    │   │
│  │  │  └────────┘  │  │  └────────────────┘  │    │   │
│  │  │              │  │                      │    │   │
│  │  │  ┌────────┐  │  │  ┌────────────────┐  │    │   │
│  │  │  │ADC     │  │  │  │  Classifier    │  │    │   │
│  │  │  └────────┘  │  │  └────────────────┘  │    │   │
│  │  │              │  │                      │    │   │
│  │  │  ┌────────┐  │  │                      │    │   │
│  │  │  │Stim    │  │  └──────────────────────┘    │   │
│  │  │  │Driver  │  │                               │   │
│  │  │  └────────┘  │  ┌──────────────────────┐    │   │
│  │  │              │  │                      │    │   │
│  │  │  ┌────────┐  │  │     V_DD_Low         │    │   │
│  │  │  │RF TX   │  │  │     1.2V             │    │   │
│  │  │  └────────┘  │  │     Area: 20%        │    │   │
│  │  └──────────────┘  │                      │    │   │
│  │                     │  ┌────────────────┐  │    │   │
│  │  ┌──────────────┐  │  │  DSP Engine    │  │    │   │
│  │  │              │  │  │  (Low-Power)   │  │    │   │
│  │  │  V_DD_Ultra  │  │  └────────────────┘  │    │   │
│  │  │  0.8V        │  │                      │    │   │
│  │  │  Area: 15%   │  └──────────────────────┘    │   │
│  │  │              │                               │   │
│  │  │  ┌────────┐  │                               │   │
│  │  │  │House-  │  │                               │   │
│  │  │  │keeping │  │                               │   │
│  │  │  └────────┘  │                               │   │
│  │  └──────────────┘                               │   │
│  │                                                 │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  Die Size: 2.0 mm × 2.0 mm = 4.0 mm²                   │
│  Voltage regulator area: 0.2 mm² (5%)                  │
│  Level shifter area: 0.01 mm² (0.25%)                  │
│  Total overhead: 5.25%                                  │
└─────────────────────────────────────────────────────────┘
```

## 3. Voltage Regulator Design

### 3.1 On-Chip LDO Regulator

```
On-Chip LDO Regulator for V_DD_Medium:

Input: V_DD_High (1.8V)
Output: V_DD_Med (1.5V)
Load Current: 50 μA (DSP active)

Circuit:
                    V_DD_High (1.8V)
                         │
                    ┌────┴────┐
                    │  PMOS   │
                    │  Pass   │
                    │  Trans. │
                    └────┬────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
     ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
     │  Error  │    │  Output │    │  Load   │
     │  Amp    │    │  Cap    │    │  (DSP)  │
     └────┬────┘    │  100pF  │    │         │
          │         └─────────┘    └─────────┘
     ┌────┴────┐
     │  Ref    │
     │  (0.5V) │
     └─────────┘

Specifications:
- Dropout voltage: 200 mV (1.8V - 1.6V)
- Output voltage: 1.5V ± 5%
- Load regulation: < 1%
- Line regulation: < 1%
- Quiescent current: 500 nA
- PSRR: > 40 dB at 1 kHz
- Area: 0.05 mm²
```

### 3.2 Ultra-Low-Power LDO

```
Ultra-Low-Power LDO for V_DD_Ultra:

Input: V_DD_High (1.8V)
Output: V_DD_Ultra (0.8V)
Load Current: 10 μA (housekeeping)

Design for Minimum Quiescent Current:

                    V_DD_High (1.8V)
                         │
                    ┌────┴────┐
                    │  PMOS   │
                    │  Pass   │
                    │  Trans. │
                    └────┬────┘
                         │
          ┌──────────────┼──────────────┐
          │              │              │
     ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
     │  Sub-   │    │  Output │    │  Load   │
     │threshold│    │  Cap    │    │  (House)│
     │  Error  │    │  50pF   │    │         │
     │  Amp    │    └─────────┘    └─────────┘
     └────┬────┘
          │
     ┌────┴────┐
     │  Ref    │
     │(Bandgap)│
     └─────────┘

Ultra-Low-Power Features:
- Sub-threshold error amplifier: 100 nA bias
- No external capacitor needed (compensated internally)
- Quiescent current: 100 nA
- Output noise: 50 μV rms
- Area: 0.02 mm²
```

### 3.3 Voltage Regulator Array

```
Voltage Regulator Array for iPACE-CHIP:

┌─────────────────────────────────────────────────────────┐
│              Voltage Regulator Array                     │
│                                                         │
│  V_DD_High (1.8V) ────────────────────────────────────  │
│  │              │              │              │          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │  LDO-1   │  │  LDO-2   │  │  LDO-3   │  │  LDO-4 │  │
│  │  1.5V    │  │  1.2V    │  │  0.8V    │  │  0.5V  │  │
│  │  50μA    │  │  30μA    │  │  10μA    │  │  1μA   │  │
│  │  500nA   │  │  300nA   │  │  100nA   │  │  50nA  │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───┬────┘  │
│       │             │             │             │        │
│       ▼             ▼             ▼             ▼        │
│  V_DD_Med      V_DD_Low      V_DD_Ultra    V_DD_Ret    │
│                                                         │
│  LDO Specifications:                                    │
│  ┌─────────┬──────────┬──────────┬──────────┬────────┐  │
│  │ LDO     │ V_out    │ I_max    │ I_q      │ Area   │  │
│  ├─────────┼──────────┼──────────┼──────────┼────────┤  │
│  │ LDO-1   │ 1.5V     │ 50 μA    │ 500 nA   │ 0.05mm²│  │
│  │ LDO-2   │ 1.2V     │ 30 μA    │ 300 nA   │ 0.04mm²│  │
│  │ LDO-3   │ 0.8V     │ 10 μA    │ 100 nA   │ 0.02mm²│  │
│  │ LDO-4   │ 0.5V     │ 1 μA     │ 50 nA    │ 0.01mm²│  │
│  └─────────┴──────────┴──────────┴──────────┴────────┘  │
│                                                         │
│  Total regulator area: 0.12 mm² (3% of die)            │
│  Total quiescent current: 950 nA                        │
└─────────────────────────────────────────────────────────┘
```

## 4. Power Savings Analysis

### 4.1 Per-Island Savings

```
Voltage Island Power Savings:

Island 0 (1.8V): Reference (no savings)
- Power: 1200 nW (all blocks at 1.8V)

Island 1 (1.5V): 30.6% dynamic power savings
- Before: 1030 nW (at 1.8V)
- After: 1030 × (1.5/1.8)² = 716 nW
- Savings: 314 nW

Island 2 (1.2V): 55.6% dynamic power savings
- Before: 500 nW (at 1.8V)
- After: 500 × (1.2/1.8)² = 222 nW
- Savings: 278 nW

Island 3 (0.8V): 80.2% dynamic power savings
- Before: 179 nW (at 1.8V)
- After: 179 × (0.8/1.8)² = 35 nW
- Savings: 144 nW

Total Dynamic Power Savings: 736 nW
Overhead (LDO quiescent): 950 nA × 1.8V = 1710 nW

Wait, that can't be right. Let me recalculate:
LDO quiescent current: 950 nA total
LDO power: 950 nA × 1.8V = 1710 nW = 1.71 μW

This is larger than the savings! Let me reconsider.

Actually, the LDO quiescent current should be much lower:
- LDO-1: 500 nA
- LDO-2: 300 nA
- LDO-3: 100 nA
- LDO-4: 50 nA
- Total: 950 nA

At 1.8V input: 950 nA × 1.8V = 1710 nW

But the savings are only 736 nW. This means voltage islands
are NOT beneficial without DVFS!

Key insight: Voltage islands alone are not beneficial.
They must be combined with DVFS (reducing frequency along
with voltage) to achieve net power savings.
```

### 4.2 Combined DVFS Savings

```
Combined Voltage + Frequency Scaling Savings:

For each island, both voltage AND frequency are reduced:

Island 1 (1.5V, 256 kHz → 200 kHz):
- Before: 1030 nW (1.8V, 256 kHz)
- After: 1030 × (1.5/1.8)² × (200/256) = 559 nW
- Savings: 471 nW

Island 2 (1.2V, 256 kHz → 128 kHz):
- Before: 500 nW (1.8V, 256 kHz)
- After: 500 × (1.2/1.8)² × (128/256) = 111 nW
- Savings: 389 nW

Island 3 (0.8V, 32 kHz → 8 kHz):
- Before: 179 nW (1.8V, 32 kHz)
- After: 179 × (0.8/1.8)² × (8/32) = 8.8 nW
- Savings: 170 nW

Total Dynamic Power Savings: 1030 nW
LDO Quiescent Overhead: 950 nA × 1.8V = 1710 nW

Still not beneficial! The LDO overhead is too high.

Alternative: Use switching regulators instead of LDOs.
Switching regulator efficiency: 85%
Quiescent current: 1 μA
Power: 1 μA × 1.8V = 1800 nW (similar overhead)

The key is that voltage islands are only beneficial when:
1. The island power is much larger than LDO overhead
2. The frequency reduction is substantial
3. The duty cycle is low (only active part of time)
```

### 4.3 Time-Weighted Savings

```
Time-Weighted Voltage Island Analysis:

Operating Modes and Island Usage:

Mode            │ Is1 P  │ Is2 P  │ Is3 P  │ Time │ Weighted
────────────────┼────────┼────────┼────────┼──────┼─────────
Active DSP      │ 559 nW │ 111 nW │ 8.8 nW │ 5%   │ 34 nW
Monitoring      │ 0 nW   │ 0 nW   │ 8.8 nW │ 70%  │ 6.2 nW
Processing      │ 559 nW │ 111 nW │ 8.8 nW │ 10%  │ 67.9 nW
Idle            │ 0 nW   │ 0 nW   │ 8.8 nW │ 15%  │ 1.3 nW
────────────────┼────────┼────────┼────────┼──────┼─────────
Weighted Avg    │        │        │        │      │ 109.4 nW

Without voltage islands (all at 1.8V):
Mode            │ Total P│ Time │ Weighted
────────────────┼────────┼──────┼─────────
Active DSP      │ 1530 nW│ 5%   │ 76.5 nW
Monitoring      │ 179 nW │ 70%  │ 125.3 nW
Processing      │ 1530 nW│ 10%  │ 153 nW
Idle            │ 179 nW │ 15%  │ 26.9 nW
────────────────┼────────┼──────┼─────────
Weighted Avg    │        │      │ 381.7 nW

Dynamic savings: 381.7 - 109.4 = 272.3 nW
LDO overhead: 1710 nW (always-on LDOs)

The LDO overhead still exceeds savings!

Conclusion: For iPACE-CHIP at these power levels,
voltage islands with LDO regulators are NOT beneficial.
DVFS alone (without separate voltage domains) is more
effective because it uses a single high-efficiency regulator.
```

## 5. When Voltage Islands Are Beneficial

### 5.1 Break-Even Analysis

```
Voltage Island Break-Even Analysis:

Break-even condition:
P_savings > P_LDO_quiescent

P_savings = P_before × (1 - (V_low/V_high)²) × duty_cycle
P_LDO_quiescent = I_q × V_high

For iPACE-CHIP:
P_savings > I_q × V_high
P_before × (1 - (V_low/V_high)²) × duty > I_q × V_high

Solving for minimum P_before:
P_before > (I_q × V_high) / ((1 - (V_low/V_high)²) × duty)

For Island 1 (1.5V, 70% duty):
P_before > (500 nA × 1.8V) / ((1 - 0.694) × 0.70)
P_before > 900 nW / 0.214 = 4206 nW

For iPACE-CHIP Island 1 power: 1030 nW
1030 nW < 4206 nW → NOT beneficial

Break-even power: 4206 nW
This is much higher than iPACE-CHIP block power levels.

When would voltage islands be beneficial?
- Blocks with > 4 μW power consumption
- DSP engines in larger ASICs
- Communication blocks with high transmit power
- Processor cores with > 10 μW power
```

### 5.2 Alternative: Single-Regulator DVFS

```
Single-Regulator DVFS for iPACE-CHIP:

Instead of multiple voltage islands with separate LDOs,
use a single high-efficiency regulator with DVFS:

Architecture:
V_DD_High (1.8V) ────┐
                      │
                 ┌────▼────┐
                 │ Single  │
                 │ Buck    │
                 │ Conv.   │
                 │ (η=85%) │
                 └────┬────┘
                      │
                 V_DD_Scalable (0.8V to 1.8V)
                      │
            ┌─────────┼─────────┐
            │         │         │
       ┌────┴────┐┌───┴───┐┌───┴───┐
       │ Sensing ││  DSP  ││Stim   │
       │ (1.8V)  ││(0.8-  ││(1.8V) │
       │         ││ 1.8V) ││       │
       └─────────┘└───────┘└───────┘

DVFS Operation:
- DSP active: V_DD = 1.8V, f = 256 kHz
- DSP idle: V_DD = 0.8V, f = 32 kHz
- Transition time: 10 μs (voltage ramp)
- Transition energy: 10 nJ

Savings:
- Active: 1030 nW (same as without DVFS)
- Idle: 1030 × (0.8/1.8)² × (32/256) = 32 nW
- Time-weighted: 5% × 1030 + 95% × 32 = 82 nW
- Without DVFS: 381.7 nW (from previous analysis)
- Savings: 300 nW

Overhead:
- Buck converter quiescent: 100 nA × 1.8V = 180 nW
- But buck converter efficiency: 85%
- Net overhead: 180 / 0.85 = 212 nW

Net savings: 300 - 212 = 88 nW (positive but modest)

This is better than voltage islands (which had negative net savings).
```

### 5.3 Recommendations for iPACE-CHIP

```
Voltage Island Recommendations:

Based on analysis:

1. Do NOT implement multiple voltage islands
   - LDO quiescent current exceeds savings
   - Block power levels too low for break-even

2. DO implement single-regulator DVFS
   - Use high-efficiency buck converter
   - Scale voltage from 0.8V to 1.8V
   - Combine with frequency scaling
   - Net savings: 88 nW

3. DO keep analog blocks at fixed 1.8V
   - Sensing amplifier needs high SNR
   - Reference generator needs stability
   - ADC needs full voltage range

4. DO use ultra-low voltage for housekeeping
   - Separate 0.8V LDO for always-on functions
   - Quiescent current: 100 nA
   - Savings: 179 × (1 - (0.8/1.8)²) = 143 nW
   - Net savings: 143 - (100 nA × 1.8V) = 125 nW

5. DO NOT use voltage islands for DSP engine
   - DVFS with single regulator is more efficient
   - Avoids complexity of multiple voltage domains
   - Simpler verification and testing
```

## 6. Voltage Island Implementation Guidelines

### 6.1 Design Rules

```
Voltage Island Design Rules:

Rule 1: Domain Separation
- Minimum 5 μm gap between voltage islands
- Guard rings required at island boundaries
- Substrate contacts every 10 μm along boundary

Rule 2: Level Shifter Requirements
- All signals crossing voltage domains require level shifters
- Level shifters must be powered by source domain voltage
- Level shifters placed in source domain

Rule 3: Isolation Requirements
- When island is powered off, all outputs must be isolated
- Isolation cells powered by always-on domain
- Isolation control from always-on domain

Rule 4: Power Switch Requirements
- Each island has independent power switch
- Power switch sized for island peak current
- Staggered turn-on for inrush control

Rule 5: Decoupling Requirements
- Each island has local decoupling capacitance
- Minimum 50 fF per mW of dynamic power
- Decap placed near power switch output
```

### 6.2 Verification Checklist

```
Voltage Island Verification Checklist:

□ Power domain assignment correct
□ Voltage levels correct for each island
□ Level shifters inserted at all crossings
□ Isolation cells inserted for OFF→ON paths
□ Power switches sized correctly
□ Decoupling capacitance adequate
□ IR drop within budget
□ Timing closure at all voltage corners
□ Functional verification with all power states
□ Formal verification of power intent
□ Power analysis matches estimates
□ Physical verification (DRC/LVS) clean
□ Reliability analysis complete
□ Test coverage adequate
```

## 7. Summary

Voltage islands for the iPACE-CHIP pacemaker ASIC provide limited benefit due to the low power levels of individual blocks and the quiescent current overhead of on-chip LDO regulators. Analysis shows that the break-even power for voltage islands is approximately 4 μW per island, significantly above the iPACE-CHIP block power levels. The recommended approach is single-regulator DVFS combined with an ultra-low-voltage LDO for always-on housekeeping functions, achieving net savings of 213 nW. This approach avoids the complexity of multiple voltage domains while still exploiting the quadratic voltage-power relationship for dynamic power reduction.

## References

1. Usami, K., et al., "Design Methodology of Macro Cells for Embedded ASICs," IEEE JSSC, 1998.
2. iPACE-CHIP Project Internal Documentation: Voltage Island Analysis Report, Rev 1.5.
3. Calhoun, B., et al., "Design Methodologies for Ultra-Low Power," Foundations and Trends in EDA, 2010.
4. TSMC 0.18μm Mixed-Signal Process Design Manual: On-Chip Regulator Library.
5. Rabaey, J., et al., "Low Power Design of Deep Sub-Micron Circuits," Kluwer, 2000.
