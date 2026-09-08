# Semiconductor Physics - Formulas

## Constants (Memorize for ISRO)
| Constant | Symbol | Value |
|----------|--------|-------|
| Electron charge | q | 1.6 × 10⁻¹⁹ C |
| Boltzmann constant | k | 1.38 × 10⁻²³ J/K = 8.617 × 10⁻⁵ eV/K |
| Thermal voltage (300K) | VT = kT/q | 25.85 mV ≈ 26 mV |
| Planck constant | h | 6.626 × 10⁻³⁴ J·s |
| Electron mass | m₀ | 9.11 × 10⁻³¹ kg |
| Permittivity of free space | ε₀ | 8.854 × 10⁻¹⁴ F/cm |
| Si relative permittivity | εsi | 11.7 |
| Ge relative permittivity | εge | 16 |
| GaAs relative permittivity | εgaas | 12.9 |

---

## Energy Band Gap

### Temperature Dependence
$$E_g(T) = E_g(0) - \frac{\alpha T^2}{T + \beta}$$

| Material | Eg(0) (eV) | α (×10⁻⁴ eV/K) | β (K) |
|----------|------------|-----------------|-------|
| Si | 1.17 | 4.73 | 636 |
| Ge | 0.74 | 4.77 | 235 |
| GaAs | 1.52 | 5.41 | 204 |

### Approximate at 300K
$$E_g(300K) \approx E_g(0) - 0.0004T \quad \text{(for Si)}$$

---

## Intrinsic Carrier Concentration

### General Formula
$$n_i = \sqrt{N_c N_v} \exp\left(-\frac{E_g}{2kT}\right)$$

### Temperature Dependence
$$n_i(T) = n_i(T_0) \left(\frac{T}{T_0}\right)^{3/2} \exp\left[-\frac{E_g}{2k}\left(\frac{1}{T} - \frac{1}{T_0}\right)\right]$$

### Values at 300K
| Material | ni (cm⁻³) |
|----------|-----------|
| Si | 1.5 × 10¹⁰ |
| Ge | 2.4 × 10¹³ |
| GaAs | 1.8 × 10⁶ |
| InP | 1.3 × 10⁷ |
| SiC | 1.0 × 10⁻⁷ |

### Quick Formula
$$n_i \approx 3.87 \times 10^{16} T^{3/2} \exp\left(-\frac{E_g}{2kT}\right) \text{ cm}^{-3}$$

---

## Law of Mass Action

### Fundamental Relation
$$n \cdot p = n_i^2$$

### With Doping (Complete Ionization)
For N-type (ND >> NA):
$$n \approx N_D - N_A$$
$$p = \frac{n_i^2}{N_D - N_A}$$

For P-type (NA >> ND):
$$p \approx N_A - N_D$$
$$n = \frac{n_i^2}{N_A - N_D}$$

---

## Carrier Concentration

### Electron Concentration
$$n = N_c \exp\left(-\frac{E_c - E_F}{kT}\right)$$

### Hole Concentration
$$p = N_v \exp\left(-\frac{E_F - E_v}{kT}\right)$$

### Fermi Level Position (N-type)
$$E_F = E_c - kT \ln\left(\frac{N_c}{N_D}\right)$$

### Fermi Level Position (P-type)
$$E_F = E_v + kT \ln\left(\frac{N_v}{N_A}\right)$$

### Intrinsic Fermi Level
$$E_i = \frac{E_c + E_v}{2} + \frac{kT}{2} \ln\left(\frac{N_v}{N_c}\right)$$

$$E_i \approx \frac{E_c + E_v}{2} + \frac{3}{4} kT \ln\left(\frac{m_p^*}{m_n^*}\right)$$

---

## Conductivity and Mobility

### Conductivity
$$\sigma = q(n\mu_n + p\mu_p) \quad \text{(S/cm)}$$

### Resistivity
$$\rho = \frac{1}{\sigma} = \frac{1}{q(n\mu_n + p\mu_p)} \quad \text{(Ω·cm)}$$

### For N-type
$$\sigma_n = q N_D \mu_n$$
$$\rho_n = \frac{1}{q N_D \mu_n}$$

### For P-type
$$\sigma_p = q N_A \mu_p$$
$$\rho_p = \frac{1}{q N_A \mu_p}$$

### Hall Coefficient
$$R_H = \frac{1}{qn} \quad \text{(N-type)}$$
$$R_H = \frac{1}{qp} \quad \text{(P-type)}$$

---

## Mobility-Temperature Relation

### Lattice Scattering Dominant
$$\mu \propto T^{-3/2}$$

### Impurity Scattering Dominant
$$\mu \propto T^{+3/2}$$

