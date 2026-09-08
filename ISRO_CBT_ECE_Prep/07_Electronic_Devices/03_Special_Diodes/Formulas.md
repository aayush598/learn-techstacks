# Special Diodes - Formulas

## Zener Diode

### Zener Voltage
$$V_Z = V_{bi} + \Delta V_{tunneling} \text{ or } V_{bi} + \Delta V_{avalanche}$$

### Load Regulation
$$\text{Load Regulation} = \frac{V_{NL} - V_{FL}}{V_{FL}} \times 100\%$$

### Line Regulation
$$\text{Line Regulation} = \frac{\Delta V_{out}}{\Delta V_{in}}$$

### Zener Diode Current
$$I_Z = I_S - I_L$$

### Power Dissipation
$$P_Z = V_Z \times I_Z$$

### Maximum Current
$$I_{Z(max)} = \frac{P_{Z(max)}}{V_Z}$$

### Series Resistance
$$R_Z = \frac{\Delta V_Z}{\Delta I_Z}$$ (dynamic resistance)

---

## Tunnel Diode

### Peak Current
$$I_P = I_S \exp\left(\frac{V_P}{V_T}\right) \text{ (approximate)}$$

### Valley Current
$$I_V = I_S \exp\left(\frac{V_V}{V_T}\right) + I_{excess}$$

### Negative Differential Resistance
$$r_n = -\frac{dV}{dI} = \frac{V_V - V_P}{I_P - I_V}$$ (in NDR region)

### Maximum Frequency
$$f_{max} = \frac{1}{2\pi r_n C_j}$$

### Oscillation Condition
$$R_L < |r_n|$$ (for oscillation)

---

## Varactor Diode

### Junction Capacitance
$$C_j = \frac{C_{j0}}{(1 + V_R/V_{bi})^m}$$

Where:
- Cj0 = zero-bias capacitance
- VR = reverse voltage
- Vbi = built-in potential
- m = grading coefficient

### Grading Coefficient (m)
| Junction Type | m |
|---------------|---|
| Abrupt | 1/2 |
| Linear graded | 1/3 |
| Hyperabrupt | 2-3 |

### Voltage-Capacitance Relation
$$C_j \propto V_R^{-m}$$

### Tuning Ratio
$$\text{TR} = \frac{C_{j(max)}}{C_{j(min)}} = \left(\frac{V_{R(max)} + V_{bi}}{V_{R(min)} + V_{bi}}\right)^m$$

### Varactor Figure of Merit
$$Q = \frac{1}{2\pi f R_s C_j}$$

---

## PIN Diode

### On-State Resistance
$$R_{on} = \frac{\rho_I W_I}{2A} + R_s$$

Where:
- ρI = intrinsic region resistivity
- WI = intrinsic region width
- A = junction area
- Rs = contact resistance

### Off-State Capacitance
$$C_{off} = \frac{\varepsilon A}{W_I + W_{dep}}$$

### Switching Time
$$t_s = \tau \ln\left(\frac{I_F}{I_R}\right)$$ (storage time)

### Forward Voltage
$$V_F = V_T \ln\left(\frac{I_F}{I_S}\right) + I_F R_{on}$$

---

## Schottky Diode

### Current-Voltage
$$I = I_S\left[\exp\left(\frac{V}{nV_T}\right) - 1\right]$$

### Saturation Current
$$I_S = AA^* T^2 \exp\left(-\frac{q\phi_B}{kT}\right)$$

Where:
- A* = effective Richardson constant
- φB = barrier height

### Barrier Height
$$\phi_B = \phi_M - \chi_s$$

Where:
- φM = metal work function
- χs = semiconductor electron affinity

### Forward Voltage
$$V_F = \phi_B + V_T \ln\left(\frac{I}{A A^* T^2}\right)$$

### Built-in Potential
$$V_{bi} = \phi_B - V_n$$

Where Vn = (EC - EF)/q

---

## LED

### Photon Energy
$$E = h\nu = \frac{hc}{\lambda}$$

### Wavelength
$$\lambda = \frac{hc}{E_g} = \frac{1240}{E_g \text{ (eV)}} \text{ nm}$$

### Threshold Wavelength
$$\lambda_{th} = \frac{hc}{E_g} = \frac{1240}{E_g} \text{ nm}$$

