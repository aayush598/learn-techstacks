# Bandgap Reference - Formulas

## Bandgap Temperature Dependence

### Varshni Equation
$$E_g(T) = E_g(0) - \frac{\alpha T^2}{T + \beta}$$

### Linear Approximation
$$E_g(T) \approx E_g(T_0) + \frac{dE_g}{dT}(T - T_0)$$

### dEg/dT for Si
$$\frac{dE_g}{dT} \approx -0.27 \text{ meV/K}$$

---

## VBE Temperature Dependence

### General Formula
$$V_{BE}(T) = V_{G0} - \frac{T}{T_0}(V_{G0} - V_{BE0}) - (n-1)V_T \ln\left(\frac{T}{T_0}\right)$$

### Simplified (first order)
$$V_{BE}(T) \approx 1.2 - \frac{T}{T_0}(1.2 - V_{BE0})$$

### Temperature Coefficient
$$\frac{dV_{BE}}{dT} = \frac{V_{BE} - E_g/q - \frac{3kT}{q}}{T}$$

### Approximation
$$\frac{dV_{BE}}{dT} \approx -2 \text{ mV/°C}$$

---

## VT Temperature Dependence

### Thermal Voltage
$$V_T = \frac{kT}{q}$$

### Temperature Coefficient
$$\frac{dV_T}{dT} = \frac{k}{q} = 0.08617 \text{ mV/K}$$

### At Various Temperatures
| T (K) | VT (mV) |
|-------|---------|
| 200 | 17.2 |
| 273 | 23.5 |
| 300 | 25.85 |
| 400 | 34.5 |
| 500 | 43.1 |

---

## ΔVBE Generation

### With Current Ratio
$$\Delta V_{BE} = V_T \ln\left(\frac{I_1}{I_2}\right)$$

### With Area Ratio
$$\Delta V_{BE} = V_T \ln(N)$$

Where N = area ratio

### PTAT Current
$$I_{PTAT} = \frac{V_T \ln(N)}{R}$$

### PTAT Voltage
$$V_{PTAT} = K \times V_T$$

---

## Bandgap Reference

### Output Voltage
$$V_{REF} = V_{BE} + K V_T$$

### Cancellation Condition
$$K = \frac{|dV_{BE}/dT|}{dV_T/dT}$$

### Numerical Values
$$K = \frac{2 \text{ mV/K}}{0.086 \text{ mV/K}} \approx 23.2$$

### Result
$$V_{REF} = V_{BE} + K \frac{kT}{q} \approx 0.6 + 23 \times 0.026 = 1.2 \text{ V}$$

---

## Brokaw Bandgap

### Reference Voltage
$$V_{REF} = V_{BE1} + 2 V_T \ln(N) \frac{R_2}{R_1}$$

### With Ratio
$$V_{REF} = V_{BE} + 2 \frac{R_2}{R_1} V_T \ln(N)$$

### Cancellation Condition
$$\frac{2R_2 \ln(N)}{R_1} = \frac{|dV_{BE}/dT|}{dV_T/dT} \approx 23$$

---

## Temperature Drift

### First-Order Temperature Coefficient
$$TC_1 = \frac{1}{V_{REF}} \frac{dV_{REF}}{dT}$$

### Drift Expression
$$\frac{\Delta V_{REF}}{V_{REF}} = TC_1 \times \Delta T + \frac{1}{2}TC_2 \times (\Delta T)^2$$

### Typical Values
| Reference Type | TC (ppm/°C) |
|----------------|-------------|
| Zener | 50-100 |
| Simple bandgap | 20-50 |
| Curvature corrected | 1-10 |
| Precision reference | 0.5-2 |

---

## Error Sources

### Resistor Mismatch
$$\frac{\Delta I_{PTAT}}{I_{PTAT}} = \frac{\Delta R}{R}$$

### Op-Amp Offset
$$\Delta V_{REF} = V_{OS}\left(1 + \frac{R_2}{R_1}\right)$$

### Transistor Mismatch
$$\Delta V_{BE} = V_T \ln\left(1 + \frac{\Delta A}{A}\right) \approx V_T \frac{\Delta A}{A}$$

---

## Measurement Formulas

### Bandgap from Wavelength
$$E_g = \frac{hc}{\lambda_c} = \frac{1240}{\lambda_c \text{ (nm)}} \text{ eV}$$

### Bandgap from Intrinsic Concentration
$$n_i = \sqrt{N_c N_v} \exp\left(-\frac{E_g}{2kT}\right)$$

### Bandgap from Temperature
$$\ln(n_i) = \ln(\sqrt{N_c N_v}) - \frac{E_g}{2kT}$$

---

## ISRO Quick Reference

### Key Numbers
1. dVBE/dT ≈ -2 mV/°C
2. dVT/dT = +0.086 mV/°C
3. K ≈ 23
4. VREF ≈ 1.2V
5. VG0 ≈ 1.2V (Si)
6. dEg/dT ≈ -0.27 meV/K

### Key Formulas
1. Eg(T) = Eg(0) - αT²/(T+β)
2. VBE(T) ≈ 1.2 - (T/T0)(1.2 - VBE0)
3. VREF = VBE + K·VT
4. ΔVBE = VT·ln(N)
5. IPTAT = VT·ln(N)/R