### Combined (Empirical)
$$\frac{1}{\mu} = \frac{1}{\mu_L} + \frac{1}{\mu_I}$$

### Doping Dependence (Empirical)
$$\mu \approx \frac{\mu_0}{1 + \left(\frac{N}{N_{ref}}\right)^\gamma}$$

For Si at 300K:
| Doping range | γ for μn | γ for μp |
|--------------|----------|----------|
| < 10¹⁷ cm⁻³ | 0.85 | 1.0 |
| > 10¹⁷ cm⁻³ | 1.5 | 2.0 |

---

## Einstein Relation

### Fundamental
$$\frac{D}{\mu} = \frac{kT}{q} = V_T$$

### Diffusion Coefficients
$$D_n = \mu_n V_T = \mu_n \frac{kT}{q}$$
$$D_p = \mu_p V_T = \mu_p \frac{kT}{q}$$

### At 300K
$$D_n = 0.026 \mu_n \quad \text{(cm²/s if μ in cm²/V-s)}$$
$$D_p = 0.026 \mu_p$$

### Values at 300K
| Material | Dn (cm²/s) | Dp (cm²/s) |
|----------|-----------|-----------|
| Si | 35 | 12.5 |
| Ge | 101 | 49 |
| GaAs | 221 | 10.4 |

---

## Drift and Diffusion Current

### Drift Current Density
$$J_{drift} = \sigma E = q(n\mu_n + p\mu_p)E$$

Electron component: $J_n = qn\mu_n E$
Hole component: $J_p = qp\mu_p E$

### Diffusion Current Density
$$J_{diff} = qD_n \frac{dn}{dx} - qD_p \frac{dp}{dx}$$

### Total Current
$$J = J_n + J_p = q(n\mu_n E + D_n \frac{dn}{dx}) + q(p\mu_p E - D_p \frac{dp}{dx})$$

---

## Quantum Numbers (for Density of States)

### Effective Density of States
$$N_c = 2\left(\frac{2\pi m_n^* kT}{h^2}\right)^{3/2} = 2\left(\frac{2\pi m_n^* kT}{h^2}\right)^{3/2}$$

$$N_v = 2\left(\frac{2\pi m_p^* kT}{h^2}\right)^{3/2}$$

### Effective Mass (Si)
| Material | mn*/m₀ | mp*/m₀ |
|----------|--------|--------|
| Si | 1.08 | 0.81 |
| Ge | 0.56 | 0.29 |
| GaAs | 0.067 | 0.45 |

---

## Heavy Doping Effects

### Bandgap Narrowing
$$\Delta E_g = 22.5 \left(\frac{N}{10^{18}}\right)^{1/2} \text{ meV (for Si)}$$

### Modified Mass Action Law
$$np = n_i^2 \exp\left(\frac{\Delta E_g}{kT}\right) = n_{ie}^2$$

Where nie = effective intrinsic carrier concentration

---

## Semiconductor at Different Temperatures

### Freeze-out Range (Low T)
- kT << ED (or EA)
- Not all dopants ionized
- n < ND

### Extrinsic Range (Room Temp)
- kT >> ED, EA
- All dopants ionized
- n ≈ ND (for N-type)
- Conductivity nearly constant

### Intrinsic Range (High T)
- ni >> ND
- n ≈ p ≈ ni
- Semiconductor becomes intrinsic
- Device fails

---

## Key Numerical Values (ISRO)

### At T = 300K
| Quantity | Value |
|----------|-------|
| VT = kT/q | 25.85 mV |
| 2VT | 51.7 mV |
| 4VT | 103.4 mV |
| 6VT | 155.1 mV |
| kT | 0.02585 eV |
| 2kT | 0.0517 eV |

### Useful Approximations
- At 300K: VT ≈ 26 mV
- ni(Si) ≈ 1.5 × 10¹⁰ cm⁻³
- At 400K: VT ≈ 34.5 mV, ni(Si) ≈ 4.5 × 10¹² cm⁻³
- At 500K: VT ≈ 43.1 mV, ni(Si) ≈ 2.2 × 10¹⁴ cm⁻³

---

## ISRO Quick Formula Sheet

### Carrier Concentration
1. n·p = ni²
2. n = ni·exp((EF-Ei)/kT)
3. p = ni·exp((Ei-EF)/kT)

### Conductivity
1. σ = q(nμn + pμp)
2. ρ = 1/σ

### Einstein Relation
1. D/μ = kT/q = VT
2. Dn = μnVT

### Fermi Level
1. EF = EC - kT·ln(NC/ND)
2. EF = EV + kT·ln(NV/NA)

### Current Densities
1. Jdrift = q(nμn + pμp)E
2. Jdiffusion = qDn(dn/dx) - qDp(dp/dx)
