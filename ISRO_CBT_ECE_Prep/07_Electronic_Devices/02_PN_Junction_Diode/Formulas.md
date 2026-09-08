# PN Junction Diode - Formulas

## Built-in Potential

### General Formula
$$V_{bi} = \frac{kT}{q} \ln\left(\frac{N_A N_D}{n_i^2}\right) = V_T \ln\left(\frac{N_A N_D}{n_i^2}\right)$$

### At 300K
$$V_{bi} = 0.026 \ln\left(\frac{N_A N_D}{(1.5 \times 10^{10})^2}\right)$$

### From Energy Band Diagram
$$V_{bi} = \frac{E_g}{2q} + \frac{kT}{q} \ln\left(\frac{N_D N_A}{n_i^2}\right)$$

### Practical Values
| Material | Vbi (V) |
|----------|---------|
| Si (moderate doping) | 0.6 - 0.8 |
| Ge | 0.2 - 0.3 |
| GaAs | 0.9 - 1.2 |

---

## Depletion Width

### General Formula (Abrupt Junction)
$$W = \sqrt{\frac{2\varepsilon_s}{q}\left(\frac{1}{N_A} + \frac{1}{N_D}\right)(V_{bi} - V_A)}$$

### Component Widths
$$W_N = \frac{N_A}{N_A + N_D}W$$
$$W_P = \frac{N_D}{N_A + N_D}W$$

### One-Sided Junction (NA >> ND)
$$W \approx \sqrt{\frac{2\varepsilon_s(V_{bi} - V_A)}{qN_D}}$$

### With Temperature
$$W(T) = \sqrt{\frac{2\varepsilon_s(V_{bi}(T) - V_A)}{q}\left(\frac{1}{N_A} + \frac{1}{N_D}\right)}$$

---

## Electric Field

### Maximum Electric Field (at junction)
$$E_{max} = \frac{qN_AW_P}{\varepsilon_s} = \frac{qN_DW_N}{\varepsilon_s}$$

### Alternative Form
$$E_{max} = \frac{2(V_{bi} - V_A)}{W}$$

### Voltage-Electric Field Relation
$$V_{bi} - V_A = \frac{1}{2}E_{max}W$$

---

## Charge Density

### Space Charge (Abrupt Junction)
$$\rho(x) = \begin{cases} +qN_D & 0 < x < W_N \\ -qN_A & -W_P < x < 0 \end{cases}$$

### Total Charge per Unit Area
$$Q = qN_DW_N = qN_AW_P$$

---

## Depletion Capacitance

### General Formula
$$C_j = \frac{\varepsilon_s A}{W} = A\sqrt{\frac{q\varepsilon_s}{2}\left(\frac{N_A N_D}{N_A + N_D}\right)\frac{1}{V_{bi} - V_A}}$$

### Per Unit Area
$$C_{j0} = \sqrt{\frac{q\varepsilon_s}{2}\left(\frac{N_A N_D}{N_A + N_D}\right)\frac{1}{V_{bi} - V_A}}$$

### One-Sided Junction
$$C_j = A\sqrt{\frac{q\varepsilon_sN_D}{2(V_{bi} - V_A)}}$$

### Voltage Dependence
$$C_j = \frac{C_{j0}}{\sqrt{1 - V_A/V_{bi}}}$$

### Junction Potential Energy
$$\frac{1}{2}C_jV^2 = \frac{1}{2}QV_{bi}$$

---

## Diffusion Capacitance

### Formula
$$C_d = \frac{\tau_p I_D}{V_T} \quad \text{(for P-N+ junction)}$$

$$C_d = \frac{\tau_n I_D}{V_T} \quad \text{(for N-P+ junction)}$$

### General
$$C_d = \tau \frac{dI_D}{dV} = \tau g_d$$

### Total Forward Capacitance
$$C_F = C_d + C_j$$

---

## Ideal Diode Equation

### Shockley Equation
$$I = I_s\left[\exp\left(\frac{V_A}{nV_T}\right) - 1\right]$$

### Reverse Saturation Current
$$I_s = qA\left(\frac{D_p}{L_p}p_{n0} + \frac{D_n}{L_n}n_{p0}\right)$$

$$I_s = qA\left(\frac{D_pp_{n0}}{L_p} + \frac{D_nn_{p0}}{L_n}\right)$$

### Temperature Dependence
$$I_s(T) = I_s(T_0)\left(\frac{T}{T_0}\right)^3 \exp\left[-\frac{E_g}{k}\left(\frac{1}{T} - \frac{1}{T_0}\right)\right]$$

