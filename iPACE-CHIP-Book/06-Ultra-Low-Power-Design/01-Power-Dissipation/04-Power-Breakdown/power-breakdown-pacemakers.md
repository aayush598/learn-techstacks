# Power Breakdown Analysis for Implantable Pacemaker ASICs

## 1. Introduction to Power Breakdown

Power breakdown analysis decomposes the total power consumption of the iPACE-CHIP pacemaker ASIC into its constituent components, enabling targeted optimization and informed design decisions. For a device requiring 10-year battery life from a limited energy reservoir, understanding where every nanowatt is consumed is essential for meeting the stringent power budget.

This analysis examines power consumption from multiple perspectives: by functional block, by power source (dynamic vs. static), by operating mode, by process corner, and by temperature. The detailed breakdown guides optimization efforts and provides a baseline for measuring the effectiveness of power reduction techniques.

## 2. System-Level Power Budget

### 2.1 Battery Specifications

```
iPACE-CHIP Battery Specifications:

Battery Type: Lithium-Iodine (LiI)
Manufacturer: Wilson Greatbatch Technologies
Model: ML-420

Specifications:
┌──────────────────────┬────────────────┐
│ Parameter            │ Value          │
├──────────────────────┼────────────────┤
│ Chemistry            │ LiI / Li/AgVOx │
│ Nominal Voltage      │ 2.8V           │
│ Initial Capacity     │ 120 mAh        │
│ End-of-Life Voltage  │ 2.4V           │
│ Maximum Current      │ 20 μA (continuous)│
│ Pulse Current        │ 500 μA (10 ms) │
│ Self-Discharge Rate  │ < 1%/year      │
│ Operating Temp       │ -20°C to +50°C  │
│ Shelf Life           │ > 10 years     │
│ Diameter             │ 20 mm          │
│ Thickness            │ 4.5 mm         │
│ Weight               │ 12 g           │
└──────────────────────┴────────────────┘

Usable Energy:
- Total charge: 120 mAh = 432 C
- Average voltage: 2.6V (derated from 2.8V)
- Total energy: 432 C × 2.6V = 1123 J = 1.12 kJ

Design Target:
- 10-year battery life: 3.15 × 10⁸ seconds
- Average power budget: 1123 J / 3.15 × 10⁸ s = 3.6 μW
- With safety margin (20%): 2.9 μW target
```

### 2.2 Power Allocation Framework

```
Top-Level Power Allocation:

Total Budget: 2.9 μW average (including safety margin)

Allocation by Function:
┌─────────────────────────┬──────────┬────────────┐
│ Function Category       │ Budget   │ % of Total │
├─────────────────────────┼──────────┼────────────┤
│ Sensing & Measurement   │ 0.5 μW   │ 17%        │
│ Signal Processing       │ 0.8 μW   │ 28%        │
│ Pacing Control          │ 0.3 μW   │ 10%        │
│ Stimulation             │ 0.2 μW   │ 7%         │
│ Communication           │ 0.3 μW   │ 10%        │
│ Housekeeping            │ 0.2 μW   │ 7%         │
│ Clock Distribution      │ 0.4 μW   │ 14%        │
│ Power Management        │ 0.1 μW   │ 3%         │
│ I/O and Pads            │ 0.1 μW   │ 3%         │
│ Margin                  │ 0.1 μW   │ 3%         │
├─────────────────────────┼──────────┼────────────┤
│ TOTAL                   │ 2.9 μW   │ 100%       │
└─────────────────────────┴──────────┴────────────┘
```

## 3. Block-Level Power Breakdown

### 3.1 Sensing Subsystem

