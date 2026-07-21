# Energy Harvesting Interface for Implantable Pacemaker ASICs

## 1. Introduction to Energy Harvesting

Energy harvesting for implantable pacemakers represents the frontier of ultra-low-power design, offering the potential to supplement or replace battery power by extracting energy from the body's natural sources. While the iPACE-CHIP primarily relies on a lithium-iodine battery for its 10-year lifetime, energy harvesting interfaces can extend battery life, provide emergency power backup, or enable future generations of self-powered pacemakers.

The human body offers several energy harvesting opportunities: thermal gradients (body heat), mechanical vibrations (heartbeat, respiration), bio-electrochemical reactions, and radio frequency (RF) energy from external sources. Each source presents unique challenges in terms of power density, reliability, and biocompatibility. This chapter explores the interface circuits required to condition and regulate harvested energy for implantable pacemaker applications.

## 2. Energy Sources for Implantable Pacemakers

### 2.1 Thermal Energy Harvesting

```
Thermal Energy Harvesting from Body Heat:

Principle: Seebeck effect in thermoelectric generators (TEGs)

Power Source:
- Temperature gradient: 1-5°C (skin to core)
- TEG output: 10-100 μV/°C per couple
- Power density: 20-60 μW/cm²

For iPACE-CHIP:
- Available TEG area: 1 cm² (implant surface)
- Temperature gradient: 2°C (conservative)
- TEG output voltage: 20 mV (100 couples × 200 μV/°C × 2°C)
- TEG power: 40 μW (at maximum power point)

Power Budget:
- iPACE-CHIP average power: 3 μW
- TEG power: 40 μW
- Surplus: 37 μW (can charge battery or power additional functions)

Interface Requirements:
- Input voltage: 5-50 mV (very low)
- Must boost to 1.8V
- Efficiency: > 50%
- Quiescent current: < 1 μA
```

### 2.2 Mechanical Energy Harvesting

```
Mechanical Energy Harvesting from Heartbeat:

Principle: Piezoelectric or electromagnetic transduction

Heartbeat Characteristics:
- Rate: 60-100 beats per minute
- Displacement: 0.1-1 mm
- Force: 0.1-1 N
- Energy per beat: 1-10 μJ

For iPACE-CHIP:
- Piezoelectric generator area: 0.5 cm²
- Output voltage: 0.5-5 V (high voltage, low current)
- Output current: 0.1-1 μA average
- Average power: 1-10 μW

Power Budget:
- iPACE-CHIP average power: 3 μW
- Mechanical harvester power: 5 μW (typical)
- Surplus: 2 μW (modest but positive)

Interface Requirements:
- Input voltage: 0.5-5 V (wide range)
- Rectification needed (AC to DC)
- Impedance matching for maximum power transfer
- Quiescent current: < 500 nA
```

### 2.3 Bio-Electrochemical Energy Harvesting

```
Bio-Electrochemical Energy Harvesting:

Principle: Glucose fuel cell or bio-battery

Source: Body glucose oxidation
- Glucose concentration: 4-8 mM (blood)
- Theoretical energy density: 1 MJ/mol
- Practical power density: 1-10 μW/cm²

For iPACE-CHIP:
- Fuel cell area: 0.2 cm²
- Output voltage: 0.3-0.6 V
- Output current: 10-50 μA
- Power: 3-30 μW

Power Budget:
- iPACE-CHIP average power: 3 μW
- Bio-fuel cell power: 10 μW (typical)
- Surplus: 7 μW

Interface Requirements:
- Input voltage: 0.3-0.6 V (very low)
- Must boost to 1.8V
- Impedance: 1-10 kΩ
- Efficiency: > 40%
- Biocompatibility: Critical
```

### 2.4 RF Energy Harvesting

```
RF Energy Harvesting:

Principle: Rectenna (rectifying antenna) for wireless power

RF Source: External transmitter (wearable or room-based)
- Frequency: 402 MHz (MICS band) or 2.4 GHz (ISM band)
- Transmit power: 1-100 mW
- Distance: 10-100 cm
- Received power: 0.1-100 μW

For iPACE-CHIP:
- On-chip antenna area: 0.1 cm² (limited by implant size)
- Received power: 1-10 μW (at 10 cm distance)
- Rectifier efficiency: 30-50%
- Available DC power: 0.3-5 μW

Power Budget:
- iPACE-CHIP average power: 3 μW
- RF harvesting power: 2 μW (typical)
- Deficit: 1 μW (supplement only, not sufficient alone)

Interface Requirements:
- Input voltage: 10-100 mV (RF rectified)
- Wideband matching network
- Low-dropout rectifier
- Quiescent current: < 200 nA
```

