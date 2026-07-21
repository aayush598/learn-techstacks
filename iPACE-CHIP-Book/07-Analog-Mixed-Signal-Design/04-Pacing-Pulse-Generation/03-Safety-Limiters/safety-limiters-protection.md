# Safety Limiters and Protection Circuits for Pacing

## Overview

Safety limiters are critical protection circuits in the iPACE-CHIP that prevent potentially lethal electrical hazards from reaching cardiac tissue. These circuits enforce hard limits on output current, voltage, pulse duration, and energy delivery regardless of software or firmware errors. Patient safety is the paramount design constraint, and all safety functions must be implemented in hardware with no software dependencies.

## Hazard Analysis

### Potential Failure Modes

```
Failure modes and consequences:

1. Over-current delivery:
   Cause: DAC malfunction, software error
   Consequence: Tissue damage, fibrillation risk
   Severity: CRITICAL (life-threatening)
   
2. Over-voltage delivery:
   Cause: Charge pump failure, feedback loop failure
   Consequence: Tissue damage, insulation breakdown
   Severity: CRITICAL
   
3. Excessive pulse width:
   Cause: Timer failure, software hang
   Consequence: Prolonged stimulation, battery drain
   Severity: HIGH
   
4. DC current delivery:
   Cause: Charge imbalance, switch failure
   Consequence: Electrode corrosion, tissue damage
   Severity: CRITICAL
   
5. Lead short circuit:
   Cause: Lead insulation failure
   Consequence: High current, device overheating
   Severity: HIGH
   
6. Lead open circuit:
   Cause: Lead fracture
   Consequence: No pacing, high voltage at output
   Severity: MEDIUM
```

### Safety Standards

```
IEC 60601-1 requirements for cardiac pacemakers:

Maximum output parameters:
  - Maximum current: 20 mA (absolute)
  - Maximum voltage: 10 V (absolute)
  - Maximum energy per pulse: 100 uJ
  - Maximum charge per pulse: 5 uC
  
iPACE-CHIP design margins:
  - Current limit: 15 mA (75% of standard max)
  - Voltage limit: 7.5V (75% of standard max)
  - Energy limit: 75 uJ (75% of standard max)
  - Charge limit: 3.75 uC (75% of standard max)
  
  All limits implemented in hardware (not software)
```

## Current Limiting

### Hardware Current Limiter

```
Fast analog current limiter:

  Vout_charge_pump ----+
                       |
                  +----+----+
                  |         |
                  |  PMOS   |  <- Pass transistor
                  |  (M1)   |
                  +----+----+
                       |
                  +----+----+
                  |  R_s    |  <- Sense resistor (25 ohm)
                  +----+----+
                       |
                       +---- To lead
                       |
               +-------+-------+
               |               |
          +----+----+     +----+----+
          |  Op-Amp |     |  NMOS   |
          | (fast)  |     |  (M2)   |  <- Limit transistor
          +----+----+     +----+----+
               |               |
          +----+----+          |
          |  V_ref  |          |
          | (0.375V)|          |
          +----+----+          |
               |               |
               +-------+-------+
                       |
                      GND

Operation:
  Normal: M2 is OFF, M1 passes current
  Over-current: V_sense > V_ref
    Op-amp turns ON M2
    M2 steals gate drive from M1
    M1 reduces current
    Current limited to: I_max = V_ref / R_s = 0.375V / 25 ohm = 15 mA

Response time: < 1 us (comparator propagation)
```

### Multi-Level Current Limiting

```
Cascoded current limits:

Level 1 (normal): Software DAC sets current
  I_programmed = DAC_code x I_step
  Range: 0 - 10 mA (normal operation)
  
Level 2 (warning): Hardware analog limiter
  I_limit1 = 15 mA (hard limit)
  If exceeded: Reduce DAC output, set warning flag
  
Level 3 (shutdown): Hardware latch
  I_limit2 = 20 mA (absolute maximum)
  If exceeded: Latch output OFF, require reset
  Cannot be cleared by software alone

Priority: Level 3 > Level 2 > Level 1

Implementation:
  Level 1: Digital DAC control
  Level 2: Analog feedback loop (shown above)
  Level 3: Comparator + SR latch (hardware only)
```

## Voltage Limiting

### Output Voltage Clamp