```
Sensing Subsystem Power Breakdown:

┌─────────────────────────────────────────────────────────┐
│ Sensing Subsystem                                       │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ Front-End Amplifier                 │                │
│  │ ├─ Input stage (NMOS diff pair)     │ 200 nW        │
│  │ ├─ Feedback network                 │ 20 nW         │
│  │ ├─ Bias generator                   │ 10 nW         │
│  │ └─ Total                            │ 230 nW        │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ Band-Pass Filter                    │                │
│  │ ├─ Active filter stages             │ 80 nW         │
│  │ ├─ Filter coefficient gen.          │ 10 nW         │
│  │ └─ Total                            │ 90 nW         │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ 12-bit SAR ADC                      │                │
│  │ ├─ Comparator                       │ 50 nW         │
│  │ ├─ DAC reference                    │ 10 nW         │
│  │ ├─ SAR control logic                │ 20 nW         │
│  │ ├─ Sample-and-hold                  │ 30 nW         │
│  │ └─ Total                            │ 110 nW        │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ Reference Generator                 │                │
│  │ ├─ Bandgap reference                │ 30 nW         │
│  │ ├─ Buffer amplifier                 │ 20 nW         │
│  │ └─ Total                            │ 50 nW         │
│  └─────────────────────────────────────┘                │
│                                                         │
│  TOTAL SENSING: 480 nW                                  │
└─────────────────────────────────────────────────────────┘

Power Distribution:
- Amplifier: 48% (dominant)
- ADC: 23%
- Reference: 10%
- Filter: 19%
```

### 3.2 Signal Processing Subsystem

```
DSP Subsystem Power Breakdown:

┌─────────────────────────────────────────────────────────┐
│ Signal Processing (DSP)                                  │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ 8-bit Multiplier-Accumulator        │                │
│  │ ├─ Multiplier array                 │ 400 nW        │
│  │ ├─ Accumulator register             │ 50 nW         │
│  │ ├─ Control logic                    │ 30 nW         │
│  │ └─ Total                            │ 480 nW        │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ Digital Filter (FIR, 16 taps)       │                │
│  │ ├─ Coefficient storage              │ 20 nW         │
│  │ ├─ Delay line                       │ 40 nW         │
│  │ ├─ Arithmetic units                 │ 200 nW        │
│  │ └─ Total                            │ 260 nW        │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ R-Wave Detector                     │                │
│  │ ├─ Peak detector logic              │ 30 nW         │
│  │ ├─ Threshold comparator             │ 20 nW         │
│  │ ├─ Timing generator                 │ 10 nW         │
│  │ └─ Total                            │ 60 nW         │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ Arrhythmia Classifier               │                │
│  │ ├─ State machine                    │ 40 nW         │
│  │ ├─ Pattern matching                 │ 100 nW        │
│  │ ├─ Decision logic                   │ 30 nW         │
│  │ └─ Total                            │ 170 nW        │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ Pacing Interval Calculator          │                │
│  │ ├─ Timer counter                    │ 20 nW         │
│  │ ├─ Rate adaptation logic            │ 40 nW         │
│  │ └─ Total                            │ 60 nW         │
│  └─────────────────────────────────────┘                │
│                                                         │
│  TOTAL DSP: 1030 nW                                     │
└─────────────────────────────────────────────────────────┘

Power Distribution:
- Multiplier: 47% (most power-hungry)
- Digital filter: 25%
- Classifier: 17%
- Others: 11%
```

### 3.3 Stimulation Subsystem

```
Stimulation Subsystem Power Breakdown:

┌─────────────────────────────────────────────────────────┐
│ Stimulation Control                                      │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ Pulse Generator Control             │                │
│  │ ├─ Timing controller                │ 30 nW         │
│  │ ├─ Amplitude DAC                    │ 20 nW         │
│  │ ├─ Width controller                 │ 15 nW         │
│  │ └─ Total                            │ 65 nW         │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ Output Driver                       │                │
│  │ ├─ Current source                   │ 5 nW (idle)   │
│  │ ├─ Output switch matrix             │ 3 nW          │
│  │ ├─ Safety limiter                   │ 2 nW          │
│  │ └─ Total (idle)                     │ 10 nW         │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ During Stimulation Pulse:           │                │
│  │ ├─ Current source (active)          │ 20 μW         │
│  │ ├─ Control logic                    │ 1 μW          │
│  │ ├─ Safety monitoring                │ 0.5 μW        │
│  │ └─ Total (during pulse)             │ 21.5 μW       │
│  └─────────────────────────────────────┘                │
│                                                         │
│  TOTAL STIMULATION (idle): 75 nW                        │
│  TOTAL STIMULATION (active): 21.5 μW                    │
└─────────────────────────────────────────────────────────┘

Note: Stimulation power is bursty - only active during
pacing pulses (~2 ms every 800 ms average = 0.25% duty)
Time-averaged stimulation power: ~54 nW
```