## 3. Energy Harvesting Interface Circuits

### 3.1 Ultra-Low-Voltage Boost Converter

```
Ultra-Low-Voltage Boost Converter for TEG:

For boosting 20 mV TEG output to 1.8V:

Architecture: Self-oscillating boost converter

                    TEG Input (20 mV)
                         │
                    ┌────┴────┐
                    │  Input  │
                    │  Filter │
                    │  (10μF) │
                    └────┬────┘
                         │
                    ┌────┴────┐
                    │  NMOS   │
                    │  Switch │
                    │  (M1)   │
                    └────┬────┘
                         │
                    ┌────┴────┐
                    │Inductor │
                    │  (10mH) │
                    └────┬────┘
                         │
                    ┌────┴────┐
                    │  PMOS   │
                    │  Rectify│
                    │  (M2)   │
                    └────┬────┘
                         │
                    ┌────┴────┐
                    │  Output │
                    │  Filter │
                    │  (1μF)  │
                    └────┬────┘
                         │
                    V_OUT (1.8V)

Specifications:
- Input voltage: 5-50 mV
- Output voltage: 1.8V
- Efficiency: 60% (at 20 mV input)
- Start-up voltage: 10 mV (with cold start circuit)
- Quiescent current: 500 nA
- Switching frequency: 10 kHz
- Area: 0.02 mm² (on-chip) + external inductor
```

### 3.2 Cold Start Circuit

```
Cold Start Circuit for Energy Harvesting:

Problem: Boost converter needs minimum voltage to start
Solution: Cold start circuit with ultra-low-voltage oscillator

Architecture:
┌─────────────────────────────────────────────────────────┐
│ Cold Start Circuit                                       │
│                                                         │
│  TEG Input (20 mV) ────────┐                            │
│                             │                            │
│                        ┌────┴────┐                      │
│                        │  Ultra- │                      │
│                        │  Low-   │                      │
│                        │  Voltage│                      │
│                        │  OSC    │                      │
│                        │  (5 mV) │                      │
│                        └────┬────┘                      │
│                             │                            │
│                        ┌────┴────┐                      │
│                        │  Charge │                      │
│                        │  Pump   │                      │
│                        │  (5mV → │                      │
│                        │   0.5V) │                      │
│                        └────┬────┘                      │
│                             │                            │
│                        ┌────┴────┐                      │
│                        │  Main   │                      │
│                        │  Boost  │                      │
│                        │  Conv.  │                      │
│                        │  Start  │                      │
│                        └────┬────┘                      │
│                             │                            │
│                        V_OUT (1.8V)                     │
│                                                         │
│  Cold Start Sequence:                                   │
│  1. Ultra-low-voltage OSC starts at 5 mV               │
│  2. Charge pump boosts 5 mV to 0.5V                    │
│  3. Main boost converter starts at 0.5V                │
│  4. Main converter boosts to 1.8V                      │
│  5. Cold start circuit shuts down (not needed)          │
│                                                         │
│  Cold Start Time: 10 seconds (with 20 mV input)        │
│  Cold Start Energy: 100 nJ                              │
└─────────────────────────────────────────────────────────┘
```

### 3.3 Power Management Unit

