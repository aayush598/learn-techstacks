# Dynamic Voltage and Frequency Scaling (DVFS) for Implantable Pacemaker ASICs

## 1. Introduction to DVFS

Dynamic Voltage and Frequency Scaling (DVFS) is a power management technique that simultaneously adjusts the supply voltage and clock frequency of a circuit block based on its current performance requirements. For the iPACE-CHIP pacemaker ASIC, DVFS enables significant power savings during periods of reduced computational demand while maintaining the timing precision required for cardiac sensing and stimulation.

The fundamental principle exploits the quadratic relationship between supply voltage and dynamic power (P ∝ V²) and the linear relationship between frequency and power (P ∝ f). By reducing both voltage and frequency when full performance is not needed, DVFS achieves power savings far greater than either technique alone. For a pacemaker with 10-year battery life, DVFS provides a critical tool for managing the dynamic power budget across varying workload conditions.

## 2. DVFS Principles

### 2.1 Voltage-Frequency Relationship

```
Critical Voltage-Frequency Relationship:

For a digital circuit, the maximum operating frequency is
determined by the critical path delay:

f_max = 1 / t_delay

Where:
t_delay = t_p0 × V_DD / (V_DD - V_th)^α

For deep submicron (α ≈ 1.3):
f_max ∝ (V_DD - V_th)^1.3 / V_DD

Simplified relationship:
f_max ≈ k × (V_DD - V_th)^1.3

Where k is a process-dependent constant.

For iPACE-CHIP 180nm process:
- V_th = 0.4V (standard Vt)
- At V_DD = 1.8V: f_max = 500 MHz (theoretical)
- At V_DD = 1.2V: f_max = 180 MHz (64% reduction)
- At V_DD = 0.8V: f_max = 45 MHz (91% reduction)

In practice, iPACE-CHIP operates at much lower frequencies:
- V_DD = 1.8V: f = 32-256 kHz
- V_DD = 1.2V: f = 16-128 kHz
- V_DD = 0.8V: f = 4-32 kHz
```

### 2.2 Power Savings from DVFS

```
DVFS Power Savings Analysis:

Without DVFS (fixed 1.8V, 256 kHz):
P = C × (1.8V)² × 256 kHz = C × 829.4

With DVFS (scaling to 1.2V, 128 kHz):
P = C × (1.2V)² × 128 kHz = C × 184.3

Savings = (829.4 - 184.3) / 829.4 = 77.8%

Voltage-Frequency Scaling Table:
┌──────────┬──────────┬──────────┬────────────────────┐
│ V_DD (V) │ f (kHz)  │ P (rel.) │ Savings vs 1.8V    │
├──────────┼──────────┼──────────┼────────────────────┤
│ 1.80     │ 256      │ 100%     │ 0% (baseline)      │
│ 1.60     │ 200      │ 61.7%    │ 38.3%              │
│ 1.40     │ 150      │ 37.6%    │ 62.4%              │
│ 1.20     │ 128      │ 22.2%    │ 77.8%              │
│ 1.00     │ 80       │ 12.3%    │ 87.7%              │
│ 0.80     │ 45       │ 5.4%     │ 94.6%              │
└──────────┴──────────┴──────────┴────────────────────┘

Key Insight: DVFS achieves nearly 95% power reduction
compared to fixed 1.8V/256 kHz operation.
```

### 2.3 Energy Efficiency

```
Energy per Operation Analysis:

Energy per operation: E = P × t = C × V² × f × (1/f) = C × V²

Without DVFS (1.8V):
E = C × (1.8V)² = C × 3.24

With DVFS (1.2V):
E = C × (1.2V)² = C × 1.44

Energy Savings = (3.24 - 1.44) / 3.24 = 55.6%

This means DVFS not only reduces power but also reduces
energy per operation, making it more efficient than
frequency scaling alone (which doesn't reduce V²).

Note: DVFS cannot reduce energy below C × V_th²
(the minimum energy point for CMOS logic).
```

