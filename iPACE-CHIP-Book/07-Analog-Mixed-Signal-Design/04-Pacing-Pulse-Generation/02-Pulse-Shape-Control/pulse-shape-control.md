# Pulse Shape Control for Cardiac Pacing

## Overview

Pulse shape control determines the waveform characteristics of pacing stimuli delivered to cardiac tissue. The iPACE-CHIP must generate precisely controlled pulse shapes including amplitude, width, rise/fall times, and biphasic waveforms. Different clinical scenarios require different pulse morphologies—exponential decay for threshold testing, rectangular for chronic pacing, and charge-balanced biphasic for lead preservation.

## Pulse Waveform Types

### Monophasic Rectangular

```
Monophasic rectangular pulse:

  V (or I)
  ^
  |    +--------+
  |    |        |
  |    |        |
  |    |        |
  +----+        +-----> t
  0   t_rise  t_pw

  Parameters:
  t_rise: Rise time (< 10 us)
  t_pw: Pulse width (0.05 - 1.5 ms)
  V_amp: Amplitude (0.5 - 7.5 V)
  
  Most common waveform for permanent pacing
  Simple to generate with digital DAC + switch
```

### Monophasic Exponential

```
Monophasic exponential (capacitor discharge):

  V (or I)
  ^
  |  \
  |   \
  |    \        <- Exponential decay
  |     \
  |      \__________
  +------------------> t
  0    tau    2*tau

  V(t) = V0 x exp(-t/tau)
  
  tau = R_lead x C_discharge
  
  Used for:
  - Threshold testing (measure strength-duration)
  - Maximum energy delivery with simple circuit
  - Defibrillation pulses (with much larger C)
```

### Biphasic Waveform

```
Biphasic charge-balanced pulse:

  V (or I)
  ^
  |    +--------+
  |    | Phase 1|
  |    | (cath.)|
  +----+        +-----> t
  |              |
  |              |
  |    +--------+
  |    | Phase 2|
  |    | (anod.)|
  |    |        |
  |    +--------+
  |    |        |
  v    |        |

  Phase 1: Cathodal stimulation (delivers therapy)
  Phase 2: Anodal recovery (removes residual charge)
  
  Charge balance: Q1 + Q2 = 0
  I1 x t1 + I2 x t2 = 0
  
  Typically: I2 = I1/10, t2 = 10 x t1
  
  Benefits:
  - Prevents tissue damage from DC current
  - Reduces electrode polarization
  - Extends electrode lifetime
  - Lower chronic stimulation threshold
```

### Triphasic Waveform

```
Triphasic pulse (advanced):

  V (or I)
  ^
  |    +--------+
  |    | Phase 1|
  +----+        +-----> t
  |              |
  |    +--------+
  |    | Phase 2|  <- Charge recovery
  |    |        |
  +----+        +
  |              |
  |    +--------+
  |    | Phase 3|  <- Post-charging
  |    |        |
  +----+--------+

  Phase 1: Main stimulus (cathodal)
  Phase 2: Charge recovery (anodal, short)
  Phase 3: Post-charging (small, prevents polarization)
  
  Used in experimental pacing for improved thresholds
```

## Digital Control Implementation

### Pulse Generator State Machine

```
Pulse generation FSM:

  +--------+     +---------+     +---------+
  | IDLE   |---->| RISE    |---->| PLATEAU |
  |        |     |         |     |         |
  +--------+     +---------+     +---------+
      ^                              |
      |                              v
  +--------+     +---------+     +---------+
  | DONE   |<----| FALL    |<----| DISCHARGE|
  |        |     |         |     |         |
  +--------+     +---------+     +---------+

  States:
  IDLE:     Wait for pacing command
  RISE:     Ramp output to target amplitude
  PLATEAU:  Hold amplitude for pulse width
  FALL:     Controlled fall (monophasic) or phase 2 (biphasic)
  DISCHARGE: Active discharge of output capacitor
  DONE:     Return to idle, generate completion signal
```

### Rise Time Control

```
Controlled rise time using DAC ramp:

  V_out
  ^
  |      /-------
  |     /
  |    /
  |   /
  |  /
  | /
  +/-------------> t
  0  t_rise

  Implementation:
  - Digital ramp generator increments DAC code
  - Rate: 1 LSB per clock cycle
  - For 8-bit DAC at 1 MHz clock:
    t_rise = 256 x 1 us = 256 us
    
  Adjusted rate for faster rise:
    t_rise = 256 / (rate_multiplier) x 1 us
    
  For rate_multiplier = 32:
    t_rise = 8 us ✓ (meets < 10 us requirement)
```

### Amplitude Control

```
DAC-based amplitude programming:

  Amplitude register: 8 bits (0-255)
  
  Voltage mapping:
  V_out = (code / 255) x V_max
  
  For V_max = 7.5V:
  Resolution: 7.5V / 255 = 29.4 mV per step
  
  For current mode:
  I_out = (code / 255) x I_max
  
  For I_max = 20 mA:
  Resolution: 20 mA / 255 = 78.4 uA per step

Amplitude accuracy requirement:
  Clinical: +/- 0.1V (for voltage mode)
  DAC INL: < 0.5 LSB = 14.7 mV ✓
```

## Pulse Width Control

### Timing Resolution

```
Pulse width resolution requirements:

  Minimum pulse width: 0.05 ms = 50 us
  Maximum pulse width: 1.5 ms = 1500 us
  Resolution: 0.01 ms = 10 us
  
  Counter requirements:
  Max count = 1500 us / 10 us = 150 counts
  Counter width: ceil(log2(150)) = 8 bits
  
  Clock: 100 kHz (10 us period)
  
  Pulse width = PW_code x 10 us
  PW_code range: 5 to 150
```