```
Energy Harvesting Power Management Unit:

Architecture:
┌─────────────────────────────────────────────────────────┐
│ Energy Harvesting PMU                                    │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Energy Source  │  │  Maximum Power  │              │
│  │  Interface      │──│  Point Tracker  │              │
│  │  (rectifier)    │  │  (MPPT)         │              │
│  └─────────────────┘  └────────┬────────┘              │
│                                │                        │
│                       ┌────────▼────────┐              │
│                       │  Energy         │              │
│                       │  Storage        │              │
│                       │  (supercap or   │              │
│                       │   battery)      │              │
│                       └────────┬────────┘              │
│                                │                        │
│  ┌─────────────────┐  ┌───────▼─────────┐              │
│  │  Load           │──│  Voltage        │              │
│  │  Management     │  │  Regulator      │              │
│  │  (priority)     │  │  (LDO)          │              │
│  └─────────────────┘  └───────┬─────────┘              │
│                               │                         │
│                      ┌────────▼────────┐               │
│                      │  iPACE-CHIP     │               │
│                      │  (1.8V, 3μW)    │               │
│                      └─────────────────┘               │
│                                                         │
│  MPPT Algorithm:                                        │
│  - Perturb and observe                                  │
│  - Update every 1 second                               │
│  - Efficiency: 95% of maximum power point              │
│                                                         │
│  Energy Storage:                                        │
│  - Supercapacitor: 100 μF, 1.8V                        │
│  - Stored energy: 162 μJ                               │
│  - Backup time: 54 seconds (at 3 μW)                   │
│                                                         │
│  PMU Specifications:                                    │
│  - Quiescent current: 100 nA                           │
│  - Efficiency: 80% (end-to-end)                        │
│  - Area: 0.05 mm² (on-chip)                            │
│  - External components: L, C (inductor, capacitor)     │
└─────────────────────────────────────────────────────────┘
```

## 4. Maximum Power Point Tracking

### 4.1 MPPT for TEG

```
TEG Maximum Power Point Tracking:

TEG Model: V_TEG = V_OC - I × R_TEG
Where:
- V_OC = open-circuit voltage (∝ ΔT)
- R_TEG = internal resistance (10-100 Ω)

Maximum power occurs when:
V_MPPT = V_OC / 2
I_MPPT = V_OC / (2 × R_TEG)
P_MPPT = V_OC² / (4 × R_TEG)

MPPT Circuit:
┌─────────────────────────────────────────────────────────┐
│ TEG MPPT Controller                                      │
│                                                         │
│  TEG ────┬─── V_TEG ──── ADC ──── Controller           │
│          │                        │                     │
│          └─── I_TEG ──── ADC ────┘                     │
│                                   │                     │
│                            ┌──────▼──────┐              │
│                            │  MPPT       │              │
│                            │  Algorithm  │              │
│                            │  (P&O)      │              │
│                            └──────┬──────┘              │
│                                   │                     │
│                            ┌──────▼──────┐              │
│                            │  Duty Cycle │              │
│                            │  Control    │              │
│                            └──────┬──────┘              │
│                                   │                     │
│                            ┌──────▼──────┐              │
│                            │  Boost      │              │
│                            │  Converter  │              │
│                            └─────────────┘              │
│                                                         │
│  MPPT Efficiency: 95%                                   │
│  Update Rate: 1 Hz                                      │
│  Power Overhead: 10 nW                                  │
└─────────────────────────────────────────────────────────┘
```

### 4.2 MPPT for Piezoelectric

```
Piezoelectric MPPT:

Challenge: Piezoelectric output is AC, not DC

Solution: Synchronous rectifier + MPPT

Architecture:
┌─────────────────────────────────────────────────────────┐
│ Piezoelectric MPPT                                        │
│                                                         │
│  Piezo ────┬─── Full-Wave ──── DC Bus ──── MPPT        │
│  (AC)      │   Synchron.      (smooth)    Controller   │
│            │   Rectifier                               │
│            │                                            │
│            └─── Impedance ────┘                        │
│                 Matching                                │
│                                                         │
│  Synchronous Rectifier:                                 │
│  - Replaces diodes with MOSFETs                        │
│  - Lower voltage drop (0.1V vs 0.6V)                   │
│  - Higher efficiency (85% vs 60%)                      │
│                                                         │
│  Impedance Matching:                                    │
│  - Piezo impedance: 10-100 kΩ                         │
│  - Optimal load: Match piezo impedance                 │
│  - Adjusted via MPPT duty cycle                        │
│                                                         │
│  Specifications:                                        │
│  - Input: 0.5-5 V AC                                   │
│  - Output: 1.8V DC                                     │
│  - Efficiency: 75%                                     │
│  - Quiescent: 200 nA                                   │
└─────────────────────────────────────────────────────────┘
```

## 5. Energy Storage

### 5.1 Supercapacitor Interface

