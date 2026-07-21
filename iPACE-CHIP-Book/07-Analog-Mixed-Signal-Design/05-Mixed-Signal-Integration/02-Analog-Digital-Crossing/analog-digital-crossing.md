# Analog-Digital Boundary Crossing Techniques

## Overview

The analog-digital boundary is where continuous-time analog signals meet discrete-time digital processing in the iPACE-CHIP. This interface includes ADCs, DACs, level shifters, and clock domain crossing circuits. Proper design of these crossing points is critical because errors at the boundary—metastability, timing violations, charge injection, and clock feedthrough—can corrupt both analog and digital signals, potentially causing pacing errors or incorrect cardiac sensing.

## ADC Interface

### ADC Output to Digital Domain

```
ADC digital output interface:

  SAR ADC Output                    Digital Controller
  +-----------+                    +-----------+
  | Dout[11:0]|---+    +---------->| Data Reg  |
  +-----------+   |    |           +-----------+
                  |    |
  +-----------+   |    |           +-----------+
  | Conv_DONE |---+----+---------->| IRQ Handler|
  +-----------+   |    |           +-----------+
                  |    |
  +-----------+   |    |           +-----------+
  | CLK_ADC   |---+----+---------->| Clock Mux |
  +-----------+        |           +-----------+
                       |
                  Clock Domain
                  Crossing (CDC)

Synchronization requirements:
  - Conv_DONE is asynchronous to digital clock
  - Must be synchronized with 2 flip-flops
  - Metastability MTBF > 10 years
```

### Metastability Prevention

```
2-flip-flop synchronizer:

  Async signal ──> [FF1] ──> [FF2] ──> Synced output
                    |          |
                  CLK_dig    CLK_dig

MTBF calculation:
  MTBF = 1 / (f_clock x f_async x T_co x tau)
  
  Where:
  f_clock = digital clock = 1 MHz
  f_async = ADC conversion rate = 2 kHz
  T_co = clock-to-output time = 1 ns
  tau = metastability time constant = 50 ps
  
  MTBF = 1 / (1e6 x 2e3 x 1e-9 x 50e-12)
  MTBF = 1 / (1e-13) = 10^13 seconds = 317,000 years ✓
```

### Multi-Bit CDC

```
Multi-bit signal crossing (12-bit ADC data):

Problem: Multiple bits may change simultaneously
  Risk: Glitches during transition (only some bits update)

Solution 1: Gray code encoding
  - Convert binary to Gray code at ADC output
  - Only 1 bit changes per code transition
  - Synchronize each Gray-coded bit
  
  Binary: 011 -> 100 (3 bits change!)
  Gray:   010 -> 110 (1 bit changes) ✓

Solution 2: Handshake-based transfer
  - ADC writes data to async FIFO
  - Digital reads from FIFO with handshake
  - No data corruption possible
  
  ADC ----[FIFO]---- Digital
           |
        [Full] [Empty]
        flags
```

## DAC Interface

### Digital Control to DAC

```
Digital-to-analog interface:

  Digital Controller                  DAC
  +-----------+                    +-----------+
  | DAC_CODE  |---+    +--------->| Input Reg |
  | [7:0]     |   |    |          +-----------+
  +-----------+   |    |
                  |    |          +-----------+
  +-----------+   |    +--------->| Current   |
  | DAC_EN    |---+               | Source    |
  +-----------+                    | Array     |
                                   +-----------+

Critical timing:
  - DAC code must be stable before enable
  - Setup time: > 1 clock cycle
  - Hold time: > 1 clock cycle
  
  CLK_dig:  ──┐  ┌──┐  ┌──
              └──┘  └──┘
  DAC_CODE:  ──XXXXXXXXXX──  (must be stable)
  DAC_EN:    ──────┐  ┌────  (pulse to load)
                   └──┘
```

### Clock Feedthrough Mitigation

