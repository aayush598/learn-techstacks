# Multi-Energy Pulse Generation

## Overview

Multi-energy pulse generation enables the iPACE-CHIP to deliver pacing stimuli with programmable energy levels, optimizing the strength-duration trade-off for cardiac stimulation. By varying amplitude, pulse width, and waveform shape across multiple energy settings, the pacemaker can automatically select the most efficient pacing parameters—minimizing battery drain while maintaining reliable capture. This chapter covers the circuit techniques for generating pulses at different energy levels and the adaptive algorithms that select optimal parameters.

## Strength-Duration Relationship

### Lapicque Strength-Duration Curve

```
Strength-duration curve for cardiac tissue:

  Amplitude
  (mA or V)
      ^
      |
  20  |\
      | \
      |  \
  15  |   \
      |    \
      |     \______
  10  |           \
      |            \________
   5  |                     \________
      |                              \________
   0  +----+----+----+----+----+----+----+---> Pulse Width
      0  0.1  0.2  0.3  0.5  1.0  1.5  2.0  (ms)

Key points:
  Rheobase (I_rh): Minimum current for infinitely long pulse
    I_rh = 2.5 mA (typical)
    
  Chronaxie (t_ch): Pulse width at 2x rheobase current
    t_ch = 0.3 ms (typical)
    
  Threshold at t_ch: 5.0 mA
    
Mathematical model:
  I_threshold(t) = I_rh / (1 - exp(-t_ch/t))
  
  For t = 0.1 ms: I = 2.5 / (1 - exp(-3)) = 2.64 mA
  For t = 0.3 ms: I = 2.5 / (1 - exp(-1)) = 3.93 mA
  For t = 1.0 ms: I = 2.5 / (1 - exp(-0.3)) = 8.33 mA
  
Wait, the formula is:
  I_threshold(t) = I_rh x (1 + t_ch/t) / 2
  
  Actually, the standard Weiss formula:
  I = a + b/t
  
  Where a = rheobase, b = chronaxie constant
  I = I_rh x (1 + t_ch/t)
  
  For t = 0.1 ms: I = 2.5 x (1 + 3) = 10 mA
  For t = 0.3 ms: I = 2.5 x (1 + 1) = 5 mA (at chronaxie)
  For t = 1.0 ms: I = 2.5 x (1 + 0.3) = 3.25 mA
```

### Energy Optimization

```
Energy delivered per pulse:

  E = V x I x t (for rectangular pulse)
  E = I^2 x R x t (for current source through R)

Optimal energy point:
  dE/dt = 0 (minimum energy for capture)

  For Weiss model:
  E_opt occurs at t_opt = t_ch (chronaxie)
  
  At t = t_ch = 0.3 ms:
  I = 5.0 mA (2x rheobase)
  E = 5.0^2 x 500 x 0.3e-3 = 3.75 mW x 0.3 ms = 3.75 uJ
  
  At t = 1.0 ms (longer pulse):
  I = 3.25 mA
  E = 3.25^2 x 500 x 1.0e-3 = 5.28 uJ (41% more energy!)
  
  At t = 0.1 ms (shorter pulse):
  I = 10.0 mA
  E = 10.0^2 x 500 x 0.1e-3 = 5.0 mW x 0.1 ms = 5.0 uJ (33% more)
  
Conclusion: Pulsing at chronaxie minimizes energy ✓
```

## Multi-Energy Architecture

### Programmable Energy Levels

```
Energy level table:

Level │ Pulse Width │ Current │ Voltage │ Energy  │ Use Case
──────┼─────────────┼─────────┼─────────┼─────────┼──────────────
1     │ 0.1 ms      │ 10 mA   │ 5.0V    │ 5.0 uJ  │ Emergency
2     │ 0.2 ms      │ 6.5 mA  │ 3.25V   │ 4.2 uJ  │ High threshold
3     │ 0.3 ms      │ 5.0 mA  │ 2.5V    │ 3.75 uJ │ Optimal (chronaxie)
4     │ 0.5 ms      │ 4.0 mA  │ 2.0V    │ 4.0 uJ  │ Normal pacing
5     │ 1.0 ms      │ 3.0 mA  │ 1.5V    │ 4.5 uJ  │ Low threshold
6     │ 1.5 ms      │ 2.5 mA  │ 1.25V   │ 4.69 uJ │ Minimum current

Energy savings by operating at optimal level:
  Level 3 vs Level 6: 3.75 uJ vs 4.69 uJ = 20% savings
  Over 10 years at 70 bpm:
    Total saved = 20% x 4.69 uJ x 70 x 60 x 24 x 365 x 10
    Total saved = 0.94 x 1.48e9 = 1.39 MJ = 386 mAh at 3V
    This is significant battery life improvement!
```

### DAC-Based Amplitude Control

