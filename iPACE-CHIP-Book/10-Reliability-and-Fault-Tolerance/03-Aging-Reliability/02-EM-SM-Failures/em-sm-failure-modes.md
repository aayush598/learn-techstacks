# 10.3.2 Electromigration (EM) and Stress Migration (SM) Failure Modes

## Chapter Overview

Electromigration (EM) and stress migration (SM) are metal interconnect failure mechanisms that can cause open circuits, short circuits, or increased resistance in the iPACE-CHIP's wiring. Unlike BTI and HCI, which affect transistor switching characteristics, EM and SM affect the physical integrity of the metal lines that carry power, ground, and signal currents. In a life-critical implantable pacemaker operating for 10+ years, these interconnect failure mechanisms must be carefully managed through design rules, current density limits, and redundancy strategies.

This chapter covers the physics of EM and SM, their impact on the iPACE-CHIP's interconnects, the design rules and current limits used to prevent them, and the monitoring and detection techniques that ensure interconnect reliability throughout the device's implant lifetime.

---

## 10.3.2.1 Electromigration Physics

### Mechanism

Electromigration is the transport of metal atoms in a conductor caused by the momentum transfer from flowing electrons (the "electron wind"):

```
Electron flow direction:  <───────────────────
Metal atoms:              ──────────────────►
                          (drift in the direction of electron flow)

The electron wind force:
  F_wind = Z* * e * rho * j

where:
  Z*    = effective valence of the metal atom (dimensionless)
  e     = electron charge (1.6 x 10^-19 C)
  rho   = resistivity of the metal (ohm.cm)
  j     = current density (A/cm^2)
```

At the cathode end of the metal line, atoms are depleted (creating voids). At the anode end, atoms accumulate (creating hillocks). Voids eventually cause open circuits; hillocks can cause short circuits to adjacent metal lines.

### Black's Equation

The median time to failure (MTTF) for electromigration is given by Black's equation:

```
MTTF = A * j^(-n) * exp(Ea_EM / (k * T))

where:
  A    = technology-dependent constant
  j    = current density (A/cm^2)
  n    = current density exponent (typically 1-2)
  Ea_EM = activation energy for EM (eV)
  k    = Boltzmann constant
  T    = temperature (K)
```

For the iPACE-CHIP's aluminum interconnect (180nm process):

```
Ea_EM (Al) = 0.7 eV (grain boundary diffusion)
n = 2 (for void nucleation-limited failure)

At j = 1 MA/cm^2 (10^6 A/cm^2), T = 37C (310K):
  MTTF = A * (10^6)^(-2) * exp(0.7 / (8.617e-5 * 310))
       = A * 10^-12 * exp(26.3)
       = A * 10^-12 * 2.94 x 10^11
       = A * 0.294

For A calibrated to a 10-year MTTF at the maximum allowed current density:
  j_max = 1 MA/cm^2 (typical for 180nm Al at 105C)
```

### Current Density Limits

The iPACE-CHIP's design rules specify maximum current densities for each metal layer:

| Metal Layer | Max DC Current Density (MA/cm^2) | Max Pulsed Current Density (MA/cm^2) |
|---|---|---|
| Metal 1 (bottom) | 1.0 | 2.0 |
| Metal 2 | 1.2 | 2.5 |
| Metal 3 | 1.5 | 3.0 |
| Metal 4 (top) | 2.0 | 4.0 |
| Via (between layers) | 0.5 | 1.0 |

The higher limits for upper metal layers reflect their greater thickness (reducing current density for the same current) and better thermal properties (improved heat dissipation).

### Pulsed Current Effects

The iPACE-CHIP's digital logic draws pulsed current (switching events), not DC current. Pulsed current is less damaging than DC current because:

1. **Off-time recovery:** During the off-time of the current pulse, some atomic backflow occurs, partially undoing the electromigration damage.
2. **Void nucleation time:** Electromigration voids require a nucleation period. If the current pulse is shorter than the nucleation time, no void forms.