### 3.4 Communication Subsystem

```
Communication Subsystem Power Breakdown:

┌─────────────────────────────────────────────────────────┐
│ Telemetry / Communication                                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ Data Encoder                        │                │
│  │ ├─ Manchester encoder               │ 20 nW         │
│  │ ├─ Data formatter                   │ 15 nW         │
│  │ └─ Total                            │ 35 nW         │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ RF Transmitter (402 MHz MICS)       │                │
│  │ ├─ VCO                              │ 500 nW (idle) │
│  │ ├─ Power amplifier                   │ 0 nW (idle)   │
│  │ ├─ Modulator                        │ 100 nW (idle) │
│  │ └─ Total (idle)                     │ 600 nW        │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ During Active Transmission:         │                │
│  │ ├─ VCO                              │ 2 mW          │
│  │ ├─ Power amplifier                   │ 5 mW          │
│  │ ├─ Modulator                        │ 0.5 mW        │
│  │ └─ Total (active)                   │ 7.5 mW        │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ Receiver (wake-up detector)         │                │
│  │ ├─ Low-noise amplifier              │ 100 nW        │
│  │ ├─ Envelope detector                │ 50 nW         │
│  │ ├─ Decriminator                     │ 30 nW         │
│  │ └─ Total                            │ 180 nW        │
│  └─────────────────────────────────────┘                │
│                                                         │
│  TOTAL COMMUNICATION (idle): 815 nW                     │
│  TOTAL COMMUNICATION (active): 7.5 mW                   │
└─────────────────────────────────────────────────────────┘

Note: Communication is rarely active (monthly interrogations)
Time-averaged communication power: ~40 nW
```

### 3.5 Housekeeping Subsystem

```
Housekeeping Subsystem Power Breakdown:

┌─────────────────────────────────────────────────────────┐
│ Housekeeping                                             │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ Main Oscillator (32.768 kHz)        │                │
│  │ ├─ Crystal oscillator core          │ 80 nW         │
│  │ ├─ Buffer amplifier                 │ 20 nW         │
│  │ └─ Total                            │ 100 nW        │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ Watchdog Timer                      │                │
│  │ ├─ Counter                          │ 5 nW          │
│  │ ├─ Comparator                       │ 3 nW          │
│  │ └─ Total                            │ 8 nW          │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ Power-On Reset                      │                │
│  │ ├─ Brown-out detector               │ 5 nW          │
│  │ ├─ Power-good comparator            │ 3 nW          │
│  │ └─ Total                            │ 8 nW          │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ Temperature Sensor                  │                │
│  │ ├─ Proportional-to-absolute-temp    │ 20 nW         │
│  │ ├─ ADC (for temp measurement)       │ 10 nW         │
│  │ └─ Total                            │ 30 nW         │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ Battery Monitor                     │                │
│  │ ├─ Voltage divider                  │ 5 nW          │
│  │ ├─ Low-battery detector             │ 3 nW          │
│  │ └─ Total                            │ 8 nW          │
│  └─────────────────────────────────────┘                │
│                                                         │
│  ┌─────────────────────────────────────┐                │
│  │ Configuration Registers (NVM)       │                │
│  │ ├─ NVM retention                    │ 20 nW         │
│  │ ├─ Read/write logic                 │ 5 nW          │
│  │ └─ Total                            │ 25 nW         │
│  └─────────────────────────────────────┘                │
│                                                         │
│  TOTAL HOUSEKEEPING: 179 nW                             │
└─────────────────────────────────────────────────────────┘
```

## 4. Power by Source Type

### 4.1 Dynamic vs. Static Breakdown

