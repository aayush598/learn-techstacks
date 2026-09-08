# Fermi Level Calculations - Formulas

## Fermi-Dirac Distribution

### Basic Function
$$f(E) = \frac{1}{1 + \exp\left(\frac{E - E_F}{kT}\right)}$$

### Boltzmann Approximation (Non-degenerate)
$$f(E) \approx \exp\left(-\frac{E - E_F}{kT}\right) \quad \text{for } E - E_F > 2kT$$

---

## Carrier Concentration

### Non-Degenerate
$$n = N_c \exp\left(-\frac{E_c - E_F}{kT}\right)$$

$$p = N_v \exp\left(-\frac{E_F - E_v}{kT}\right)$$

### From Intrinsic Concentration
$$n = n_i \exp\left(\frac{E_F - E_i}{kT}\right)$$

$$p = n_i \exp\left(\frac{E_i - E_F}{kT}\right)$$

### Product (Mass Action)
$$np = n_i^2$$

---

## Fermi Level Position

### Intrinsic
$$E_i = \frac{E_c + E_v}{2} + \frac{3}{4}kT \ln\left(\frac{m_p^*}{m_n^*}\right)$$

### N-Type (from EC)
$$E_F = E_c - kT \ln\left(\frac{N_c}{N_D}\right)$$

### P-Type (from EV)
$$E_F = E_v + kT \ln\left(\frac{N_v}{N_A}\right)$$

### From Intrinsic Level
$$E_F - E_i = kT \ln\left(\frac{N_D}{n_i}\right) \quad \text{(N-type)}$$

$$E_i - E_F = kT \ln\left(\frac{N_A}{n_i}\right) \quad \text{(P-type)}$$

---

## Effective Density of States

### Conduction Band
$$N_c = 2\left(\frac{2\pi m_n^* kT}{h^2}\right)^{3/2}$$

### Valence Band
$$N_v = 2\left(\frac{2\pi m_p^* kT}{h^2}\right)^{3/2}$$

### At 300K (Si)
$$N_c = 2.8 \times 10^{19} \text{ cm}^{-3}$$

$$N_v = 1.04 \times 10^{19} \text{ cm}^{-3}$$

---

## Degeneracy Conditions

### Non-Degenerate
$$(E_c - E_F) > 2kT$$
$$N_D < N_c \exp(-2) = 0.135 N_c$$

### Degenerate
$$(E_c - E_F) \leq 2kT$$
$$N_D \geq 0.135 N_c$$

### For Si
- Degenerate if ND > ~3.8 × 10¹⁸ cm⁻³

---

## Fermi Integral

### General Form
$$F_j(\eta) = \frac{1}{\Gamma(j+1)}\int_0^\infty \frac{\epsilon^j d\epsilon}{1 + \exp(\epsilon - \eta)}$$

### Carrier Concentration (Degenerate)
$$n = N_c \cdot \frac{2}{\sqrt{\pi}} F_{1/2}(\eta)$$

Where η = (EF - EC)/kT

### Asymptotic Approximations
| Condition | F_{1/2}(η) |
|-----------|------------|
| η << -1 | (√π/2)·exp(η) |
| η = 0 | 0.653 |
| η >> 1 | (4/3√π)·η^{3/2} |

---

## Temperature Dependence

### n_i vs Temperature
$$n_i = \sqrt{N_c N_v} \exp\left(-\frac{E_g}{2kT}\right)$$

### n_i vs 1/T
$$\ln(n_i) = \frac{1}{2}\ln(N_c N_v) - \frac{E_g}{2kT}$$

### Slope
$$\frac{d\ln(n_i)}{d(1/T)} = -\frac{E_g}{2k}$$

### Bandgap from ni slope
$$E_g = -2k \frac{d\ln(n_i)}{d(1/T)}$$

---

## Numerical Values (Si, 300K)

### kT Values
| Quantity | Value |
|----------|-------|
| kT | 0.02585 eV |
| 2kT | 0.0517 eV |
| 3kT | 0.0775 eV |
| 4kT | 0.103 eV |
| kT/q = VT | 25.85 mV |

### EF - Ei for Various Doping
| ND (cm⁻³) | EF - Ei (eV) |
|------------|--------------|
| 10¹⁵ | 0.29 |
| 10¹⁶ | 0.35 |
| 10¹⁷ | 0.41 |
| 10¹⁸ | 0.47 |

### Calculation: EF - Ei = 0.026 × ln(ND/1.5×10¹⁰)

---

## Complete Ionization Model

### N-Type (ND > NA)
$$n = \frac{(N_D - N_A) + \sqrt{(N_D - N_A)^2 + 4n_i^2}}{2}$$

### Approximate
- Extrinsic: n ≈ ND - NA
- Intrinsic: n ≈ ni

### Charge Neutrality
$$n + N_A = p + N_D$$

---

## ISRO Quick Reference

### Key Formulas
1. f(E) = 1/(1+exp((E-EF)/kT))
2. n = Nc·exp(-(EC-EF)/kT)
3. p = Nv·exp(-(EF-EV)/kT)
4. n = ni·exp((EF-Ei)/kT)
5. EF - Ei = kT·ln(ND/ni) [N-type]
6. np = ni²

### Deferring Non-Degeneracy
- EF - EC < -2kT: non-degenerate
- EF - EC ≥ -2kT: degenerate

### Quick Values
- ln(1.5×10¹⁰) = 23.4
- kT·ln(ND/ni) at 300K
- Eg/2 = 0.56 eV (Si midgap)