The iPACE-CHIP's pulsed current density is characterized by:

```
Peak current density: j_peak = I_peak / (W * T)
  where W = metal width, T = metal thickness

Average current density: j_avg = j_peak * D
  where D = duty cycle

For EM assessment:
  Use j_avg for DC EM analysis (conservative)
  Or use pulsed EM models for more accurate assessment
```

### Via Electromigration

Vias (connections between metal layers) are particularly susceptible to electromigration because:

1. Current crowding at the via entrance creates locally high current density
2. The via interface (different materials, different grain structures) provides fast diffusion paths
3. The small via cross-section limits the current-carrying capacity

The iPACE-CHIP's design rules require multiple vias for any connection carrying more than 100 microamps:

```
Current per via: I_per_via = I_total / N_vias

For N_vias = 4 (minimum for power connections):
  I_per_via = 1 mA / 4 = 250 uA per via
  
  Via current density: 250e-6 / (0.3e-4)^2 = 27.8 MA/cm^2
  
  This exceeds the single-via limit (0.5 MA/cm^2), but the effective
  current density through the via array is:
  j_eff = I_total / (N_vias * A_via) = 1e-3 / (4 * 9e-10) = 0.28 MA/cm^2
  
  This is within the design rule limit.
```

---

## 10.3.2.2 Stress Migration Physics

### Mechanism

Stress migration (SM) is the movement of metal atoms driven by mechanical stress gradients rather than electrical current. The stress is caused by the thermal expansion mismatch between the metal interconnect and the surrounding dielectric:

```
During manufacturing:
  1. Metal is deposited at high temperature (~400C for CVD aluminum)
  2. Dielectric is deposited around the metal
  3. As the device cools, the metal contracts more than the dielectric
     (CTE_Al = 23 ppm/C, CTE_SiO2 = 0.5 ppm/C)
  4. Tensile stress builds up in the metal lines
  
  This stress can cause void formation even without current flow.
```

### Stress Migration Rate

The SM void growth rate depends on the stress gradient, temperature, and microstructure:

```
v_SM = (D_SM / (k * T)) * Omega * d(sigma)/dx

where:
  D_SM    = diffusion coefficient for stress-driven transport
  Omega   = atomic volume
  d(sigma)/dx = stress gradient along the metal line
```

SM is most severe during thermal cycling (temperature changes cause stress changes), making it particularly relevant for the iPACE-CHIP because:

1. The device experiences temperature variations during implantation (body temperature stabilization)
2. The device experiences temperature variations during the cardiac cycle (local heating from pacing pulses)
3. Long-term body temperature fluctuations (fever, exercise) create additional thermal cycling

### SM vs. EM

| Property | Electromigration | Stress Migration |
|---|---|---|
| Driving force | Electron wind (current) | Mechanical stress (thermal) |
| Temperature dependence | Strong (Arrhenius) | Moderate |
| Current dependence | Strong (j^n) | None (occurs without current) |
| Void location | Cathode end, along current path | At vias, line ends, narrow sections |
| Time dependence | Power-law | Approximately linear |
| Primary concern | High-current paths | All metal lines (especially narrow) |

For the iPACE-CHIP, EM is the primary concern for power delivery and output stage interconnects (high current), while SM is the primary concern for signal interconnects (narrow lines, no high current).

---

## 10.3.2.3 Impact on iPACE-CHIP Circuits

### Power Delivery Network

The iPACE-CHIP's power delivery network must carry the total supply current without exceeding the EM current density limits:

```
Total supply current: I_DD = 8 mA (average)
  Pacing output pulse: 15 mA (peak, during pulse)
  Digital logic: 5 mA (average)
  Analog circuits: 2 mA (average)
  Telemetry: 1 mA (during transmission)

Power bus width calculation (Metal 4, top layer):
  Required width for DC EM: W = I / (j_max * T_metal)
  For Metal 4: j_max = 2.0 MA/cm^2, T_metal = 0.8 um
  
  For I_DD = 8 mA:
    W = 8e-3 / (2.0e6 * 0.8e-4) = 8e-3 / 1.6e2 = 50 um
    
  The iPACE-CHIP's main VDD bus is 60 um wide (with margin).
  
  For the pacing output current (15 mA peak):
    W = 15e-3 / (2.0e6 * 0.8e-4) = 93.75 um
    
  The iPACE-CHIP's output stage power bus is 100 um wide.
```

### Signal Interconnect Reliability

Signal interconnects carry much lower currents than power buses, so EM is less of a concern. However, SM can affect narrow signal lines:

```
Minimum metal width (180nm process): 0.18 um
  At this width, SM voids can grow to span the entire line width
  within 10 years at 37C, causing an open circuit.
  
  Mitigation: The iPACE-CHIP uses a minimum width of 0.24 um for
  all signal lines (33% wider than the process minimum).
  
  For critical signals (pacing output enable, sensing threshold):
    Minimum width: 0.5 um (2.8x the process minimum)
    Redundant routing: two independent paths
```

### Impact on Analog Circuits

EM and SM affect analog circuits through:

1. **Increased resistance:** A partially voided metal line has higher resistance, which can affect the voltage drop across precision resistor networks and the accuracy of current mirrors.

2. **Open circuits:** A fully voided line causes a complete open circuit, disconnecting the affected circuit.

3. **Short circuits:** Hillocks from EM can short adjacent lines, creating unintended connections.

For the iPACE-CHIP's bandgap reference:

```
Bandgap reference resistor network:
  Resistors are implemented using high-resistance polysilicon (not metal)
  The metal routing between resistors is wider than minimum (0.5 um)
  The resistor values are trimmed at production and stored in flash
  
  EM impact on resistor routing:
    Additional resistance from EM: < 0.1 ohm over 10 years
    Effect on Vref: < 0.01 mV (negligible)
```

---

## 10.3.2.4 EM and SM Design Rules

### Current Density Rules

The iPACE-CHIP's design rules enforce current density limits at three levels:

**Level 1: DC Current Density**
```
For each metal layer, the DC current density must not exceed j_max at the maximum
operating temperature (37C for the iPACE-CHIP):

  Metal 1: j_DC < 1.0 MA/cm^2
  Metal 2: j_DC < 1.2 MA/cm^2
  Metal 3: j_DC < 1.5 MA/cm^2
  Metal 4: j_DC < 2.0 MA/cm^2
```

**Level 2: Peak Current Density (Pulsed)**
```
For pulsed currents (e.g., pacing output), the peak current density must not
exceed j_peak_max:

  Metal 1: j_peak < 2.0 MA/cm^2
  Metal 2: j_peak < 2.5 MA/cm^2
  Metal 3: j_peak < 3.0 MA/cm^2
  Metal 4: j_peak < 4.0 MA/cm^2
```

**Level 3: Integrated Current Density (Electromigration Budget)**
```
The iPACE-CHIP uses an electromigration budget approach for the output stage:

  EM_budget = sum(j_i^n * t_i) / MTTF_required

where:
  j_i = current density during operating state i
  t_i = duration of state i
  n   = current density exponent (2 for Al)
  MTTF_required = 10^6 hours (114 years -- 10x the implant lifetime)

The total EM budget must be less than 1.0 for the device to meet its
10-year lifetime requirement with adequate margin.
```

### Width and Spacing Rules

**Minimum Width Rules:**
```
Signal lines:     0.24 um (1.33x process minimum)
Power lines:      0.5 um minimum (for current capacity)
Output stage:     1.0 um minimum (for high current)
```

**Minimum Spacing Rules (SM prevention):**
```
Between adjacent metal lines: 0.24 um (process minimum)
Between power and signal lines: 0.5 um
Between output stage and all other lines: 1.0 um

The increased spacing for the output stage prevents hillock-induced shorts
from affecting other circuits.
```