### Forward Current (V >> nVT)
$$I \approx I_s \exp\left(\frac{V_A}{nV_T}\right)$$

### Reverse Current (VA << -nVT)
$$I \approx -I_s$$

---

## Dynamic Resistance

### DC Resistance
$$R_D = \frac{V_D}{I_D}$$

### AC (Dynamic) Resistance
$$r_d = \frac{dV}{dI} = \frac{nV_T}{I_D} = \frac{nV_T}{I_Q}$$

### At 300K (n=1)
$$r_d = \frac{26 \text{ mV}}{I_D \text{ (mA)}} \quad \text{(Ω)}$$

### Incremental Resistance
$$r_d = \frac{\eta V_T}{I_D + I_s} \approx \frac{\eta V_T}{I_D}$$

---

## Diffusion Length

### Definition
$$L_n = \sqrt{D_n \tau_n}$$
$$L_p = \sqrt{D_p \tau_p}$$

### Using Einstein Relation
$$L_n = \sqrt{\mu_n V_T \tau_n}$$
$$L_p = \sqrt{\mu_p V_T \tau_p}$$

### Diffusion Current Components
$$J_{p,diff} = -qD_p \frac{dp}{dx}$$
$$J_{n,diff} = qD_n \frac{dn}{dx}$$

---

## Reverse Recovery Time

### Components
$$t_{rr} = t_s + t_t$$

### Storage Time
$$t_s = \tau_p \ln\left(1 + \frac{I_F}{I_R}\right)$$

### Transition Time
$$t_t = \tau_p \frac{I_R}{I_R + I_F}$$ (approximate)

### Relationship
$$t_{rr} \approx \tau_p \ln\left(1 + \frac{I_F}{I_R}\right) + \text{transition time}$$

---

## Breakdown Voltage

### Avalanche Breakdown
$$V_{BR} \propto \left(\frac{1}{N_D}\right)^{3/4} \quad \text{(for N-P+ junction)}$$

### Zener Breakdown
$$V_{BR} \propto \left(\frac{1}{N_D}\right)^{3/4} \quad \text{(same dependence, different mechanism)}$$

### Empirical Formula (Si)
$$V_{BR} = 60\left(\frac{E_g}{1.1}\right)^{3/2}\left(\frac{N_B}{10^{16}}\right)^{-3/4}$$

Where NB = background doping concentration

---

## Temperature Effects

### Forward Voltage Temperature Coefficient
$$\frac{dV_F}{dT} = -\frac{E_g - V_F}{T} \approx -2 \text{ mV/°C (for Si)}$$

### Reverse Current Temperature Coefficient
$$\frac{dI_s}{dT} = \frac{I_s E_g}{kT^2}$$

### Approximate
$$I_s(T_2) = I_s(T_1) \times 2^{(T_2 - T_1)/10}$$

### Breakdown Voltage Temperature Coefficient
- Avalanche: positive (VBR increases with T)
- Zener: negative (VBR decreases with T)
- At VBR ≈ 5.6V: dVBR/dT ≈ 0

---

## Power Dissipation

### DC Power
$$P_D = V_D I_D$$

### With Load Resistance
$$P_D = I_D^2 R_D + I_D V_D$$

### Maximum Power (with heatsink)
$$P_{max} = \frac{T_j - T_A}{\theta_{JA}}$$

Where:
- Tj = junction temperature
- TA = ambient temperature
- θJA = thermal resistance (junction to ambient)

---

## Load Line Equations

### DC Load Line
$$V_{DD} = V_D + I_D R_L$$

### Intercepts
- V-axis: VDD (when ID = 0)
- I-axis: VDD/RL (when VD = 0)

### AC Load Line
$$v_d = i_d r_d$$

Slope = -1/rd

---

## Important Ratios

### Current Ratio
$$\frac{I}{I_s} = \exp\left(\frac{V_A}{nV_T}\right)$$

### For V = nVT
$$I = I_s(e^1 - 1) = 1.718 I_s$$

### For V = 2nVT
$$I = I_s(e^2 - 1) = 6.389 I_s$$

### For V = 10nVT
$$I \approx I_s e^{10} = 22026 I_s$$

---

## ISRO Quick Reference

### Key Formulas
1. Vbi = VT·ln(NAND/ni²)
2. W = √(2ε(Vbi-V)/q · (1/NA+1/ND))
3. CJ = εA/W
4. rD = nVT/ID
5. I = Is[exp(V/nVT) - 1]

### Key Values at 300K
- VT = 26 mV
- Si Vbi ≈ 0.7V
- Ge Vbi ≈ 0.3V
- rd = 26mV/ID(mA)
- dVF/dT ≈ -2 mV/°C
