# GTO, TRIAC, DIAC - Concepts

## 1. GTO (Gate Turn-Off Thyristor)

### Construction
- Similar four-layer (PNPN) structure to SCR
- Cathode divided into many narrow fingers (interdigitated)
- Gate electrode surrounds cathode fingers
- P2 base layer is thin to allow carrier extraction
- Anode short (P1-N1 shorts) for faster turn-off
- N+ buffer layer for punch-through design

### Turn-Off Mechanism
- **Turn-on**: Same as SCR (positive gate pulse)
- **Turn-off**: Large negative gate pulse extracts carriers from P2 base
- Negative gate current pulls holes from P2 base
- Injected electrons from N2 cathode are extracted through gate
- Stored charge removed, J2 recovers blocking capability
- Turn-off gain βoff = IA(-IG) = IA/|IG| (typically 3-5)

### Key Parameters
- **IAM**: Maximum anode current
- **ITGQ**: Maximum turn-off anode current
- **βoff**: Turn-off gain (IA/|IG|)
- **tq**: Turn-off time (stored time + fall time)
- **ts**: Stored time (time for gate to establish current path)
- **tf**: Fall time (anode current drops to 10%)
- **sn：dv/dt rating at turn-off
- **tc**: Circuit-commutated turn-off time

### Turn-Off Characteristics
```
Negative gate pulse → extracts carriers from P2 base
IA must be reduced below ITGQ before tq expires
Remaining current is "tail current" due to stored charge
```

### GTO vs SCR Comparison
| Parameter | SCR | GTO |
|-----------|-----|-----|
| Turn-on | Gate pulse | Gate pulse |
| Turn-off | Natural/forced commutation | Negative gate pulse |
| Turn-off gain | N/A | 3-5 |
| Switching loss | High | Medium |
| Frequency | <1 kHz | 1-5 kHz |
| Gate drive power | Low | High (turn-off) |
| On-state loss | Low | Higher than SCR |

### Applications
- Medium voltage drives (2-6 kV)
- Traction inverters
- FACTS (Flexible AC Transmission Systems)
- HVDC converters (older technology)
- Being replaced by IGBTs in many applications

## 2. TRIAC (Triode for Alternating Current)

### Construction
- Two SCRs connected in anti-parallel (monolithic)
- Single gate terminal controls both directions
- Five-layer structure (N-P-N-P-N)
- Three terminals: MT1, MT2, Gate
- Gate near MT1 for triggering

### Operation - Four Quadrants
```
Quadrant I:   MT2(+), Gate(+)  → MT1(-), Gate(-)  [Most sensitive]
Quadrant II:  MT2(+), Gate(-)  → MT1(-), Gate(+)  [Moderate]
Quadrant III: MT2(-), Gate(-)  → MT1(+), Gate(+)  [Moderate]
Quadrant IV:  MT2(-), Gate(+)  → MT1(+), Gate(-)  [Least sensitive]
```

### Triggering Modes
1. **I+ mode**: MT2+, Gate+ → Main SCR1 triggers, sensitivity = 1
2. **I- mode**: MT2+, Gate- → Auxiliary SCR triggers, sensitivity = 0.3-1
3. **III- mode**: MT2-, Gate- → Main SCR2 triggers, sensitivity = 1
4. **III+ mode**: MT2-, Gate+ → Auxiliary SCR triggers, sensitivity = 0.3

### Key Parameters
- **VDRM**: Repetitive peak off-state voltage (up to 1kV)
- **IT(RMS)**: RMS on-state current (up to 40A)
- **IH**: Holding current (10-50 mA typical)
- **IL**: Latching current
- **VGT**: Gate trigger voltage
- **IGT**: Gate trigger current
- **dv/dt**: Critical rate of voltage rise (100-1000 V/μs)
- **di/dt**: Critical rate of current rise

### Quadrant IV Sensitivity
- Least sensitive quadrant
- Requires higher gate current
- In practice, AC triggering alternates between I+ and III-
- Quadrant IV triggering is avoided by proper gate circuit design
- snubber circuits help with dv/dt immunity