## 3. DVFS Architecture for iPACE-CHIP

### 3.1 DVFS System Architecture

```
iPACE-CHIP DVFS System Architecture:

┌─────────────────────────────────────────────────────────┐
│                   DVFS Controller                        │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │ Workload        │  │ Voltage/Freq    │              │
│  │ Monitor         │  │ Selector        │              │
│  └────────┬────────┘  └────────┬────────┘              │
│           │                    │                        │
│  ┌────────▼────────┐  ┌───────▼─────────┐              │
│  │ Activity        │  │ Transition      │              │
│  │ Counter         │  │ Manager         │              │
│  └────────┬────────┘  └───────┬─────────┘              │
│           │                   │                         │
│           └──────────┬────────┘                         │
│                      │                                  │
│              ┌───────▼───────┐                          │
│              │  DVFS State   │                          │
│              │  Machine      │                          │
│              └───────┬───────┘                          │
│                      │                                  │
│         ┌────────────┼────────────┐                     │
│         │            │            │                     │
│    ┌────▼────┐  ┌────▼────┐  ┌────▼────┐               │
│    │ Voltage │  │ Clock   │  │ Status  │               │
│    │ Control │  │ Control │  │ Monitor │               │
│    └────┬────┘  └────┬────┘  └────┬────┘               │
│         │            │            │                     │
│         └────────────┼────────────┘                     │
│                      │                                  │
│              ┌───────▼───────┐                          │
│              │  Controlled   │                          │
│              │  Block        │                          │
│              └───────────────┘                          │
└─────────────────────────────────────────────────────────┘
```

### 3.2 DVFS Operating Points

```
iPACE-CHIP DVFS Operating Points:

Point 0: Maximum Performance
- V_DD = 1.8V
- f = 256 kHz
- Application: Arrhythmia classification (real-time)
- Power: 1030 nW
- Use: < 1% of time

Point 1: High Performance
- V_DD = 1.5V
- f = 192 kHz
- Application: ECG processing, R-wave detection
- Power: 534 nW
- Use: 5% of time

Point 2: Medium Performance
- V_DD = 1.2V
- f = 128 kHz
- Application: General signal processing
- Power: 222 nW
- Use: 15% of time

Point 3: Low Power
- V_DD = 0.8V
- f = 32 kHz
- Application: Basic monitoring, housekeeping
- Power: 32 nW
- Use: 79% of time

Operating Point Selection:
- Real-time workload monitor determines current demand
- DVFS controller selects appropriate operating point
- Transitions occur within 10 μs (voltage ramp time)
```

### 3.3 DVFS State Machine

```
DVFS State Machine:

States:
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  ┌──────────┐                                           │
│  │  INIT    │                                           │
│  │ (1.8V)   │                                           │
│  └────┬─────┘                                           │
│       │ Boot complete                                   │
│       ▼                                                 │
│  ┌──────────┐  High    ┌──────────┐                    │
│  │  MONITOR │◄────────│  PEAK    │                    │
│  │ (0.8V)   │  demand  │ (1.8V)   │                    │
│  │          │─────────►│          │                    │
│  └────┬─────┘ demand   └────┬─────┘                    │
│       │                     │                          │
│       │ Medium              │ Medium                   │
│       │ demand              │ demand                   │
│       ▼                     ▼                          │
│  ┌──────────┐  High    ┌──────────┐                    │
│  │  NORMAL  │◄────────│  HIGH    │                    │
│  │ (1.2V)   │  demand  │ (1.5V)   │                    │
│  │          │─────────►│          │                    │
│  └──────────┘ demand   └──────────┘                    │
│                                                         │
│  Transitions:                                           │
│  MONITOR → NORMAL: Workload > 30%                      │
│  NORMAL → HIGH: Workload > 60%                         │
│  HIGH → PEAK: Workload > 90%                           │
│  PEAK → HIGH: Workload < 70%                           │
│  HIGH → NORMAL: Workload < 40%                         │
│  NORMAL → MONITOR: Workload < 10%                      │
│                                                         │
│  Transition Time: 10 μs (voltage ramp)                 │
│  Transition Energy: 10 nJ                              │
└─────────────────────────────────────────────────────────┘
```