```
Current amplitude DAC for multi-energy:

  +-----+-----+-----+-----+-----+-----+-----+-----+
  | I/128| I/64 | I/32 | I/16 | I/8  | I/4  | I/2  | I   |
  | D0   | D1   | D2   | D3   | D4   | D5   | D6   | D7  |
  +--+---+--+---+--+---+--+---+--+---+--+---+--+---+--+---+
     |      |      |      |      |      |      |      |
     v      v      v      v      v      v      v      v
  +-----------------------------------------------------------+
  |              Current Summing Node                         |
  +-----------------------------------------------------------+
                              |
                         I_out (to lead)

  Binary-weighted current sources:
  I_unit = 78.1 uA (LSB)
  I_max = 255 x 78.1 uA = 19.9 mA (MSB full scale)
  
  For Level 3 (5.0 mA):
  Code = 5000 uA / 78.1 uA = 64 = 0x40
  D7=0, D6=1, D5=0, D4=0, D3=0, D2=0, D1=0, D0=0
```

### Pulse Width DAC

```
Pulse width timer with fine resolution:

  Timer clock: 1 MHz (1 us period)
  Resolution: 1 us per count
  
  For Level 3 (0.3 ms):
  PW_code = 300 us / 1 us = 300 counts
  Timer width: 9 bits (512 max)
  
  For Level 1 (0.1 ms):
  PW_code = 100 us / 1 us = 100 counts
  
  For Level 6 (1.5 ms):
  PW_code = 1500 us / 1 us = 1500 counts
  Timer width: 11 bits (2048 max)

Programmable timer:
  +------------------+
  | PW_code[10:0]   |  <- From control register
  +------------------+
           |
           v
  +------------------+
  | Down Counter     |  <- Counts down from PW_code
  | (11-bit)         |
  +------------------+
           |
           v
  +------------------+
  | Zero Detector    |  <- Generates PW_DONE when count = 0
  +------------------+
           |
           v
  +------------------+
  | Output Control   |  <- Controls pacing output switch
  +------------------+
```

## Adaptive Energy Selection

### Threshold Search Algorithm

```
Auto-capture threshold search:

  1. Start at Level 4 (normal pacing)
  2. If capture confirmed:
     Try lower energy level (reduce by 1)
  3. If no capture:
     Increase energy level by 2 (safety margin)
  4. Repeat until optimal level found
  
  +-----------+
  | Start at  |
  | Level 4   |
  +-----------+
       |
       v
  +-----------+     +-----------+
  | Pace at   |---->| Capture?  |
  | current   |     |           |
  | level     |     +-----------+
  +-----------+     |     |     |
                    | Yes | No  |
                    v     v     |
  +-----------+  +-----------+ +-----------+
  | Try lower |  | Maintain  | | Increase  |
  | level     |  | level     | | by 2      |
  +-----------+  +-----------+ +-----------+
       |              |              |
       +--------------+--------------+
                      |
                      v
                 +-----------+
                 | Next      |
                 | pacing    |
                 | cycle     |
                 +-----------+
  
  Search time: < 10 pacing cycles (1.5 seconds at 70 bpm)
  Safety margin: Always pace 2 levels above threshold
```

### Capture Detection

```
Capture verification after pacing:

Method 1: Evoked Response Sensing
  1. Pace cardiac tissue
  2. Wait 50 ms (blanking period)
  3. Sense for R-wave or P-wave
  4. If detected: capture confirmed
  5. If not detected: no capture

Method 2: Impedance Measurement
  1. Pace with test pulse (100 uA, 10 us)
  2. Measure voltage across lead
  3. Calculate impedance
  4. Impedance drop = tissue capture (electrode polarization)

Method 3: ST-Segment Analysis
  1. Pace cardiac tissue
  2. Wait 100 ms
  3. Sense ST-segment on electrogram
  4. ST elevation = capture confirmed

iPACE-CHIP uses Method 1 (evoked response) as primary
Method 2 (impedance) as backup
```

## Waveform Shapes

### Rectangular vs Truncated Exponential

```
Rectangular pulse:

  V
  ^
  |    +--------+
  |    |        |
  |    |        |
  |    |        |
  +----+        +----> t
  
  Energy: E = V x I x t (constant amplitude)
  Tissue response: Uniform stimulation
  
Truncated exponential pulse:

  V
  ^
  |  \
  |   \
  |    \
  |     \________
  |              |
  +--------------+----> t
  
  Energy: E = (V0^2 x C) / 2 x (1 - exp(-2t/RC))
  Tissue response: Front-loaded stimulation
  
  Advantages of truncated exponential:
  - Simpler circuit (capacitor discharge)
  - Lower peak current (reduces tissue damage)
  - More efficient for high-impedance leads
```

### Programmable Waveform Shapes