```
Voltage clamp circuit:

  To lead ----+----[R_sense]----+
              |                  |
              |            +----+----+
              |            | TVS     |  <- Transient voltage
              |            | Diode   |     suppressor (7.5V)
              |            +----+----+
              |                  |
              |            +----+----+
              |            | Zener   |  <- Backup clamp (8V)
              |            | (8V)    |
              |            +----+----+
              |                  |
              +---- To output    |
                                |
                           +----+----+
                           | Output  |
                           | voltage |
                           | monitor |
                           | (ADC)   |
                           +----+----+

Clamping operation:
  Normal: TVS and Zener are OFF (high impedance)
  Over-voltage: TVS conducts at 7.5V
  Backup: Zener conducts at 8V (if TVS fails)
  
  Both are passive, no software needed
```

### Voltage Monitoring

```
Continuous voltage monitoring:

  V_out ----[R_div]----+
            (1:10)      |
                        +---- To ADC input
                        |
                   +----+----+
                   | Comparator|  <- Over-voltage detect
                   | (7V ref)  |
                   +----+----+
                        |
                        v
                   +---------+
                   | Fault   |
                   | Latch   |
                   +---------+

  If V_out > 7V for > 1 us:
    Assert OVP_FAULT
    Latch output to safe state
    Require hardware reset to clear
```

## Energy Limiting

### Energy Calculation

```
Pulse energy calculation:

  E_pulse = integral(V(t) x I(t)) dt

For rectangular pulse:
  E_pulse = V_amp x I_amp x t_pw

For exponential pulse:
  E_pulse = V0^2 x C / 2 (capacitor energy)

Maximum energy per pulse:
  For V=7.5V, I=15mA, t=1ms:
  E = 7.5 x 0.015 x 0.001 = 112.5 uJ
  
  Need to limit to 75 uJ:
  Option 1: Limit V to 5V (E = 75 uJ at 15mA, 1ms)
  Option 2: Limit I to 10mA (E = 75 uJ at 7.5V, 1ms)
  Option 3: Limit t to 0.67ms (E = 75 uJ at 7.5V, 15mA)
  
  Design choice: Use all three (redundant protection)
```

### Energy Limit Implementation

```
Hardware energy limiter:

  +-------------------+
  | Power Monitor     |
  | (V_out x I_out)   |
  +-------------------+
           |
           v
  +-------------------+
  | Integrator        |
  | (accumulates      |
  |  energy)          |
  +-------------------+
           |
           v
  +-------------------+
  | Comparator        |
  | (compare to E_max)|
  +-------------------+
           |
           v
  +-------------------+
  | Shutdown Latch    |
  | (cuts output)     |
  +-------------------+

  E_max = 75 uJ (stored in fixed resistor divider)
  
  Response time: < 5 us (integrator + comparator)
  
  This provides a third layer of protection beyond
  current and voltage limiting
```

## DC Blocking

### Active DC Blocking

```
Capacitor-based DC blocking:

  Pacing output ----[C_block]----+---- To lead
                    (10 uF)      |
                                |
                           +----+----+
                           | Bleed   |  <- Bleed resistor
                           | R_bleed |     (100 kohm)
                           | (100k)  |
                           +----+----+
                                |
                               GND

  DC blocking: Prevents any DC current flow
  Time constant: tau = R_bleed x C_block = 100k x 10u = 1s
  
  For pacing pulses (1 ms):
  V_C_change = I x t / C = 15mA x 1ms / 10uF = 1.5V
  
  This is acceptable (V_C << V_burst)
```

### Active Charge Recovery

```
Active charge recovery circuit:

  After pacing pulse:
  1. Open output switch
  2. Connect electrode to active load
  3. Discharge residual charge

  +---- To electrode
  |
  +----[R_rec]----+
  (10 kohm)       |
             +----+----+
             | Active  |  <- Op-amp with feedback
             | Load    |     forces V_electrode to 0V
             +----+----+
                  |
                 GND

  Recovery time: < 50 us
  Final voltage: < 10 mV (within safety limit)
```

## Short Circuit Protection

### Short Circuit Detection