## 4. DVFS Implementation

### 4.1 On-Chip Voltage Regulator

```
DVFS Voltage Regulator Design:

For DVFS, a switching regulator is preferred over LDO
due to higher efficiency:

Buck Converter Design:
Input: V_DD_High (1.8V)
Output: V_DD_Scalable (0.8V to 1.8V)
Maximum load: 100 μA

Specifications:
- Topology: Synchronous buck
- Switching frequency: 1 MHz
- Inductor: 10 μH (external)
- Output capacitor: 100 nF (external)
- Efficiency: 85% at full load
- Quiescent current: 100 nA
- Output ripple: < 10 mV
- Transient response: < 10 μs (for DVFS transitions)

Control:
- PWM modulation for voltage regulation
- Voltage DAC for setpoint control
- Feedback from output voltage sensor
- Current limit protection

Area: 0.1 mm² (on-chip control, external passives)
```

### 4.2 Clock Generator

```
DVFS Clock Generator:

Input: 32.768 kHz reference
Output: Configurable clock (4 kHz to 256 kHz)

Architecture:
                    ┌─────────────┐
  32.768 kHz ──────►│  Phase-     │
  (reference)       │  Locked     │
                    │  Loop (PLL) │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Clock      │
                    │  Divider    │
                    │  (÷1 to ÷64)│
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Clock      │
                    │  MUX        │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Output     │──── GCLK
                    │  Buffer     │
                    └─────────────┘

Specifications:
- Output frequency: 4 kHz to 256 kHz
- Frequency accuracy: ±100 ppm
- Phase noise: < -100 dBc/Hz at 1 kHz offset
- Jitter: < 1 ns rms
- Switching time: < 1 μs (frequency change)
- Power: 50 nW (at 32 kHz output)
```

### 4.3 DVFS Control Logic

```
DVFS Control Logic:

Workload Monitor:
┌─────────────────────────────────────────────────────────┐
│ Workload Monitor                                         │
│                                                         │
│  GCLK ─────────────────── Counter                      │
│                               (16-bit)                  │
│  ACTIVE ────────────────── Enable                       │
│                                                         │
│  Sample Period: 1 ms (via timer)                        │
│                                                         │
│  Output: Activity count (0 to 65535)                    │
│  Activity Level: count / 65535 × 100%                   │
│                                                         │
│  Thresholds:                                            │
│  - Low: < 10% → MONITOR mode (0.8V)                   │
│  - Medium: 10-40% → NORMAL mode (1.2V)                │
│  - High: 40-70% → HIGH mode (1.5V)                    │
│  - Peak: > 70% → PEAK mode (1.8V)                     │
└─────────────────────────────────────────────────────────┘

Voltage/Frequency Selector:
┌─────────────────────────────────────────────────────────┐
│ DVFS Selector                                           │
│                                                         │
│  Input: Activity Level (0-100%)                         │
│                                                         │
│  Mapping:                                               │
│  0-10%:   V_DD = 0.8V, f = 32 kHz                    │
│  10-40%:  V_DD = 1.2V, f = 128 kHz                   │
│  40-70%:  V_DD = 1.5V, f = 192 kHz                   │
│  70-100%: V_DD = 1.8V, f = 256 kHz                   │
│                                                         │
│  Hysteresis: ±5% to prevent oscillation                │
│  Debounce: 10 ms (prevent rapid switching)              │
└─────────────────────────────────────────────────────────┘
```

## 5. DVFS Transition Analysis

### 5.1 Voltage Ramp

