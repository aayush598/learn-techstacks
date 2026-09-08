# MOSFET Models - Formulas

## Small-Signal Parameters

### Transconductance
$$g_m = \frac{\partial I_D}{\partial V_{GS}} = \mu_n C_{ox} \frac{W}{L}(V_{GS} - V_T)$$

$$g_m = \sqrt{2\mu_n C_{ox} \frac{W}{L} I_D}$$

$$g_m = \frac{2I_D}{V_{GS} - V_T} = \frac{2I_D}{V_{OV}}$$

### Output Resistance
$$r_o = \frac{\partial V_{DS}}{\partial I_D} = \frac{1}{\lambda I_D} = \frac{V_A}{I_D}$$

### Body Transconductance
$$g_{mb} = \frac{\partial I_D}{\partial V_{SB}} = \frac{\gamma g_m}{2\sqrt{2\phi_f + V_{SB}}} = \eta g_m$$

---

## Hybrid-π Model Parameters

### Input Resistance
$$R_{in} = \infty \text{ (ideal)}$$

### Output Resistance
$$R_{out} = r_o || R_D$$

### Voltage Gain
$$A_v = -g_m (r_o || R_D || R_L)$$

### Current Gain
$$A_i = \infty \text{ (ideal)}$$

---

## T-Model Parameters

### Source Resistance
$$R_s = \frac{1}{g_m} || r_o$$

### Voltage Gain
$$A_v = g_m (r_o || R_D || R_L)$$

### Input Resistance
$$R_{in} = R_S || \frac{1}{g_m}$$

---

## Capacitance Formulas

### Gate-Source (Saturation)
$$C_{gs} = \frac{2}{3}WLC_{ox}$$

### Gate-Drain (Overlap)
$$C_{gd} = WLC_{ov}$$

### Gate-Body
$$C_{gb} = \frac{WLC_{ox}}{1 + C_{ox}/C_{dep}}$$

### Oxide Capacitance
$$C_{ox} = \frac{\varepsilon_{ox}}{t_{ox}} = \frac{3.9 \times 8.85 \times 10^{-14}}{t_{ox}} \text{ F/cm}^2$$

---

## Frequency Response

### Unity Current Gain Frequency
$$f_T = \frac{g_m}{2\pi(C_{gs} + C_{gd})}$$

### Maximum Oscillation Frequency
$$f_{max} = \frac{f_T}{2\sqrt{R_g C_{gd}/r_o}}$$

### Gain-Bandwidth Product
$$GBW = f_T \times A_{v0}$$

---

## Noise Models

### Thermal Noise Current
$$i_{nd}^2 = \frac{4kT\gamma}{r_{ds0}} B = 4kT\gamma g_m B$$

Where γ = 2/3 (saturation)

### Flicker Noise Current
$$i_{nf}^2 = \frac{K_f I_D^2}{f C_{ox} WL} B$$

### Input Referred Noise
$$v_{ni}^2 = \frac{i_{nd}^2}{g_m^2} + v_{ng}^2$$

---

## Large Signal Model

### Drain Current (Saturation)
$$I_D = \frac{1}{2}\mu_n C_{ox} \frac{W}{L}(V_{GS} - V_T)^2(1 + \lambda V_{DS})$$

### Drain Current (Linear)
$$I_D = \mu_n C_{ox} \frac{W}{L}\left[(V_{GS} - V_T)V_{DS} - \frac{V_{DS}^2}{2}\right]$$

### Transconductance Parameter
$$K_n = \frac{\mu_n C_{ox} W}{2L}$$

---

## Intrinsic Parameters

### Intrinsic Gain
$$A_{v,intrinsic} = g_m r_o = \frac{2V_A}{V_{OV}}$$

### gm/ID Ratio
$$\frac{g_m}{I_D} = \frac{2}{V_{OV}}$$

### gm·ro Product
$$g_m r_o = \frac{2V_A}{V_{OV}}$$

---

## Body Effect Formulas

### Threshold Voltage
$$V_T = V_{T0} + \gamma\left(\sqrt{2\phi_f + V_{SB}} - \sqrt{2\phi_f}\right)$$

### Body Effect Parameter
$$\gamma = \frac{\sqrt{2\varepsilon_s q N_A}}{C_{ox}}$$

### Fermi Potential
$$\phi_f = V_T \ln\left(\frac{N_A}{n_i}\right)$$

---

## Channel Length Modulation

### Output Resistance
$$r_o = \frac{1}{\lambda I_D} = \frac{V_A}{I_D}$$

### Lambda Dependence
$$\lambda \propto \frac{1}{L}$$

### Early Voltage
$$V_A = \frac{1}{\lambda}$$

---

## Velocity Saturation

### Critical Electric Field
$$E_{sat} = \frac{2v_{sat}}{\mu_n}$$

### Velocity Saturation Current
$$I_{D,sat} = W C_{ox} v_{sat}(V_{GS} - V_T)$$

### Modified Transconductance
$$g_m = W C_{ox} v_{sat}$$

---

## ISRO Quick Reference

### gm Formulas
1. gm = μnCox(W/L)(VGS-VT)
2. gm = √(2μnCox(W/L)ID)
3. gm = 2ID/Vov

### ro Formula
1. ro = 1/(λID) = VA/ID

### gmb Formula
1. gmb = ηgm, η ≈ 0.1-0.3

### Capacitance
1. Cgs = (2/3)WLCox (saturation)
2. Cgd = WLCov (overlap)

### Frequency
1. fT = gm/(2π(Cgs + Cgd))

### Intrinsic Gain
1. Av = gmro = 2VA/Vov
