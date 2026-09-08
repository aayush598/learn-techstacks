# Inverters - Concepts

## 1. Single-Phase Half-Bridge Inverter

### Circuit
- Two switches (Q1, Q2) in series across DC bus
- Two capacitors (C1, C2) split DC bus voltage
- Load connected between switch midpoint and capacitor midpoint
- Center-tapped DC bus provides ±Vin/2

### Operation
- Q1 ON, Q2 OFF: Vo = +Vin/2
- Q1 OFF, Q2 ON: Vo = -Vin/2
- Alternating at switching frequency
- Output: square wave ±Vin/2

### Output Voltage
- Peak = Vin/2 (half of DC bus)
- RMS = Vin/2 (for square wave)
- Fundamental peak = (2/π) × Vin/2 = Vin/π

### Advantages
- Simple circuit (2 switches)
- No shoot-through risk (capacitors provide dead time)

### Disadvantages
- Requires split DC bus (two capacitors)
- Output voltage is half of full bridge
- Capacitor voltage balancing needed

## 2. Single-Phase Full-Bridge Inverter

### Circuit
- Four switches (Q1-Q4) in H-bridge configuration
- Load connected between leg midpoints
- Full DC bus voltage across load

### Operation Modes
- **Mode 1**: Q1, Q4 ON → Vo = +Vin
- **Mode 2**: Q2, Q3 ON → Vo = -Vin
- **Mode 3**: Q1, Q3 ON → Vo = 0 (freewheeling)
- **Mode 4**: Q2, Q4 ON → Vo = 0 (freewheeling)

### Output Voltage
- Peak = Vin (full DC bus voltage)
- RMS = Vin (for square wave)
- Fundamental peak = 4Vin/π = 1.27Vin

### Bipolar Switching
- Q1/Q4 ON → +Vin
- Q2/Q3 ON → -Vin
- No zero state
- Simple control

### Unipolar Switching
- Q1/Q4 ON → +Vin
- Q2/Q3 ON → -Vin
- Q1/Q3 ON → 0 (or Q2/Q4 ON → 0)
- Adds zero states
- Better harmonic performance

## 3. Three-Phase Voltage Source Inverter (VSI)

### Circuit
- Six switches (Q1-Q6) in three legs
- Each leg has two switches (upper and lower)
- Loads connected in star or delta

### Switching Modes
- **180° conduction**: Each switch conducts for 180°
- **120° conduction**: Each switch conducts for 120°
- 180° conduction more common (higher utilization)

### 180° Conduction Mode
- Six active states + two zero states
- Each phase shifted by 120°
- Line voltage has 6-step waveform
- Phase voltage has stepped waveform

### Line-to-Line Voltage
- Peak = Vin (DC bus voltage)
- Fundamental peak = (2√3/π) × Vin = 1.1 Vin
- Contains 5th, 7th, 11th, 13th harmonics

### Phase Voltage (Star Load)
- Peak = (2/3)Vin (for 180° conduction)
- Fundamental peak = Vin/π × √3 = 0.551Vin
- 6-step waveform with harmonics

### Space Vector Modulation (SVM)
- 8 switching states (6 active + 2 zero)
- Reference vector rotated in α-β plane
- Better DC bus utilization
- Lower harmonics than square wave

## 4. PWM Techniques

### Square Wave Inverter
- Simple: switches at fundamental frequency
- Output: square wave
- High harmonic content
- Fixed output voltage (V/f = constant)
- THD ≈ 48.3% (single-phase)

### Sinusoidal PWM (SPWM)
- Carrier signal (high frequency triangle) compared with reference (sine)
- Switching frequency = carrier frequency
- Output voltage controlled by modulation index
- Lower harmonics than square wave
- THD ≈ 3-5% with filtering

### Modulation Index
```
ma = Vref(peak)/Vcarrier(peak)

ma < 1: linear modulation (linear relationship)
ma = 1: maximum linear output
ma > 1: overmodulation (increased harmonics)
```

### Harmonic Spectrum
- **Square wave**: 3rd, 5th, 7th, 9th... (all odd harmonics)
- **SPWM**: harmonics around switching frequency (fsw, 2fsw, ...)
- **SVM**: similar to SPWM but better DC utilization

### Selective Harmonic Elimination (SHE)
- Pre-calculated switching angles
- Eliminates specific harmonics (5th, 7th, etc.)
- Lower switching frequency
- Complex computation

## 5. Total Harmonic Distortion (THD)

### Definition
```
THD = √(ΣVn²(n=2 to ∞)/V1²) × 100%

Or equivalently:
THD = √(Vrms² - V1²)/V1 × 100%

V1 = RMS value of fundamental component
Vrms = total RMS value
```

### THD Values
- Square wave: 48.3% (single-phase)
- 6-step three-phase: 31.1% (line voltage)
- SPWM: 3-5% (with moderate switching frequency)
- SVM: 2-4%
- SHE: <1% (with specific harmonic elimination)

### Filtering
- Output filter removes high-frequency harmonics
- LC filter: cutoff frequency between fundamental and switching freq
- For motor drives: motor inductance acts as filter

## 6. Comparison: Square Wave vs PWM

| Parameter | Square Wave | SPWM | SVM |
|-----------|-------------|------|-----|
| Switching freq | Fundamental | High (10-20 kHz) | High |
| Output voltage control | None (fixed) | By ma | By ma |
| Harmonic content | High (48%) | Low (3-5%) | Low (2-4%) |
| DC bus utilization | 100% | 78.5% (ma=1) | 90.7% (ma=1) |
| Switching losses | Low | High | High |
| EMI | Low | High | High |
| Filter size | Large | Small | Small |
| Complexity | Simple | Moderate | Complex |
| Application | Simple drives | General purpose | High performance |

## 7. ISRO-Specific Focus

- Inverter topologies for satellite power systems
- V/f control for motor drives in spacecraft mechanisms
- THD requirements for power quality
- Radiation effects on switching devices
- Efficiency requirements for space applications
- Redundancy in inverter configurations