```
Supercapacitor Interface for Energy Storage:

Supercapacitor Specifications:
- Capacitance: 100 μF
- Voltage rating: 2.5V
- ESR: 1 Ω
- Leakage: 1 μA (at 1.8V)
- Size: 3 mm × 3 mm × 1 mm (surface mount)
- Lifetime: > 10 years

Interface Circuit:
┌─────────────────────────────────────────────────────────┐
│ Supercapacitor Interface                                 │
│                                                         │
│  Energy ────┬─── Charge ──── Supercap ──── Discharge    │
│  Harvester  │   Controller   (100μF)      Controller   │
│             │                                            │
│             └─── Voltage ────┘                          │
│                 Monitor                                  │
│                                                         │
│  Charge Controller:                                     │
│  - Constant current charging: 10 μA                    │
│  - Voltage limit: 1.8V                                 │
│  - Overcharge protection                                │
│                                                         │
│  Discharge Controller:                                  │
│  - Regulated output: 1.8V                              │
│  - Minimum voltage: 1.0V                               │
│  - Load disconnect at min voltage                      │
│                                                         │
│  Stored Energy:                                         │
│  E = 0.5 × C × V² = 0.5 × 100μF × (1.8V)² = 162 μJ  │
│                                                         │
│  Backup Time:                                           │
│  At 3 μW load: 162 μJ / 3 μW = 54 seconds            │
│  At 0.1 μW load: 162 μJ / 0.1 μW = 27 minutes       │
└─────────────────────────────────────────────────────────┘
```

### 5.2 Hybrid Energy Storage

```
Hybrid Energy Storage System:

Combines battery and supercapacitor for optimal performance:

┌─────────────────────────────────────────────────────────┐
│ Hybrid Energy Storage                                     │
│                                                         │
│  ┌─────────────────┐  ┌─────────────────┐              │
│  │  Energy         │  │  Energy         │              │
│  │  Harvester      │──│  Manager        │              │
│  │  (TEG/Piezo)    │  │  (MPPT + ctrl)  │              │
│  └─────────────────┘  └────────┬────────┘              │
│                                │                        │
│              ┌─────────────────┼─────────────────┐     │
│              │                 │                 │     │
│         ┌────▼────┐     ┌─────▼─────┐    ┌─────▼──┐  │
│         │ LiI     │     │ Supercap  │    │ Load   │  │
│         │ Battery │     │ (100 μF)  │    │(iPACE) │  │
│         │ (120 mAh)│   │           │    │        │  │
│         └─────────┘     └───────────┘    └────────┘  │
│                                                         │
│  Operating Strategy:                                    │
│  1. Energy harvester charges supercapacitor first      │
│  2. Supercapacitor provides transient power            │
│  3. Battery provides baseline power                    │
│  4. Energy harvester supplements battery              │
│  5. Battery life extended by harvested energy         │
│                                                         │
│  Battery Life Extension:                                │
│  - Harvested energy: 10 μW × 8 hours/day = 80 μWh/day│
│  - Battery energy: 120 mAh × 2.8V = 336 mWh         │
│  - Extension: 80 μWh / 336 mWh × 365 days = 88 days │
│  - 10-year life extended to 10.24 years (+2.4%)       │
└─────────────────────────────────────────────────────────┘
```

## 6. Reliability and Safety

### 6.1 Biocompatibility

```
Energy Harvester Biocompatibility Requirements:

Materials:
- TEG: Bismuth telluride (Bi₂Te₃) - biocompatible
- Piezo: PZT (lead zirconate titanate) - coated
- Supercapacitor: Carbon electrode - biocompatible
- Encapsulation: Titanium or ceramic hermetic package

Regulatory Requirements:
- ISO 10993 (Biological Evaluation of Medical Devices)
- Biocompatibility testing: cytotoxicity, sensitization
- Long-term stability: > 10 years in body environment

Safety Considerations:
- Maximum temperature: 41°C (1°C above body temp)
- Maximum current density: 100 μA/cm² (tissue heating)
- Electromagnetic interference: < MICS band limits
- Mechanical stress: No tissue damage
```

### 6.2 Fault Protection

```
Energy Harvesting Fault Protection:

Fault 1: Harvester Failure
- Detection: Output power drops below threshold
- Response: Switch to battery-only mode
- Recovery: Automatic when harvester restored

Fault 2: Overvoltage
- Detection: Output voltage > 2.0V
- Response: Disconnect harvester
- Recovery: Automatic when voltage drops

Fault 3: Overcurrent
- Detection: Output current > 50 μA
- Response: Current limiting
- Recovery: Automatic

Fault 4: Short Circuit
- Detection: Output voltage near 0V with high current
- Response: Immediate disconnect
- Recovery: Manual reset required

Fault 5: Supercapacitor Failure
- Detection: ESR increase or capacitance decrease
- Response: Switch to battery backup
- Recovery: Replace device (if possible)
```

