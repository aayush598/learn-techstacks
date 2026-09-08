# Rectifiers - Concepts

## 1. Half-Wave Rectifier (with Diode)

### Circuit Operation
- Single diode conducts during positive half-cycle
- Output appears only during positive half-cycle
- Negative half-cycle blocked (output = 0)
- Simple, low-cost, but poor performance

### Waveforms
- Input: AC sine wave
- Output: Positive half-sine only
- Diode current: half-sine pulses
- Input current: same as diode current (non-sinusoidal)

### Key Parameters
- **Vm**: Peak input voltage
- **Vdc**: Average output voltage = Vm/π
- **Vrms**: RMS output voltage = Vm/2
- **Idc**: Average load current = Vm/(πRL)
- **Irms**: RMS load current = Vm/(2RL)

### With SCR (Phase Control)
- Firing angle α controls output
- Vdc = Vm/(2π) × (1 + cos α)
- Allows variable DC output
- Used in battery chargers, low-power supplies

## 2. Full-Wave Center Tap Rectifier

### Circuit Operation
- Two diodes, center-tapped transformer
- Each diode conducts during alternate half-cycles
- Output frequency = 2 × input frequency
- Transformer utilization factor lower than bridge

### Waveforms
- Input: AC sine wave (full cycle)
- Output: Full-wave rectified (100 Hz for 50 Hz input)
- Diode current: half-sine in each diode
- Input current: full sine wave (with DC offset in each half)

### Key Parameters
- **Vm**: Peak voltage from center tap to each end
- **Vdc**: Average output voltage = 2Vm/π
- **Vrms**: RMS output voltage = Vm/√2
- **Idc**: Average load current = 2Vm/(πRL)
- **Peak Inverse Voltage (PIV)**: 2Vm (each diode)

### With SCR (Phase Control)
- Vdc = (Vm/π) × (1 + cos α)
- α range: 0° to 180°
- Used in medium-power controlled rectifiers

## 3. Single-Phase Full-Bridge Rectifier

### Circuit Operation
- Four diodes in bridge configuration
- No center-tapped transformer needed
- Better transformer utilization
- Most common topology for single-phase rectification

### Operation Sequence
- D1, D2 conduct during positive half-cycle
- D3, D4 conduct during negative half-cycle
- Output always positive across load

### Waveforms
- Input current: square-like (with harmonics)
- Output voltage: full-wave rectified sine
- Output frequency: 2 × input frequency
- Input power factor: depends on load

### Key Parameters
- **Vm**: Peak input voltage
- **Vdc**: Average output voltage = 2Vm/π
- **Vrms**: RMS output voltage = Vm/√2
- **TUF**: Transformer Utilization Factor = 0.812
- **FF**: Form Factor = Vrms/Vdc = π/(2√2) = 1.11
- **RF**: Ripple Factor = √(FF² - 1) = 0.482

### With SCR (Fully Controlled Bridge)
- Four SCRs replace diodes
- Vdc = (2Vm/π) × cos α
- α range: 0° to 180° (for resistive load)
- For inductive load with freewheeling: 0° to 180°

### With SCR (Semi-Converter)
- Two SCRs + two diodes
- Vdc = (Vm/π) × (1 + cos α)
- Lower harmonic content than full converter
- α range: 0° to 180°

## 4. Three-Phase Rectifiers

### Three-Phase Half-Wave
- Three diodes (or SCRs), common cathode
- Each phase conducts for 120°
- Vdc = (3√3 × Vm_phase)/(2π) × cos α

### Three-Phase Full-Bridge
- Six diodes (or SCRs)
- Most common three-phase topology
- Vdc = (3√3 × Vm_phase)/π × cos α = (3Vml/π) × cos α
- Where Vml = √3 × Vm_phase = line-to-line peak voltage
- Output ripple frequency: 6 × supply frequency

## 5. Freewheeling Diode (FD)

