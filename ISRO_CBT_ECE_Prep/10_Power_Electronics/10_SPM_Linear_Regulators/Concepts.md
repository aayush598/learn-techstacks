# SMPS and Linear Regulators - Concepts

## 1. Switched-Mode Power Supply (SMPS) Topologies

### Flyback Converter
- Derived from buck-boost with isolation
- Coupled inductor stores energy during ON, transfers during OFF
- Simple, low component count
- Up to 150W typically
- Multiple outputs possible
- Cross-regulation issues

### Forward Converter
- Derived from buck with isolation
- Transformer transfers energy during ON time
- Output inductor and capacitor filter
- 100W to 500W range
- Better regulation than flyback
- Requires reset winding

### Push-Pull Converter
- Two switches on transformer primary
- Alternating conduction
- High transformer utilization
- 100W to 1kW range
- Voltage stress = 2Vin on switches
- Good for low-input voltage applications

### Half-Bridge Converter
- Two capacitors split DC bus
- Two switches alternate
- Voltage stress = Vin on switches
- 200W to 2kW range
- Popular for PC power supplies

### Full-Bridge Converter
- Four switches in H-bridge
- Highest power capability
- 500W to 10kW+ range
- Phase-shifted control for ZVS
- Used in high-power applications

### Comparison Table
| Topology | Power Range | Isolation | Outputs | Complexity |
|----------|-------------|-----------|---------|------------|
| Flyback | <150W | Yes | Multiple | Low |
| Forward | 100-500W | Yes | 1-2 | Medium |
| Push-Pull | 100-1kW | Yes | 1-2 | Medium |
| Half-Bridge | 200-2kW | Yes | 1-2 | Medium |
| Full-Bridge | 500W-10kW+ | Yes | 1+ | High |

## 2. Linear vs Switching Regulators

### Linear Regulator
- Pass transistor operates in linear (active) region
- Acts as variable resistor
- Simple, low cost
- Low noise
- Poor efficiency (especially for large Vin-Vo difference)

### Switching Regulator
- Pass transistor switches between ON/OFF
- Uses LC filter to average
- Higher efficiency (85-95%)
- More complex
- Generates switching noise
- Can step up or down

### Comparison
| Parameter | Linear | Switching |
|-----------|--------|-----------|
| Efficiency | 30-60% | 85-95% |
| Output noise | Very low | Moderate (switching) |
| Complexity | Low | High |
| Cost | Low | Medium-High |
| Size | Large (heatsink) | Small |
| Transient response | Fast | Moderate |
| EMI | Low | High |
| Input-output ratio | Vo < Vin only | Vo can be >, <, or = Vin |

### When to Use Linear
- Low dropout voltage (Vo close to Vin)
- Low noise required (analog circuits, RF)
- Low power (<1W)
- Simple, low-cost design

### When to Use Switching
- Large Vin-Vo difference
- High power (>1W)
- Efficiency critical (battery operation)
- Need boost or buck-boost function

## 3. Linear Regulator Efficiency

### Efficiency Formula
```
η = Po/Pin = Vo × Io / (Vin × Iin)
η ≈ Vo/Vin (for low quiescent current)

Example:
Vin = 12V, Vo = 5V
η = 5/12 = 41.7% (poor)
```

### Power Dissipation
```
Pd = (Vin - Vo) × Io + Vin × Iq
Pd ≈ (Vin - Vo) × Io (if Iq << Io)

Example:
Pd = (12-5) × 1 = 7W (for 1A load)
Requires heatsink!
```

### Dropout Voltage
```
Vdropout = Vin - Vo(min) required
For 78xx: Vdropout ≈ 2V
For LDO: Vdropout ≈ 0.1-0.5V
```

## 4. 78xx Voltage Regulators

### Fixed Positive Regulators
- 7805: +5V output
- 7808: +8V output
- 7812: +12V output
- 7815: +15V output
- 7824: +24V output