```
Waveform shape control:

  Shape register: 4 bits (16 shapes)
  
  0x0: Rectangular (constant amplitude)
  0x1: Truncated exponential (tau = 200 us)
  0x2: Truncated exponential (tau = 500 us)
  0x3: Truncated exponential (tau = 1000 us)
  0x4: Linear ramp up (100 us rise)
  0x5: Linear ramp down (100 us fall)
  0x6: Biphasic rectangular
  0x7: Biphasic exponential
  0x8: Triphasic
  0x9-0xF: Reserved (custom shapes via LUT)

Implementation:
  +-------------------+
  | Waveform LUT      |  <- 256 x 8-bit lookup table
  | (stores V(t)      |     Programmed at power-up
  |  waveform)        |
  +-------------------+
           |
           v
  +-------------------+
  | DAC               |  <- Outputs voltage at each time step
  | (8-bit, 1 MHz)    |
  +-------------------+
           |
           v
  +-------------------+
  | Output Stage      |  <- Drives lead with shaped waveform
  +-------------------+
```

## Power Considerations

### Energy Budget

```
Multi-energy pacing power analysis:

At Level 3 (optimal, 70 bpm):
  E_per_pulse = 3.75 uJ
  P_pacing = 3.75 uJ x 70/60 = 4.375 uW
  P_overhead = 0.5 uW (DAC, timers, control)
  Total = 4.875 uW

At Level 5 (conservative):
  E_per_pulse = 4.5 uJ
  P_pacing = 4.5 uJ x 70/60 = 5.25 uW
  P_overhead = 0.5 uW
  Total = 5.75 uW

Savings from optimal energy selection:
  (5.75 - 4.875) / 5.75 = 15.2%
  
  Over 10-year battery life:
  15.2% x 10 years x 365 x 24 x 3600 x 5.75 uW
  = 15.2% x 1.81 kJ = 275 J = 76.4 mAh at 3V
  
  This is 7.6% of total battery capacity (1 Ah)
```

### Charge Pump Efficiency

```
Charge pump efficiency at different energy levels:

Level │ V_out │ I_out │ P_out  │ Efficiency │ P_input
──────┼───────┼───────┼────────┼────────────┼────────
1     │ 5.0V  │ 10 mA │ 50 mW  │ 45%        │ 111 mW
2     │ 3.25V │ 6.5mA │ 21.1mW │ 50%        │ 42.2 mW
3     │ 2.5V  │ 5.0mA │ 12.5mW │ 55%        │ 22.7 mW
4     │ 2.0V  │ 4.0mA │ 8.0 mW │ 58%        │ 13.8 mW
5     │ 1.5V  │ 3.0mA │ 4.5 mW │ 60%        │ 7.5 mW
6     │ 1.25V │ 2.5mA │ 3.1mW  │ 62%        │ 5.0 mW

Efficiency improves at lower output voltages
(due to lower switching losses relative to output power)

Optimal operation: Level 3-4 for best efficiency/energy trade-off
```

## Layout Considerations

```
Multi-energy pulse generator layout:

+-------------------------------------------+
|       Multi-Energy Pulse Generator        |
|                                           |
|  +------------------+                    |
|  | Amplitude DAC    |                    |
|  | (8-bit, binary   |                    |
|  |  weighted)       |                    |
|  +------------------+                    |
|                                           |
|  +------------------+                    |
|  | Pulse Width      |                    |
|  | Timer            |                    |
|  | (11-bit counter) |                    |
|  +------------------+                    |
|                                           |
|  +------------------+                    |
|  | Waveform LUT     |                    |
|  | (256 x 8-bit)    |                    |
|  +------------------+                    |
|                                           |
|  +------------------+                    |
|  | Adaptive Control |                    |
|  | FSM              |                    |
|  +------------------+                    |
|                                           |
|  +------------------+                    |
|  | Output Stage     | <- High current    |
|  | (power transistors)|   path (wide metal)|
|  +------------------+                    |
|                                           |
|  ++++ Guard Ring ++++                    |
+-------------------------------------------+

Key considerations:
- DAC current sources: matched placement
- Output stage: wide metal for high current
- Waveform LUT: close to DAC for fast access
- Control FSM: separate from analog blocks
```

## Summary

| Parameter | Value |
|-----------|-------|
| Energy levels | 6 programmable |
| Amplitude range | 2.5 - 10 mA (current mode) |
| Pulse width range | 0.1 - 1.5 ms |
| Energy range | 3.75 - 5.0 uJ |
| Optimal energy | 3.75 uJ (at chronaxie) |
| Waveform shapes | 9 built-in + custom LUT |
| Adaptive selection time | < 1.5 seconds |
| Energy savings (optimal vs conservative) | 15-20% |
| Battery life improvement | 7-8% |
| DAC resolution | 8 bits (amplitude) |
| Timer resolution | 1 us (pulse width) |
| Power (average, optimal) | 4.875 uW |
| Technology | 180 nm CMOS |

Multi-energy pulse generation enables the iPACE-CHIP to optimize pacing efficiency by automatically selecting the lowest-energy parameters that reliably capture cardiac tissue, significantly extending battery life over the 10-year implant duration.