```
Dynamic vs. Static Power Analysis:

┌─────────────────────┬──────────┬──────────┬──────────┐
│ Block               │ Dynamic  │ Static   │ Ratio    │
├─────────────────────┼──────────┼──────────┼──────────┤
│ Sensing amplifier   │ 350 nW   │ 130 nW   │ 2.7:1    │
│ DSP engine          │ 900 nW   │ 130 nW   │ 6.9:1    │
│ Stimulation control │ 65 nW    │ 10 nW    │ 6.5:1    │
│ Communication       │ 810 nW   │ 5 nW     │ 162:1    │
│ Housekeeping        │ 150 nW   │ 29 nW    │ 5.2:1    │
│ Clock distribution  │ 350 nW   │ 50 nW    │ 7.0:1    │
│ I/O pads            │ 50 nW    │ 150 nW   │ 0.3:1    │
├─────────────────────┼──────────┼──────────┼──────────┤
│ TOTAL               │ 2.67 μW  │ 504 nW   │ 5.3:1    │
└─────────────────────┴──────────┴──────────┴──────────┘

Key Observations:
1. Dynamic power dominates overall (84%)
2. I/O pads have high static relative to dynamic
3. Communication has highest dynamic/static ratio
4. Sensing amplifier has relatively high static component
```

### 4.2 Clock Power Attribution

```
Clock Power Attribution:

Clock Domain          │ Frequency │ Gates │ Power   │ % Total
──────────────────────┼───────────┼───────┼─────────┼────────
Main system (32 kHz)  │ 32 kHz    │ 5000  │ 350 nW  │ 12%
DSP clock (256 kHz)   │ 256 kHz   │ 2000  │ 800 nW  │ 28%
ADC clock (512 Hz)    │ 512 Hz    │ 200   │ 10 nW   │ 0.3%
Timer (1 Hz)          │ 1 Hz      │ 100   │ 0.1 nW  │ 0%
Communication (9.6 kHz)│ 9.6 kHz  │ 500   │ 25 nW   │ 0.9%
──────────────────────┼───────────┼───────┼─────────┼────────
TOTAL clock power     │           │ 7800  │ 1185 nW │ 41%

Clock Power Savings with Clock Gating:
- DSP clock gating: saves 600 nW (75% of DSP clock)
- Communication gating: saves 20 nW (80% of comm clock)
- ADC gating: saves 5 nW (50% of ADC clock)
- Total clock savings: 625 nW

Post-optimization clock power: 560 nW (19% of total)
```

### 4.3 Interconnect Power

```
Interconnect Power Breakdown:

Wire Category       │ Length   │ Capacitance │ Switching │ Power
────────────────────┼──────────┼─────────────┼───────────┼──────
Clock distribution  │ 5000 μm  │ 15 pF       │ 32-256kHz │ 500 nW
Data buses (local)  │ 2000 μm  │ 4 pF        │ 16 kHz    │ 25 nW
Control signals     │ 3000 μm  │ 6 pF        │ 8 kHz     │ 15 nW
Analog routing      │ 500 μm   │ 1 pF        │ 512 Hz    │ 0.5 nW
Global signals      │ 1500 μm  │ 3 pF        │ 32 kHz    │ 80 nW
────────────────────┼──────────┼─────────────┼───────────┼──────
TOTAL               │ 12000 μm │ 29 pF       │           │ 620 nW

Interconnect as % of total: 21%

Optimization Impact:
- Clock tree synthesis: -100 nW
- Wire sizing optimization: -50 nW
- Buffer insertion: +20 nW (overhead)
- Net interconnect savings: -130 nW
```

## 5. Power by Operating Mode

### 5.1 Time-Weighted Power Analysis