### Via Redundancy Rules

```
For connections carrying > 10 uA: minimum 2 vias
For connections carrying > 100 uA: minimum 4 vias
For power connections: minimum 4 vias (8 for output stage)
For signal connections to critical circuits: minimum 2 vias with independent paths
```

---

## 10.3.2.5 EM Monitoring and Detection

### On-Chip Current Monitors

The iPACE-CHIP includes current monitors on the critical power delivery paths:

**Sense Resistor Current Monitor:**
```
A precision 10-ohm sense resistor is placed in series with the VDD supply
to the output stage. The voltage across the sense resistor is measured by
a dedicated ADC channel:

  I_out = V_sense / R_sense

  If I_out > I_max (20 mA for 10 us): warning
  If I_out > I_max for 100 us: output pulse terminated
  If I_out > I_max for 1 ms: output stage disabled
```

### Interconnect Resistance Monitoring

The iPACE-CHIP monitors the resistance of critical interconnects by measuring the voltage drop along selected metal lines:

**Pulse Generator Output Path Resistance:**
```
At each power-on, the iPACE-CHIP measures the resistance of the output stage
power path:

  1. Apply a small test current (100 uA) through the output path
  2. Measure the voltage drop across the path
  3. Compute R_path = V_drop / I_test
  4. Compare against the baseline resistance (measured at production)
  
  If R_path increases by > 10%: warning (potential void formation)
  If R_path increases by > 20%: alert (significant degradation)
  If R_path increases by > 50%: disable output stage, enter safe mode
```

### Via Resistance Monitoring

Critical via connections (output stage, power delivery) are monitored using Kelvin (4-wire) resistance measurements:

```
Kelvin measurement:
  Force current through two terminals of the via connection
  Measure voltage on two separate terminals
  
  R_via = V_measured / I_force
  
  If R_via increases by > 50%: void detected in via
  Action: switch to redundant via path (if available)
```

---

## 10.3.2.6 EM and SM in the iPACE-CHIP Output Stage

### Output Stage Current Profile

The iPACE-CHIP's output stage delivers pacing pulses to the heart. The current profile during a pacing pulse:

```
Pacing pulse waveform:
  t = 0: Pulse starts, output voltage ramps to 5V
  t = 0 to 0.5 ms: Constant current delivery (10-20 mA)
  t = 0.5 ms: Pulse ends, output voltage returns to 0V
  t = 0.5 ms to 600 ms: No output current (recovery period)
  
  Duty cycle: D = 0.5 ms / 600 ms = 8.3 x 10^-4
  
  Average current: I_avg = 15 mA * 8.3 x 10^-4 = 12.5 uA
  Peak current: I_peak = 15 mA
```

The low duty cycle of the pacing pulse means that the EM impact is much less than for continuous current:

```
EM effective current density:
  j_eff = j_peak * D^n = 15e-3 / (100e-4 * 0.8e-4) * (8.3e-4)^2
        = 18.75 MA/cm^2 * 6.9 x 10^-7
        = 0.013 MA/cm^2
        
  This is well below the DC limit (2.0 MA/cm^2), providing >150x margin.
```

### Via Reliability in the Output Stage

The output stage vias carry the highest current in the iPACE-CHIP. The via EM reliability is ensured by:

```
Via array design for output stage:
  Number of vias: 8 (2 rows x 4 columns)
  Via size: 0.3 x 0.3 um
  Via pitch: 0.6 um
  
  Current per via: 15 mA / 8 = 1.875 mA
  Via current density: 1.875e-3 / (0.3e-4)^2 = 208 MA/cm^2
  
  Wait, that's way too high. Let me recalculate:
  
  Via area: 0.3 um x 0.3 um = 0.09 um^2 = 9e-10 cm^2
  Current per via: 15 mA / 8 = 1.875 mA = 1.875e-3 A
  Current density: 1.875e-3 / 9e-10 = 2.08 MA/cm^2
  
  For pulsed operation (D = 8.3e-4):
    j_eff = 2.08 * (8.3e-4)^2 = 2.08 * 6.9e-7 = 1.44e-6 MA/cm^2
    
  This is negligible compared to the DC limit.
```

