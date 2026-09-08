# BJT Biasing Circuits - Concepts

## Purpose of Biasing
- Establish proper operating point (Q-point)
- Ensure transistor operates in desired region
- Maintain stable operation despite parameter variations
- Prevent thermal runaway

---

## Fixed Bias (Base Bias)

### Circuit Configuration
```
VCC ──── RC ──── Collector
           │
           BJT
           │
           RB ──── VCC
```

### Operating Point
$$I_B = \frac{V_{CC} - V_{BE}}{R_B}$$

$$I_C = \beta I_B$$

$$V_{CE} = V_{CC} - I_C R_C$$

### Stability Factor
$$S(\beta) = \frac{\partial I_C}{\partial \beta} = I_B$$

### Advantages
- Simple circuit
- Low component count

### Disadvantages
- Poor stability (S = IB)
- Q-point varies with β
- Not suitable for production

---

## Collector-to-Base Bias

### Circuit Configuration
```
VCC ──── RC ──── Collector
                    │
                    RB
                    │
                  Base
```

### Operating Point
$$I_B = \frac{V_{CE} - V_{BE}}{R_B}$$

$$I_C = \beta I_B$$

$$V_{CE} = V_{CC} - I_C(R_C + R_E)$$

### Stability Factor
$$S(\beta) = \frac{1}{1 - \alpha\frac{R_C}{R_B + R_C}}$$

### Advantages
- Better stability than fixed bias
- Negative feedback through RB

### Disadvantages
- Limited range of stable Q-points
- Still depends on β

---

## Voltage Divider Bias (Self Bias)

### Circuit Configuration
```
VCC ──── R1 ──── Base
                │
                R2
                │
               GND

VCC ──── RC ──── Collector
                    │
                    RE
                    │
                   GND
```

### Thevenin Equivalent
$$V_{TH} = V_{CC} \frac{R_2}{R_1 + R_2}$$

$$R_{TH} = R_1 || R_2 = \frac{R_1 R_2}{R_1 + R_2}$$

### Operating Point
$$I_B = \frac{V_{TH} - V_{BE}}{R_{TH} + (\beta + 1)R_E}$$

$$I_C \approx \frac{V_{TH} - V_{BE}}{R_E} \quad \text{(if } (\beta+1)R_E >> R_{TH})$$

$$V_{CE} = V_{CC} - I_C(R_C + R_E)$$

### Stability Factor
$$S(\beta) = \frac{1 + \frac{R_{TH}}{R_E}}{1 + (\beta+1)\frac{R_E}{R_{TH} + R_E}} \approx \frac{1 + R_{TH}/R_E}{1 + \beta R_E/(R_{TH}+R_E)}$$

### Design Rules (for β-independent bias)
1. $(\beta+1)R_E >> R_{TH}$
2. $V_{TH} >> V_{BE}$
3. $R_E >> R_{TH}/\beta$

### Advantages
- Excellent stability
- Q-point nearly independent of β
- Most widely used biasing method

---

## Emitter Bias

### Circuit Configuration
```
VCC ──── RC ──── Collector
                    │
                    BJT
                    │
                    RE
                    │
                  -VEE
```

### Operating Point
$$I_B = \frac{V_{BE} - V_{EE}}{R_E + R_{TH}/(\beta+1)}$$

$$I_C \approx \frac{V_{EE} - V_{BE}}{R_E} \quad \text{(for large } \beta)$$

### Stability
- Excellent stability
- Independent of β for large β
- Requires dual supplies

---

## Collector Feedback Bias

### Circuit Configuration
```
VCC ──── RC ──── Collector
                    │
                    RB
                    │
                  Base
```

### Operating Point
$$I_B = \frac{V_{CE} - V_{BE}}{R_B}$$

$$V_{CE} = V_{CC} - I_C R_C$$

### Stability
Better than fixed bias, but still β-dependent

---

## Stability Factor Analysis

### Definition
$$S = \frac{\partial I_C}{\partial I_{CBO}}$$

### General Formula
$$S = \frac{(\beta+1)(1 + R_{TH}/R_E)}{1 + \beta R_E/(R_{TH}+R_E)}$$

### Ideal Stability
- S = 1: perfect stability
- S < 10: good stability
- S > 20: poor stability

### Effect of Components
| Parameter | Effect on S |
|-----------|-------------|
| ↑ RE | ↓ S (better) |
| ↓ RTH | ↓ S (better) |
| ↑ β | ↑ S (worse) |
| ↑ RC | No effect |

---

## Thermal Stability

### Thermal Runaway Condition
$$\frac{\partial P_D}{\partial T} > \frac{1}{\theta_{JA}}$$

### Prevention
1. Adequate emitter resistance RE
2. Proper biasing (voltage divider)
3. Heat sinking
4. Negative feedback

### Thermal Resistance
$$\theta_{JA} = \theta_{JC} + \theta_{CS} + \theta_{SA}$$

Where:
- θJC = junction to case
- θCS = case to heatsink
- θSA = heatsink to ambient

---

## Q-point Stabilization

### Methods
1. **Emitter degeneration**: RE provides negative feedback
2. **Voltage divider bias**: establishes fixed VBE
3. **Diode bias**: compensates VBE temperature dependence
4. **Current mirror bias**: provides constant current

### Design Procedure
1. Choose IC (desired operating current)
2. Choose VCE (typically VCC/2 for max swing)
3. Calculate RC + RE = (VCC - VCE)/IC
4. Choose RE (10-20% of VCC/IC)
5. Calculate RC
6. Choose VTH and RTH for stability

---

## Bias Stability Comparison

| Bias Method | Stability | Complexity | Supply |
|-------------|-----------|------------|--------|
| Fixed | Poor | Simple | Single |
| Collector-Base | Fair | Simple | Single |
| Voltage Divider | Good | Moderate | Single |
| Emitter | Excellent | Moderate | Dual |
| Current Mirror | Excellent | Complex | Single/Dual |

---

## Diode Bias Compensation

### VBE Compensation
- Use diode with same temperature coefficient
- Diode voltage tracks VBE with temperature
- Improves thermal stability

### Circuit
```
VCC ──── RC ──── Collector
                    │
              D1 || BJT
                    │
                    RE
                    │
                   GND
```

---

## Current Mirror Bias

### Basic Current Mirror
```
VCC ──── Q1 (diode) ──── Q2 (current source)
```

### Output Current
$$I_{OUT} = I_{REF} \frac{A_2}{A_1}$$

### Wilson Current Mirror
- Improved output resistance
- Better current matching
- Used in IC design

---

## ISRO Key Points
- Voltage divider bias: most common, best stability
- RE provides negative feedback for stability
- S = 1: ideal stability
- Thermal runaway prevented by RE and proper biasing
- VBE decreases 2 mV/°C
- β increases 0.5%/°C
- Design rule: (β+1)RE >> RTH