```
DVFS Voltage Transition Analysis:

Voltage Ramp Requirements:
- Ramp time: 10 μs (0.8V to 1.8V)
- Ramp rate: 100 mV/μs
- Overshoot: < 5% (90 mV)
- Undershoot: < 5% (40 mV)
- Settling time: < 1 μs after ramp

Ramp Profile:
V_DD (V)
1.80 ┤                    ┌───────────────
     │                   ╱
1.60 ┤                  ╱
     │                 ╱
1.40 ┤                ╱
     │               ╱
1.20 ┤              ╱
     │             ╱
1.00 ┤            ╱
     │           ╱
0.80 ┤──────────╱
     └──┴──────┴──────┴──────┴──────┴── t
        0     2     4     6     8    10 μs

Ramp Implementation:
- DAC-controlled voltage reference
- Error amplifier feedback
- Current-limited charging
- 10 μs ramp time meets settling requirement
```

### 5.2 Frequency Transition

```
DVFS Frequency Transition Analysis:

Frequency Change Sequence:
1. Switch to reference clock (32.768 kHz)
2. Wait for PLL to lock at new frequency
3. Switch output to new frequency
4. Resume operation at new frequency

Sequence Timing:
T0:      Request frequency change
T0+1μs:  Switch to reference clock
T0+2μs:  Begin PLL relock
T0+5μs:  PLL locked at new frequency
T0+6μs:  Switch output to new frequency
T0+7μs:  Resume operation

Total transition time: 7 μs
Frequency glitch: None (reference clock used during transition)
```

### 5.3 Combined Voltage-Frequency Transition

```
Combined DVFS Transition:

For simultaneous voltage and frequency change:

T0:      DVFS transition request
T0+1μs:  Begin voltage ramp (0.8V → 1.8V)
T0+1μs:  Switch to reference clock
T0+2μs:  Begin PLL relock
T0+5μs:  PLL locked at new frequency
T0+6μs:  Switch output to new frequency
T0+10μs: Voltage ramp complete
T0+11μs: Voltage settling complete
T0+12μs: Full operation at new DVFS point

Total transition time: 12 μs
Energy per transition: 10 nJ

Transition Energy Breakdown:
- Voltage ramp: 5 nJ (charging output capacitance)
- PLL relock: 2 nJ (PLL power during lock)
- Clock switch: 1 nJ (clock tree charge/discharge)
- Control logic: 2 nJ (state machine operations)
```

## 6. Power Savings Analysis

### 6.1 Time-Weighted Power Analysis

```
DVFS Power Savings Over 10-Year Lifetime:

Operating Point Distribution:
Point 0 (1.8V, 256 kHz): 1% of time
Point 1 (1.5V, 192 kHz): 5% of time
Point 2 (1.2V, 128 kHz): 15% of time
Point 3 (0.8V, 32 kHz): 79% of time

Without DVFS (fixed 1.8V, 256 kHz):
P_avg = 1030 nW × 100% = 1030 nW

With DVFS:
P_avg = (1030 × 0.01) + (534 × 0.05) + (222 × 0.15) + (32 × 0.79)
      = 10.3 + 26.7 + 33.3 + 25.3 = 95.6 nW

Power Savings: 1030 - 95.6 = 934.4 nW (90.7%)
```

### 6.2 Energy Savings Over Lifetime

```
10-Year Energy Savings from DVFS:

Without DVFS:
E = 1030 nW × 3.15 × 10⁸ s = 324.5 mJ

With DVFS:
E = 95.6 nW × 3.15 × 10⁸ s = 30.1 mJ

DVFS Transition Energy:
- 100,000 transitions × 10 nJ = 1 mJ

Net Energy Savings: 324.5 - 30.1 - 1 = 293.4 mJ

Battery Impact:
- 293.4 mJ / 1123 mJ = 26.1% of battery capacity saved
- Equivalent to 2.6 additional years of operation
- Significant contribution to 10-year battery life target
```

### 6.3 Transition Overhead