```
Lead short circuit detection:

During pacing attempt:
  1. Apply test pulse (100 uA, 10 us)
  2. Measure voltage across lead
  3. Calculate Z_lead = V_measured / I_test
  
  If Z_lead < 50 ohm:
    SHORT_CIRCUIT detected
    
  Response:
    1. Abort pacing attempt
    2. Set SHORT_FAULT flag
    3. Reduce output voltage limit to 2V
    4. Log event with timestamp
    5. Continue monitoring (may be transient)
    
  If short persists for > 10 consecutive attempts:
    Enter safe mode (minimum output)
    Notify clinician via telemetry
```

### Current Limiting During Short

```
Output during short circuit:

  Z_lead = 10 ohm (dead short)
  V_out_max = 7.5V (charge pump)
  
  Without limiter:
  I_out = 7.5V / 10 ohm = 750 mA (DANGEROUS!)
  
  With current limiter:
  I_out = 15 mA (limited by hardware)
  V_out = I_out x Z_lead = 15mA x 10 ohm = 0.15V
  
  Power dissipated:
  P_out = V_out x I_out = 0.15V x 15mA = 2.25 mW
  
  This is safe for the device and patient ✓
```

## Redundancy

### Triple Redundancy Architecture

```
Safety redundancy:

  Software Control
       |
       v
  +----+----+     +----+----+     +----+----+
  | Level 1 |     | Level 2 |     | Level 3 |
  | Current |     | Voltage |     | Energy  |
  | Limit   |     | Limit   |     | Limit   |
  +----+----+     +----+----+     +----+----+
       |               |               |
       v               v               v
  +----+----+     +----+----+     +----+----+
  | Analog  |     | Analog  |     | Hardware|
  | DAC     |     | Feedback|     | Latch   |
  | Control |     | Loop    |     | (failsafe)|
  +----+----+     +----+----+     +----+----+
       |               |               |
       +-------+-------+-------+-------+
               |
               v
          To Patient

If any level fails:
  Level 2 catches Level 1 failures
  Level 3 catches Level 2 failures
  Level 3 is hardware-only (no software dependency)
```

### Watchdog Timer

```
Safety watchdog:

  +-------------------+
  | Watchdog Timer    |
  | (hardware)        |
  +-------------------+
           |
           v
  +-------------------+
  | Pulse Width       |
  | Monitor           |
  | (max 2 ms)        |
  +-------------------+
           |
           v
  +-------------------+
  | Output Disable    |
  | (if timeout)      |
  +-------------------+

  If pacing pulse exceeds 2 ms:
    Watchdog triggers
    Output forced OFF
    Device reset required
    
  This catches timer failures or software hangs
```

## Layout Considerations

```
Safety circuit layout:

  +-------------------------------------------+
  |           Safety Limiter Block            |
  |                                           |
  |  +------------------+                    |
  |  | Current Sense    | <- Short trace     |
  |  | (R_sense)        |    to output pad   |
  |  +------------------+                    |
  |                                           |
  |  +------------------+                    |
  |  | Voltage Clamp    | <- TVS + Zener     |
  |  | (passive)        |    near output     |
  |  +------------------+                    |
  |                                           |
  |  +------------------+                    |
  |  | Energy Monitor   |                    |
  |  | (integrator)     |                    |
  |  +------------------+                    |
  |                                           |
  |  +------------------+                    |
  |  | Safety Latch     | <- Hardware-only   |
  |  | (SR flip-flop)   |    no SW access    |
  |  +------------------+                    |
  |                                           |
  |  ++++ Dedicated guard ring ++++          |
  |  ++++ (isolated from digital) ++++      |
  +-------------------------------------------+

  Layout rules:
  - Sense resistor: Kelvin connection
  - TVS diodes: short, wide traces
  - Safety latch: physically separated from SW-controlled logic
  - Guard ring: continuous, connected to analog ground
```

## Summary

| Protection Layer | Mechanism | Limit | Response Time |
|-----------------|-----------|-------|---------------|
| Level 1: Current | Analog feedback | 15 mA | < 1 us |
| Level 2: Voltage | TVS + Zener clamp | 7.5V | < 100 ns |
| Level 3: Energy | Hardware integrator | 75 uJ | < 5 us |
| Level 4: Time | Watchdog timer | 2 ms | 2 ms |
| Level 5: DC | Active charge recovery | < 10 mV | < 50 us |
| Level 6: Short | Impedance monitor | < 50 ohm | 10 us |

All safety functions are hardware-only with no software dependency. The triple-redundancy architecture ensures that no single fault can result in a hazardous output to the patient.
