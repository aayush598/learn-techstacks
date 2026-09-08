# BJT Biasing Circuits - Formulas

## Fixed Bias

### Base Current
$$I_B = \frac{V_{CC} - V_{BE}}{R_B}$$

### Collector Current
$$I_C = \beta I_B$$

### Collector-Emitter Voltage
$$V_{CE} = V_{CC} - I_C R_C$$

### Stability Factor
$$S = \frac{\partial I_C}{\partial I_{CBO}} = \beta + 1$$

### Q-point
$$Q = (I_C, V_{CE}) = \left(\beta \frac{V_{CC} - V_{BE}}{R_B}, V_{CC} - \beta \frac{V_{CC} - V_{BE}}{R_B} R_C\right)$$

---

## Voltage Divider Bias

### Thevenin Equivalent
$$V_{TH} = V_{CC} \frac{R_2}{R_1 + R_2}$$

$$R_{TH} = \frac{R_1 R_2}{R_1 + R_2}$$

### Base Current
$$I_B = \frac{V_{TH} - V_{BE}}{R_{TH} + (\beta + 1)R_E}$$

### Collector Current
$$I_C = \beta I_B = \frac{\beta(V_{TH} - V_{BE})}{R_{TH} + (\beta + 1)R_E}$$

### Approximate (when βRE >> RTH)
$$I_C \approx \frac{V_{TH} - V_{BE}}{R_E}$$

### Collector-Emitter Voltage
$$V_{CE} = V_{CC} - I_C(R_C + R_E)$$

### Stability Factor
$$S = \frac{(\beta + 1)(1 + R_{TH}/R_E)}{1 + \beta R_E/(R_{TH} + R_E)}$$

### Approximate Stability (βRE >> RTH)
$$S \approx 1 + \frac{R_{TH}}{R_E}$$

---

## Emitter Bias

### Base Current
$$I_B = \frac{V_{EE} - V_{BE}}{R_E + R_{TH}/(\beta + 1)}$$

### Collector Current (Approximate)
$$I_C \approx \frac{V_{EE} - V_{BE}}{R_E}$$

### Collector-Emitter Voltage
$$V_{CE} = V_{CC} + V_{EE} - I_C(R_C + R_E)$$

### Stability Factor
$$S = \frac{1 + R_{TH}/R_E}{1 + \beta R_E/(R_{TH} + R_E)}$$

---

## Collector Feedback Bias

### Base Current
$$I_B = \frac{V_{CE} - V_{BE}}{R_B}$$

### Collector Current
$$I_C = \beta I_B$$

### KVL Equation
$$V_{CC} = I_C R_C + V_{CE} + I_B R_B$$

### Solving for IC
$$I_C = \frac{V_{CC} - V_{BE}}{R_C + R_B/\beta}$$

### Stability Factor
$$S = \frac{1 + R_C/R_B}{1 - \alpha R_C/R_B}$$

---

## Thermal Stability

### Power Dissipation
$$P_D = V_{CE} I_C + V_{BE} I_B \approx V_{CE} I_C$$

### Thermal Runaway Condition
$$\frac{\partial P_D}{\partial T} \theta_{JA} > 1$$

### Temperature Dependence of IC
$$I_C(T) = I_C(T_0) \exp\left[\frac{E_g}{k}\left(\frac{1}{T_0} - \frac{1}{T}\right)\right]$$

### Stability Against Thermal Runaway
$$R_E > \frac{V_T}{I_C} \cdot \frac{\partial I_C}{\partial T} \cdot \theta_{JA}$$

---

## Design Equations

### For Desired IC and VCE
$$R_C + R_E = \frac{V_{CC} - V_{CE}}{I_C}$$

### For Good Stability
$$R_E \geq 10 R_{TH}/\beta$$

$$V_{TH} \geq 10 V_{BE}$$

$$V_{RE} = I_C R_E \geq 1V \text{ (typically)}$$

### Component Selection
$$R_1 = \frac{V_{CC}}{I_{R}} \quad \text{where } I_R = 10I_B$$

$$R_2 = \frac{V_{TH} R_1}{V_{CC} - V_{TH}}$$

---

## Current Mirror Bias

### Basic Mirror
$$I_{OUT} = I_{REF} \frac{A_2}{A_1} \exp\left[\frac{V_{BE1} - V_{BE2}}{V_T}\right]$$

### For Matched Transistors
$$I_{OUT} = I_{REF}$$

### With Emitter Resistors
$$I_{OUT} = \frac{V_{BE1} - V_{BE2}}{R_{E2}} + \frac{V_{BE1}}{R_{E1}}$$

### Wilson Current Mirror
$$I_{OUT} = I_{REF} \frac{1}{1 + \frac{2}{\beta^2}}$$

### Output Resistance
$$R_{out} = \frac{\beta r_o}{2}$$

---

## Load Line Equations

### DC Load Line
$$V_{CC} = I_C(R_C + R_E) + V_{CE}$$

### Intercepts
- V-axis: VCC (when IC = 0)
- I-axis: VCC/(RC + RE) (when VCE = 0)

### AC Load Line
$$v_{ce} = -i_c(R_C || R_L)$$

### AC Load Line Slope
$$\text{Slope} = -\frac{1}{R_C || R_L}$$

### Maximum Swing
$$V_{CE(Q)} = I_{C(Q)}(R_C || R_L)$$

---

## Stability Factor Values

### Typical Stability Factors
| Bias Method | S Value |
|-------------|---------|
| Fixed Bias | β + 1 (very high) |
| Collector Feedback | 10-50 |
| Voltage Divider | 5-20 |
| Emitter Bias | 1-5 |
| Current Mirror | 1-2 |

### Design Target
- S < 10: Good stability
- S < 5: Excellent stability
- S = 1: Ideal stability

---

## Temperature Effects on Bias

### VBE Temperature Dependence
$$V_{BE}(T) = V_{BE}(T_0) - \frac{E_g - V_{BE}}{T_0}(T - T_0)$$

### β Temperature Dependence
$$\beta(T) = \beta(T_0)\left(\frac{T}{T_0}\right)^{3/2}$$

### IC Temperature Dependence
$$I_C(T) = I_C(T_0) \exp\left[\frac{E_g}{k}\left(\frac{1}{T_0} - \frac{1}{T}\right)\right]$$

---

## ISRO Quick Reference

### Voltage Divider Bias Design
1. Choose IC, VCE
2. VRE = 1V (typical)
3. RE = VRE/IC
4. RC = (VCC - VCE - VRE)/IC
5. VTH = 10VBE = 7V
6. RTH = βRE/10
7. Calculate R1, R2

### Stability Comparison
- Fixed: S = β + 1 (worst)
- Voltage divider: S ≈ 1 + RTH/RE (best practical)
- Current mirror: S ≈ 1 (best, IC design)
