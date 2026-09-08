# DC-DC Converters - Concepts

## 1. Buck Converter (Step-Down)

### Circuit
- Switch (MOSFET/IGBT) in series with input
- Diode (freewheeling) across load
- Inductor in series with output
- Capacitor across output for filtering

### Operation
- **Switch ON**: Current flows through L to load, L stores energy
- **Switch OFF**: L releases energy through diode to load
- Output voltage always less than input voltage

### Key Equations (CCM)
```
Vo = D × Vin
D = duty cycle = ton/T
Vo/Vin = D (0 ≤ D ≤ 1)
```

### Waveforms
- Vo: PWM pulses (0 to Vin)
- IL: triangular waveform
- Average Vo = D × Vin
- Output ripple depends on L and C

### Applications
- CPU voltage regulators (12V to 1V)
- Battery-powered devices
- Point-of-load converters

## 2. Boost Converter (Step-Up)

### Circuit
- Inductor at input
- Switch to ground
- Diode to output
- Capacitor across output

### Operation
- **Switch ON**: L stores energy (current through L to ground)
- **Switch OFF**: L releases energy (VL adds to Vin) → Vo > Vin
- Output voltage always greater than input voltage

### Key Equations (CCM)
```
Vo = Vin/(1-D)
Vo/Vin = 1/(1-D) (D approaches 1 → Vo very high)
D = 1 - Vin/Vo
```

### Applications
- Power factor correction (PFC)
- Battery to higher voltage bus
- LED drivers
- Solar MPPT converters

## 3. Buck-Boost Converter

### Circuit
- Switch in series with input
- Inductor to ground
- Diode to output (inverted polarity)
- Capacitor across output

### Operation
- **Switch ON**: L stores energy from Vin
- **Switch OFF**: L releases energy to load (inverted polarity)
- Output can be higher or lower than input
- Output polarity is inverted

### Key Equations (CCM)
```
Vo/Vin = D/(1-D)   [magnitude]
Vo is negative (inverted)

D < 0.5: Vo < Vin (buck mode)
D = 0.5: Vo = Vin
D > 0.5: Vo > Vin (boost mode)
```

### Applications
- ±5V or ±12V from single battery
- Negative voltage generation
- Regulated supplies from variable input

## 4. Flyback Converter

### Circuit
- Coupled inductor (transformer-like energy storage)
- Switch on primary side
- Diode and capacitor on secondary side
- Provides isolation

### Operation
- **Switch ON**: Energy stored in magnetizing inductance
- **Switch OFF**: Energy transferred to secondary through diode
- No energy transfer during ON time (unlike forward converter)

### Key Equations
```
Vo = Vin × (N2/N1) × D/(1-D)

Where:
N2/N1 = turns ratio
D = duty cycle

Vo/Vin = (N2/N1) × D/(1-D)
```

### Applications
- Low-power isolated supplies (up to 150W)
- AC-DC adapters
- LED drivers
- Auxiliary power supplies

## 5. Cuk Converter

### Circuit
- Coupled inductor (series capacitors transfer energy)
- Input inductor, output inductor
- Switch and diode
- Provides isolation (with coupled inductors)

### Operation
- Energy stored in input inductor during ON
- Energy transferred to output during OFF
- Output polarity is inverted (can be corrected with coupled inductors)
- Continuous input and output currents (low ripple)

### Key Equations (CCM)
```
Vo/Vin = D/(1-D)   [magnitude, inverted polarity]

With isolation:
Vo = Vin × (N2/N1) × D/(1-D)
```

### Advantages over Buck-Boost
- Continuous input current (lower EMI)
- Continuous output current (lower ripple)
- Better efficiency
- Suitable for high-power applications

## 6. Duty Cycle Relationships Summary

| Converter | Vo/Vin (CCM) | D Range | Polarity |
|-----------|--------------|---------|----------|
| Buck | D | 0-1 | Same |
| Boost | 1/(1-D) | 0-1 | Same |
| Buck-Boost | D/(1-D) | 0-1 | Inverted |
| Flyback | (N2/N1)×D/(1-D) | 0-1 | Depends on winding |
| Cuk | D/(1-D) | 0-1 | Inverted |

## 7. CCM vs DCM

### Continuous Conduction Mode (CCM)
- Inductor current never falls to zero
- Continuous energy transfer
- Lower peak currents
- Better for medium-high power
- Vo depends on D only (simpler control)

### Discontinuous Conduction Mode (DCM)
- Inductor current falls to zero each cycle
- Discontinuous energy transfer
- Higher peak currents
- Better for low-power, light-load operation
- Vo depends on load (more complex control)

### Boundary between CCM and DCM
```
Critical inductance:
LC = (1-D) × R/(2f)

Or equivalently:
Io(critical) = (Vin × D × (1-D)²)/(2Lf)

For Io > Io(critical) → CCM
For Io < Io(critical) → DCM
```

### Advantages/Disadvantages
| Aspect | CCM | DCM |
|--------|-----|-----|
| Output ripple | Lower | Higher |
| Peak current | Lower | Higher |
| Control | Simpler (Vo = f(D)) | Complex (Vo = f(D,RL)) |
| Efficiency | Higher at full load | Lower at full load |
| Transient response | Slower | Faster |
| EMI | Lower | Higher |

## 8. ISRO-Specific Focus

- Buck converters for satellite bus voltage regulation
- Boost converters for solar panel MPPT
- Flyback converters for isolated auxiliary supplies
- Efficiency requirements for spacecraft power systems
- Radiation effects on switching devices
- EMI filtering for electromagnetic compatibility
