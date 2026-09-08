# Power Semiconductor Devices - Concepts

## 1. Power Diode

### Structure
- PN junction with larger area than signal diodes
- Drift region (lightly doped, wide) added for voltage blocking capability
- Higher doping at cathode for better ohmic contact

### Forward Recovery
- When diode is switched from OFF to ON state rapidly
- Initial voltage overshoot occurs before settling to steady-state forward drop
- Caused by stored charge redistribution and conductivity modulation lag
- Forward recovery time (tfr): time for forward voltage to drop to 110% of steady-state value
- Forward recovery voltage (Vfr): peak voltage overshoot
- More significant in fast-recovery and PIN diodes

### Reverse Recovery
- When diode is switched from ON to OFF state
- Stored minority carriers must be removed before diode can block reverse voltage
- Reverse recovery time (trr): time from zero crossing to when reverse current decays to 25% of peak reverse current
- Reverse recovery charge (Qrr): total charge removed during reverse recovery
- Softness factor (S): ratio of tB/tA where tA = time to reach peak reverse current, tB = time to decay from peak
- S > 1 → soft recovery diode (preferred for most applications)
- S < 1 → snap-off diode (causes high EMI)
- Snappy diodes cause voltage spikes due to L di/dt

### Fast Recovery Diode (FRD)
- Designed for reduced trr (typically 35-200 ns)
- Gold doping or electron irradiation to control minority carrier lifetime
- Used in switching converters, inverters
- RE-xxx series (e.g., RE1000 = 1000V, 35A)

### Schottky Diode
- Metal-semiconductor junction (no PN junction)
- Majority carrier device → negligible reverse recovery
- Low forward voltage drop (0.2-0.4V vs 0.7-1.2V for Si PN)
- Lower reverse breakdown voltage (typically < 200V)
- Higher reverse leakage current
- Ideal for low-voltage, high-frequency applications

## 2. Power MOSFET

### Construction
- Vertical structure (DMOS - Double-diffused MOS)
- Source at top, Drain at bottom, Gate on top
- N+ source, P-body, N- drift region, N+ substrate
- Current flows vertically through the device

### Operation
- Enhancement mode (normally OFF)
- Gate voltage > Vth creates inversion channel in P-body
- Electron current flows from source through channel into drift region
- Majority carrier device → fast switching
- No minority carrier storage → no reverse recovery issues

### Key Parameters
- **RDS(on)**: On-state drain-source resistance (increases with voltage rating)
- **VGS(th)**: Gate threshold voltage (typically 2-4V)
- **VGS(max)**: Maximum gate voltage (typically ±20V)
- **ID(max)**: Maximum continuous drain current
- **Ciss, Coss, Crss**: Input, output, reverse transfer capacitances
- **Body diode**: Intrinsic PN junction (slow, high forward drop)

### Advantages
- Voltage-controlled (very high input impedance)
- Very fast switching (ns range)
- No secondary breakdown
- Easy paralleling (positive temperature coefficient of RDS(on))

### Disadvantages
- High RDS(on) for high-voltage devices (RDS(on) ∝ BV^2.5)
- Body diode has poor reverse recovery
- Susceptible to gate oxide damage from ESD

## 3. IGBT (Insulated Gate Bipolar Transistor)

### Construction
- Combination of MOSFET (input) and BJT (output)
- P+ substrate, N- drift, P-body, N+ source, Gate
- MOSFET provides high input impedance
- BJT provides low on-state voltage drop

### Operation
- Gate voltage > Vth creates MOSFET channel
- MOSFET turns on, injecting electrons into N- drift region
- P+ substrate injects holes → conductivity modulation of drift region
- Low on-state voltage (1.5-3V) independent of voltage rating

### Key Parameters
- **VCE(sat)**: Collector-emitter saturation voltage
- **VGE(th)**: Gate-emitter threshold voltage
- **tON, tOFF**: Turn-on and turn-off times
- **Tail current**: Current during turn-off due to stored charge in drift region
- **SOA**: Safe Operating Area

### IGBT Types
- **PT (Punch-Through)**: N+ buffer layer, faster switching, higher VCE(sat)
- **NPT (Non-Punch-Through)**: No buffer, lower VCE(sat), rugged
- **Field Stop**: Combines advantages of PT and NPT

### Advantages
- High input impedance (MOSFET gate)
- Low on-state losses (BJT conductivity modulation)
- High voltage and current capability (up to 6.5kV, 600A+)
- No secondary breakdown

