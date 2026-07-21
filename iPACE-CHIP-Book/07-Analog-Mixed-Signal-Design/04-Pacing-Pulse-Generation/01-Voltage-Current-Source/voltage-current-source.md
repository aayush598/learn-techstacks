# Voltage and Current Source Design for Pacing Pulses

## Overview

The voltage and current source circuits in the iPACE-CHIP generate the precisely controlled electrical stimuli delivered to cardiac tissue through the pacing electrodes. The choice between voltage-mode and current-mode pacing affects circuit complexity, power consumption, lead impedance sensitivity, and therapeutic effectiveness. This chapter covers both source types and their implementation in implantable pacemakers.

## Pacing Source Requirements

### Clinical Specifications

```
Pacing pulse requirements:

Parameter           | Minimum | Typical | Maximum | Unit
--------------------|---------|---------|---------|-----
Amplitude (voltage) | 0.5     | 2.5     | 7.5     | V
Amplitude (current) | 0.5     | 5.0     | 20.0    | mA
Pulse width         | 0.05    | 0.4     | 1.5     | ms
Rise time           | < 10    | -       | 100     | us
Overshoot           | < 5     | -       | -       | %
Back-EMF tolerance  | -       | -       | 10      | V
```

### Lead Impedance Model

```
Pacing lead electrical model:

  +----[R_lead]----+----[C_electrode]----+
  |                |                      |
  |              [R_polar]               Tissue
  |                |                      |
  +----------------+----------------------+

Typical values:
  R_lead: 200-2000 ohm (wire resistance)
  C_electrode: 1-10 uF (electrode-tissue interface)
  R_polar: 1-100 kohm (charge transfer resistance)
  
  Effective impedance at DC: R_lead + R_polar
  Effective impedance at 1 kHz: R_lead + 1/(2pi x f x C_electrode)
  
  For typical lead:
  Z_eff(DC) = 500 ohm + 10 kohm = 10.5 kohm
  Z_eff(1 kHz) = 500 ohm + 16 ohm = 516 ohm
  
  Lead impedance varies with:
  - Electrode material (platinum, iridium oxide)
  - Tissue encapsulation (fibrosis over time)
  - Current density (nonlinear electrode behavior)
  - Frequency (capacitive effects)
```

## Voltage-Mode Pacing Source

### Architecture

```
Voltage-mode pacing source:

  Vbat (3V) ----+
                 |
            +----+----+
            |         |
            | Charge  |
            | Pump    |  (Step-up converter)
            |         |
            +----+----+
                 |
            +----+----+
            |         |
            | Output  |---- Vout to lead
            | Switch  |
            | Network |
            +----+----+
                 |
            +----+----+
            |         |
            | Current |---- I_limit (safety)
            | Limiter |
            +----+----+
                 |
                GND

Operation:
  1. Charge pump boosts Vbat to programmed Vout
  2. Output switch connects Vout to lead
  3. Current limiter prevents over-current
  4. After pulse width, discharge switch activates
```

### Charge Pump Design

```
Dickson charge pump for voltage boosting:

  Vbat ---+---[C1]---+---[C2]---+
          |          |          |
         =|=        =|=        =|=  (flying caps)
          |          |          |
  CLK1 ---+    CLK2--+    CLK3--+
          |          |          |
         GND        GND       Vout

Output voltage:
  Vout = (N+1) x (Vbat - V_drop) - V_drop
  
  For 3-cell pump:
  Vout = 4 x (3V - 0.3V) - 0.3V = 10.5V (no load)
  
  Under load (5 mA):
  Vout = 10.5V - I_load / (f x C_flying)
  Vout = 10.5V - 5mA / (100kHz x 100pF) = 10.5V - 0.5V = 10.0V
  
  Sufficient for 7.5V maximum pacing amplitude ✓
```

### Output Switch Network

```
Output switch for voltage-mode pacing:

  Vout_charge_pump ----+
                       |
                  +----+----+
                  |         |
                  |  PMOS   |  (High-side switch)
                  |  Pass   |
                  |  Trans. |
                  +----+----+
                       |
                       +---- To lead (via current limiter)
                       |
                  +----+----+
                  |         |
                  |  NMOS   |  (Discharge switch)
                  |  Disch. |
                  +----+----+
                       |
                      GND

Switch sizing for 20 mA:
  R_on = V_drop / I_max = 100mV / 20mA = 5 ohm
  W/L = mu_p x Cox x (Vgs - Vth)^2 / (2 x I_D x R_on)
  For 180nm: W/L = 200/1 (approx)
```

## Current-Mode Pacing Source

### Architecture