### TRIAC vs Two SCRs
| Feature | TRIAC | Two anti-parallel SCRs |
|---------|-------|------------------------|
| Package | Single | Two separate devices |
| Gate drive | Single | Two independent |
| Current rating | Up to 40A | Up to kA |
| Voltage rating | Up to 1kV | Up to several kV |
| Switching speed | Moderate | Faster |
| Cost | Lower (medium power) | Higher |
| Isolation | None | Can have separate isolation |

### Applications
- AC voltage regulators (light dimmers)
- Small motor speed control
- Heating control
- Solid-state relays
- Low-medium power AC switching (up to ~5 kW)

## 3. DIAC (Diode for Alternating Current)

### Construction
- Two-layer structure (PN or NPN)
- No gate terminal
- Symmetric breakover in both polarities
- Also called: trigger diode, symmetrical trigger diode

### Operation
- Off-state: blocks current in both directions
- When |V| > VBO (breakover voltage, ~32V typical):
  - Negative resistance region
  - Voltage drops to ~1-2V
  - Current increases rapidly
- Symmetric: same VBO in both polarities

### Key Parameters
- **VBO**: Breakover voltage (20-60V, typically 32V)
- **VBO(BO)**: Voltage drop after breakover (1-2V)
- **ID**: Off-state current (very small)
- **ITS**: Switching current (current at which switching occurs)
- **DV/DT**: Rate of voltage change (affects triggering)

### V-I Characteristic
```
     I ↑
       |      /  Breakover
       |     / ← Negative resistance
       |    /
       |---/--- → Forward blocking
       |/
-------+--------→ V
      /|
     / |
    /  |  Reverse blocking
   /   |
```

### Applications
- Triggering TRIACs in AC control circuits
- Relaxation oscillators
- Timing circuits
- Pulse generators
- Overvoltage protection (crowbar-like)

### DIAC-TRIAC Circuit
```
AC Supply → TRIAC → Load
              ↑
         DIAC ← Capacitor ← Resistor
              ↑
         Gate of TRIAC

Capacitor charges through R until Vc > VDIAC
DIAC fires → capacitor discharges into TRIAC gate
TRIAC turns on → conduction until current zero
```

## 4. Comparison Table

| Parameter | SCR | GTO | TRIAC | DIAC |
|-----------|-----|-----|-------|------|
| Layers | 4 (PNPN) | 4 (PNPN) | 5 | 2 |
| Terminals | A, K, G | A, K, G | MT1, MT2, G | A, K |
| Turn-on | Gate+ | Gate+ | Gate± | Breakover |
| Turn-off | Current→0 | Gate- | Current→0 | Current→0 |
| Current direction | Unidirectional | Unidirectional | Bidirectional | Bidirectional |
| Gate control | ON only | ON and OFF | ON both dirs | None |
| Max current | kA | kA | 40A | 1A |
| Max voltage | 10kV | 6kV | 1kV | 100V |
| Switching freq | <1 kHz | 1-5 kHz | <1 kHz | N/A |
| Gate power | Low | High | Low | None |
| Applications | High power DC/AC | Medium drives | AC control | Triggering |

## 5. Selection Criteria

### When to Use GTO
- Medium voltage (2-6 kV) applications
- Where forced commutation is needed but IGBT voltage is insufficient
- Traction and industrial drives
- HVDC (legacy systems)

### When to Use TRIAC
- AC phase control below 5 kW
- Simple, low-cost AC dimming
- Small motor speed control
- Heating element control
- Where bidirectional switching is needed

### When to Use DIAC
- As TRIAC trigger element
- In relaxation oscillators
- For symmetric voltage reference
- In timing circuits

## 6. ISRO-Specific Focus

- TRIAC for satellite thermal control (heater switching)
- GTO for high-power satellite power systems (legacy)
- Radiation effects on gate trigger thresholds
- Reliability considerations for space-grade TRIACs
- Redundancy requirements for critical switching functions
