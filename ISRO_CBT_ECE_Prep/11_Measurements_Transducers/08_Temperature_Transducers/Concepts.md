# Temperature Transducers - Concepts

## 1. RTD (Resistance Temperature Detector)

### 1.1 Principle
Resistance of metals increases with temperature (positive TCR).
```
R_T = R₀[1 + α(T - T₀)]
```

### 1.2 Pt100
- Platinum RTD with R₀ = 100Ω at 0°C
- Most common standard RTD
- α = 0.00385 Ω/Ω/°C (IEC 60751 standard)
- Range: -200°C to +850°C

### 1.3 Configuration
- 2-wire: Simple but includes lead wire resistance (error)
- 3-wire: Compensates lead wire resistance (most common)
- 4-wire: Most accurate, eliminates all lead wire effects

### 1.4 RTD Characteristics
- Highly linear (small α → linear over wide range)
- Excellent stability and accuracy (±0.1°C possible)
- Slow response (thermal mass)
- Requires excitation current

## 2. Thermistor

### 2.1 NTC (Negative Temperature Coefficient)
- Resistance DECREASES with temperature
- Semiconductor material (metal oxide)
- Very high sensitivity: -3% to -6% per °C
- Non-linear: R = R₀ × exp[B(1/T - 1/T₀)]
  B = material constant (2000-5000K)

### 2.2 PTC (Positive Temperature Coefficient)
- Resistance INCREASES with temperature
- Sharp resistance increase at Curie temperature
- Used as over-temperature protection (resettable fuse)

### 2.3 Thermistor vs RTD
| Feature | Thermistor (NTC) | RTD (Pt100) |
|---------|------------------|-------------|
| TCR | -3% to -6%/°C | +0.385%/°C |
| Linearity | Poor (exponential) | Excellent |
| Range | -100°C to +300°C | -200°C to +850°C |
| Sensitivity | Very high | Low |
| Accuracy | ±0.2°C | ±0.1°C |

## 3. Thermocouple

### 3.1 Seebeck Effect
When two dissimilar metals are joined at two junctions at different temperatures, an EMF is generated.
```
V = S × (T₁ - T₂)
S = Seebeck coefficient (μV/°C)
```

### 3.2 Types
| Type | Materials | Range | S (μV/°C) |
|------|-----------|-------|-----------|
| K | Chromel-Alumel | -200 to +1250°C | ~41 |
| J | Iron-Constantan | -40 to +750°C | ~52 |
| T | Copper-Constantan | -200 to +350°C | ~43 |
| E | Chromel-Constantan | -200 to +900°C | ~68 |
| S | Pt-Rh/Pt | 0 to +1450°C | ~10 |

### 3.3 Reference Junction
- Seebeck EMF depends on temperature difference
- Reference junction must be at known temperature
- Ice bath (0°C) or electronic cold junction compensation

### 3.4 Thermocouple Laws
- **Law of Intermediate Metals:** Inserting a third metal doesn't affect EMF if both junctions are at same temperature
- **Law of Intermediate Temperatures:** EMF for T₁ to T₃ = EMF(T₁ to T₂) + EMF(T₂ to T₃)

## 4. IC Temperature Sensor

### 4.1 Types
- **Voltage output:** LM35 (10 mV/°C), LM335 (10 mV/K)
- **Current output:** AD590 (1 μA/K)
- **Digital:** DS18B20 (1-Wire, 9-12 bit)

### 4.2 LM35
- Output: 10 mV/°C (linear)
- Range: -55°C to +150°C
- Accuracy: ±0.5°C
- No calibration needed

### 4.3 AD590
- Output: 1 μA/K (absolute temperature)
- Range: -55°C to +150°C
- Two-terminal device (current source)

## 5. Comparison
| Transducer | Range | Accuracy | Response | Cost |
|------------|-------|----------|----------|------|
| RTD | -200 to 850°C | ±0.1°C | Slow | Medium |
| Thermistor | -100 to 300°C | ±0.2°C | Fast | Low |
| Thermocouple | -200 to 1450°C | ±1°C | Very fast | Low |
| IC Sensor | -55 to 150°C | ±0.5°C | Medium | Low |

## 6. Calibration
- Compare with standard at known temperatures (ice point, steam point)
- Use fixed points: 0°C (ice), 100°C (steam), 231.9°C (tin), 419.5°C (zinc)
- Linear interpolation between calibration points

## 7. ISRO Focus Areas
- Pt100 resistance calculation
- NTC thermistor exponential characteristic
- Seebeck effect and thermocouple EMF
- LM35 output (10 mV/°C)
- Thermocouple types and ranges