### Purpose
- Provides path for inductive load current when main devices turn off
- Prevents voltage spikes from L di/dt
- Improves output voltage waveform
- Reduces distortion and improves power factor

### Operation
- Connected across load (reverse polarity to output)
- Conducts when main device turns off
- Allows load current to decay through FD
- Clamps output voltage to zero during freewheeling

### Benefits
1. **Prevents voltage spikes**: L di/dt path provided
2. **Improves Vdc**: Output voltage doesn't go negative
3. **Reduces harmonics**: Smoother output current
4. **Improves power factor**: Input current closer to sinusoidal
5. **Protects devices**: No voltage spikes across SCRs

### With Fully Controlled Bridge
- Without FD: Vdc = (2Vm/π) × cos α (can be negative for α > 90°)
- With FD: Vdc = (Vm/π) × (1 + cos α) (always positive)
- α range becomes 0° to 180° for rectification

### Placement
- Connected anti-parallel across load terminals
- Must carry full load current
- Fast recovery diode preferred
- Rating: same as load current rating

## 6. Performance Parameters

### Ripple Factor (RF)
```
RF = √(Vrms² - Vdc²) / Vdc = √(FF² - 1)

Half-wave: RF = 1.21 (poor)
Full-wave: RF = 0.482 (good)
Three-phase: RF = 0.04 (excellent)
```

### Form Factor (FF)
```
FF = Vrms / Vdc

Half-wave: FF = π/2 = 1.57
Full-wave: FF = π/(2√2) = 1.11
Three-phase 6-pulse: FF ≈ 1.0009
```

### Rectification Efficiency (η)
```
η = Pdc / Pac = Vdc²/RL / (Vrms²/RL) = (Vdc/Vrms)²

Half-wave: η = (2/π)² = 40.6%
Full-wave: η = (2√2/π)² = 81.2%
Three-phase: η = 99.9%
```

### Transformer Utilization Factor (TUF)
```
TUF = Pdc / VA rating of transformer

Half-wave: TUF = 0.287
Full-wave center tap: TUF = 0.693
Full-wave bridge: TUF = 0.812
Three-phase half-wave: TUF = 0.675
Three-phase full-wave: TUF = 0.955
```

### Power Factor (Input)
```
PF = Pinput / (Vin × Iin)

For resistive load with diode bridge: PF ≈ 0.9
For inductive load: PF improves with higher inductance
With FD: PF improves significantly
```

### Crest Factor
```
CF = Ipeak / Irms

Half-wave: CF = 2
Full-wave: CF = √2 = 1.414
Three-phase: CF ≈ 1.414
```

## 7. Filter Circuits

### Capacitor Filter
- Large capacitor across load
- Charges during conduction, discharges between pulses
- Reduces ripple significantly
- Output approaches DC with small ripple

### Design Considerations
- **Time constant**: τ = RL × C >> T (period)
- **Ripple voltage**: ΔV ≈ Iload/(2fC) for full-wave
- **Peak diode current**: Much higher than average (2-5× Iload)
- **Capacitor value**: C = Iload/(2f × ΔV) for full-wave

### LC Filter
- Inductor in series, capacitor in parallel
- Better ripple reduction than C alone
- Inductor smooths current, capacitor smooths voltage
- Output approaches pure DC

### π-Filter
- C-L-C configuration
- Excellent ripple rejection
- Used in high-quality power supplies
- Larger and more expensive

### Comparison
| Filter Type | Ripple | Size | Cost | Application |
|-------------|--------|------|------|-------------|
| C only | Medium | Small | Low | Low-power supplies |
| LC | Low | Medium | Medium | Medium-power supplies |
| π | Very low | Large | High | High-quality supplies |

## 8. ISRO-Specific Focus

- Rectifier efficiency for satellite power systems
- Input power factor requirements (EMC compliance)
- Redundancy in rectifier configurations
- Radiation effects on semiconductor devices
- Thermal management in space environment
- EMI filtering requirements for spacecraft
