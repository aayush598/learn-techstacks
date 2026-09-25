# Voltmeter Loading Effect - Concepts

## 1. Loading Effect Definition
When a voltmeter is connected across a circuit element, it draws current due to its finite internal resistance. This changes the circuit conditions and the measured voltage differs from the true voltage.

## 2. Voltmeter Sensitivity
```
Sensitivity (S) = R_v / V_range  (ohms per volt)
```
- Determined by the PMMC movement: S = 1/I_fs
- Higher S means higher R_v, less loading
- Typical values: 20 kohm/V (decent), 50 kohm/V (good), 100 kohm/V (excellent)

## 3. Internal Resistance
```
R_v = S × V_range
Example: S = 20 kohm/V, range = 10V
R_v = 20k x 10 = 200 kohm
```

## 4. Loading Error Analysis

### 4.1 Series Circuit
Source V_s with R_s in series with R_load.
True voltage across R_load:
```
V_true = V_s × R_load / (R_s + R_load)
```
Measured voltage (with voltmeter):
```
V_meas = V_s × (R_load || R_v) / (R_s + (R_load || R_v))
Loading error = V_meas - V_true
```

### 4.2 Simplified Case
When measuring voltage across a resistance R with source resistance R_s:
```
Loading error (%) = R_s / (R_s + R_v) × 100%

For small loading: Error ≈ R_s/R_v × 100%
```

### 4.3 Key Insight
- Loading error depends on R_s/R_v ratio
- If R_v >> R_s, loading is negligible (rule of thumb: R_v > 100 × R_s)
- Higher sensitivity voltmeter = less loading

## 5. Minimum Sensitivity Requirement
For a given maximum allowable loading error:
```
R_v = R_s × (1/epsilon - 1)

where epsilon = maximum allowable fractional error

Sensitivity = R_v / V_range
```

## 6. Loading Effect on Different Circuits

### 6.1 Voltage Divider
Loading reduces the effective resistance of the measured element.
Measured voltage is always less than true voltage.

```circuit
# Voltage divider with a load R_L drawing current at the output node
V = elm.SourceV().up().label("V_in 10V")
R1 = elm.Resistor().right().label("R1 10k", loc="bottom")
elm.Line().right()
R2 = elm.Resistor().down().label("R2 10k", loc="bottom")
elm.Line().down()
elm.Dot().label("out", loc="right")
RL = elm.Resistor().right().label("R_L 10k", loc="bottom")
elm.Line().down()
elm.Line().left()
elm.Line().up()
elm.Line().left()
elm.Line().up().to(V.start)
elm.Ground()
```

### 6.2 Thevenin Equivalent
Use Thevenin equivalent at measurement point:
```
V_th = true open-circuit voltage
R_th = Thevenin resistance

V_meas = V_th × R_v / (R_th + R_v)
Error = -R_th / (R_th + R_v) × 100%
```

## 7. Digital vs Analog Voltmeter Loading
| Feature | Analog (PMMC) | Digital (DVM) |
|---------|---------------|---------------|
| Sensitivity | 20 kohm/V typical | Fixed 10 MOhm |
| Loading | Depends on range | Constant |
| At low range | Higher R_v | Same 10 MOhm |
| At high range | Lower R_v | Same 10 MOhm |

## 8. Design Guidelines
- For accurate measurement: S >= 20 kohm/V for general circuits
- For high-impedance circuits: use DVM (10 MOhm fixed)
- Calculate expected loading before measurement
- If loading > 1%, consider buffer amplifier

## 9. ISRO Focus Areas
- Loading error calculation
- Minimum sensitivity for given error
- R_v = S × V_range
- Thevenin approach to loading analysis
- Comparison of analog vs digital voltmeter loading
