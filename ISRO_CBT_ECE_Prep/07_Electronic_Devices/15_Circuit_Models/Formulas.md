# Circuit Models - Formulas

## Two-Port Parameter Definitions

### z-parameters (Open-circuit impedance)
$$z_{11} = \frac{V_1}{I_1}\bigg|_{I_2=0}, \quad z_{12} = \frac{V_1}{I_2}\bigg|_{I_1=0}$$
$$z_{21} = \frac{V_2}{I_1}\bigg|_{I_2=0}, \quad z_{22} = \frac{V_2}{I_2}\bigg|_{I_1=0}$$

### y-parameters (Short-circuit admittance)
$$y_{11} = \frac{I_1}{V_1}\bigg|_{V_2=0}, \quad y_{12} = \frac{I_1}{V_2}\bigg|_{V_1=0}$$
$$y_{21} = \frac{I_2}{V_1}\bigg|_{V_2=0}, \quad y_{22} = \frac{I_2}{V_2}\bigg|_{V_1=0}$$

### h-parameters (Hybrid)
$$h_{11} = \frac{V_1}{I_1}\bigg|_{V_2=0}, \quad h_{12} = \frac{V_1}{V_2}\bigg|_{I_1=0}$$
$$h_{21} = \frac{I_2}{I_1}\bigg|_{V_2=0}, \quad h_{22} = \frac{I_2}{V_2}\bigg|_{I_1=0}$$

### ABCD parameters (Transmission)
$$A = \frac{V_1}{V_2}\bigg|_{I_2=0}, \quad B = \frac{V_1}{-I_2}\bigg|_{V_2=0}$$
$$C = \frac{I_1}{V_2}\bigg|_{I_2=0}, \quad D = \frac{I_1}{-I_2}\bigg|_{V_2=0}$$

---

## h-Parameter Relations (BJT)

### CE Configuration
$$v_{be} = h_{ie} i_b + h_{re} v_{ce}$$
$$i_c = h_{fe} i_b + h_{oe} v_{ce}$$

### CB Configuration
$$v_{eb} = h_{ib} i_e + h_{rb} v_{cb}$$
$$i_c = h_{fb} i_e + h_{ob} v_{cb}$$

### CC Configuration
$$v_{bc} = h_{ic} i_b + h_{rc} v_{ec}$$
$$i_e = h_{fc} i_b + h_{oc} v_{ec}$$

---

## h to Hybrid-π Conversion

$$h_{ie} = r_b + r_\pi$$
$$h_{fe} = \beta$$
$$h_{oe} = \frac{1}{r_o} = \frac{h_{fe}}{V_A} \text{ (per unit)}$$
$$h_{re} \approx 0$$

---

## z-y-h-g Conversions

### z from y
$$z_{11} = \frac{y_{22}}{\Delta y}, \quad z_{12} = \frac{-y_{12}}{\Delta y}$$
$$z_{21} = \frac{-y_{21}}{\Delta y}, \quad z_{22} = \frac{y_{11}}{\Delta y}$$

### y from z
$$y_{11} = \frac{z_{22}}{\Delta z}, \quad y_{12} = \frac{-z_{12}}{\Delta z}$$
$$y_{21} = \frac{-z_{21}}{\Delta z}, \quad y_{22} = \frac{z_{11}}{\Delta z}$$

### h from z
$$h_{11} = \frac{\Delta z}{z_{22}}, \quad h_{12} = \frac{z_{12}}{z_{22}}$$
$$h_{21} = \frac{-z_{21}}{z_{22}}, \quad h_{22} = \frac{1}{z_{22}}$$

Where Δz = z11z22 - z12z21, Δy = y11y22 - y12y21

---

## Amplifier Gains (h-parameters, CE)

### Voltage Gain
$$A_v = \frac{-h_{fe} R_L}{h_{ie} + \Delta h R_L}$$

### Current Gain
$$A_i = \frac{h_{fe}}{1 + h_{oe} R_L}$$

### Input Impedance
$$R_{in} = h_{ie} - \frac{h_{re} h_{fe}}{h_{oe} + 1/R_L}$$

### Output Impedance
$$R_{out} = \frac{h_{ie} + R_S}{h_{ie} + h_{oe}(R_S + h_{ie}) - h_{re}h_{fe}}$$

### Simplified (neglecting hre, hoe)
$$A_v = \frac{-h_{fe} R_L}{h_{ie}} = \frac{-\beta R_L}{r_\pi}$$
$$A_i = h_{fe} = \beta$$

---

## DC Equivalents

### BJT (Active)
$$V_{BE} = 0.7V$$
$$I_C = \beta I_B$$
$$V_{CE} = V_{CC} - I_C(R_C + R_E)$$

### BJT (Saturation)
$$V_{CE(sat)} = 0.2V$$
$$I_{C(sat)} = \frac{V_{CC} - 0.2}{R_C + R_E}$$

### MOSFET (Saturation)
$$V_{GS} = V_G - V_S$$
$$I_D = \frac{1}{2}k_n'\frac{W}{L}(V_{GS} - V_T)^2$$
$$V_{DS(sat)} = V_{GS} - V_T$$

### MOSFET (Linear)
$$I_D = k_n'\frac{W}{L}\left[(V_{GS} - V_T)V_{DS} - \frac{V_{DS}^2}{2}\right]$$

---

## AC Analysis Rules

### Capacitor Impedance
$$Z_C = \frac{1}{j\omega C}$$

### Low Frequency (DC)
$$Z_C \to \infty \text{ (open circuit)}$$

### High Frequency (AC short)
$$Z_C \to 0 \text{ (short circuit)}$$

### Inductor Impedance
$$Z_L = j\omega L$$

### DC: ZL → 0 (short), AC high freq: ZL → ∞

---

## Common Configuration Parameters

### CE Amplifier
$$A_v = \frac{-g_m(R_C || r_o || R_L)}{1 + g_m R_E} \text{ (with degeneration)}$$
$$A_i = \beta$$
$$R_{in} = R_B || r_\pi$$
$$R_{out} = R_C || r_o$$

### CC (Emitter Follower)
$$A_v \approx 1$$
$$R_{in} = R_B || (r_\pi + (1+\beta)R_E)$$
$$R_{out} = \frac{r_\pi + R_S}{\beta+1} || R_E$$

### CB
$$A_v = g_m(R_C || r_o)$$
$$A_i \approx 1$$
$$R_{in} = r_e$$
$$R_{out} = R_C || r_o$$

---

## Cascade (CE-CE) Total Gain

### Voltage Gain
$$A_v = A_{v1} \times A_{v2}$$

### Input Impedance
$$R_{in} = R_{in1}$$

### Output Impedance
$$R_{out} = R_{out2}$$

### Current Gain
$$A_i = A_{i1} \times A_{i2}$$

---

## ISRO Quick Reference

### h-Parameters (BJT CE)
1. hie = rπ (input)
2. hfe = β (current gain)
3. hoe = 1/ro (output)
4. hre ≈ 0

### Derived
1. Av = -βRL/rπ (no degeneration)
2. Ai = β
3. Rin = RB||rπ
4. Rout = RC||ro

### DC (Forward Active)
1. VBE = 0.7V
2. IC = βIB
3. VCE(sat) = 0.2V

### Parameter Sets
1. z, y, h, g, ABCD
2. h most common for devices