```
Current-mode pacing source:

  Vbat (3V) ----+
                 |
            +----+----+
            |         |
            | Current |---- I_programmed
            | Source  |
            | Array   |
            +----+----+
                 |
            +----+----+
            |         |
            | Output  |---- Iout to lead
            | Cascode |
            | Stage   |
            +----+----+
                 |
            +----+----+
            |         |
            | Voltage |---- V_compliance monitoring
            | Monitor |
            +----+----+
                 |
                GND

Operation:
  1. Current source generates programmed current
  2. Output cascode provides high impedance
  3. Voltage monitor detects lead faults
  4. Output current flows through lead to tissue
```

### Current Source Implementation

```
PMOS cascode current source:

       VDD (3V)
        |
   +----+----+
   |         |
   |   M1    |  <- Main current source (W/L=20/2)
   |         |     VGS set by bias voltage
   +----+----+
        |
   +----+----+
   |         |
   |   M2    |  <- Cascode transistor (W/L=10/1)
   |         |     Increases output impedance
   +----+----+
        |
        +---- Iout (to output stage)

Bias generation:
  Vbias = VGS1 + VDS2(sat)
  
  For Iout = 5 mA (typical pacing):
  M1: W/L = 20/2, VGS = 0.6V
  M2: W/L = 10/1, VDS(sat) = 0.2V
  
  Output impedance:
  R_out = g_m2 x r_o2 x r_o1
  R_out = 1mS x 200kohm x 200kohm = 40 Gohm (ideal)
  Actual (with parasitics): ~500 kohm
  
  This ensures constant current for lead impedance 200-2000 ohm ✓
```

### Current Source Array (Binary-Weighted)

```
8-bit current source array:

  VDD ---+---+---+---+---+---+---+---+---
         |   |   |   |   |   |   |   |
        [I0] [I1] [I2] [I4] [I8] [I16] [I32] [I64]
         |   |   |   |   |   |   |   |
        [S0] [S1] [S2] [S4] [S8] [S16] [S32] [S64]
         |   |   |   |   |   |   |   |
         +---+---+---+---+---+---+---+--- Iout

Binary weighting:
  I0 = I_unit (LSB) = 39.1 uA
  I1 = 2 x I_unit = 78.1 uA
  I2 = 4 x I_unit = 156.3 uA
  I3 = 8 x I_unit = 312.5 uA
  I4 = 16 x I_unit = 625 uA
  I5 = 32 x I_unit = 1.25 mA
  I6 = 64 x I_unit = 2.5 mA
  I7 = 128 x I_unit = 5.0 mA (MSB)

Full scale: 255 x 39.1 uA = 10 mA
Resolution: 39.1 uA (8-bit)
```

## Voltage Compliance

### Compliance Calculation

```
Voltage compliance for current-mode pacing:

  V_compliance = V_out_max - I_out x R_lead

For VDD = 3V, V_dsat = 0.3V:
  V_out_max = VDD - V_dsat = 2.7V

At 5 mA through typical lead (500 ohm):
  V_lead = 5 mA x 500 ohm = 2.5V
  
  V_compliance = 2.7V - 2.5V = 0.2V (very tight!)

This is insufficient for high-impedance leads.

Solution: Use charge pump for current-mode pacing too:

  V_boost = 10V (from charge pump)
  V_out_max = 10V - 0.3V = 9.7V
  
  For 5 mA through 2000 ohm lead:
  V_lead = 5 mA x 2000 ohm = 10V
  V_compliance = 9.7V - 10V = -0.3V (insufficient!)
  
  Need V_boost > 10.3V for 2000 ohm, 5 mA
  
  Design choice: V_boost = 12V (3-cell charge pump)
  V_compliance = 12V - 0.3V - 10V = 1.7V (sufficient) ✓
```

### Back-EMF Handling

```
Back-EMF from inductive lead:

During current turn-off:
  V_emf = -L_lead x dI/dt

For L_lead = 100 uH, dI/dt = 5 mA / 1 us:
  V_emf = -100 uH x 5000 A/s = -500V (!)

This would destroy the output stage!

Protection:
  1. Clamp diodes (TVS) at output
  2. Controlled dI/dt (soft turn-off)
  3. Active clamp circuit

Soft turn-off:
  dI/dt < V_clamp / L_lead
  dI/dt < 12V / 100 uH = 120 A/s
  
  For 5 mA:
  t_fall > 5 mA / 120 A/s = 42 us
  
  Design choice: 50 us fall time (within 1 ms pulse width) ✓
```

## Output Stage Design

### Voltage-Mode Output Stage

```
Voltage-mode output with current limiting:

  Vout_charge_pump ----+
                       |
                  +----+----+
                  | PMOS    |  <- Output pass transistor
                  | (sized  |
                  |  for    |
                  |  20 mA) |
                  +----+----+
                       |
                  +----+----+
                  | R_sense |  <- Current sensing resistor
                  | (25 ohm)|
                  +----+----+
                       |
                       +---- To lead
                       |
                  +----+----+
                  | NMOS    |  <- Discharge switch
                  | (fast)  |
                  +----+----+
                       |
                      GND

Current limiting:
  When I_out x R_sense > V_ref (0.5V):
  PMOS gate voltage adjusts to limit current
  
  I_max = V_ref / R_sense = 0.5V / 25 ohm = 20 mA ✓
```

