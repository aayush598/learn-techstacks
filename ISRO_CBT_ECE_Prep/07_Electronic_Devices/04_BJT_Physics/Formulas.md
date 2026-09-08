# BJT Physics - Formulas

## Current Relationships

### Basic Equations
$$I_E = I_B + I_C$$

$$I_C = \beta I_B = \alpha I_E$$

$$I_B = \frac{I_C}{\beta} = (1-\alpha)I_E$$

$$I_E = \frac{I_C}{\alpha} = \frac{\beta+1}{\beta}I_C$$

### Alpha-Beta Conversion
$$\alpha = \frac{\beta}{1+\beta}$$

$$\beta = \frac{\alpha}{1-\alpha}$$

### With Reverse Saturation Current
$$I_C = \alpha I_E + I_{CBO}$$

$$I_B = (1-\alpha)I_E - I_{CBO}$$

$$I_E = \frac{I_C + I_{CBO}}{\alpha}$$

---

## Ebers-Moll Model

### Forward Active
$$I_C = I_S \exp\left(\frac{V_{BE}}{V_T}\right)$$

$$I_B = \frac{I_C}{\beta_F}$$

### Complete Ebers-Moll
$$I_E = I_{ES}\left[\exp\left(\frac{V_{BE}}{V_T}\right) - 1\right] - \alpha_R I_{CS}\left[\exp\left(\frac{V_{BC}}{V_T}\right) - 1\right]$$

$$I_C = \alpha_F I_{ES}\left[\exp\left(\frac{V_{BE}}{V_T}\right) - 1\right] - I_{CS}\left[\exp\left(\frac{V_{BC}}{V_T}\right) - 1\right]$$

### Reciprocity
$$\alpha_F I_{ES} = \alpha_R I_{CS}$$

---

## Saturation Region

### Collector-Emitter Saturation Voltage
$$V_{CE(sat)} = V_{BE(sat)} - V_{BC(sat)}$$

### Saturation Current
$$I_{C(sat)} = \frac{V_{CC} - V_{CE(sat)}}{R_C + R_E}$$

### Overdrive Factor
$$ODF = \frac{I_B}{I_{B(min)}} = \frac{I_B \beta}{I_{C(sat)}}$$

### Base Current for Saturation
$$I_{B(min)} = \frac{I_{C(sat)}}{\beta}$$

---

## Early Effect

### Output Resistance
$$r_o = \frac{V_A + V_{CE}}{I_C} \approx \frac{V_A}{I_C}$$

### Modified Collector Current
$$I_C = I_S \exp\left(\frac{V_{BE}}{V_T}\right)\left(1 + \frac{V_{CE}}{V_A}\right)$$

### Early Voltage
$$V_A = \frac{I_C}{\partial I_C / \partial V_{CE}}$$

---

## Small-Signal Parameters

### Transconductance
$$g_m = \frac{I_C}{V_T} = \frac{qI_C}{kT}$$

### Input Resistance (Base)
$$r_\pi = \frac{\beta}{g_m} = \frac{\beta V_T}{I_C} = \frac{V_T}{I_B}$$

### Emitter Resistance
$$r_e = \frac{V_T}{I_E} = \frac{\alpha}{g_m} = \frac{r_\pi}{\beta+1}$$

### Output Resistance
$$r_o = \frac{V_A}{I_C}$$

### Relationships
$$g_m = \frac{I_C}{V_T} = \frac{\beta}{r_\pi}$$

$$r_\pi = \frac{\beta}{g_m}$$

$$r_e = \frac{\alpha}{g_m} \approx \frac{1}{g_m}$$

---

## Frequency Response

### Cutoff Frequency
$$f_T = \frac{g_m}{2\pi(C_\pi + C_\mu)}$$

### Beta Cutoff
$$f_\beta = \frac{f_T}{\beta_0}$$

### Alpha Cutoff
$$f_\alpha = \frac{f_T}{\sqrt{1-\alpha^2}}$$

### Frequency Dependent Beta
$$\beta(j\omega) = \frac{\beta_0}{1 + j(\omega/\omega_\beta)}$$

### Miller Capacitance
$$C_M = C_\mu(1 + g_m R_L)$$

---

## Transit Time

### Forward Transit Time
$$\tau_F = \frac{W_B^2}{2D_n}$$

### Total Transit Time
$$\tau_T = \tau_E + \tau_B + \tau_C + \tau_{CS}$$

### Base Transit Time
$$\tau_B = \frac{W_B^2}{2D_n}$$

### Emitter Delay
$$\tau_E = \frac{C_{je}}{g_m}$$

---

## Diffusion Capacitance

### Base Charge
$$Q_B = \frac{W_B^2}{2D_n} I_C = \tau_F I_C$$

### Diffusion Capacitance
$$C_d = \frac{\tau_F I_C}{V_T} = \tau_F g_m$$

### Total Input Capacitance
$$C_{in} = C_\pi + C_M = C_d + C_{je} + C_M$$

---

## Gummel Number

### Definition
$$G_B = \int_0^{W_B} \frac{N_B(x)}{D_n(x)} dx$$

### For Uniform Base
$$G_B = \frac{N_B W_B}{D_n}$$

### Collector Current
$$I_C = \frac{qA D_n n_i^2}{G_B} \exp\left(\frac{V_{BE}}{V_T}\right)$$

---

## Temperature Effects

### VBE Temperature Coefficient
$$\frac{dV_{BE}}{dT} \approx -2 \text{ mV/°C}$$

### β Temperature Coefficient
$$\frac{d\beta}{dT} \approx +0.5\% \text{ per °C}$$

### ICBO Temperature Coefficient
$$I_{CBO}(T_2) = I_{CBO}(T_1) \times 2^{(T_2-T_1)/10}$$

### Thermal Voltage
$$V_T = \frac{kT}{q} = 25.85 \text{ mV at 300K}$$

---

## Noise Parameters

### Shot Noise
$$i_n^2 = 2qI_B B$$ (base)
$$i_c^2 = 2qI_C B$$ (collector)

### Thermal Noise
$$v_n^2 = 4kTR_{bb'}B$$

### Flicker Noise
$$i_f^2 = \frac{K I_B^2}{f} B$$

### Noise Figure
$$NF = 10\log\left(\frac{S_i/N_i}{S_o/N_o}\right) \text{ dB}$$

---

## Power Dissipation

### Maximum Power
$$P_{max} = \frac{T_j - T_A}{\theta_{JA}}$$

### Instantaneous Power
$$P_D = V_{CE} I_C + V_{BE} I_B \approx V_{CE} I_C$$

### Safe Operating Area
$$I_C \times V_{CE} \leq P_{max}$$

---

## ISRO Quick Reference

### Current Relations
1. IE = IB + IC
2. IC = βIB = αIE
3. α = β/(1+β)
4. β = α/(1-α)

### Small-Signal
1. gm = IC/VT
2. rπ = β/gm
3. re = α/gm
4. ro = VA/IC

### Frequency
1. fT = gm/(2π(Cπ + Cμ))
2. fβ = fT/β
3. fα = fT/√(1-α²)

### Temperature
1. dVBE/dT ≈ -2 mV/°C
2. dβ/dT ≈ +0.5%/°C
3. ICBO doubles per 10°C
