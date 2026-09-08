# FET & MOSFET - Formulas

## JFET Equations

### Transfer Characteristic (Shockley Equation)
$$I_D = I_{DSS}\left(1 - \frac{V_{GS}}{V_P}\right)^2$$

### Maximum Drain Current
$$I_{DSS} = \text{drain current at } V_{GS} = 0$$

### Pinch-off Voltage
$$V_P = V_{GS} \text{ at which } I_D = 0$$

### Transconductance
$$g_m = g_{m0}\left(1 - \frac{V_{GS}}{V_P}\right)$$

$$g_{m0} = \frac{2I_{DSS}}{|V_P|}$$

### Output Resistance
$$r_d = \frac{1}{\lambda I_D} \approx \frac{|V_P|}{I_D} \text{ (in saturation)}$$

---

## MOSFET Drain Current

### Linear Region
$$I_D = \mu_n C_{ox} \frac{W}{L}\left[(V_{GS} - V_T)V_{DS} - \frac{V_{DS}^2}{2}\right]$$

### Saturation Region
$$I_D = \frac{1}{2}\mu_n C_{ox} \frac{W}{L}(V_{GS} - V_T)^2$$

### With Channel Length Modulation
$$I_D = \frac{1}{2}\mu_n C_{ox} \frac{W}{L}(V_{GS} - V_T)^2(1 + \lambda V_{DS})$$

### Velocity Saturation
$$I_D = W C_{ox} v_{sat}(V_{GS} - V_T)$$

---

## Process Parameters

### Process Transconductance
$$k_n' = \mu_n C_{ox}$$

### MOSFET Transconductance Parameter
$$K_n = \frac{k_n' W}{2L} = \frac{\mu_n C_{ox} W}{2L}$$

### Oxide Capacitance
$$C_{ox} = \frac{\varepsilon_{ox}}{t_{ox}} = \frac{3.9 \times 8.85 \times 10^{-14}}{t_{ox}} \text{ F/cm}^2$$

### Typical Values
| Parameter | NMOS | PMOS |
|-----------|------|------|
| μn (cm²/V-s) | 500-700 | 150-250 |
| tox (nm) | 5-10 | 5-10 |
| VT (V) | 0.3-0.7 | -0.3 to -0.7 |
| kn' (μA/V²) | 100-200 | 30-60 |

---

## Small-Signal Parameters

### Transconductance
$$g_m = \mu_n C_{ox} \frac{W}{L}(V_{GS} - V_T) = \sqrt{2\mu_n C_{ox} \frac{W}{L} I_D}$$

### Alternative Forms
$$g_m = \frac{2I_D}{V_{GS} - V_T} = \frac{2I_D}{V_{OV}}$$

Where VOV = VGS - VT = overdrive voltage

### Output Resistance
$$r_o = \frac{1}{\lambda I_D} = \frac{V_A}{I_D}$$

### Body Transconductance
$$g_{mb} = \frac{\gamma g_m}{2\sqrt{2\phi_f + V_{SB}}} = \eta g_m$$

### Intrinsic Gain
$$A_v = g_m r_o = \frac{2V_A}{V_{OV}}$$

---

## Threshold Voltage

### Basic Formula
$$V_T = V_{FB} + 2\phi_f + \frac{\sqrt{2\varepsilon_s q N_A (2\phi_f)}}{C_{ox}}$$

### Body Effect
$$V_T = V_{T0} + \gamma\left(\sqrt{2\phi_f + V_{SB}} - \sqrt{2\phi_f}\right)$$

### Body Effect Parameter
$$\gamma = \frac{\sqrt{2\varepsilon_s q N_A}}{C_{ox}}$$

### Fermi Potential
$$\phi_f = V_T \ln\left(\frac{N_A}{n_i}\right)$$

---

## Operating Regions

### Cutoff
$$V_{GS} < V_T \Rightarrow I_D = 0$$

### Linear
$$V_{GS} > V_T \text{ and } V_{DS} < V_{GS} - V_T$$

### Saturation
$$V_{GS} > V_T \text{ and } V_{DS} \geq V_{GS} - V_T$$

### Boundary Condition
$$V_{DS(sat)} = V_{GS} - V_T = V_{OV}$$

---

## Capacitances

### Gate Capacitance (Saturation)
$$C_{gs} = \frac{2}{3}WLC_{ox}$$

$$C_{gd} = 0 \text{ (ideal, ignoring overlap)}$$

### Gate Capacitance (Linear)
$$C_{gs} = C_{gd} = \frac{1}{2}WLC_{ox}$$

### Overlap Capacitance
$$C_{ov} = W L_{ov} C_{ox}$$

### Total Input Capacitance
$$C_{in} = C_{gs} + C_{gd}(1 + A_v) \text{ (Miller effect)}$$

---

## Power MOSFET

### On-State Resistance
$$R_{DS(on)} = \frac{1}{\mu_n C_{ox} \frac{W}{L}(V_{GS} - V_T)}$$

### Current Rating
$$I_{D(max)} = \frac{V_{GS(max)} - V_T}{R_{DS(on)}}$$

### Switching Time
$$t_{on} = R_g C_{iss}$$

$$t_{off} = R_g C_{oss}$$

---

## Temperature Effects

### VT Temperature Dependence
$$\frac{dV_T}{dT} = -\frac{dV_T}{dT} \approx -1 \text{ to } -3 \text{ mV/°C}$$

### Mobility Temperature Dependence
$$\mu(T) = \mu(T_0)\left(\frac{T_0}{T}\right)^{3/2}$$

### Drain Current Temperature
$$\frac{dI_D}{dT} \approx I_D\left[\frac{1}{V_{GS}-V_T}\frac{dV_T}{dT} - \frac{3}{2T}\right]$$

---

## ISRO Quick Reference

### JFET
1. ID = IDSS(1 - VGS/VP)²
2. gm = 2IDSS/|VP| × (1 - VGS/VP)
3. gm0 = 2IDSS/|VP|

### MOSFET
1. ID = (1/2)μnCox(W/L)(VGS-VT)²
2. gm = μnCox(W/L)(VGS-VT)
3. gm = √(2μnCox(W/L)ID)
4. ro = 1/(λID)

### Body Effect
1. VT = VT0 + γ(√(2φf+VSB) - √(2φf))
2. γ = √(2εs qNA)/Cox

### Key Relations
1. gm = 2ID/Vov
2. gm·ro = 2VA/Vov
3. gm/ID = 2/Vov