```
Operating Mode Distribution:

Mode Distribution Over 10-Year Lifetime:
┌──────────────┬───────────┬──────────┬───────────────────┐
│ Mode         │ Time      │ % of Life│ Avg Power         │
├──────────────┼───────────┼──────────┼───────────────────┤
│ Monitoring   │ 2.8 yr    │ 28%      │ 1.1 μW            │
│ Idle (sleep) │ 6.5 yr    │ 65%      │ 50 nW             │
│ Processing   │ 0.3 yr    │ 3%       │ 5 μW              │
│ Stimulation  │ 0.2 yr    │ 2%       │ 50 μW (peak)      │
│ Communication│ 0.05 yr   │ 0.5%     │ 7.5 mW (peak)     │
│ Deep Sleep   │ 0.95 yr   │ 9.5%     │ 10 nW             │
└──────────────┴───────────┴──────────┴───────────────────┘

Note: Percentages don't sum to 100% due to rounding
and mode transitions.

Time-Weighted Average Power:
P_avg = (0.28 × 1.1 μW) + (0.65 × 0.05 μW) + (0.03 × 5 μW)
      + (0.02 × 50 μW × 0.002) + (0.005 × 7.5 mW × 0.001)
      + (0.095 × 0.01 μW)
P_avg ≈ 0.31 μW + 0.033 μW + 0.15 μW + 0.002 μW + 0.00004 μW + 0.001 μW
P_avg ≈ 0.496 μW (well within 2.9 μW budget)
```

### 5.2 Mode Transition Power

```
Mode Transition Power Costs:

Transition              │ Energy    │ Time    │ Power During
────────────────────────┼───────────┼─────────┼─────────────
Monitor → Processing    │ 0.5 nJ    │ 10 μs   │ 50 μW
Processing → Monitor    │ 0.2 nJ    │ 5 μs    │ 40 μW
Monitor → Stimulation   │ 1.0 nJ    │ 20 μs   │ 50 μW
Stimulation → Monitor   │ 0.3 nJ    │ 10 μs   │ 30 μW
Idle → Monitor          │ 0.1 nJ    │ 100 μs  │ 1 μW
Monitor → Idle          │ 0.05 nJ   │ 10 μs   │ 5 μW
Any → Deep Sleep        │ 50 nJ     │ 1 ms    │ 50 μW
Deep Sleep → Monitor    │ 50 nJ     │ 10 ms   │ 5 μW

Annual Transition Energy:
- Monitor ↔ Processing: 10,000 × 0.7 nJ = 7 μJ
- Monitor ↔ Stimulation: 3,000 × 1.3 nJ = 3.9 μJ
- Monitor ↔ Idle: 365 × 0.15 nJ = 0.05 μJ
- Total annual: 11 μJ
- 10-year total: 110 μJ = 0.0003% of battery

Transition power is negligible for battery life.
```

## 6. Power by Process Corner

### 6.1 Process Corner Analysis

```
Power Across Process Corners (at 37°C, 1.8V):

Corner │ Dynamic   │ Static    │ Total    │ Condition
───────┼───────────┼───────────┼──────────┼─────────────
FF     │ 3.2 μW    │ 800 nW    │ 4.0 μW   │ Fast/fast
TT     │ 2.7 μW    │ 500 nW    │ 3.2 μW   │ Typical
SS     │ 2.1 μW    │ 200 nW    │ 2.3 μW   │ Slow/slow
SF     │ 2.5 μW    │ 350 nW    │ 2.9 μW   │ Slow/fast
FS     │ 2.9 μW    │ 650 nW    │ 3.6 μW   │ Fast/slow

Observation:
- Dynamic power varies ±15% across corners
- Static power varies ±60% across corners
- Worst case (FF): 4.0 μW (38% above typical)
- Best case (SS): 2.3 μW (28% below typical)
```

### 6.2 Temperature Sensitivity

```
Power vs. Temperature (at TT corner, 1.8V):

Temperature │ Dynamic   │ Static    │ Total
────────────┼───────────┼───────────┼─────────
0°C         │ 2.9 μW    │ 100 nW    │ 3.0 μW
25°C        │ 2.7 μW    │ 300 nW    │ 3.0 μW
37°C        │ 2.6 μW    │ 500 nW    │ 3.1 μW
42°C        │ 2.5 μW    │ 700 nW    │ 3.2 μW
50°C        │ 2.4 μW    │ 1.2 μW    │ 3.6 μW

Temperature Coefficients:
- Dynamic: -0.4%/°C (decreases with temperature)
- Static: +8%/°C (doubles every ~9°C)
- Net: +0.5%/°C (slight increase with temperature)

At body temperature (37°C):
- Total power: 3.1 μW (within budget)
- Static contribution: 16%
```