### External Quantum Efficiency
$$\eta_{ext} = \frac{\text{photons emitted externally}}{\text{electrons injected}}$$

### Luminous Intensity
$$I_v = \eta_{ext} \times \frac{P_{optical}}{K_m V(\lambda)}$$

Where Km = 683 lm/W

### Bandgap Wavelength Table
| Material | Eg (eV) | λ (nm) | Color |
|----------|---------|--------|-------|
| GaAs | 1.43 | 867 | IR |
| GaAsP | 1.8 | 690 | Red |
| GaAsP | 2.0 | 620 | Orange |
| GaP | 2.2 | 565 | Green |
| GaN | 3.4 | 365 | UV |
| InGaN | 2.5 | 496 | Blue |

---

## Photodiode

### Photo Current
$$I_{ph} = q\eta A G_{opt}$$

Where:
- η = quantum efficiency
- A = area
- Gopt = optical generation rate

### Responsivity
$$R = \frac{I_{ph}}{P_{opt}} = \frac{q\eta}{h\nu} = \frac{\eta\lambda}{1240} \text{ (A/W)}$$

### Noise Current
$$i_n = \sqrt{2q(I_{ph} + I_d)B + \frac{4kTB}{R_L}}$$

Where:
- Id = dark current
- B = bandwidth
- RL = load resistance

### Detectivity
$$D^* = \frac{R\sqrt{A}}{i_n} \text{ (cm·Hz}^{1/2}\text{/W)}$$

### Cutoff Wavelength
$$\lambda_c = \frac{hc}{E_g} = \frac{1240}{E_g} \text{ nm}$$

### Response Time
$$\tau = R_L C_j + \tau_{transit}$$

---

## Solar Cell

### Open Circuit Voltage
$$V_{OC} = V_T \ln\left(1 + \frac{I_{ph}}{I_S}\right)$$

### Short Circuit Current
$$I_{SC} = I_{ph}$$

### Maximum Power Point
$$P_{max} = V_{mp} \times I_{mp}$$

### Fill Factor
$$FF = \frac{V_{mp} I_{mp}}{V_{OC} I_{SC}}$$

### Power Conversion Efficiency
$$\eta = \frac{P_{max}}{P_{in}} = \frac{FF \times V_{OC} \times I_{SC}}{P_{in}}$$

### Ideal Solar Cell
$$I = I_{ph} - I_S\left[\exp\left(\frac{V}{nV_T}\right) - 1\right]$$

---

## Power Diode

### Average Output Voltage (Full Wave)
$$V_{avg} = \frac{2V_m}{\pi}$$

### RMS Voltage
$$V_{rms} = \frac{V_m}{\sqrt{2}}$$

### Form Factor
$$FF = \frac{V_{rms}}{V_{avg}} = \frac{\pi}{2\sqrt{2}} = 1.11$$

### Reverse Recovery Time
$$t_{rr} = \tau_p \ln\left(1 + \frac{I_F}{I_R}\right)$$

---

## Temperature Coefficients

### Zener Diode
- VZ < 5V: dVZ/dT < 0 (Zener breakdown)
- VZ > 6V: dVZ/dT > 0 (Avalanche breakdown)
- VZ ≈ 5.6V: dVZ/dT ≈ 0

### LED
$$\frac{d\lambda}{dT} = \frac{hc}{E_g^2} \frac{dE_g}{dT} \approx +0.3 \text{ nm/°C}$$

### Schottky Diode
$$\frac{dV_F}{dT} \approx -1.5 \text{ mV/°C}$$ (less than Si PN junction)

---

## ISRO Quick Reference

### Zener
- VZ < 5V: Zener, negative temp coeff
- VZ > 6V: Avalanche, positive temp coeff
- P = VZ × IZ

### Tunnel
- NDR region: VP < V < VV
- fmax = 1/(2πrnCj)

### Varactor
- Cj = Cj0/(1+VR/Vbi)^m
- m = 1/2 (abrupt), 1/3 (linear)

### Schottky
- Vf = 0.2-0.5V (lower than PN)
- Fast switching (no minority carriers)

### LED
- λ = 1240/Eg (nm)
- Direct bandgap required

### Photodiode
- R = ηλ/1240 (A/W)
- λc = 1240/Eg (nm)
