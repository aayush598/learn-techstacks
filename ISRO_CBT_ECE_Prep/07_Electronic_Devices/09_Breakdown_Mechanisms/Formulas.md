# Breakdown Mechanisms - Formulas

## Avalanche Breakdown

### Multiplication Factor
$$M = \frac{1}{1 - \left(\frac{V}{V_{BR}}\right)^n}$$

Where n = 4-6 for Si

### Breakdown Voltage (Empirical)
$$V_{BR} = 60\left(\frac{E_g}{1.1}\right)^{3/2}\left(\frac{N_B}{10^{16}}\right)^{-3/4} \text{ V}$$

### Doping Dependence
$$V_{BR} \propto N_B^{-3/4}$$

### Impact Ionization Coefficient
$$\alpha_n = \alpha_0 \exp\left(-\frac{E_c}{E}\right)$$

Where Ec = critical field

### Critical Field
$$E_c = \frac{4 \times 10^5}{1 - \log_{10}(N/10^{16})} \text{ V/cm}$$

---

## Zener Breakdown

### Tunneling Probability
$$P_{tunnel} \propto \exp\left(-\frac{4\sqrt{2m^*}(E_g)^{3/2}}{3q\hbar E}\right)$$

### Tunneling Current
$$I_t \propto E^2 \exp\left(-\frac{K}{E}\right)$$

### Doping Dependence
$$V_{BR} \propto N_B^{-3/4}$$

### Depletion Width Relation
$$W \propto \frac{1}{\sqrt{N}} \propto \frac{1}{\sqrt{V_{BR}}}$$

---

## Temperature Dependence

### Avalanche Breakdown
$$\frac{1}{V_{BR}}\frac{dV_{BR}}{dT} \approx +0.1\% \text{ per °C}$$

### Zener Breakdown
$$\frac{1}{V_{BR}}\frac{dV_{BR}}{dT} \approx -0.1\% \text{ per °C}$$ (approximately)

### Temperature Coefficient (TC)
$$TC = \frac{1}{V_{BR}}\frac{dV_{BR}}{dT} \times 100\% \text{ (in %/°C)}$$

---

## Punch-Through

### Punch-Through Voltage
$$V_{PT} = \frac{qN_D W_B^2}{2\varepsilon_s}$$

Where WB = base width

### Condition for Punch-Through
$$W_{dep} = W_B$$

### Depletion Width at Pinch-off
$$W_{dep} = \sqrt{\frac{2\varepsilon_s V_{CB}}{qN_C}}$$

---

## MOSFET Drain Breakdown

### Breakdown Current
$$I_{BR} = I_{sub} + I_{impact}$$

### Substrate Current
$$I_{sub} = I_D \exp\left(-\frac{\phi_i}{q\lambda E_m}\right)$$

Where:
- φi = impact ionization threshold
- λ = mean free path
- Em = maximum field

### Maximum Field Near Drain
$$E_m = \frac{V_{DS} - V_{DS,sat}}{l}$$

Where l = characteristic length

---

## Hot Carrier Effects

### Substrate Current (Empirical)
$$I_{sub} = I_D \cdot A \cdot \exp\left(-\frac{B}{V_{DS} - V_{DS,sat}}\right)$$

### Gate Current
$$I_G = I_D \cdot A_G \cdot \exp\left(-\frac{B_G}{V_{DS} - V_{DS,sat}}\right)$$

### Threshold Voltage Shift
$$\Delta V_T = f(I_G, t)$$

$$\Delta V_T \propto (I_G \cdot t)^{1/3}$$

---

## Gate Oxide Breakdown

### Fowler-Nordheim Tunneling Current
$$J_{FN} = A E_{ox}^2 \exp\left(-\frac{B}{E_{ox}}\right)$$

Where:
- A = 1.54 × 10⁻⁶ (A/V²)
- B = 2.28 × 10⁸ (V/cm)

### Breakdown Time (TDDB)
$$TDDB \propto \exp\left(\frac{\gamma}{E_{ox}}\right)$$

### Oxide Electric Field
$$E_{ox} = \frac{V_{GS}}{t_{ox}}$$

---

## Thermal Breakdown

### Power Dissipation
$$P = I \times V$$

### Thermal Resistance
$$\theta_{JA} = \frac{T_J - T_A}{P}$$

### Thermal Runaway Condition
$$\frac{\partial I}{\partial T} \times V \times \theta_{JA} > 1$$

---

## Voltage Rating Formulas

### PN Junction Breakdown
$$V_{BR} = \frac{\varepsilon_s E_c^2}{2qN}$$

### Pin Diode (Intrinsic Region)
$$V_{BR} \approx E_c \times W$$

(where W = intrinsic region width)

### One-Sided Junction
$$V_{BR} = \frac{\varepsilon_s E_c}{qN_B}$$

---

## Safe Operating Area (SOA)

### DC SOA Limits
1. Maximum current: I_max
2. Maximum voltage: V_max
3. Maximum power: P = V×I ≤ P_max
4. Thermal limit: T_J ≤ T_J,max

### Second Breakdown
$$P_{SB} = \frac{K}{\sqrt{t}}$$

Where K = constant, t = pulse width

---

## ISRO Quick Reference

### Breakdown Voltage
1. VBR ∝ N⁻³/⁴
2. VBR = 60(Eg/1.1)³/²(NB/10¹⁶)⁻³/⁴

### Temperature Coefficients
1. Avalanche: positive (VBR ↑ with T)
2. Zener: negative (VBR ↓ with T)
3. At ~5.6V: TC ≈ 0

### Mechanisms
1. < 5V: Zener (tunneling)
2. > 6V: Avalanche (impact ionization)
3. 5-6V: both

### Formulas
1. M = 1/(1-(V/VBR)^n)
2. JFN = A·E²·exp(-B/E)
3. Isub ∝ exp(-B/(VDS-VDS,sat))