### Pin Configuration
- Pin 1: Input
- Pin 2: Ground
- Pin 3: Output

### Key Specifications
- Output voltage tolerance: ±4%
- Dropout voltage: 2V typical
- Line regulation: 10-50 mV/V
- Load regulation: 10-50 mV
- Maximum output current: 1A (with heatsink)
- Quiescent current: 5-8 mA

### Fixed Negative Regulators
- 7905: -5V output
- 7912: -12V output
- 7915: -15V output

### Adjustable Regulators
- LM317: adjustable positive (1.25V to 37V)
- LM337: adjustable negative (-1.25V to -37V)
- Output: Vo = 1.25 × (1 + R2/R1)

### Protection Features
- Current limiting (foldback)
- Thermal shutdown
- SOA protection
- Input polarity reversal protection

## 5. Low-Dropout Regulators (LDO)

### What is LDO?
- Linear regulator with very low dropout voltage
- Uses PNP or PMOS pass element
- Dropout: 0.1-0.5V (vs 2V for 78xx)
- Better efficiency when Vin-Vo is small

### LDO vs Standard Linear
| Parameter | Standard (78xx) | LDO |
|-----------|-----------------|-----|
| Dropout | 2V | 0.1-0.5V |
| Efficiency at Vin=5.5V, Vo=5V | 91% (if dropout met) | 90% |
| Efficiency at Vin=12V, Vo=5V | 41.7% | 41.7% |
| Noise | Low | Very low |
| Cost | Very low | Low-Medium |

### LDO Applications
- Battery-powered devices (near end-of-life voltage)
- Noise-sensitive circuits (RF, audio, ADC/DAC)
- Post-regulation after SMPS
- Reference voltage supplies

### LDO Specifications
- Dropout voltage: 0.1-0.5V
- PSRR (Power Supply Rejection Ratio): 60-80 dB
- Output noise: 10-100 μVrms
- Quiescent current: 1-100 μA (ultra-low for battery)
- Line/load regulation: very good

## 6. Ripple Rejection

### Definition
- Ability to reject input voltage ripple at output
- Measured in dB (PSRR or ripple rejection)
- Higher dB → better rejection

### PSRR Formula
```
PSRR = 20 × log10(ΔVin/ΔVo) dB

Typical values:
78xx: 60-72 dB (at 120 Hz)
LDO: 60-80 dB (at 120 Hz)
Switching: 20-40 dB (at switching frequency)
```

### Frequency Dependence
```
PSRR decreases with frequency
At low freq (120 Hz): high PSRR (60-80 dB)
At high freq (1 MHz): low PSRR (20-40 dB)

LDO datasheet shows PSRR vs frequency curve
```

### Improving Ripple Rejection
1. Add input capacitor (reduces source impedance)
2. Add output capacitor (improves transient response)
3. Use post-regulator after SMPS
4. Choose LDO with high PSRR at ripple frequency

## 7. SMPS Design Considerations

### Input Filter
- Differential mode choke
- Common mode choke
- X and Y capacitors
- Meets conducted EMI standards

### Output Filter
- LC filter for buck-derived topologies
- Capacitor ESR affects ripple and stability
- Low-ESR capacitors preferred
- Bulk + ceramic capacitor combination

### Control Loop
- Voltage mode control
- Current mode control
- Type II or Type III compensator
- Bandwidth: 1/10 to 1/5 of switching frequency

### Protection
- Overcurrent protection (foldback, constant current)
- Overvoltage protection (crowbar, OVP IC)
- Short circuit protection
- Thermal shutdown
- Input undervoltage lockout (UVLO)

## 8. ISRO-Specific Focus

- SMPS for satellite power distribution
- Linear regulators for noise-sensitive analog circuits
- Radiation hardness requirements
- Efficiency for power budget compliance
- EMI filtering for electromagnetic compatibility
- Redundancy in power supply configurations
