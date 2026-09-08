# Small Signal Models - Formulas

## BJT Small-Signal Parameters

### Transconductance
$$g_m = \frac{I_C}{V_T} = \frac{qI_C}{kT} = 40 I_C \quad \text{(IC in A, gm in S)}$$

### Input Resistance
$$r_\pi = \frac{\beta}{g_m} = \frac{\beta V_T}{I_C} = \frac{V_T}{I_B}$$

### Emitter Resistance
$$r_e = \frac{V_T}{I_E} = \frac{\alpha}{g_m} = \frac{r_\pi}{\beta + 1}$$

### Output Resistance
$$r_o = \frac{V_A}{I_C} = \frac{V_A + V_{CE}}{I_C}$$

### Relations
$$g_m = \frac{\beta}{r_\pi} = \frac{1}{r_e} \text{ (for } \alpha \approx 1)$$

---

## MOSFET Small-Signal Parameters

### Transconductance
$$g_m = \frac{\partial I_D}{\partial V_{GS}} = \mu_n C_{ox}\frac{W}{L}(V_{GS} - V_T)$$

$$g_m = \sqrt{2\mu_n C_{ox}\frac{W}{L} I_D}$$

$$g_m = \frac{2I_D}{V_{GS} - V_T} = \frac{2I_D}{V_{OV}}$$

### Output Resistance
$$r_o = \frac{1}{\lambda I_D} = \frac{V_A}{I_D}$$

### Body Transconductance
$$g_{mb} = \eta g_m$$

$$\eta = \frac{g_{mb}}{g_m} = \frac{\gamma}{2\sqrt{2\phi_f + V_{SB}}}$$

---

## h-Parameters (BJT)

### Two-Port Equations
$$v_{be} = h_{11} i_b + h_{12} v_{ce}$$
$$i_c = h_{21} i_b + h_{22} v_{ce}$$

### Definitions
| Symbol | Name | Formula |
|--------|------|---------|
| h11 = hie | Input impedance | vbe/ib \| vce=0 |
| h12 = hre | Reverse transfer | vbe/vce \| ib=0 |
| h21 = hfe | Forward current gain | ic/ib \| vce=0 |
| h22 = hoe | Output admittance | ic/vce \| ib=0 |

### Relation to Hybrid-π
$$h_{ie} = r_\pi + r_b$$
$$h_{fe} = \beta$$
$$h_{oe} = \frac{1}{r_o} = \frac{1}{V_A/I_C}$$
$$h_{re} \approx 0$$

---

## Common Emitter Amplifier

### Voltage Gain (with Re)
$$A_v = \frac{-g_m R_C || r_o}{1 + g_m R_E} \approx \frac{-R_C}{r_e + R_E} \text{ (if } R_E >> r_e)$$

### Without Re
$$A_v = -g_m (R_C || r_o || R_L)$$

### Input Resistance
$$R_{in} = R_B || r_\pi$$

### Output Resistance
$$R_{out} = R_C || r_o$$

### Current Gain
$$A_i = \frac{\beta R_B}{R_B + r_\pi}$$

---

## Common Base Amplifier

### Voltage Gain
$$A_v = g_m (R_C || r_o)$$

### Input Resistance
$$R_{in} = r_e = \frac{V_T}{I_E}$$

### Output Resistance
$$R_{out} = R_C || r_o$$

### Current Gain
$$A_i = \alpha \approx 1$$

---

## Common Collector (Emitter Follower)

### Voltage Gain
$$A_v = \frac{(1+\beta)(R_E || r_o)}{r_\pi + (1+\beta)(R_E || r_o)} \leq 1$$

### Input Resistance
$$R_{in} = r_\pi + (1+\beta)(R_E || r_o)$$

### Output Resistance
$$R_{out} = r_e = \frac{r_\pi + R_S}{\beta + 1}$$

---

## Common Source Amplifier

### Voltage Gain
$$A_v = -g_m (R_D || r_o || R_L)$$

### Input Resistance
$$R_{in} = R_G \text{ (very high)}$$

### Output Resistance
$$R_{out} = R_D || r_o$$

---

## Common Gate Amplifier

### Voltage Gain
$$A_v = g_m (R_D || r_o)$$

### Input Resistance
$$R_{in} = \frac{1}{g_m} = \frac{1}{g_m}$$

### Output Resistance
$$R_{out} = R_D || r_o$$

---

## Common Drain (Source Follower)

### Voltage Gain
$$A_v = \frac{g_m(R_S || r_o)}{1 + g_m(R_S || r_o)} \leq 1$$

### Input Resistance
$$R_{in} = R_G$$

### Output Resistance
$$R_{out} = \frac{1}{g_m} || R_S$$

---

## Frequency Response

### Miller Multiplication
$$C_{in} = C_{gs} + C_{gd}(1 + |A_v|)$$
$$C_{out} = C_{gd}\left(1 + \frac{1}{|A_v|}\right)$$

### High-Frequency Pole
$$f_H = \frac{1}{2\pi R_{in} C_{in}}$$

### Gain-Bandwidth Product
$$GBW = f_T = \frac{g_m}{2\pi(C_{gs} + C_{gd})}$$

### BJT fT
$$f_T = \frac{g_m}{2\pi(C_\pi + C_\mu)}$$

---

## Noise Small-Signal

### BJT Noise
- Thermal: 4kT·rbb'
- Shot: 2qIC

### MOSFET Noise
- Thermal: 4kT(2/3)gm
- Flicker: K·gm²/(f·Cox·WL)

### Input-Referred Noise
$$\overline{v_{n,in}^2} = \frac{\overline{i_n^2}}{g_m^2}$$

---

## ISRO Quick Reference

### BJT
1. gm = IC/VT = 40IC
2. rπ = β/gm
3. re = VT/IE
4. ro = VA/IC

### MOSFET
1. gm = 2ID/Vov
2. gm = √(2μnCox(W/L)ID)
3. ro = 1/(λID)
4. gmb = ηgm

### Gains
1. CE: Av = -gm(RC||ro)
2. CS: Av = -gm(RD||ro)
3. CC: Av ≈ 1
4. CD: Av ≈ 1

### Frequency
1. fT = gm/(2π(Cin))
2. Miller: Cin = Cgs + Cgd(1+Av)