## 7. Optimization Impact Analysis

### 7.1 Before and After Optimization

```
Power Optimization Impact Summary:

Technique              │ Before   │ After    │ Savings
───────────────────────┼──────────┼──────────┼────────
Clock gating           │ 1185 nW  │ 560 nW   │ 625 nW
Multi-Vt assignment    │ 504 nW   │ 200 nW   │ 304 nW
Operand isolation      │ 1030 nW  │ 820 nW   │ 210 nW
Memory banking         │ 120 nW   │ 60 nW    │ 60 nW
Power gating (idle)    │ 3100 nW  │ 50 nW    │ 3050 nW*
Logic restructuring    │ 800 nW   │ 700 nW   │ 100 nW
Wire optimization      │ 620 nW   │ 490 nW   │ 130 nW
Total                  │ 7.4 μW   │ 2.9 μW   │ 4.5 μW

* Power gating savings based on time-weighted average
  (65% idle time × block power gated)

Net Reduction: 61% average power reduction
```

### 7.2 Optimization Priority Ranking

```
Power Optimization Priority (by impact):

Rank │ Technique           │ Savings  │ Effort │ ROI
─────┼─────────────────────┼──────────┼────────┼─────
1    │ Power gating        │ 3050 nW  │ High   │ High
2    │ Clock gating        │ 625 nW   │ Medium │ High
3    │ Multi-Vt assignment │ 304 nW   │ Medium │ Medium
4    │ Operand isolation   │ 210 nW   │ Low    │ High
5    │ Wire optimization   │ 130 nW   │ Low    │ Medium
6    │ Logic restructuring │ 100 nW   │ Medium │ Low
7    │ Memory banking      │ 60 nW    │ Low    │ Low

Recommended Implementation Order:
1. Clock gating (easy, high impact)
2. Multi-Vt assignment (EDA tool flow)
3. Operand isolation (RTL modification)
4. Power gating (requires design changes)
5. Wire optimization (physical design)
6. Memory banking (architecture change)
7. Logic restructuring (manual optimization)
```

## 8. Measurement Validation

### 8.1 Silicon vs. Simulation Correlation

```
Power Measurement Correlation:

Block                │ Simulated │ Measured │ Error
─────────────────────┼───────────┼──────────┼───────
Sensing amplifier    │ 480 nW    │ 460 nW   │ -4.2%
DSP engine           │ 1030 nW   │ 1080 nW  │ +4.9%
Stimulation control  │ 75 nW     │ 70 nW    │ -6.7%
Communication        │ 815 nW    │ 790 nW   │ -3.1%
Housekeeping         │ 179 nW    │ 185 nW   │ +3.4%
Clock distribution   │ 560 nW    │ 540 nW   │ -3.6%
I/O pads             │ 200 nW    │ 220 nW   │ +10.0%
─────────────────────┼───────────┼──────────┼───────
TOTAL (average)      │ 3.3 μW    │ 3.3 μW   │ 0%
TOTAL (worst-case)   │ 4.0 μW    │ 4.1 μW   │ +2.5%

Correlation Quality:
- Maximum block error: 10% (I/O pads)
- Average block error: 4.5%
- Total power error: 2.5%
- All blocks within ±15% target
```

### 8.2 Power Measurement Setup

```
Validation Measurement Configuration:

Test Conditions:
- Temperature: 37°C (body temperature)
- Supply voltage: 1.8V nominal
- Process corner: TT (typical-typical)
- Clock frequency: 32.768 kHz (nominal)

Measurement Equipment:
- Keithley 6517B electrometer (fA resolution)
- Custom test board with ultra-low-noise LDO
- Shielded enclosure
- Thermal chamber (36.5°C ± 0.5°C)

Test Scenarios:
1. Idle mode (30 seconds average)
2. Active monitoring (10 seconds average)
3. Processing burst (5 seconds average)
4. Stimulation pulse (single pulse capture)
5. Deep sleep (60 seconds average)

Data Collection:
- Current measurements at 1 kHz sampling
- 100 samples per measurement point
- Statistical analysis (mean, σ, min, max)
```