## 7. Power Budget Analysis

### 7.1 Energy Harvesting Power Budget

```
Energy Harvesting Power Budget:

Power Generation:
┌──────────────────────┬──────────┬──────────┬──────────┐
│ Source               │ Average  │ Peak     │ Efficiency│
├──────────────────────┼──────────┼──────────┼──────────┤
│ Thermal (TEG)        │ 40 μW    │ 100 μW   │ 60%      │
│ Mechanical (piezo)   │ 5 μW     │ 50 μW    │ 75%      │
│ RF harvesting        │ 2 μW     │ 10 μW    │ 40%      │
├──────────────────────┼──────────┼──────────┼──────────┤
│ TOTAL                │ 47 μW    │ 160 μW   │ 55% avg  │
└──────────────────────┴──────────┴──────────┴──────────┘

Power Consumption:
┌──────────────────────┬──────────┬──────────┐
│ Block                │ Power    │ Duty     │
├──────────────────────┼──────────┼──────────┤
│ iPACE-CHIP (normal)  │ 3 μW     │ 100%     │
│ PMU overhead         │ 0.5 μW   │ 100%     │
│ MPPT overhead        │ 0.01 μW  │ 100%     │
├──────────────────────┼──────────┼──────────┤
│ TOTAL                │ 3.51 μW  │ 100%     │
└──────────────────────┴──────────┴──────────┘

Net Energy Balance:
Generated: 47 μW
Consumed: 3.51 μW
Surplus: 43.49 μW (92.5% surplus)

The surplus can:
1. Charge the LiI battery (extend life)
2. Power additional functions
3. Provide emergency backup
```

### 7.2 Battery Life Extension

```
Battery Life Extension with Energy Harvesting:

Without Energy Harvesting:
- Average power: 3 μW
- Battery energy: 336 mWh
- Battery life: 336 mWh / 3 μW = 112,000 hours = 12.8 years

With Energy Harvesting:
- Average power: 3 μW
- Harvested power: 47 μW (surplus used for charging)
- Net battery drain: 3 μW - 47 μW = -44 μW (net charging!)
- Battery life: Unlimited (net energy positive)

Practical Scenario:
- Energy harvesting availability: 70% (not always optimal)
- Effective harvested power: 47 × 0.7 = 32.9 μW
- Net battery drain: 3 - 32.9 = -29.9 μW (still net positive)

Battery Life Impact:
- Battery actually gets charged during high harvesting periods
- Battery discharge occurs during low harvesting periods
- Net effect: Battery life extended to > 20 years
- Device replacement essentially unnecessary
```

## 8. Summary

Energy harvesting interfaces for the iPACE-CHIP pacemaker ASIC demonstrate the feasibility of supplementing battery power with harvested energy from thermal (40 μW), mechanical (5 μW), and RF (2 μW) sources. The total harvested power of 47 μW far exceeds the device's 3 μW average consumption, creating a net positive energy balance that can extend battery life beyond 20 years. The interface circuits include ultra-low-voltage boost converters (efficiency 60% at 20 mV input), cold start circuits (start at 5 mV), maximum power point trackers (95% efficiency), and hybrid energy storage (supercapacitor + battery). While energy harvesting adds complexity and area overhead, the potential for essentially unlimited battery life makes it a compelling technology for next-generation implantable pacemakers.

## References

1. Deterre, M., et al., "Energy Harvesting for Pacemakers," IEEE Trans. Biomedical Circuits and Systems, 2014.
2. iPACE-CHIP Project Internal Documentation: Energy Harvesting Feasibility Study, Rev 1.0.
3. Mitcheson, P.D., et al., "Energy Harvesting for Implantable Medical Devices," Proc. IEEE, 2014.
4. Tashiro, R., et al., "Feasibility of Cardiac Pacemaker Powered by Thermoelectric Generator," PACE, 2002.
5. TSMC 0.18μm Mixed-Signal Process Design Manual: Ultra-Low-Power Analog Library.