---

## 10.3.2.7 EM and SM Acceleration Testing

### Test Structure Design

The iPACE-CHIP includes dedicated EM and SM test structures on the die:

**EM Test Structure:**
```
Narrow metal line (minimum width) withKelvin contacts:
  
  ┌──────────────────────────────────────┐
  │  Force+  │    Metal Line    │  Force- │
  │          │  (0.24 um width) │         │
  │  Sense+  │                  │  Sense- │
  └──────────────────────────────────────┘
  
  Force current through the line, measure voltage for resistance.
  Monitor resistance increase over time as EM voids grow.
```

**SM Test Structure:**
```
Metal line with via at one end:
  
  ┌───────────────┐
  │  Metal Line    │
  │  (0.24 um)    │
  │               │
  │    Via        │
  │    │          │
  │  Metal 2      │
  └───────────────┘
  
  Monitor via resistance over time (without current) to detect SM voids.
```

### Accelerated Test Conditions

```
EM accelerated testing:
  Temperature: 250C (acceleration factor ~1000x vs. 37C)
  Current density: 5 MA/cm^2 (acceleration factor ~25x vs. nominal)
  Duration: 500 hours
  
  Total acceleration: 1000 x 25 = 25,000x
  500 hours at 250C, 5 MA/cm^2 = 12.5 million hours at 37C, 0.2 MA/cm^2
  = 1428 years equivalent
  
  If no failure occurs in 500 hours at these conditions, the MTTF at
  operating conditions exceeds 1428 years (>> 10-year requirement).
```

---

## 10.3.2.8 Chapter Summary

Electromigration and stress migration are managed in the iPACE-CHIP through conservative design rules, current density limits, via redundancy, and on-chip monitoring.

Key design rules:

- **Maximum DC current density:** 1.0-2.0 MA/cm^2 depending on metal layer
- **Minimum metal width:** 0.24 um for signals, 0.5 um for power, 1.0 um for output stage
- **Via redundancy:** minimum 2-8 vias depending on current level
- **Spacing:** increased to 0.5-1.0 um for output stage interconnects

Key monitoring:

- **On-chip current monitors** detect overcurrent conditions in the output stage
- **Interconnect resistance monitoring** detects void formation in critical paths
- **Via resistance monitoring** detects degradation in critical via connections

The iPACE-CHIP's EM and SM reliability is ensured by:
- Electromigration budget approach (total EM exposure < 1.0 over 10 years)
- Conservative current density limits (10x margin for pulsed operation)
- Accelerated testing validation (>1400 year equivalent MTTF)
- Real-time monitoring and degradation tracking

The next chapter (10.3.3) covers accelerated life testing methodologies that validate the iPACE-CHIP's reliability predictions.

---

## References

1. Black, J.R., "Electromigration -- A Brief Survey and Some Recent Results," *IEEE TED*, Vol. 16, No. 4, 1969.
2. Hu, C., et al., "Copper Electromigration Lifetime Enhancement with Barrier Layers," *IRPS*, 1999.
3. JEDEC JEP154, "Guideline for Determining Electromigration and Stress Migration Susceptibility of Integrated Circuits," 2009.
4. Dwyer, V.M., et al., "A Thermal Analysis of Stress Migration in IC Interconnects," *IEEE TED*, Vol. 37, No. 3, 1990.
5. IEC 60601-1:2005, "Medical Electrical Equipment -- Part 1."
6. Ho, P.S., and Kwok, T., "Electromigration in Metals," *Annual Review of Materials Science*, Vol. 18, 1988.
7. Shingubara, S., "Electromigration in Advanced Interconnects," *IEEE IEDM*, 2004.
8. IRPS Tutorial Notes, "Interconnect Reliability: EM, SM, and Beyond," 2012.