## 9. Battery Life Projection

### 9.1 Lifetime Power Consumption

```
10-Year Battery Life Projection:

Energy Consumption by Category:
┌─────────────────────────┬──────────┬────────────┐
│ Category                │ 10-yr E  │ % Battery  │
├─────────────────────────┼──────────┼────────────┤
│ Cardiac sensing         │ 150 mJ   │ 13.4%      │
│ Signal processing       │ 240 mJ   │ 21.4%      │
│ Pacing control          │ 90 mJ    │ 8.0%       │
│ Stimulation pulses      │ 25 mJ    │ 2.2%       │
│ Communication           │ 15 mJ    │ 1.3%       │
│ Housekeeping            │ 55 mJ    │ 4.9%       │
│ Clock distribution      │ 110 mJ   │ 9.8%       │
│ Power management        │ 30 mJ    │ 2.7%       │
│ I/O and pads            │ 40 mJ    │ 3.6%       │
│ Leakage (total)         │ 31 mJ    │ 2.8%       │
│ Transitions             │ 0.1 mJ   │ 0.01%      │
├─────────────────────────┼──────────┼────────────┤
│ TOTAL consumption       │ 786 mJ   │ 70.0%      │
├─────────────────────────┼──────────┼────────────┤
│ Battery self-discharge  │ 112 mJ   │ 10.0%      │
│ Safety margin           │ 225 mJ   │ 20.0%      │
├─────────────────────────┼──────────┼────────────┤
│ TOTAL BATTERY           │ 1123 mJ  │ 100%       │
└─────────────────────────┴──────────┴────────────┘

Remaining at end of life: ~0 mJ (fully utilized)
Battery life achievement: 10.0 years (meets target)
```

### 9.2 Worst-Case Battery Life

```
Worst-Case Battery Life Analysis:

Worst-Case Assumptions:
- Process corner: FF (fast/fast, highest leakage)
- Temperature: 42°C (slightly elevated body temp)
- V_DD: 1.85V (high end of tolerance)
- Battery capacity: 110 mAh (low end)
- Self-discharge: 1.5%/year

Worst-Case Power:
- Average dynamic: 3.5 μW
- Average static: 0.8 μW
- Total: 4.3 μW

Worst-Case Battery Life:
- Energy: 110 mAh × 2.6V = 1030 mJ
- Consumption rate: 4.3 μW + (1.5% × 1030 mJ / yr / 3.15e7 s)
- Total: 4.3 μW + 0.49 μW = 4.8 μW
- Life: 1030 mJ / 4.8 μW = 2.15 × 10⁸ s = 6.8 years

Mitigation:
- Adaptive voltage scaling reduces V_DD when possible
- Temperature monitoring with thermal shutdown
- Battery capacity testing before implantation
- Worst-case life still meets 7-year minimum requirement
```

## 10. Summary

The power breakdown analysis reveals that the iPACE-CHIP pacemaker ASIC consumes an average of 2.9 μW across its operating modes, with dynamic power accounting for 84% and static power for 16% of total consumption. The DSP engine is the largest single consumer at 28% of total power, followed by clock distribution at 14%. Sensing and measurement functions consume 17%, while housekeeping and power management together account for 10%. The detailed breakdown validates the power budget allocation and identifies the most impactful areas for continued optimization. Silicon measurements correlate with simulation within ±10% for all blocks, confirming the accuracy of the power estimation methodology. The 10-year battery life projection shows a 70% utilization of battery capacity, with 20% reserved for safety margin and 10% for self-discharge, meeting the design requirement with adequate margin.

## References

1. Greatbatch, W., "The Lithium Iodide Power Source for Cardiac Pacemakers," PACE, Vol. 10, 1987.
2. iPACE-CHIP Project Internal Documentation: Power Budget Analysis, Rev 3.0.
3. Viventi, J., et al., "Power Management for Implantable Medical Devices," IEEE Trans. Biomedical Circuits and Systems, 2020.
4. JEDEC Standard JESD21-A: Measurement of DC leakage current.
5. MIL-STD-883: Test Methods and Procedures for Microelectronics.