```
DAC switching transients:

When DAC code changes:
  - Charge injection from switches
  - Clock feedthrough to output
  - Power supply bounce

Mitigation techniques:

1. Return-to-zero coding:
   Code: N -> 0 -> M (instead of N -> M)
   Glitch occurs at zero level (smaller amplitude)
   
2. Synchronized switching:
   All DAC elements switch at same clock edge
   Minimizes code-dependent glitches
   
3. Bottom-plate sampling:
   Open bottom plate of sampling cap first
   Reduces charge injection by ~50%
   
4. Dummy switches:
   Complementary switches inject opposite charge
   Net charge injection = 0
```

## Level Shifting

### Voltage Domain Crossing

```
Level shifter for mixed-voltage design:

  1.8V Domain          5V Domain
  (Digital)            (Pacing Output)
  
  Logic ──>+----------+──> Level ──> Logic
           | Shifter  |
  1.8V ───>+----------+──> 5V
  
  Level shifter types:
  
  1. Simple inverter chain:
     VDD_L (1.8V) ─┬─ M1 ─┬─ M3 ─┬─ VDD_H (5V)
                    │       │       │
     Input ────────┤M2     │M4     │
                    │       │       │
     GND ──────────┴───────┴───────┘
     
  2. Current-mirror level shifter:
     - Low static power
     - Adequate speed (10 MHz)
     
  3. Pulse-based level shifter:
     - Very low power
     - Good for slow signals (< 1 MHz)
```

### Bi-Directional Level Shifting

```
Bi-directional level shifter:

  A (1.8V) <---> B (5V)
  
  Implementation:
  +---+---+---+
  |   |   |   |
  +---+---+---+
  |         |
  A (1.8V) B (5V)
  
  Uses weak feedback inverters
  Automatically determines direction
  
  For iPACE-CHIP:
  - ADC output: 1.8V to 1.8V (no level shift needed)
  - DAC control: 1.8V to 1.8V (no level shift needed)
  - Pacing output: 1.8V to 5V (level shift needed)
  - Telemetry: 1.8V to 1.8V (no level shift needed)
```

## Clock Domain Crossing

### Multi-Clock Architecture

```
iPACE-CHIP clock domains:

  +-----------+
  | 32 kHz    |  <- Low-frequency oscillator (always on)
  | (RTC)     |
  +-----+-----+
        |
        v
  +-----------+     +-----------+
  | 256 kHz   |---->| 1 MHz     |  <- ADC clock
  | (Main osc)|     | (divided) |
  +-----------+     +-----------+
        |
        v
  +-----------+
  | 10 MHz    |  <- SPI interface clock (external)
  | (Telemetry)|
  +-----------+

Crossing requirements:
  - 32 kHz to 256 kHz: Synchronizer (async)
  - 256 kHz to 1 MHz: Synchronizer (async)
  - 1 MHz to 10 MHz: Synchronizer (async)
  - All domains share common reset
```

### Async FIFO Design

```
Async FIFO for multi-clock data transfer:

  Write Domain          Read Domain
  +-----------+        +-----------+
  | Write     |        | Read      |
  | Pointer   |        | Pointer   |
  +-----------+        +-----------+
       |                     |
       v                     v
  +-----------+        +-----------+
  | Binary to |        | Binary to |
  | Gray      |        | Gray      |
  +-----------+        +-----------+
       |                     |
       v                     v
  +-----------+        +-----------+
  | Write     |        | Read      |
  | Logic     |        | Logic     |
  +-----------+        +-----------+
       |                     |
       +--------+------------+
                |
           +----+----+
           | Memory  |
           | Array   |
           | (N x W) |
           +----+----+

  FIFO depth: 4-8 entries
  Pointer width: 3 bits (for 8 entries)
  Data width: 12 bits (ADC data)
  Gray code: Prevents multi-bit glitches
```

## Sampling Interface

### Analog Input Sampling