```
DVFS Transition Overhead Analysis:

Transition Frequency:
- Mode changes: ~100,000 per year (based on cardiac activity)
- Average transitions per day: 274
- Average time between transitions: 5.3 minutes

Transition Energy Cost:
- Per transition: 10 nJ
- Annual cost: 100,000 × 10 nJ = 1 mJ
- 10-year cost: 10 mJ

Transition Time Cost:
- Per transition: 12 μs
- Annual cost: 100,000 × 12 μs = 1.2 s
- 10-year cost: 12 s (negligible)

Overhead as Percentage of Savings:
- Energy overhead: 10 mJ / 293.4 mJ = 3.4%
- Time overhead: 12 s / 3.15×10⁸ s = 0.0000038%

DVFS overhead is minimal and well-justified by savings.
```

## 7. DVFS Verification

### 7.1 Functional Verification

```
DVFS Functional Verification:

Test 1: Voltage Ramp
- Request 0.8V → 1.8V transition
- Measure voltage ramp time: 10 μs ✓
- Measure overshoot: < 5% ✓
- Measure settling time: < 1 μs ✓

Test 2: Frequency Switch
- Request 32 kHz → 256 kHz transition
- Measure switch time: 7 μs ✓
- Verify no clock glitches ✓
- Verify PLL lock time: 5 μs ✓

Test 3: Combined Transition
- Request simultaneous V/f change
- Measure total transition time: 12 μs ✓
- Verify correct final V and f ✓
- Verify no functional errors ✓

Test 4: Rapid Transitions
- Request transitions every 100 μs
- Verify all transitions complete correctly
- Verify no metastability issues
- Pass: 10,000 consecutive transitions ✓

Test 5: Transition Under Load
- Apply maximum workload during transition
- Verify no data loss or corruption
- Verify timing constraints met
- Pass: All tests pass ✓
```

### 7.2 Power Verification

```
DVFS Power Verification:

Measurement Setup:
- Precision ammeter: Keithley 6517B
- Controlled temperature: 37°C ± 0.5°C
- Supply voltage: Variable (0.8V to 1.8V)
- Measurement window: 10 seconds average

Results:
┌──────────────┬──────────┬──────────┬──────────┐
│ DVFS Point   │ Simulated│ Measured │ Error    │
├──────────────┼──────────┼──────────┼──────────┤
│ 1.8V/256kHz  │ 1030 nW  │ 1010 nW  │ -1.9%   │
│ 1.5V/192kHz  │ 534 nW   │ 520 nW   │ -2.6%   │
│ 1.2V/128kHz  │ 222 nW   │ 215 nW   │ -3.2%   │
│ 0.8V/32kHz   │ 32 nW    │ 31 nW    │ -3.1%   │
├──────────────┼──────────┼──────────┼──────────┤
│ Average      │ 95.6 nW  │ 93.0 nW  │ -2.7%   │
└──────────────┴──────────┴──────────┴──────────┘

All measurements within ±5% of simulation.
DVFS power savings validated on silicon.
```

## 8. Summary

DVFS in the iPACE-CHIP pacemaker ASIC achieves 90.7% power reduction compared to fixed-voltage operation, reducing average DSP power from 1030 nW to 95.6 nW. The implementation uses a 4-point DVFS table (0.8V/32kHz to 1.8V/256kHz) with automatic workload-based switching. Transition time of 12 μs and energy cost of 10 nJ per transition result in minimal overhead (3.4% of savings). Over the 10-year lifetime, DVFS saves 293.4 mJ of energy, equivalent to 26.1% of battery capacity. The combination of switching regulator efficiency (85%) and intelligent workload monitoring ensures that DVFS provides substantial power savings while maintaining the timing precision required for cardiac sensing and stimulation.

## References

1. Burd, T., Brodersen, R., "Design Issues for Dynamic Voltage Scaling," ISLPED, 2000.
2. iPACE-CHIP Project Internal Documentation: DVFS Design Specification, Rev 2.0.
3. Calhoun, B., et al., "Ultra-Low Voltage Digital Design," IEEE JSSC, 2005.
4. TSMC 0.18μm Mixed-Signal Process Design Manual: Clock Management.
5. Semeraro, G., et al., "Energy-Efficient Processor Design Using Multiple Voltage Domains," MICRO, 2002.