### Disadvantages
- Slower than MOSFET (tail current)
- Limited switching frequency (typically < 100 kHz)
- Latch-up risk at high temperature
- Gate oxide sensitive

## 4. Device Ratings

### Voltage Ratings
- **VRRM**: Maximum repetitive peak reverse voltage
- **VRWM**: Maximum working peak reverse voltage
- **VR(DC)**: DC reverse voltage rating
- **VDS(max)**: Maximum drain-source voltage (MOSFET)
- **VCES**: Collector-emitter voltage with gate shorted (IGBT)
- Design voltage should be 80% of rated for reliability

### Current Ratings
- **IF(AV)**: Average forward current (for rectifier diodes)
- **IF(RMS)**: RMS forward current
- **IFSM**: Non-repetitive peak forward surge current (8.3 ms half-sine for 60Hz)
- **ID(AV)**: Average drain current (MOSFET)
- **IC(cont)**: Continuous collector current (IGBT)
- **ICM**: Peak collector current (pulsed)

### Thermal Ratings
- **Tj(max)**: Maximum junction temperature (150°C or 175°C typical)
- **Rth(j-c)**: Junction-to-case thermal resistance
- **Rth(j-a)**: Junction-to-ambient thermal resistance
- **Pd(max)**: Maximum power dissipation

### Derating
- Current and voltage ratings decrease with temperature
- Always derate by 20-25% for reliability in space applications

## 5. Safe Operating Area (SOA)

### Definition
- Region on I-V plane where device can operate without damage
- Bounded by: maximum current, maximum voltage, maximum power, second breakdown

### SOA Boundaries
1. **RDS(on) line**: V = ID × RDS(on) - left boundary
2. **Maximum current**: horizontal line at top
3. **Maximum power dissipation**: P = V × I = constant (hyperbola)
4. **Second breakdown**: V^n × I = constant (n depends on device)
5. **Maximum voltage**: vertical line at right

### For MOSFETs
- No second breakdown (positive temp coefficient of RDS(on))
- SOA limited by RDS(on), ID(max), power, and BVdss

### For IGBTs
- Latch-up current must be considered
- SOA may be limited at high voltages and currents
- Transient SOA (pulsed) is larger than DC SOA

## 6. Thermal Management

### Power Loss Calculation
- Ptotal = Pconduction + Pswitching + Pgate
- Pconduction = Vce(sat) × IC(AV) for IGBT
- Pconduction = ID² × RDS(on) for MOSFET
- Pswitching = 0.5 × V × I × (tON + tOFF) × fsw

### Thermal Model
- Tj = Ta + Ptotal × Rth(j-a)
- Tj = Tc + Ptotal × Rth(j-c)
- Rth(total) = Rth1 + Rth2 + ... (series thermal circuit)

### Heatsink Selection
- Required Rth = (Tj(max) - Ta) / Ptotal - Rth(j-c) - Rth(c-s) - Rth(s-a)
- Thermal grease at interfaces reduces Rth(c-s) and Rth(s-a)
- Forced air cooling reduces Rth(s-a) significantly

## 7. Comparison Table

| Parameter | Power Diode | MOSFET | IGBT | SCR |
|-----------|-------------|--------|------|-----|
| Control | None | Gate voltage | Gate voltage | Gate pulse |
| Switching Speed | Medium | Very fast (ns) | Medium (μs) | Slow (μs) |
| On-state Loss | Low (VF) | Medium (I²R) | Low (VCE(sat)) | Low (VTM) |
| Switching Loss | Low | Low | Medium | High |
| Max Frequency | N/A | MHz range | <100 kHz | <1 kHz |
| Voltage Rating | Up to 10kV | <1kV typical | Up to 6.5kV | Up to 10kV |
| Current Rating | Up to 5kA | Up to 100A | Up to 600A | Up to 5kA |
| Gate Drive | None | Simple | Simple | Simple pulse |
| Latching | No | No | Possible | Yes |
| Paralleling | Easy | Easy (PTC) | Moderate | Difficult |
| Applications | Rectification | Switching, HF | Motor drives, UPS | High power conversion |

## 8. ISRO-Specific Focus Areas

- Reverse recovery characteristics and their impact on switching losses
- MOSFET vs IGBT selection criteria for different applications
- SOA constraints and derating for space applications
- Thermal management in satellite power systems
- Radiation hardness of semiconductor devices
- Device failure modes in space (single-event effects, total ionizing dose)