### Programmable Timer

```
Pulse width timer implementation:

  Input: PW_code[7:0] (from control register)
  
  +----+----+----+----+----+----+----+----+
  | D7 | D6 | D5 | D4 | D3 | D2 | D1 | D0 |
  +----+----+----+----+----+----+----+----+
        |                              |
        +------------------------------+
        |                              |
        v                              v
  +-----------+                 +-----------+
  | Counter   |                 | Comparator|
  | (counts   |                 | (compare  |
  |  down)    |                 |  to 0)    |
  +-----------+                 +-----------+
        |                              |
        v                              |
  +-----------+                        |
  | Clock     |                        |
  | (100 kHz) |                        |
  +-----------+                        |
                                       v
                                  +---------+
                                  | PW_DONE |
                                  | (flag)  |
                                  +---------+

  Operation:
  1. Load PW_code into counter
  2. Count down on each clock edge
  3. When counter = 0, assert PW_DONE
  4. PW_DONE triggers end of pulse
```

## Biphasic Control

### Phase Timing

```
Biphasic pulse timing:

  Phase 1 (cathodal):
    Duration: t1 = PW_code1 x 10 us
    Amplitude: I1 (programmed)
    Polarity: Positive (current into tissue)
    
  Phase 2 (anodal):
    Duration: t2 = PW_code2 x 10 us
    Amplitude: I2 (programmed, typically I1/10)
    Polarity: Negative (current out of tissue)
    
  Inter-phase delay:
    t_delay = DELAY_code x 1 us
    Typical: 0 us (no delay) to 10 us

Charge balance verification:
  Q1 = I1 x t1
  Q2 = I2 x t2
  
  Requirement: |Q2/Q1| = 1.0 +/- 0.01 (1% tolerance)
  
  For I2 = I1/10:
  t2 = 10 x t1 (to maintain charge balance)
```

### Automatic Charge Balancing

```
Charge balancing algorithm:

1. During Phase 2:
   - Monitor residual voltage on electrode
   - Adjust Phase 2 duration until V_residual < threshold
   
2. Post-pulse:
   - Sample electrode voltage
   - If |V_residual| > 50 mV:
     Apply small correction pulse
   - Repeat until balanced

Implementation:
  +-------------------+
  | Charge Balance    |
  | Comparator        |
  | (monitors V_elec) |
  +-------------------+
           |
           v
  +-------------------+
  | Phase 2 Duration |
  | Adjuster          |
  | (extends if needed)|
  +-------------------+
           |
           v
  +-------------------+
  | Verification      |
  | (confirms balance)|
  +-------------------+
```

## Exponential Pulse Generation

### Capacitor Discharge Circuit

```
Exponential pulse using capacitor discharge:

  V_charge (7.5V) ----+
                       |
                  +----+----+
                  | Switch  |  <- Pre-charge switch
                  | (CHG)   |
                  +----+----+
                       |
                  +----+----+
                  |         |
                  | C_dis   |  <- Discharge capacitor (1 uF)
                  | (1 uF)  |
                  +----+----+
                       |
                  +----+----+
                  |         |
                  | R_dis   |  <- Discharge resistor (500 ohm)
                  | (500 ohm)|
                  +----+----+
                       |
                       +---- To lead
                       |
                      GND

  Time constant: tau = R_dis x C_dis = 500 x 1u = 500 us
  
  V(t) = V_charge x exp(-t/tau)
  
  At t = 0: V = 7.5V
  At t = tau: V = 7.5 x 0.368 = 2.76V
  At t = 2*tau: V = 7.5 x 0.135 = 1.01V
```

### Adjustable Time Constant

```
Programmable tau using switched resistors:

  R_dis network:
  
  V_out ----+----[R1=250]----+
            |                  |
            +----[R2=250]----+----[SW1]
            |                  |
            +----[R1=500]----+----[SW2]
            
  SW1=ON, SW2=OFF: R = 250 ohm, tau = 250 us
  SW1=OFF, SW2=ON: R = 500 ohm, tau = 500 us
  SW1=ON, SW2=ON:  R = 167 ohm, tau = 167 us
  
  Or use R-2R ladder for continuous control
```

## Layout Considerations

```
Pulse shape control layout:

  +-----------------------------------+
  |     Pulse Shape Control           |
  |                                   |
  |  +-----------------------------+ |
  |  | DAC (8-bit)                 | |
  |  | For amplitude control       | |
  |  +-----------------------------+ |
  |                                   |
  |  +-----------------------------+ |
  |  | Timer (8-bit counter)       | |
  |  | For pulse width control     | |
  |  +-----------------------------+ |
  |                                   |
  |  +-----------------------------+ |
  |  | State Machine               | |
  |  | (waveform sequencing)       | |
  |  +-----------------------------+ |
  |                                   |
  |  +-----------------------------+ |
  |  | Output Switch Network       | |
  |  | (high-current path)         | |
  |  +-----------------------------+ |
  |                                   |
  |  ++++ Guard Ring ++++            |
  +-----------------------------------+

Key layout considerations:
- High-current output path: wide metal, short routing
- DAC and timer: separated from analog front-end
- Digital control: shielded from sensitive circuits
```

## Summary

| Parameter | Value |
|-----------|-------|
| Pulse types | Monophasic, Biphasic, Exponential |
| Amplitude resolution | 8 bits (29.4 mV or 78.4 uA) |
| Pulse width range | 0.05 - 1.5 ms |
| Pulse width resolution | 10 us |
| Rise time | < 10 us |
| Charge balance accuracy | 1% |
| Exponential tau range | 100 - 1000 us |
| Clock frequency | 100 kHz (for timing) |
| Control interface | SPI (8-bit registers) |
| Power | 0.5 mW during pulse |