### Current-Mode Output Stage

```
Current-mode output with voltage monitoring:

  From current source ----+
                          |
                     +----+----+
                     | Cascode  |  <- High impedance output
                     | (M3,M4)  |
                     +----+----+
                          |
                          +---- To lead
                          |
                     +----+----+
                     | Voltage  |  <- Monitors V_out
                     | Monitor  |     Detects lead fault
                     | (ADC)    |
                     +----+----+
                          |
                     +----+----+
                     | Discharge|  <- Active load for
                     | Load     |     charge recovery
                     +----+----+
                          |
                         GND

Operation modes:
  1. Pacing: Current source active, voltage monitored
  2. Sensing: High-Z output, measure electrode voltage
  3. Discharge: Active load drains residual charge
```

## Power Analysis

### Voltage-Mode Power

```
Voltage-mode pacing power:

During pulse (5 mA, 2.5V across lead):
  P_pulse = V_charge_pump x I_out
  P_pulse = 5V x 5 mA = 25 mW (charge pump efficiency 50%)
  
  P_total = 25 mW / 0.5 = 50 mW (input power)
  
Pulse energy:
  E_pulse = P_total x t_pulse
  E_pulse = 50 mW x 1 ms = 50 uJ

At 70 bpm:
  P_avg = E_pulse x (70/60) = 50 uJ x 1.17 = 58.3 uW

Idle power:
  P_idle = 1 uW (charge pump standby)
  
Total average: 59.3 uW
```

### Current-Mode Power

```
Current-mode pacing power:

During pulse (5 mA through lead):
  V_lead = 5 mA x 500 ohm = 2.5V
  V_headroom = 0.5V (for cascode)
  V_boost = 5V (from charge pump)
  
  P_pulse = V_boost x I_out = 5V x 5 mA = 25 mW
  P_charge_pump = 25 mW / 0.5 = 50 mW (input)
  
Same as voltage-mode for same lead impedance.

For high-impedance lead (2000 ohm):
  V_lead = 5 mA x 2000 ohm = 10V
  V_boost = 12V (higher voltage needed)
  
  P_pulse = 12V x 5 mA = 60 mW
  P_charge_pump = 60 mW / 0.5 = 120 mW
  
  Current-mode requires more power for high-impedance leads ✓
  (But delivers constant current regardless of impedance)
```

## Safety Features

### Over-Current Protection

```
Hardware current limiter:

  +---- Vout
  |
  +----[R_sense]----+
                    |
               +----+----+
               |  Op-Amp  |  <- Feedback loop
               | (fast)   |     Limits I_out
               +----+----+
                    |
               +----+----+
               | PMOS     |  <- Current limiting transistor
               | (pass)   |
               +----+----+
                    |
                    +---- To lead

  Feedback: V_sense = I_out x R_sense
  When V_sense > V_ref: Op-amp reduces PMOS gate voltage
  
  Response time: < 1 us (fast enough to protect)
  
  Current limit accuracy: +/- 5% (set by R_sense tolerance)
```

### Open-Circuit Detection

```
Lead impedance monitoring:

During each pacing attempt:
  1. Apply test current pulse (100 uA, 10 us)
  2. Measure voltage across lead
  3. Calculate R_lead = V_measured / I_test
  4. Compare with threshold:
     R_lead < 200 ohm: Short circuit (abort)
     R_lead > 2000 ohm: Open circuit (fault)
     200-2000 ohm: Normal (proceed with pacing)

Response to fault:
  1. Set fault flag in status register
  2. Log fault event with timestamp
  3. Switch to backup pacing parameters
  4. Generate alert to clinician (via telemetry)
```

## Summary

| Parameter | Voltage-Mode | Current-Mode |
|-----------|--------------|--------------|
| Output type | Voltage | Constant current |
| Impedance sensitivity | High (V=IR) | None (I constant) |
| Charge pump needed | Yes (>3V) | Yes (for high Z) |
| Output switch | PMOS pass | Cascode source |
| Current limiting | Feedback loop | Inherent |
| Power (500 ohm, 5 mA) | 50 mW | 50 mW |
| Power (2000 ohm, 5 mA) | 200 mW | 200 mW |
| Lead fault detection | Voltage monitor | Voltage monitor |
| Complexity | Moderate | High |
| Best for | Low-Z leads | Variable-Z leads |

The iPACE-CHIP supports both modes with automatic selection based on measured lead impedance at implant and during follow-up.