```
S/H circuit at ADC input:

  Analog Input ──[R_s]──┬──[M1]──┬── V_sh
                        |         |
                       ===       ===
                       C_s       C_h
                        |         |
                       GND       GND

  M1: Sampling switch (CMOS transmission gate)
  R_s: Source resistance (from PGA)
  C_s: Parasitic capacitance
  C_h: Hold capacitor (5 pF)

Sampling phases:
  
  Sample (CLK=1):
    M1 ON, V_sh tracks Vin
    Time constant: tau = R_s x C_h
    For R_s = 10 kohm, C_h = 5 pF: tau = 50 ns
    Acquisition time (0.01%): 10 x tau = 500 ns
    
  Hold (CLK=0):
    M1 OFF, V_sh holds value
    Droop: dV/dt = I_leak / C_h
    For I_leak = 100 pA: dV/dt = 20 mV/ms
    During 12 us conversion: droop = 0.24 mV (< 0.5 LSB) ✓
```

### Clock Feedthrough in S/H

```
Charge injection during sampling switch turn-off:

  Q_inj = C_ox x W x L x (V_clk - V_th - V_input)
  
  For 180nm NMOS switch:
  C_ox = 8.5 fF/um^2
  W/L = 2/0.18
  V_clk = 1.8V
  V_th = 0.4V
  V_input = 0.9V (mid-rail)
  
  Q_inj = 8.5e-15 x 2 x 0.18 x (1.8 - 0.4 - 0.9)
  Q_inj = 8.5e-15 x 0.36 x 0.5
  Q_inj = 1.53e-15 C = 1.53 fC
  
  Voltage error: V_err = Q_inj / C_h
  V_err = 1.53e-15 / 5e-12 = 0.306 mV = 0.13 LSB ✓
  
  With CMOS transmission gate (charge cancellation):
  V_err = 0.306 x 0.1 = 0.03 mV (< 0.01 LSB) ✓
```

## Reset and Initialization

### Power-On Reset (POR)

```
POR circuit for mixed-signal design:

  VDD ──[R1]──┬──[R2]──┬── POR_n
               |         |
              ===        |
              C1         |
               |         |
             GND        GND

  Timing:
  - R1 = 100 kohm, R2 = 100 kohm
  - C1 = 1 pF
  - Delay = R1 x C1 x ln(2) = 100 ns
  
  POR_n goes high when VDD > V_th (1.0V typical)
  
  Sequence:
  1. VDD rises from 0V
  2. POR_n stays low (reset active)
  3. VDD reaches 1.0V
  4. After 100 ns delay, POR_n goes high
  5. Digital logic releases from reset
  6. Analog bias circuits start up
```

### Analog Startup Sequence

```
Analog circuit startup:

Phase 1 (0-100 us): Power-on reset
  - All digital registers cleared
  - Analog bias disabled
  - DAC outputs at zero
  
Phase 2 (100-500 us): Bias generation
  - Bandgap reference starts
  - Bias currents stabilize
  - Reference voltages settle
  
Phase 3 (500 us - 1 ms): Calibration
  - ADC self-calibration
  - DAC offset measurement
  - PGA gain verification
  
Phase 4 (> 1 ms): Normal operation
  - Sensing and pacing enabled
  - Digital controller active
  - Telemetry interface ready

Total startup time: < 2 ms
```

## Summary

| Interface | Technique | Key Requirement |
|-----------|-----------|-----------------|
| ADC to digital | 2-FF synchronizer | MTBF > 100 years |
| Digital to DAC | Gray code / handshake | Glitch-free transfer |
| Voltage domains | Level shifter | Proper logic levels |
| Clock domains | Async FIFO | No data corruption |
| Analog sampling | S/H with CMOS switch | < 0.5 LSB charge injection |
| Reset | POR with delay | Clean startup sequence |

Proper design of analog-digital boundary crossings ensures reliable operation of the iPACE-CHIP mixed-signal system, preventing errors that could compromise patient safety.
